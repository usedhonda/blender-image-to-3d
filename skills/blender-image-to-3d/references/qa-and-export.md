# Review and delivery

Keep one comparison camera per stage. Select views that prove the stage acceptance criteria: source-match, identity close-up, oblique, side/back, and top/bottom when joins require them. During repairs rerender only views affected by the changed properties; a full turntable is not a default per-repair check. Use low-resolution changed views during iteration and high-resolution final evidence. Review image and scene data together: identity locks, ratios, intersections, dimensions, object names, materials, UVs, bones, and shape keys.

Classify each issue as camera, geometry, join, material/texture, normals/shading, or motion. Prioritize defects that block acceptance; specify the affected part, discrepancy, fixed properties, and diagnostic view before each repair. Rerender under the same comparison conditions. If the same failure persists without new evidence, revisit the diagnosis instead of repeating the same edit. Keep passing evidence tied to its scene revision and relevant camera/material/environment conditions; invalidate only evidence affected by a change. Scores organize work; they do not override a missing face, broken join, failed save, or failed target-format import.

Before delivery, save the editable `.blend` with relative or packed dependencies, export the requested format, import it into a clean scene, and render again. Include review images, a README or handoff record, source versus inferred design, provider/model/settings identifiers, known limits, and required add-ons. Separate the editable source from optimized delivery output.

For motion, test shoulder/arm, knee, neck/hair, eyes/mouth, accessories, and export/re-import. For print, verify closed volume, joins, scale, wall thickness, and printer/material constraints; do not hard-code a universal thickness.

## Independent acceptance and learned checks

Keep connection success, geometry creation, visual acceptance, and target-format validation as separate evidence. Human approval covers preference and design adoption; it does not override missing parts, unintended intersections, failed saves, or unusable exports. Explain source differences, remaining defects, and scoped repair options with comparison images.

Record render engine, lighting, camera, sampling/denoising, and display mode when diagnosing shading. Establish whether a symptom comes from presentation or geometry before editing the mesh. A noisy preview alone is not a geometry failure.

When a real defect recurs or exposes an uncovered reusable contract, preserve the failing example and add the smallest relevant check to the reusable builder or quality guide after the repair stabilizes. Suitable checks include unintended duplicate/degenerate faces and required part/material references; do not apply print/manifold or motion rules to every static mesh. Keep aesthetic judgments as matched-view examples and reasons rather than inventing a universal score. No test per cosmetic adjustment or repeated unchanged passing check.

For the chronological delivery record, use `templates/production-story.md`. Production screenshots, reconstruction illustrations, and post-completion showcase renders must be labeled separately.
