#!/usr/bin/env python3
"""Portable state and approval runtime for image-to-3D jobs.

The module deliberately has no provider, Blender, or credential dependencies.  The
state file is the durable handoff between design, approval, and production steps.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import platform
import sys
import tempfile
import time
import uuid
import copy
from pathlib import Path
from typing import Any, Iterator

try:
    import fcntl
except ImportError:  # pragma: no cover - Windows fallback
    fcntl = None
try:
    import msvcrt
except ImportError:  # pragma: no cover - POSIX
    msvcrt = None

SCHEMA_VERSION = 1


class RuntimeErrorBase(RuntimeError):
    """Base class for actionable runtime errors."""


class ApprovalError(RuntimeErrorBase):
    pass


class DuplicateJobError(RuntimeErrorBase):
    pass


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: str | os.PathLike[str]) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return sha256_bytes(encoded)


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


@contextlib.contextmanager
def file_lock(path: Path) -> Iterator[None]:
    """Serialize writes; fail closed if this platform has no lock primitive."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a+") as handle:
        if fcntl:
            handle.seek(0)
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        elif msvcrt:
            handle.seek(0)
            if handle.tell() == 0 and os.fstat(handle.fileno()).st_size == 0:
                handle.write("0")
                handle.flush()
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
        else:  # pragma: no cover - unsupported platform
            raise RuntimeErrorBase("no supported file-lock primitive on this platform")
        try:
            yield
        finally:
            if fcntl:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            elif msvcrt:
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)


def atomic_json_write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, indent=2, sort_keys=True, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


