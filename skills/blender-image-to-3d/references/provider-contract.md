# External provider contract

Record provider, actual model identifier, input hashes, settings, submission time, task id, state, cost/usage if exposed, and output locations. Keep credentials in the runtime secret store, never in templates or state.

Use explicit provider fields; do not copy one service's model, image, polling, or output fields into another. A request may be accepted while the client timed out. Distinguish `unsent`, `accepted`, `processing`, `succeeded`, `failed`, and `unknown`. On `unknown`, query the task id or provider history before retrying. Download and import-check outputs before calling them usable; temporary URLs are not final deliverables.

External image generation, 3D generation, uploads, paid jobs, and third-party assets require explicit permission and a defined budget/rights scope. Do not assume a local model's hardware requirements, a free service's free compute, or a public asset's commercial license. Preserve source ownership and provenance.

Provider versions, endpoints, Blender add-ons, and hardware requirements drift. Verify current official docs at execution time and record the date/version; this skill does not pin a vendor as universally best.
