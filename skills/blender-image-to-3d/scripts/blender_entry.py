#!/usr/bin/env python3
"""Single short-argument Blender entry point.

Run with Blender's Python (``blender --background --python blender_entry.py -- ...``).
Inspection is read-only.  Mutations require a job-owned output path and a current
human approval recorded by :mod:`runtime`.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Blender --python does not add the script directory to sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from runtime import Runtime


def _bpy():
    try:
        import bpy
    except ImportError as exc:  # pragma: no cover - exercised only on Blender host
        raise RuntimeError("Blender Python (bpy) is required for this operation") from exc
    return bpy


def inspect_scene() -> dict:
    bpy = _bpy()
    objects = list(bpy.data.objects)
    meshes = [obj for obj in objects if obj.type == "MESH"]
    names = [obj.name for obj in objects[:50]]
    dimensions = {obj.name: [round(float(value), 6) for value in obj.dimensions] for obj in objects[:50]}
    return {"scene": bpy.context.scene.name, "object_count": len(objects), "object_names": names, "dimensions": dimensions, "mesh_count": len(meshes), "mesh_vertices": sum(len(obj.data.vertices) for obj in meshes), "mesh_polygons": sum(len(obj.data.polygons) for obj in meshes), "material_count": len(list(bpy.data.materials))}


def _mutation_guard(runtime: Runtime, revision: str, output: Path, job_id: str, stage: str) -> None:
    state = runtime.read()
    if state.get("job_id") != job_id:
        raise RuntimeError("job_id does not own this output")
    runtime.require_approval(revision)
    runtime.require_production(revision)
    state = runtime.read()
    if stage == "final":
        runtime.require_finish(revision)
    if not output.is_absolute():
        raise RuntimeError("mutation output must be an absolute job-owned path")
    output_root_value = state.get("output_root")
    if not output_root_value:
        raise RuntimeError("state has no job-owned output_root")
    output_root = Path(output_root_value).resolve()
    try:
        output.resolve().relative_to(output_root)
    except ValueError as exc:
        raise RuntimeError(f"output must be inside job-owned output_root: {output_root}")
    output.parent.mkdir(parents=True, exist_ok=True)


def upsert_object(name: str, object_type: str, data: dict | None = None, job_id: str | None = None) -> dict:
    """Update/create one job-owned Empty semantic object; preserve all other objects."""
    bpy = _bpy()
    if not job_id:
        raise RuntimeError("job_id is required for semantic upsert")
    scoped_name = f"it3d_{job_id}_{name}"
    obj = bpy.data.objects.get(scoped_name)
    created = obj is None
    if obj is not None and obj.get("image_to_3d_owner") != job_id:
        raise RuntimeError("existing semantic object is owned by another job")
    if obj is None:
        obj = bpy.data.objects.new(scoped_name, None)
        bpy.context.scene.collection.objects.link(obj)
    obj["image_to_3d_owner"] = job_id
    obj["image_to_3d_semantic_type"] = object_type
    for key, value in (data or {}).items():
        obj[key] = value
    return {"name": obj.name, "created": created, "kind": "empty_semantic_object"}


def run(argv: list[str] | None = None) -> dict:
    parser = argparse.ArgumentParser(description="Reusable Blender image-to-3D operations")
    parser.add_argument("--operation", choices=("inspect", "render", "save", "reopen", "upsert"), required=True)
    parser.add_argument("--state", required=True)
    parser.add_argument("--revision")
    parser.add_argument("--job-id")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--name")
    parser.add_argument("--object-type", default="semantic")
    parser.add_argument("--data-json", default="{}")
    raw = list(sys.argv[1:] if argv is None else argv)
    if "--" in raw:
        raw = raw[raw.index("--") + 1:]
    parser.add_argument("--stage", choices=("coarse", "final"), default="final")
    parser.add_argument("--view", default="front")
    parser.add_argument("--resolution", default="")
    args = parser.parse_args(raw)
    runtime = Runtime(args.state)
    if args.operation == "inspect":
        return inspect_scene()
    if not args.revision or not args.job_id or not args.output:
        raise RuntimeError("mutating operations require --revision, --job-id, and --output")
    _mutation_guard(runtime, args.revision, args.output, args.job_id, args.stage)
    bpy = _bpy()
    state = runtime.read()
    scene_identity = getattr(bpy.data, "filepath", "") or str(Path(state["output_root"]) / "scene.blend")
    with runtime.scene_lock(scene_identity):
        if args.operation == "render":
            render = bpy.context.scene.render
            scene = bpy.context.scene
            camera_name = f"it3d_{args.job_id}_camera_{args.view}"
            camera = bpy.data.objects.get(camera_name)
            if camera is None or camera.type != "CAMERA" or camera.get("image_to_3d_owner") != args.job_id:
                raise RuntimeError(f"missing job-owned comparison camera: {camera_name}")
            old = (render.filepath, render.resolution_x, render.resolution_y, render.resolution_percentage, scene.camera)
            try:
                scene.camera = camera
                render.filepath = str(args.output)
                if args.resolution:
                    width, height = (int(value) for value in args.resolution.lower().split("x", 1))
                    render.resolution_x, render.resolution_y, render.resolution_percentage = width, height, 100
                elif args.stage == "coarse":
                    render.resolution_x = render.resolution_y = 512
                    render.resolution_percentage = 100
                bpy.ops.render.render(write_still=True)
            finally:
                render.filepath, render.resolution_x, render.resolution_y, render.resolution_percentage, scene.camera = old
            return {"operation": "render", "output": str(args.output)}
        if args.operation == "save":
            bpy.ops.wm.save_as_mainfile(filepath=str(args.output))
            return {"operation": "save", "output": str(args.output)}
        if args.operation == "reopen":
            if getattr(bpy.data, "is_dirty", False):
                raise RuntimeError("refusing to reopen while current scene has unsaved changes")
            bpy.ops.wm.open_mainfile(filepath=str(args.output))
            return {"operation": "reopen", "output": str(args.output)}
        if not args.name:
            raise RuntimeError("upsert requires --name")
        result = upsert_object(args.name, args.object_type, json.loads(args.data_json), args.job_id)
        bpy.ops.wm.save_as_mainfile(filepath=str(args.output))
        return {"operation": "upsert", "output": str(args.output), **result}


if __name__ == "__main__":
    try:
        print(json.dumps(run(), sort_keys=True))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        raise SystemExit(2)
