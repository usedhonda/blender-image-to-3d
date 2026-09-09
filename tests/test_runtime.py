import json
import hashlib
import tempfile
import unittest
import sys
import types
from unittest import mock
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "skills" / "blender-image-to-3d" / "scripts"))
from runtime import ApprovalError, DuplicateJobError, Runtime, RuntimeErrorBase, mcp_status_error
import blender_entry


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.input = self.root / "input.png"
        self.input.write_bytes(b"image")
        self.asset = self.root / "reference.png"
        self.asset.write_bytes(b"reference")
        self.runtime = Runtime(self.root / "state.json")
        self.runtime.init(self.input)

    def design(self, value):
        return {**value, "assets": [{"path": str(self.asset), "sha256": __import__("hashlib").sha256(self.asset.read_bytes()).hexdigest()}]}

    def plan(self, **overrides):
        value = {
            "dimensions": {"units": "meters", "overall_height": 1.8},
            "axes": {"up": "+Z", "front": "-Y", "right": "+X"},
            "parts": [{"name": "head", "dimensions": [0.4, 0.3, 0.4], "location": [0, 0, 1.5]}],
            "joins": ["neck overlap 0.02m"],
            "materials": [{"name": "body", "base_color_srgb": [0.7, 0.4, 0.3], "roughness": 0.5, "metallic": 0}],
            "fixed_scope": ["approved proportions"],
            "steps": ["build", "check"],
            "outputs": ["model.blend"],
            "validation": ["save and reopen"],
            "references": [{"path": str(self.asset), "sha256": hashlib.sha256(self.asset.read_bytes()).hexdigest()}],
        }
        value.update(overrides)
        return value

    def tearDown(self):
        self.tmp.cleanup()

    def test_revision_approval_and_design_invalidation(self):
        self.assertTrue(self.runtime.resume()["input_valid"])
        self.assertFalse(self.runtime.resume()["design_approved"])
        first = self.runtime.register_design(self.design({"objects": ["hero"]}))
        with self.assertRaises(ApprovalError):
            self.runtime.approve(first["revision"], "", "")
        self.runtime.approve(first["revision"], "human", "review-123")
        self.runtime.require_approval(first["revision"])
        second = self.runtime.register_design(self.design({"objects": ["hero", "camera"]}))
        self.assertNotEqual(first["design_hash"], second["design_hash"])
        with self.assertRaises(ApprovalError):
            self.runtime.require_approval(second["revision"])

    def test_asset_or_original_mutation_invalidates_approval_and_init_is_immutable(self):
        design = self.runtime.register_design(self.design({"objects": ["hero"]}))
        self.runtime.approve(design["revision"], "human", "review")
        self.input.write_bytes(b"changed original")
        self.assertFalse(self.runtime.resume()["input_valid"])
        with self.assertRaises(ApprovalError):
            self.runtime.require_approval(design["revision"])
        self.input.write_bytes(b"image")
        self.asset.write_bytes(b"changed")
        with self.assertRaises(ApprovalError):
            self.runtime.require_approval(design["revision"])
        with self.assertRaises(Exception):
            self.runtime.init(self.input)

    def test_production_requires_detailed_plan(self):
        rev = self.runtime.register_design(self.design({"mesh": "low-poly"}))
        with self.assertRaises(ApprovalError):
            self.runtime.production_check({"steps": ["build"]}, rev["revision"])
        self.runtime.approve(rev["revision"], "human", "signed note")
        with self.assertRaises(Exception):
            self.runtime.production_check({"steps": ["build"]}, rev["revision"])
        plan = self.plan()
        result = self.runtime.production_check(plan, rev["revision"])
        self.assertTrue(result["production"]["plan"])

    def test_production_rejects_placeholder_and_bad_types(self):
        rev = self.runtime.register_design(self.design({"mesh": "low-poly"}))
        self.runtime.approve(rev["revision"], "human", "signed note")
        with self.assertRaises(Exception):
            self.runtime.production_check(self.plan(dimensions={"overall_height": "SET_FROM_APPROVED_DESIGN"}), rev["revision"])
        with self.assertRaises(Exception):
            self.runtime.production_check(self.plan(parts=[{"name": "head", "dimensions": [True, 1, 1], "location": [0, 0, 0]}]), rev["revision"])
        with self.assertRaises(Exception):
            self.runtime.production_check(self.plan(axes={"up": "+Z", "front": "+Z", "right": "+X"}), rev["revision"])

    def test_invalid_stored_plan_cannot_resume_or_register_coarse(self):
        rev = self.runtime.register_design(self.design({"mesh": "low-poly"}))
        self.runtime.approve(rev["revision"], "human", "signed note")
        self.runtime.production_check(self.plan(), rev["revision"])
        self.runtime._update(lambda state: state["production"]["plan"].pop("dimensions"))
        self.assertFalse(self.runtime.resume()["production_checked"])
        with self.assertRaises(RuntimeErrorBase):
            self.runtime.require_production(rev["revision"])
        with self.assertRaises(RuntimeErrorBase):
            self.runtime.register_coarse(rev["revision"], self.design({"vertices": 10}))
        with self.assertRaises(RuntimeErrorBase):
            blender_entry._mutation_guard(self.runtime, rev["revision"], self.root / "outputs" / "blocked.blend", self.runtime.read()["job_id"], "coarse")

    def test_non_direct_route_requires_hashed_asset_and_transforms(self):
        rev = self.runtime.register_design(self.design({"mesh": "generated"}))
        self.runtime.approve(rev["revision"], "human", "signed note")
        with self.assertRaises(Exception):
            self.runtime.production_check(self.plan(route="generated"), rev["revision"])
        self.assertTrue(self.runtime.production_check(self.plan(route="generated", asset={"path": str(self.asset), "sha256": hashlib.sha256(self.asset.read_bytes()).hexdigest()}, transforms={"location": [0, 0, 0], "rotation": [0, 0, 0], "scale": [1, 1, 1]}), rev["revision"])["production"]["plan"])

    def test_checkpoint_and_ambiguous_job_are_idempotent(self):
        render = self.root / "front.png"
        render.write_bytes(b"render")
        render_hash = hashlib.sha256(render.read_bytes()).hexdigest()
        first = self.runtime.checkpoint("render", "input", "r1", {"blender": "5.2.1"}, {"view": "front"}, {"path": "front.png", "sha256": render_hash}, True)
        second = self.runtime.checkpoint("render", "input", "r1", {"blender": "5.2.1"}, {"view": "front"}, {"path": "front.png", "sha256": render_hash}, True)
        self.assertFalse(first["reused"])
        self.assertTrue(second["reused"])
        render.unlink()
        missing = self.runtime.checkpoint("render", "input", "r1", {"blender": "5.2.1"}, {"view": "front"}, {"fileless": True}, True)
        self.assertFalse(missing["reused"])
        self.assertTrue(missing["record"]["fileless"])
        self.assertTrue(self.runtime.checkpoint("render", "input", "r1", {"blender": "5.2.1"}, {"view": "front"}, {"fileless": True}, True)["reused"])
        changed_view = self.runtime.checkpoint("render", "input", "r1", {"blender": "5.2.1"}, {"view": "back"})
        self.assertFalse(changed_view["reused"])
        unperformed = self.runtime.checkpoint("render", "input", "r1", {"blender": "5.2.1"}, {"view": "back"})
        self.assertFalse(unperformed["reused"])
        modified = self.root / "modified.png"
        modified.write_bytes(b"before")
        modified_hash = hashlib.sha256(modified.read_bytes()).hexdigest()
        self.runtime.checkpoint("modified", "input", "r1", {"blender": "5.2.1"}, {"view": "front"}, {"path": "modified.png", "sha256": modified_hash}, True)
        modified.write_bytes(b"after")
        self.assertFalse(self.runtime.checkpoint("modified", "input", "r1", {"blender": "5.2.1"}, {"view": "front"}, {"fileless": True}, True)["reused"])
        with self.assertRaises(Exception):
            self.runtime.checkpoint("legacy", "input", "r1", {"blender": "5.2.1"}, result={"path": "missing.png"}, passed=True)
        job = self.runtime.reserve_job({"kind": "mesh", "revision": "r1"})
        self.assertTrue(self.runtime.reserve_job({"kind": "mesh", "revision": "r1"})["reused"])
        self.runtime.update_job(job["request_hash"], "unknown")
        with self.assertRaises(DuplicateJobError):
            self.runtime.update_job(job["request_hash"], "submitted")
        self.runtime.reconcile_job(job["request_hash"], "failed", "provider lookup: absent")

    def test_mcp_error_helper(self):
        self.assertEqual(mcp_status_error({"isError": True, "content": [{"text": "bad"}]}), "bad")
        self.assertIsNone(mcp_status_error({"structuredContent": {"ok": True}}))
        self.assertEqual(mcp_status_error({"structuredContent": {"status": "error", "message": "bad"}}), "bad")

    def test_finish_requires_independent_coarse_approval(self):
        design = self.runtime.register_design(self.design({"mesh": "coarse"}))
        self.runtime.approve(design["revision"], "human", "design-review")
        plan = self.plan()
        self.runtime.production_check(plan, design["revision"])
        coarse = self.runtime.register_coarse(design["revision"], self.design({"vertices": 100, "materials": ["skin"]}))
        with self.assertRaises(ApprovalError):
            self.runtime.require_finish(design["revision"], coarse["revision"])
        self.runtime.approve_coarse(coarse["revision"], "human", "coarse-review")
        self.assertEqual(self.runtime.require_finish(design["revision"], coarse["revision"])["revision"], coarse["revision"])
        changed = self.runtime.register_coarse(design["revision"], self.design({"vertices": 101, "materials": ["skin"]}))
        with self.assertRaises(ApprovalError):
            self.runtime.require_finish(design["revision"], changed["revision"])

    def test_synthetic_blender_entry_argv_and_job_owned_upsert(self):
        class Obj(dict):
            def __init__(self, name):
                super().__init__(); self.name = name; self.type = "EMPTY"; self.dimensions = (0, 0, 0); self.data = types.SimpleNamespace(vertices=[], polygons=[])
        class Objects(dict):
            def new(self, name, _data): self[name] = Obj(name); return self[name]
            def __iter__(self): return iter(self.values())
        objects = Objects()
        foreign = Obj("it3d_job_foreign"); foreign["image_to_3d_owner"] = "other"; objects[foreign.name] = foreign
        class Collection:
            objects = types.SimpleNamespace(link=lambda obj: None)
        scene = types.SimpleNamespace(name="Test", collection=Collection())
        fake = types.SimpleNamespace(data=types.SimpleNamespace(objects=objects, materials=[]), context=types.SimpleNamespace(scene=scene))
        with mock.patch.dict(sys.modules, {"bpy": fake}):
            self.assertEqual(blender_entry.run(["--operation", "inspect", "--state", str(self.root / "state.json")])["scene"], "Test")
            created = blender_entry.upsert_object("body", "coarse", {"part": "body"}, "job")
            repeated = blender_entry.upsert_object("body", "coarse", {"part": "body"}, "job")
            self.assertTrue(created["created"])
            self.assertFalse(repeated["created"])
            self.assertEqual(len(objects), 2)
            with self.assertRaises(RuntimeError):
                blender_entry.upsert_object("foreign", "coarse", {}, "job")


if __name__ == "__main__":
    unittest.main()
