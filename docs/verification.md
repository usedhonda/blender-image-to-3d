# Verification matrix

This document separates completed evidence from pending checks. It is intentionally conservative: a pending character run is not represented as a successful production result.

| Surface | Evidence | Status | Remaining check |
|---|---|---|---|
| Blender direct scene operation | Blender 5.2.1 environment produced the reference cube render through direct operation. | Verified baseline | Repeat only if Blender version or runtime changes. |
| Official Blender MCP | The same Blender 5.2.1 environment produced an identical cube render through the official MCP route. | Verified baseline | Confirm the exact MCP package/version if the host changes. |
| Save and reopen | The baseline cube scene saved and reopened successfully. | Verified baseline | Verify the character `.blend` after the approved run. |
| Imagegen background cleanup | A clean RGB reference with a white background was observed; alpha transparency was not claimed. | Verified handling rule | Inspect alpha mode for each future imagegen result. |
| Design approval | The workflow requires an approved complete design revision before production. | Pending for current character | Obtain the user's R2 design approval. |
| Coarse geometry and representative materials | The workflow requires a second human gate before finish work. | Pending for current character | Produce the coarse pass after R2 approval and obtain the gate. |
| Astra high design/review host | Documentation defines explicit high reasoning selection when available. | Host/config dependent | Read back the actual host/model configuration at execution time. |
| Astra low production host | Documentation defines explicit low reasoning handoff with no fork. | Not run for current character | Execute after the complete design revision is approved; then obtain the separate coarse geometry/material approval before finish work. |
| Imagegen/reference set | R2 produced front, back, side, oblique, top, and sole views, plus neutral/smile references and four material references. | Evidence available; design approval pending | Obtain approval, then use only the approved views and record observed versus inferred content. |
| Editable semantic parts and joins | Required by the skill and templates. | Pending for current character | Inspect named parts, hairline/neck, clothing, accessories, and hidden intersections. |
| Export and re-import | Required completion gate. | Pending for current character | Export requested format, import into a clean scene, and render again. |
| Motion/expressions/print | Separate optional completion gates. | Not claimed | Run only when requested and their specific checks are in scope. |

## Reproduction notes

The baseline check proves the direct and official-MCP scene paths for a simple cube in the recorded Blender 5.2.1 environment. It does not prove anime identity, image-to-3D quality, Astra Low behavior, provider cost, or character rig quality. Those remain explicit acceptance checks for the approved production run.

MCP is optional. If it is unavailable, the skill may use Blender's Python or another verified local route, but it must not claim MCP evidence for that route. If an external provider times out after acceptance, query its task state before retrying.

## Runtime and distribution checks

- Seven focused stdlib tests cover pre-approval refusal, original/design asset changes, detailed plan validation, independent coarse approval, checkpoint reuse and affected views, unknown-job reconciliation, nested MCP errors, Blender argument parsing, and namespaced Empty idempotency. The Blender-free fixture is not live geometry proof.
- The packaged entry script was executed by Blender 5.2.1 LTS for a read-only scene inspection: three default objects, one mesh, eight vertices, six polygons. The live test caught and fixed Blender's missing sibling-module search path. Direct commands use `--python-exit-code 1` so a Python exception cannot be mistaken for success.
- Skill and plugin format validators passed. Codex `skills/list` discovered the local skill as enabled under the qualified name `blender-image-to-3d:blender-image-to-3d`. Discovery is not a completed production invocation.
- No token reduction percentage is claimed. The image-reference trial used five image-generation calls (including one failed RGB checkerboard extraction and its white-background replacement, then one material correction). No image-generation token usage was exposed.
- The original manual, generated demo images, production state, and local environment records are excluded from Git.

Reproduced failures and their reusable fixes are documented in [workflow troubleshooting](../skills/blender-image-to-3d/references/troubleshooting.md), including Blender sibling imports, misleading process exit status, RGB checkerboards, material drift, and independent resume validity fields.
