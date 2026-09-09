# Practical technique recipes

## Face landmarks and bounded edits

Store normalized landmarks for hairline, brow, eye inner/outer corners, nose, mouth, chin, and jaw width. Keep image-pixel coordinates separate from face-local coordinates. Treat inferred measurements as ranges, not exact truth. Change one bounded parameter at a time (for example, eye spacing or chin length), render the fixed camera, and record the result.

## Hair masses

Build a cap, major bangs, side masses, back mass, and signature tufts before strands. Curves with a controlled bevel or named low-poly masses are easier to edit than individual hair. Check hairline/neck and hair/shoulder joins from oblique and back views. Preserve a semantic object per major mass.

## Material diagnostics

Base color is appearance color; roughness/gloss controls highlight spread; bump changes shading normals without changing silhouette; displacement changes geometry and can break joins. Compare a flat color pass, a roughness/gloss pass, and the final light separately. A dark patch may be painted color, a material response, or a cast shadow; change lighting before reshaping geometry.

## Preserved topology and scene checks

Before retopology, remesh, UV edits, or rigging, checkpoint the source and record mesh counts, object names, materials, UV layers, vertex groups, shape keys, and armatures. After each operation verify that identity-critical objects still exist, expected topology is preserved or intentionally replaced, joins remain separate where required, and the scene reopens. Never use a successful save as proof that topology or deformation survived.
