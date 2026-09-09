---
name: blender-image-to-3d
description: Build an editable Blender model from an approved reference image, using imagegen, direct Blender work, a base mesh, or image-to-3D as appropriate. Use when the user wants an image-derived character or object in Blender; default to a static, editable result that preserves the source style.
metadata:
  short-description: Turn an approved image into an editable Blender model
---

# Blender image to 3D

Invoke as `$blender-image-to-3d /path/to/image`. Treat the supplied image as the identity source. The default deliverable is a static, editable `.blend`, GLB, and review renders; do not infer rigging, animation, or 3D printing unless requested. Preserve the source style, proportions, asymmetry, and visible design. Keep inferred back/inside details marked as inferred.

## Gates and scope

Ask only questions that change the finished result: intended use, scope (head/bust/full body), identity priorities, unseen-part choice, external generation permission/budget, and requested expressions or motion. If unspecified, choose a static model of the visible scope, prioritize face/hair/silhouette, and record assumptions.

The original is immutable. Before any production, make a design brief from observed, inferred, and undecided facts. Use GPT-6 Astra at high reasoning for planning and image/design review on an explicit host when available, then use GPT-6 Astra at low reasoning for production on an explicit host with no fork, only after the complete design revision is approved. Never claim this skill changed the model. If a manual model switch is needed, confirm the configured model/host first. No Plan mode is required.

**Human approval is mandatory:** present the complete image design (identity locks, proportions, parts, joins, materials, expressions, and inferred areas) and obtain actual approval of a revision before production. After approval, produce coarse geometry and representative materials, then obtain a second human approval before finishing. An already authorized external provider may create the coarse candidate after design approval. Approval does not authorize a new external service, cost, public upload, or rights decision.

## Astra production loop

1. Inspect the original at high detail and write the brief. Preserve the original file.
2. Use imagegen, when available and permitted, to remove the background while retaining the original as the source; inspect the result's alpha mode before calling it transparent. If the result is RGB with a white background, treat it as a clean modeling reference and disclose that no alpha was recovered. Reject checkerboard or other composited backgrounds as a failed extraction and keep the original. Generate a consistent front, back, side, and oblique set. Add top/bottom views only when geometry or joins require them. Generate detail references for materials (roughness/gloss/color/bump) and close-ups for identity-critical parts. Never treat generated unseen views as observed truth.
3. Inspect observed versus inferred identity, joins, and symmetry. Use Astra high to assemble the complete design revision and images for review. Obtain actual human approval of that revision before production. Keep requested expressions neutral plus the requested expression(s); choose continuous topology (shape keys) or discrete face swaps only after checking vertex correspondence and export needs.
4. After approval, Astra high writes the durable production plan, then hands it to Astra low with `fork_turns="none"` for execution: dimensions and axes, named parts, join strategy, direct/base-mesh/generated/hybrid route, material method, implementation order, acceptance criteria, fixed scope, permitted repairs, and handoff boundaries. Default the exchange output to GLB unless the user's approved plan requires another format. Read the relevant references and templates before executing that mode.
5. Build blockout geometry first. Keep semantic objects/collections and rerunnable state. Keep head, hair, body, clothing, and important accessories independently editable where that improves repair or inspection. Diagnose camera, geometry, materials, and shading separately.
6. Add representative materials and show coarse geometry plus representative materials for a second human approval gate. Continue only after that approval. Then refine face/hair/silhouette, clothing and accessories, UV/topology, materials, expressions, and rig in that order as applicable.
7. Inspect with changed views at low resolution and compact JSON scene reports. Use high detail only for final identity/material evidence.
8. Save semantic state and checkpoints idempotently. An unknown provider job is not an unsent job: query by provider/task id before retrying, and never duplicate a possibly accepted request. Keep tokens out of state and do not upload third-party or private images without explicit approval.
9. Finish with editable `.blend`, requested exchange format, source/assumption record, and renders. Re-import the export and render again. Report only checks actually performed, plus source limits and known defects.

## Durable contracts

Use `templates/brief.md` for design approval; initialize resumable state with `scripts/runtime.py` (`templates/state.json` illustrates its shape). Use `templates/plan.md` for the Astra handoff, `templates/quality.md` for review, `templates/external-job.json` for provider jobs, and `templates/image-prompts.md` for reusable reference prompts. Load `references/technique-recipes.md` only for the chosen modeling or material technique. `references/workflow.md` covers route selection, references, joins, and implementation order; `references/diagnostics-and-style.md` covers anime identity, camera/geometry/material diagnostics, topology, expressions, and materials; `references/qa-and-export.md` covers review, delivery, and limits; `references/provider-contract.md` covers API/provider state and privacy boundaries; `references/runtime-interface.md` covers the bundled approval/state and Blender entry interfaces.

## Completion gates

- Static: source-match, face close-up, oblique, side/back (and top/bottom if needed), editable named parts, representative materials, saved `.blend`, export re-import, and final renders.
- Motion: static gates plus tested poses, weights, hair/clothing intersections, expressions, and target-app re-import.
- 3D print: static gates plus closed volume, joins, wall thickness, scale, and printer/material-specific checks.

Never call an image, mock, successful API response, accepted job, or pretty render a finished model. A successful job is only a candidate until imported and inspected. Do not claim measured cost, quality, or token savings without measurement.
