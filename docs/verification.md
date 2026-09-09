# Verification matrix

This document separates completed evidence from pending checks. It is intentionally conservative: a pending character run is not represented as a successful production result.

| Surface | Evidence | Status | Remaining check |
|---|---|---|---|
| Blender direct scene operation | Blender 5.2.1 environment produced the reference cube render through direct operation. | Verified baseline | Repeat only if Blender version or runtime changes. |
| Official Blender MCP | The same Blender 5.2.1 environment produced an identical cube render through the official MCP route. | Verified baseline | Confirm the exact MCP package/version if the host changes. |
| Save and reopen | The baseline cube scene saved and reopened successfully. | Verified baseline | Verify the character `.blend` after the approved run. |
| Imagegen background cleanup | A clean RGB reference with a white background was observed; alpha transparency was not claimed. | Verified handling rule | Inspect alpha mode for each future imagegen result. |
| Design approval | The workflow requires an approved complete design revision before production. | Pending for current character | Approve the selected character's staged design revision; the earlier robot R2 is not an approval for this run. |
| Coarse geometry and representative materials | The workflow requires a second human gate before finish work. | Pending for current character | Produce the face/hair coarse pass after its design approval and obtain the gate. |
| Astra high design/review host | Documentation defines explicit high reasoning selection when available. | Host/config dependent | Read back the actual host/model configuration at execution time. |
| Astra low production host | Documentation defines explicit low reasoning handoff with no fork. | Not run for current character | Execute after the complete design revision is approved; then obtain the separate coarse geometry/material approval before finish work. |
| Imagegen/reference set | An earlier robot R2 trial produced multiple views and material references; it was not adopted for character production. | Historical trial only | Start the selected character from its single original; add and approve references only when the staged run needs them. |
| Editable semantic parts and joins | Required by the skill and templates. | Pending for current character | Inspect named parts, hairline/neck, clothing, accessories, and hidden intersections. |
| Export and re-import | Required completion gate. | Pending for current character | Export requested format, import into a clean scene, and render again. |
| Motion/expressions/print | Separate optional completion gates. | Not claimed | Run only when requested and their specific checks are in scope. |

## Reproduction notes

The baseline check proves the direct and official-MCP scene paths for a simple cube in the recorded Blender 5.2.1 environment. It does not prove anime identity, image-to-3D quality, Astra Low behavior, provider cost, or character rig quality. Those remain explicit acceptance checks for the approved production run.

MCP is optional. If it is unavailable, the skill may use Blender's Python or another verified local route, but it must not claim MCP evidence for that route. If an external provider times out after acceptance, query its task state before retrying.

## Runtime and distribution checks

- Focused stdlib tests cover pre-approval refusal, original/design asset changes, detailed plan validation, independent coarse approval, checkpoint reuse and affected views, unknown-job reconciliation, nested MCP errors, Blender argument parsing, and namespaced Empty idempotency. The Blender-free fixture is not live geometry proof.
- The packaged entry script was executed by Blender 5.2.1 LTS for a read-only scene inspection: three default objects, one mesh, eight vertices, six polygons. The live test caught and fixed Blender's missing sibling-module search path. Direct commands use `--python-exit-code 1` so a Python exception cannot be mistaken for success.
- Skill and plugin format validators passed. Codex `skills/list` discovered the local skill as enabled under the qualified name `blender-image-to-3d:blender-image-to-3d`. Discovery is not a completed production invocation.
- No token reduction percentage is claimed. The image-reference trial used five image-generation calls (including one failed RGB checkerboard extraction and its white-background replacement, then one material correction). No image-generation token usage was exposed.
- The original manual, generated demo images, production state, and local environment records are excluded from Git.

Reproduced failures and their reusable fixes are documented in [workflow troubleshooting](../skills/blender-image-to-3d/references/troubleshooting.md), including Blender sibling imports, misleading process exit status, RGB checkerboards, material drift, and independent resume validity fields.

## Efficiency workflow revision

The 2026-09-09 revision changes instructions and Markdown templates only; runtime CLI, JSON state, approval validation, and existing jobs remain compatible. Existing live Blender baseline evidence is reused. No character production or paid comparison was performed, and no savings percentage is established.

| Scenario | Instruction walkthrough result | Evidence limit |
|---|---|---|
| Initial production | Inspect immutable input, approve full design, pass only the bounded contract to Low, batch blockout, then require coarse approval. References are selected for the chosen route. | Documentation consistency, not a live character run. |
| Local repair | Name the discrepancy and fixed properties, invalidate affected evidence, and inspect the relevant views under matching conditions. No fixed repair count or automatic full turntable. | No measured repair-token reduction. |
| Long render wait | Use host waiting/completion signals within responsiveness constraints; an empty timeout does not authorize a restart or duplicate request. | Actual host scheduling remains environment-dependent. |
| Saved-state resume | Validate current state, retain scripts and artifacts, reuse still-valid evidence, and execute the recorded next action. | Existing runtime checks remain the state-validation authority. |

The quality template records available usage across stages and agents, separates API accounting from Codex quota, and prevents cumulative-counter and reasoning double counting. Missing data remains unknown. The optional [token efficiency reference](../skills/blender-image-to-3d/references/token-efficiency.md) separates official facts from unmeasured workflow hypotheses.

## Practitioner knowledge integration

Documentation now distinguishes input/environment route selection, representative reusable construction, human design preference vs technical acceptance, and actual production history vs showcase imagery. The chronological template starts from one original and records added references and repairs. These are workflow requirements, not new live production evidence. Issue #3 requires runtime corrections, an approved character production run, and repeat quality evidence. Runtime corrections alone do not close the issue.

## Issue #3 runtime correction

The runtime now validates typed dimensions, axes, named parts, material values, route assets/transforms, and approved reference hashes. Resume, coarse registration, and Blender mutation revalidate the stored plan. Passed checkpoints require verified file hashes or an explicit fileless result; deleted, modified, and hashless legacy artifacts are not reused.

The old revision reproduced both acceptance of placeholder plans and reuse of a deleted hashless result. Focused regressions cover the corrected boundaries, including matching-key missing/modified artifacts and stored-plan mutation refusal. An independent representative checkpoint test passed after diff inspection. This is runtime evidence, not character quality or hair-motion proof; Issue #3 remains open for its production and repeat-run criteria.

## Reference-image fidelity pitfalls

A reference-cleanup trial exposed identity drift despite source-preservation instructions: contour, facial marks, and shading changed the perceived softness. The guidance now separates cleanup from fidelity, original authority from supplemental adoption, and aesthetic polish from source match. It makes cleanup optional and records original/previous/current comparison and scoped acceptance. More detailed prompts are a repair method, not evidence of exact preservation.

This revision changes instructions and templates only. It adds no image-generation run, runtime behavior, character-quality proof, or measured savings claim. Private trial assets remain outside the public repository.

## Failed character trial and quality decision correction

A local character trial saved/reopened successfully but failed likeness. The implementation used estimated ring/curve parameters and facial overlays without adequate correspondence to the adopted design. Subsequent local improvements were incorrectly treated as grounds to request stage advancement; the user rejected the result. The procedural character method remains unverified for the intended quality. Save/reopen evidence proves only that technical operation.

The skill now separates original provenance from the adopted modeling target, requires target-relative visual judgment during construction, and rejects known failures before human preference approval. Further execution needs a supported cause/intervention/expected-improvement link; otherwise the method is reassessed. This documentation correction does not establish successful character production or token savings. Private trial artifacts remain excluded.
