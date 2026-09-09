# Image-to-3D runtime interface

`runtime.py` is a dependency-free state machine for handing a job from image
intake through design approval and production. It records the SHA-256 of the
original input, immutable design revisions, human approval evidence, detailed
production plans, environment fingerprints, resumable checkpoints, and external
job request hashes. Design `assets` must be file-backed `{path, sha256}` entries;
the input and every asset are rehashed at approval time. It never calls a
provider or stores credentials.

```sh
python3 scripts/runtime.py --state work/state.json init input.png
python3 scripts/runtime.py --state work/state.json design design.json
python3 scripts/runtime.py --state work/state.json approve r1 --approved-by 'Name' --evidence 'ticket/URL or signed note'
python3 scripts/runtime.py --state work/state.json production-check plan.json --revision r1
python3 scripts/runtime.py --state work/state.json coarse-register coarse.json --revision r1
python3 scripts/runtime.py --state work/state.json coarse-approve c1 --approved-by 'Name' --evidence 'coarse review note'
python3 scripts/runtime.py --state work/state.json finish-check --revision r1 --coarse-revision c1
python3 scripts/runtime.py --state work/state.json resume
```

Registering a new or changed design clears approval. Approval is valid only when its
revision and design hash match the current revision. `production-check` requires
non-empty `dimensions`, `axes`, `parts`, `joins`, `materials`, `fixed_scope`,
`steps`, `outputs`, and `validation` fields. A job marked `unknown`
cannot be retried by reserving/submitting another request with the same stable
request hash; inspect the external system first.

Coarse geometry/materials have a separate revision and human approval gate.
`finish-check` requires both the current design approval and matching coarse
approval, so design approval alone cannot authorize fine detail, rigging, or
expensive work.

`blender_entry.py` is the sole Blender entry script. `inspect` is read-only;
`render`, `save`, `reopen`, and `upsert` require `--state`, `--revision`,
`--job-id`, and an absolute `--output` path. Operations take a scene lock.
`upsert` creates or updates a job-owned Empty semantic object under a namespaced
name and preserves other objects; it does not reset or delete a scene. Mutations
require a checked production plan; `--stage final` additionally requires the
coarse-model approval gate. Blender's full argv is accepted, while direct and
MCP callers share this same entry script.

```sh
blender --background --python-exit-code 1 --python scripts/blender_entry.py -- \
  --operation inspect --state work/state.json
```
