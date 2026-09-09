# Production workflow

## Route selection

Choose the smallest route that can preserve the identity locks.

- Direct Blender: simple mascots, regular props, or designs where semantic parts matter more than organic reconstruction.
- Base mesh: human or anime characters that need a useful face, joints, UVs, or rig foundation.
- Image-to-3D: complex volume, clothing, or a fast candidate; always treat output as raw and repairable.
- Hybrid: base mesh for face/body, generated candidates for clothing, hair masses, or props.

Before selecting a route, record face readability, occlusion, perspective, visible scope, hair/clothing complexity, available tools/assets, permitted services, and budget. Do not infer a whole body from a face-only input without adopting that scope.

| Condition | Route or preparation |
|---|---|
| Readable simple mascot or geometric prop | Direct parameterized Blender construction |
| Human/anime face requiring stable editable structure | Evaluate an available suitable base mesh or VRoid-based route against identity locks, editability, import support, and asset/license terms; neither VRoid nor custom geometry is mandatory |
| Identity-critical regions hidden or too small | Request or generate only the missing reference information for approval before geometry production |
| Complex volume outside the validated direct/base route | Consider an authorized generated candidate or hybrid; retain import and repair checks |
| Connection/setup stalls | Separate connection diagnosis from modeling quality; use another verified local route when available rather than repeatedly testing the same setup |

Route changes must preserve the approved scope and identity. Obtain authorization for new services, costs, or data transfers; do not silently substitute a generic character. A route is validated only for completed examples, not because its tool connected.

Compare at most the permitted candidate count. If the same failure repeats, change the input or route before changing seeds. Keep raw output and a working copy.

## Reference design

Record identity locks (usually 5–8), head-to-body ratios, face landmarks, character-relative left/right asymmetry, parts, joins, camera, and unseen areas. Separate observed facts, reasonable inference, and unresolved choices. A generated back or side is a design proposal, not evidence.

Imagegen order: original analysis -> neutral design only if the pose hides required structure -> missing views -> inconsistency check -> adopt or discard. Keep front/back/side/oblique scale, landmarks, and palette consistent. Add top/bottom only for required geometry. Use separate files for provider multi-image inputs when required; a single contact sheet is a human review aid, not a universal API input.

## Representative construction and materials

Establish a representative accepted part or assembly before spreading its construction method across the model. Keep parameterized builders and shared materials reusable; do not require a new from-scratch generator for every character. A successful geometric prop is not evidence for an organic face.

Compare representative materials under the same lighting before detailed assignment. Reuse named skin/hair/eye/clothing materials when appropriate instead of creating duplicates per part. Preserve deliberate differences. Record any human mesh edits and reconcile them with the saved script/checkpoint before rerunning a generator, so accepted manual work is not overwritten.

## Implementation order

Block out head, torso, pelvis, limbs, hair masses, clothing, and props. Fix silhouette and proportion before small details. Bring face and major bangs into alignment early, then return to the body. Preserve semantic objects and meaningful names. Separate parts when later edits, joins, material assignment, or visibility checks require it; do not split every polygon.

For joins, inspect hairline/neck, clothing openings, hands/tools, shoes, accessories, and hidden intersections from oblique and back views. A repair may be local separation, a rebuilt part, base-mesh replacement, or route change. Record the repair and its fixed scope.

For direct scripts, prefer Blender data APIs where possible; isolate context-dependent operators. Write one scene at a time, verify affected objects/dimensions and required artifacts after each meaningful batch, and checkpoint before topology, UV, shape-key, or rig changes. Re-running a stage must update semantic objects instead of duplicating them.

## Astra handoff

The plan must state units, X/Y/Z meaning and front direction, dimensions or anchors, part list, joins, route, material strategy, order, acceptance, permitted repairs, and fixed items. Pass only the approved scope, image revision and hashes, necessary reference files, current scene/checkpoint, and exact next action. Do not fork the entire design conversation or rediscover resolved choices. Use the bundled runtime interface when it is available; otherwise use a verified Blender Python or MCP entry point and record which one was used.