class Runtime:
    def __init__(self, state_path: str | os.PathLike[str]):
        self.state_path = Path(state_path)
        self.lock_path = self.state_path.with_suffix(self.state_path.suffix + ".lock")

    def read(self) -> dict[str, Any]:
        if not self.state_path.exists():
            raise RuntimeErrorBase(f"state does not exist: {self.state_path}")
        with self.state_path.open(encoding="utf-8") as handle:
            return json.load(handle)

    def _write(self, state: dict[str, Any]) -> dict[str, Any]:
        with file_lock(self.lock_path):
            atomic_json_write(self.state_path, state)
        return state

    def _update(self, mutator) -> Any:
        """Read, mutate, and replace state while holding one transaction lock."""
        with file_lock(self.lock_path):
            if not self.state_path.exists():
                raise RuntimeErrorBase(f"state does not exist: {self.state_path}")
            with self.state_path.open(encoding="utf-8") as handle:
                state = json.load(handle)
            result = mutator(state)
            atomic_json_write(self.state_path, state)
            return result

    @staticmethod
    def _asset_entries(design: dict[str, Any]) -> list[dict[str, str]]:
        assets = design.get("assets")
        if not isinstance(assets, list) or not assets:
            raise RuntimeErrorBase("design requires non-empty file-backed assets [{path, sha256}]")
        normalized = []
        for asset in assets:
            if not isinstance(asset, dict) or not asset.get("path") or not asset.get("sha256"):
                raise RuntimeErrorBase("each design asset requires path and sha256")
            path = Path(asset["path"]).resolve()
            if not path.is_file() or sha256_file(path) != asset["sha256"]:
                raise RuntimeErrorBase(f"design asset hash mismatch: {path}")
            normalized.append({"path": str(path), "sha256": asset["sha256"]})
        return normalized

    def _input_unchanged(self, state: dict[str, Any]) -> None:
        source = Path(state["input"]["path"])
        if not source.is_file() or sha256_file(source) != state["input"]["sha256"]:
            raise ApprovalError("original input changed since init; approval is invalid")

    def init(self, input_path: str | os.PathLike[str], environment: dict[str, Any] | None = None) -> dict[str, Any]:
        source = Path(input_path).resolve()
        if not source.is_file():
            raise RuntimeErrorBase(f"input is not a file: {source}")
        if self.state_path.exists():
            raise RuntimeErrorBase(f"refusing to overwrite existing state: {self.state_path}")
        job_id = uuid.uuid4().hex
        state = {
            "schema_version": SCHEMA_VERSION,
            "job_id": job_id,
            "created_at": _now(),
            "stage": "image_intake",
            "next_action": "register_design",
            "input": {"path": str(source), "sha256": sha256_file(source)},
            "output_root": str(self.state_path.parent.resolve() / "outputs" / job_id),
            "design_revisions": [],
            "approval": None,
            "coarse_revisions": [],
            "coarse_approval": None,
            "production": {"plan": None, "checks": []},
            "checkpoints": {},
            "jobs": {},
            "environment": environment or {},
        }
        with file_lock(self.lock_path):
            if self.state_path.exists():
                raise RuntimeErrorBase(f"refusing to overwrite existing state: {self.state_path}")
            atomic_json_write(self.state_path, state)
        return state

    def register_design(self, design: dict[str, Any], label: str | None = None) -> dict[str, Any]:
        design = copy.deepcopy(design)
        design["assets"] = self._asset_entries(design)
        design_hash = stable_hash(design)
        def mutate(state):
            revisions = state.setdefault("design_revisions", [])
            if revisions and revisions[-1]["design_hash"] == design_hash:
                return revisions[-1]
            revision = {"revision": f"r{len(revisions) + 1}", "design_hash": design_hash, "label": label or "", "registered_at": _now(), "design": design}
            revisions.append(revision)
            state["approval"] = None
            state["coarse_approval"] = None
            state["production"] = {"plan": None, "checks": [], "invalidated_at": _now()}
            state["stage"] = "design"
            state["next_action"] = "human_design_approval"
            return revision
        return self._update(mutate)

    def approve(self, revision: str, approved_by: str, evidence: str, approved_at: str | None = None) -> dict[str, Any]:
        if not approved_by.strip() or not evidence.strip():
            raise ApprovalError("human approval requires non-empty approved_by and evidence")
        def mutate(state):
            self._input_unchanged(state)
            match = next((item for item in state.get("design_revisions", []) if item["revision"] == revision), None)
            if not match:
                raise ApprovalError(f"unknown design revision: {revision}")
            self._asset_entries(match.get("design", {}))
            state["approval"] = {"revision": revision, "design_hash": match["design_hash"], "approved_by": approved_by, "evidence": evidence, "approved_at": approved_at or _now()}
            state["stage"] = "approved_design"
            state["next_action"] = "production_check"
            return state
        return self._update(mutate)

    def register_coarse(self, design_revision: str, artifact: dict[str, Any], label: str | None = None) -> dict[str, Any]:
        """Register a coarse geometry/material candidate after design approval."""
        self.require_approval(design_revision)
        state_before = self.read()
        if not state_before.get("production", {}).get("plan") or state_before["production"].get("design_revision") != design_revision:
            raise RuntimeErrorBase("production-check is required before coarse registration")
        artifact = copy.deepcopy(artifact)
        artifact["assets"] = self._asset_entries(artifact)
        artifact_hash = stable_hash(artifact)
        def mutate(state):
            current = next(item for item in state["design_revisions"] if item["revision"] == design_revision)
            revisions = state.setdefault("coarse_revisions", [])
            if revisions and revisions[-1]["artifact_hash"] == artifact_hash and revisions[-1]["design_revision"] == design_revision:
                return revisions[-1]
            revision = {"revision": f"c{len(revisions) + 1}", "design_revision": design_revision, "design_hash": current["design_hash"], "artifact_hash": artifact_hash, "label": label or "", "registered_at": _now(), "artifact": artifact}
            revisions.append(revision)
            state["coarse_approval"] = None
            state["stage"] = "coarse"
            state["next_action"] = "human_coarse_approval"
            return revision
        return self._update(mutate)

    def approve_coarse(self, coarse_revision: str, approved_by: str, evidence: str, approved_at: str | None = None) -> dict[str, Any]:
        if not approved_by.strip() or not evidence.strip():
            raise ApprovalError("coarse approval requires non-empty approved_by and evidence")
        state = self.read()
        match = next((item for item in state.get("coarse_revisions", []) if item["revision"] == coarse_revision), None)
        if not match:
            raise ApprovalError(f"unknown coarse revision: {coarse_revision}")
        self.require_approval(match["design_revision"])
        def mutate(state):
            match = next((item for item in state.get("coarse_revisions", []) if item["revision"] == coarse_revision), None)
            if not match:
                raise ApprovalError(f"unknown coarse revision: {coarse_revision}")
            self._asset_entries(match.get("artifact", {}))
            state["coarse_approval"] = {"revision": coarse_revision, "design_revision": match["design_revision"], "design_hash": match["design_hash"], "artifact_hash": match["artifact_hash"], "approved_by": approved_by, "evidence": evidence, "approved_at": approved_at or _now()}
            state["stage"] = "coarse_approved"
            state["next_action"] = "finish"
            return state
        # The design approval was checked above; the transaction binds the coarse record.
        return self._update(mutate)

    def require_finish(self, design_revision: str | None = None, coarse_revision: str | None = None) -> dict[str, Any]:
        """Require both independent design and coarse-model human approvals."""
        self.require_approval(design_revision)
        state = self.read()
        current_design = (state.get("design_revisions") or [])[-1]
        approval = state.get("coarse_approval")
        revisions = state.get("coarse_revisions") or []
        current = revisions[-1] if revisions else None
        wanted = coarse_revision or (current or {}).get("revision")
        if not approval or not current or approval["revision"] != wanted:
            raise ApprovalError("coarse-model human approval is required before finish")
        if approval["design_revision"] != current_design["revision"] or approval["design_hash"] != current_design["design_hash"] or approval["artifact_hash"] != current["artifact_hash"]:
            raise ApprovalError("coarse approval is stale or bound to a different design/artifact")
        self._asset_entries(current.get("artifact", {}))
        return approval

    def require_approval(self, revision: str | None = None) -> dict[str, Any]:
        state = self.read()
        self._input_unchanged(state)
        approval = state.get("approval")
        revisions = state.get("design_revisions", [])
        current = revisions[-1] if revisions else None
        if not approval or not current:
            raise ApprovalError("human approval is required")
        wanted = revision or current["revision"]
        if approval["revision"] != wanted or approval["design_hash"] != current["design_hash"]:
            raise ApprovalError("approval is stale or bound to a different design revision")
        assets = current.get("design", {}).get("assets", [])
        for asset in assets:
            if not Path(asset["path"]).is_file() or sha256_file(asset["path"]) != asset["sha256"]:
                raise ApprovalError("design asset changed since approval; approval is invalid")
        return approval

    def production_check(self, plan: dict[str, Any], revision: str | None = None) -> dict[str, Any]:
        self.require_approval(revision)
        required = ("dimensions", "axes", "parts", "joins", "materials", "fixed_scope", "steps", "outputs", "validation")
        if any(not plan.get(key) for key in required):
            raise RuntimeErrorBase("production plan requires non-empty dimensions, axes, parts, joins, materials, fixed_scope, steps, outputs, validation")
        def mutate(state):
            state["production"] = {"plan": plan, "checked_at": _now(), "checks": list(required), "design_revision": (state.get("design_revisions") or [])[-1]["revision"]}
            state["stage"] = "production_plan"
            state["next_action"] = "register_coarse"
            return state
        return self._update(mutate)

    def checkpoint(self, name: str, input_hash: str, revision: str, environment: dict[str, Any], scope: dict[str, Any] | None = None, result: Any = None, passed: bool = False) -> dict[str, Any]:
        scope = scope or {}
        key = stable_hash({"input": input_hash, "revision": revision, "environment": environment, "scope": scope})
        state = self.read()
        previous = state.setdefault("checkpoints", {}).get(name)
        if previous and previous["key"] == key and previous.get("passed") is True and previous.get("result") is not None:
            return {"name": name, "key": key, "reused": True, "record": previous}
        record = {"key": key, "input_hash": input_hash, "revision": revision, "environment": environment, "scope": scope, "result": result, "passed": bool(passed), "updated_at": _now()}
        def mutate(current):
            current.setdefault("checkpoints", {})[name] = record
            return current
        self._update(mutate)
        return {"name": name, "key": key, "reused": False, "record": record}

    def reserve_job(self, request: dict[str, Any]) -> dict[str, Any]:
        request_hash = stable_hash(request)
        def mutate(state):
            jobs = state.setdefault("jobs", {})
            existing = jobs.get(request_hash)
            if existing:
                return {**existing, "reused": True}
            record = {"request_hash": request_hash, "status": "reserved", "created_at": _now(), "request": request}
            jobs[request_hash] = record
            return {**record, "reused": False}
        return self._update(mutate)

    _JOB_TRANSITIONS = {"reserved": {"submitted", "unknown", "cancelled"}, "submitted": {"processing", "unknown", "failed"}, "processing": {"succeeded", "failed", "unknown"}}
    _JOB_TERMINAL = {"succeeded", "failed", "cancelled"}

    def update_job(self, request_hash: str, status: str, result: Any = None) -> dict[str, Any]:
        def mutate(state):
            job = state.setdefault("jobs", {}).get(request_hash)
            if not job:
                raise RuntimeErrorBase(f"unknown job request hash: {request_hash}")
            current = job["status"]
            if status not in self._JOB_TRANSITIONS.get(current, set()):
                raise DuplicateJobError(f"invalid job transition {current} -> {status}; reconcile unknown status explicitly")
            job.update({"status": status, "updated_at": _now()})
            if result is not None:
                job["result"] = result
            return job
        return self._update(mutate)

    def reconcile_job(self, request_hash: str, status: str, evidence: str, result: Any = None) -> dict[str, Any]:
        if not evidence.strip() or status not in {"succeeded", "failed", "cancelled"}:
            raise DuplicateJobError("reconciliation requires evidence and a terminal status")
        def mutate(state):
            job = state.setdefault("jobs", {}).get(request_hash)
            if not job or job["status"] != "unknown":
                raise DuplicateJobError("only an unknown job can be reconciled")
            job.update({"status": status, "reconciliation_evidence": evidence, "updated_at": _now()})
            if result is not None:
                job["result"] = result
            return job
        return self._update(mutate)

    def preflight(self, blender_path: str, version: str, extra: dict[str, Any] | None = None) -> dict[str, Any]:
        fingerprint = stable_hash({"path": blender_path, "version": version, "extra": extra or {}})
        def mutate(state):
            cache = state.setdefault("environment", {})
            reused = cache.get("fingerprint") == fingerprint
            if not reused:
                cache.update({"blender_path": blender_path, "blender_version": version, "fingerprint": fingerprint, "checked_at": _now()})
            return {"fingerprint": fingerprint, "reused": reused, "environment": dict(cache)}
        return self._update(mutate)

    def resume(self) -> dict[str, Any]:
        state = self.read()
        design_ok = coarse_ok = input_ok = production_ok = False
        try:
            self._input_unchanged(state)
            input_ok = True
        except (ApprovalError, RuntimeErrorBase):
            pass
        try:
            self.require_approval()
            design_ok = True
        except (ApprovalError, RuntimeErrorBase):
            pass
        try:
            self.require_finish()
            coarse_ok = True
        except (ApprovalError, RuntimeErrorBase):
            pass
        current = (state.get("design_revisions") or [{}])[-1]
        production = state.get("production", {})
        production_ok = design_ok and bool(production.get("plan")) and production.get("design_revision") == current.get("revision")
        return {"job_id": state["job_id"], "input": state["input"], "stage": state.get("stage"), "next_action": state.get("next_action"), "current_revision": current.get("revision"), "coarse_revision": (state.get("coarse_revisions") or [{}])[-1].get("revision"), "input_valid": input_ok, "design_approved": design_ok, "coarse_approved": coarse_ok, "production_checked": production_ok}

    def scene_lock(self, scene_path: str | os.PathLike[str] | None = None) -> contextlib.AbstractContextManager[None]:
        target = Path(scene_path).resolve() if scene_path else self.state_path.resolve()
        return file_lock(target.with_suffix(target.suffix + ".scene.lock"))


