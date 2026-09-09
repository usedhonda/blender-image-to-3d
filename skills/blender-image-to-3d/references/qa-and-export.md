# Review and delivery

Keep one comparison camera per stage. Review source-match, face close-up, oblique, side, back, and 45-degree/8-way views; add top/bottom when joins require them. Use low-resolution changed views during iteration and high-resolution final evidence. Review image and scene data together: identity locks, ratios, intersections, dimensions, object names, materials, UVs, bones, and shape keys.

Classify each issue as camera, geometry, join, material/texture, normals/shading, or motion. Fix the largest three, rerender under the same conditions, and stop repeating a stage that does not improve. Scores organize work; they do not override a missing face, broken join, failed save, or failed target-format import.

Before delivery, save the editable `.blend` with relative or packed dependencies, export the requested format, import it into a clean scene, and render again. Include review images, a README or handoff record, source versus inferred design, provider/model/settings identifiers, known limits, and required add-ons. Separate the editable source from optimized delivery output.

For motion, test shoulder/arm, knee, neck/hair, eyes/mouth, accessories, and export/re-import. For print, verify closed volume, joins, scale, wall thickness, and printer/material constraints; do not hard-code a universal thickness.
