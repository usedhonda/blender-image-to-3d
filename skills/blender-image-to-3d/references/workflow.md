# Production workflow

## Route selection

Choose the smallest route that can preserve the identity locks.

- Direct Blender: simple mascots, regular props, or designs where semantic parts matter more than organic reconstruction.
- Base mesh: human or anime characters that need a useful face, joints, UVs, or rig foundation.
- Image-to-3D: complex volume, clothing, or a fast candidate; always treat output as raw and repairable.
- Hybrid: base mesh for face/body, generated candidates for clothing, hair masses, or props.

Compare at most the permitted candidate count. If the same failure repeats, change the input or route before changing seeds. Keep raw output and a working copy.

## Reference design

Record identity locks (usually 5–8), head-to-body ratios, face landmarks, character-relative left/right asymmetry, parts, joins, camera, and unseen areas. Separate observed facts, reasonable inference, and unresolved choices. A generated back or side is a design proposal, not evidence.

Imagegen order: original analysis -> neutral design only if the pose hides required structure -> missing views -> inconsistency check -> adopt or discard. Keep front/back/side/oblique scale, landmarks, and palette consistent. Add top/bottom only for required geometry. Use separate files for provider multi-image inputs when required; a single contact sheet is a human review aid, not a universal API input.

## Implementation order

Block out head, torso, pelvis, limbs, hair masses, clothing, and props. Fix silhouette and proportion before small details. Bring face and major bangs into alignment early, then return to the body. Preserve semantic objects and meaningful names. Separate parts when later edits, joins, material assignment, or visibility checks require it; do not split every polygon.

For joins, inspect hairline/neck, clothing openings, hands/tools, shoes, accessories, and hidden intersections from oblique and back views. A repair may be local separation, a rebuilt part, base-mesh replacement, or route change. Record the repair and its fixed scope.

For direct scripts, prefer Blender data APIs where possible; isolate context-dependent operators. Write one scene at a time, verify affected objects/dimensions and required artifacts after each meaningful batch, and checkpoint before topology, UV, shape-key, or rig changes. Re-running a stage must update semantic objects instead of duplicating them.

## Astra handoff

The plan must state units, X/Y/Z meaning and front direction, dimensions or anchors, part list, joins, route, material strategy, order, acceptance, permitted repairs, and fixed items. Pass only the approved scope, image revision and hashes, necessary reference files, current scene/checkpoint, and exact next action. Do not fork the entire design conversation or rediscover resolved choices. Use the bundled runtime interface when it is available; otherwise use a verified Blender Python or MCP entry point and record which one was used.