def mcp_status_error(response: Any) -> str | None:
    """Return a compact error from common MCP/JSON response shapes."""
    if not isinstance(response, dict):
        return "invalid MCP response"
    if response.get("isError") is True:
        content = response.get("content") or []
        text = " ".join(item.get("text", "") for item in content if isinstance(item, dict)).strip()
        return text or "MCP tool reported an error"
    error = response.get("error")
    if error:
        return error if isinstance(error, str) else json.dumps(error, sort_keys=True)
    structured = response.get("structuredContent")
    if isinstance(structured, dict):
        status = str(structured.get("status", "")).lower()
        if status in {"error", "failed", "failure"}:
            return str(structured.get("message") or structured.get("error") or status)
    for item in response.get("content") or []:
        if isinstance(item, dict) and isinstance(item.get("text"), str):
            text = item["text"].strip()
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                parsed = None
            if isinstance(parsed, dict) and str(parsed.get("status", "")).lower() in {"error", "failed", "failure"}:
                return str(parsed.get("message") or parsed.get("error") or parsed["status"])
    return None


def environment_fingerprint(blender_path: str, version: str) -> str:
    return stable_hash({"path": blender_path, "version": version, "python": platform.python_version()})


def _cli() -> int:
    parser = argparse.ArgumentParser(description="Approval-gated image-to-3D job state runtime")
    parser.add_argument("--state", required=True, help="JSON state file")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("init"); p.add_argument("input"); p.add_argument("--environment-json")
    p = sub.add_parser("design"); p.add_argument("design_json"); p.add_argument("--label")
    p = sub.add_parser("approve"); p.add_argument("revision"); p.add_argument("--approved-by", required=True); p.add_argument("--evidence", required=True)
    p = sub.add_parser("production-check"); p.add_argument("plan_json"); p.add_argument("--revision")
    p = sub.add_parser("coarse-register"); p.add_argument("artifact_json"); p.add_argument("--revision", required=True); p.add_argument("--label")
    p = sub.add_parser("coarse-approve"); p.add_argument("coarse_revision"); p.add_argument("--approved-by", required=True); p.add_argument("--evidence", required=True)
    p = sub.add_parser("finish-check"); p.add_argument("--revision"); p.add_argument("--coarse-revision")
    sub.add_parser("resume")
    args = parser.parse_args()
    runtime = Runtime(args.state)
    if args.command == "init":
        value = json.loads(args.environment_json) if args.environment_json else None
        result = runtime.init(args.input, value)
    elif args.command == "design":
        result = runtime.register_design(json.loads(Path(args.design_json).read_text(encoding="utf-8")), args.label)
    elif args.command == "approve":
        result = runtime.approve(args.revision, args.approved_by, args.evidence)
    elif args.command == "production-check":
        result = runtime.production_check(json.loads(Path(args.plan_json).read_text(encoding="utf-8")), args.revision)
    elif args.command == "coarse-register":
        result = runtime.register_coarse(args.revision, json.loads(Path(args.artifact_json).read_text(encoding="utf-8")), args.label)
    elif args.command == "coarse-approve":
        result = runtime.approve_coarse(args.coarse_revision, args.approved_by, args.evidence)
    elif args.command == "finish-check":
        result = runtime.require_finish(args.revision, args.coarse_revision)
    else:
        result = runtime.resume()
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
