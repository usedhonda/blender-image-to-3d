# Local runtime interface

Run commands from the installed skill directory, or substitute its absolute script path. Keep the job directory outside the skill installation. `scripts/runtime.py init` creates the authoritative state; do not overwrite it with a template on resume. The bundled runtime records approvals; it cannot prove who typed a CLI command. Only record an approval after an actual user response, with that response's reference and approved image revision. Never self-approve a real job.

```bash
python3 scripts/runtime.py --state /absolute/job/state.json init /absolute/job/original.png
python3 scripts/runtime.py --state /absolute/job/state.json design /absolute/job/design.json --label R1
python3 scripts/runtime.py --state /absolute/job/state.json resume
```

`templates/design.json` illustrates the asset contract: each design image has a real file path and SHA-256. Resolve paths absolutely when preparing a job so changing the working directory does not change their meaning. A new design revision clears design approval, the production plan, and coarse approval. Re-registering an unchanged revision is idempotent. Changing the original or approved asset bytes makes the gate fail even if the JSON path is unchanged.

After the user approves the exact candidate, record their response using `approve <revision> --approved-by <human> --evidence <response-reference>`. Save the detailed plan described in `templates/plan.md`; `templates/plan.json` shows its machine-readable fields. Replace all example values and file references with the adopted design. `production-check <plan.json> --revision <revision>` requires finite numeric dimensions, signed orthogonal axes, named parts with positive dimensions and locations, unique materials with bounded color/roughness/metallic values, non-placeholder string lists for joins/scope/steps/outputs/validation, and references matching the approved design asset hashes. Direct plans use measured part dimensions and placement. `base_mesh`, `generated`, and `hybrid` plans additionally require an existing file-backed `asset` (or `source_asset`) with its SHA-256 and complete location, rotation, and scale transforms. A checked plan is revalidated at coarse registration, resume, and every Blender mutation, so editing a stored plan cannot bypass the gate.

After coarse geometry and representative materials exist, register their immutable file-backed review snapshot with `coarse-register <artifact.json> --revision <design-revision>`. Present it to the user, then record the actual response with `coarse-approve <coarse-revision> --approved-by <human> --evidence <response-reference>`. `finish-check` checks both gates. Preserve the approved coarse snapshot; refine a separate working file.

## Blender transport

The direct and MCP paths import the same `scripts/blender_entry.py`. Use a separate background process for batch construction; use MCP for a saved, job-owned interactive scene. Never reset an existing scene. `inspect` is read-only. `save`, `render`, `reopen`, and `upsert` require a checked plan and job-owned output path; final-stage operations also require coarse approval. `upsert` is an Empty-object ownership helper, not a mesh generator. The execution agent writes the task-specific, parameterized geometry script from the plan.

```bash
blender --background --python-exit-code 1 --python /absolute/skill/scripts/blender_entry.py -- \
  --operation inspect --state /absolute/job/state.json
```

An MCP execution snippet can import the entry module from its installed script directory and call `run([...])` with the same short arguments. Do not copy geometry code into repeated tool calls. Treat `isError`, `structuredContent.status`, and embedded JSON error results as failures; `mcp_status_error` checks these representations. A transport success is not artifact proof.

The Python API also exposes checkpoint records (input, revision, environment, affected parts/views, result, pass status), preflight fingerprints, stable external-job reservations, and job-state reconciliation. Passed checkpoints must explicitly declare `fileless: true` or provide an `artifacts` list of `{path, sha256}` records; the legacy single `result.path` shape remains accepted only when it also supplies `result.sha256`. Relative artifact paths resolve against the state file's parent. Missing or changed artifacts invalidate only that checkpoint and prevent reuse; a hashless legacy file record is never reusable. Read `scripts/README.md` for the current API details. These helpers do not send requests or authorize external services. A reused reservation is never permission to submit again; an ambiguous request must be reconciled with the provider.
