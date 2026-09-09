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

The original is immutable. Before any production, make a design brief from observed, inferred, and undecided facts. Use GPT-6 Astra at high reasoning for planning and image/design review on an explicit host when available, then use GPT-6 Astra at low reasoning for production on an explicit host with no fork, only after the complete design revision is approved. Never claim this skill changed the model. If a manual model switch is needed, confirm the configured model/host first. No Plan mode is required. High design followed by Low production is the chosen workflow, not a measured token-saving claim.

**Human approval is mandatory:** present the complete image design (identity locks, proportions, parts, joins, materials, expressions, and inferred areas) and obtain actual approval of a revision before production. After approval, produce coarse geometry and representative materials, then obtain a second human approval before finishing. An already authorized external provider may create the coarse candidate after design approval. Approval does not authorize a new external service, cost, public upload, or rights decision.

## Astra production loop

1. Inspect the original at high detail and write the brief. Preserve the original file. Verify the bundled entry once in real Blender using `--python-exit-code 1`; reuse that evidence until relevant code or environment changes. On failures, load only the matching entry in `references/troubleshooting.md`.
2. Use imagegen, when available and permitted, to remove the background while retaining the original as the source; inspect the result's alpha mode before calling it transparent. If the result is RGB with a white background, treat it as a clean modeling reference and disclose that no alpha was recovered. Reject checkerboard or other composited backgrounds as a failed extraction and keep the original. Inventory existing references first; generate missing front/back/side/oblique views only when needed to resolve the approved shape. Keep the adopted set consistent. Add top/bottom views only when geometry or joins require them. Generate detail references for materials (roughness/gloss/color/bump) and close-ups for identity-critical parts. Never treat generated unseen views as observed truth.
3. Inspect observed versus inferred identity, joins, and symmetry. Use Astra high to assemble the complete design revision and images for review. Obtain actual human approval of that revision before production. Keep requested expressions neutral plus the requested expression(s); choose continuous topology (shape keys) or discrete face swaps only after checking vertex correspondence and export needs.
4. After approval, Astra high writes the durable production plan, then hands it to Astra low with `fork_turns="none"` for execution: dimensions and axes, named parts, join strategy, direct/base-mesh/generated/hybrid route, material method, implementation order, acceptance criteria, fixed scope, permitted repairs, and handoff boundaries. Default the exchange output to GLB unless the user's approved plan requires another format. Pass the approved image revision, required references, plan, current artifact/checkpoint, and exact next action instead of the full design conversation. Read only references needed for the chosen route; do not repeat resolved design research.
5. Select the route using the input/environment criteria in `references/workflow.md`; do not mandate custom geometry or a new external tool. Build blockout geometry first. Batch related construction, placement, materials, save, and diagnostic operations in a rerunnable script through either CLI or MCP. Keep one writer per scene, semantic objects/collections, and rerunnable state. Keep head, hair, body, clothing, and important accessories independently editable where that improves repair or inspection. Diagnose camera, geometry, materials, and shading separately.
6. Add representative materials and show coarse geometry plus representative materials for a second human approval gate. Continue only after that approval. Then refine face/hair/silhouette, clothing and accessories, UV/topology, materials, expressions, and rig in that order as applicable.
7. Inspect only views and checks affected by the changed properties, initially at low resolution; increase detail when the decision requires it. Return compact JSON with changed parts, saved artifacts, validation failures, and required renders rather than full scene dumps. For each repair specify the target, discrepancy, fixed properties, and diagnostic view. Reuse passing evidence only while its scene revision and relevant conditions remain valid; retain final identity/material evidence.
8. Save semantic state and checkpoints idempotently. An unknown provider job is not an unsent job: query by provider/task id before retrying, and never duplicate a possibly accepted request. Keep credentials and authentication tokens out of state and do not upload third-party or private images without explicit approval.
9. Resume from validated state, existing scripts, artifacts, and the exact next action; do not rebuild completed work. While a render or delegated job runs, prefer host-side waiting or completion events within host responsiveness limits. Avoid repeated empty model wakeups; a timeout alone does not justify restarting a job.
10. Keep human preference approval separate from technical acceptance; approval does not waive a failed technical check. Finish with editable `.blend`, requested exchange format, source/assumption record, and renders. Re-import the export and render again. Report only checks actually performed, plus source limits and known defects. Maintain a chronological production README from the single starting image using `templates/production-story.md`, recording each supplemental reference and repair when introduced.

Record available usage across design, handoff, production, repair, and verification, including every participating agent. Distinguish API tokens/cost from Codex quota; unknown values stay unknown. Do not add paid runs solely to populate the record.

## Durable contracts

Use `templates/brief.md` for design approval; initialize resumable state with `scripts/runtime.py` (`templates/state.json` illustrates its shape). Use `templates/plan.md` for the Astra handoff, `templates/quality.md` for review, `templates/external-job.json` for provider jobs, and `templates/image-prompts.md` for reusable reference prompts. Load `references/technique-recipes.md` only for the chosen modeling or material technique. `references/workflow.md` covers route selection, references, joins, and implementation order; `references/diagnostics-and-style.md` covers anime identity, camera/geometry/material diagnostics, topology, expressions, and materials; `references/qa-and-export.md` covers review, delivery, and limits; `references/provider-contract.md` covers API/provider state and privacy boundaries; `references/runtime-interface.md` covers the bundled approval/state and Blender entry interfaces.

Load `references/token-efficiency.md` only when diagnosing consumption or comparing workflows. Use the usage section of `templates/quality.md`; the research report is not a runtime dependency.

Load `references/practitioner-lessons.md` only when choosing an unfamiliar route or improving reusable construction/quality rules; it records firsthand examples and their limits.

## Completion gates

- Static: source-match, face close-up, oblique, side/back (and top/bottom if needed), editable named parts, representative materials, saved `.blend`, export re-import, and final renders.
- Motion: static gates plus tested poses, weights, hair/clothing intersections, expressions, and target-app re-import.
- 3D print: static gates plus closed volume, joins, wall thickness, scale, and printer/material-specific checks.

Never call an image, mock, successful API response, accepted job, or pretty render a finished model. A successful job is only a candidate until imported and inspected. Do not claim measured cost, quality, or token savings without measurement.
