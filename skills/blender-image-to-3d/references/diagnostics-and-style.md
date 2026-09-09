# Identity, style, and diagnostics

## Anime identity

Face recognition is dominated by silhouette, head proportions, eye shape/spacing, bangs, jaw/cheek width, and distinctive accessories. Check the face in front and oblique views; a flat face can match front art while failing in 3D. Build hair as head cover, bangs, side/back masses, and signature tufts before individual strands.

Use neutral plus requested expressions. Continuous expressions require stable topology and vertex correspondence; discrete swaps require aligned scale, position, materials, and visibility. Do not turn independently generated faces into shape keys without checking correspondence. A hidden inactive face can still affect shadows, outlines, export, or VRM.

## Diagnose before editing

Use fixed comparison cameras. Compare:

1. single-color, weak light: silhouette, depth, normals, camera, and geometry;
2. flat/low-shadow color: palette, UV, textures, and material assignment;
3. final toon view: light direction, shader, custom normals, masks, and outlines.

If the face fails only in final light, inspect normals/materials/lighting before reshaping it. If it fails only from an angle, inspect camera and depth. Do not use a camera change to hide geometry drift.

## Reference drift pitfalls

Background extraction is a new image operation, not evidence that the face stayed unchanged. Preserve original provenance and the scope of each adopted reference; candidates never silently replace the original or inherit from a rejected candidate. Once a candidate is adopted as the production target, it must appear in production comparisons. Source provenance and the current modeling target are different roles.

Do not equate prettier with faithful or a more detailed prompt with verified preservation. When a soft face hardens, decompose “softness” into:

- contour: chin, jaw, cheek width, and nose projection;
- lineweight/contrast: feature strokes, edge strength, and spacing;
- shading: bridge, lip, cheek, and cast-shadow emphasis.

Restore only the dimensions the source supports. “Soft” is source-specific; do not impose it on every anime reference.

If review finds a narrower chin, a stronger nose bridge, or newly emphasized lip detail or shadows, map each change to contour, lineweight/contrast, or shading before editing. For reference generation, correct the failed dimension from the designated identity source. For modeling, correct against the adopted production target. Keep a repair provisional until the relevant comparison passes.

Compare the original, previous candidate (with its accepted/rejected status), and current candidate as actual images at comparable face scale and the same angle. Preserve full originals and disclose any crop or zoom. Do not use a generative comparison collage as evidence.

Record the accepted scope and latest version in the context record. Once that evidence is sufficient, stop regenerating. Acceptance records reference scope; it does not promote a candidate to canonical source or approve 3D quality. Clarify only when the referent is genuinely ambiguous.
This identity comparison cannot establish hidden geometry or topology.

## Topology, UV, and materials

Decimate reduces density; voxel remesh joins or regularizes volume; quad remesh helps rebuild flow; none supplies character-specific facial or joint topology. Copy before any operation that may affect UVs, attributes, shape keys, or rigs. Use controlled retopology or fit a good base where deformation matters. Check texture projection for leaks, seams, and front details appearing on the back.

Start with simple toon bands/masks. Use custom normals only when a controlled shadow is needed; flat normals are not a universal anime rule. Keep Blender-only shading separate from exchange-format capabilities (for example, Shader to RGB is EEVEE-specific). Match materials to the target format and re-import it.

## Failed construction and unsupported continuation

- Procedural rings, curves and facial patches are tools, not a likeness method. Arbitrary numerical seeds do not become reference-driven modeling because the image hash was checked or an agent viewed it. Establish how the adopted contour, landmarks and feature shapes constrain editable geometry; use a suitable base or reference-guided modeling when the procedural representation cannot express them.
- Simplification must retain identity-bearing shape. A different jaw, expression or fringe structure is not an acceptable blockout merely because topology and save/reopen pass. Do not assume later textures or lighting will repair geometry without diagnostic evidence.
- Evaluate distance to the adopted target. Fixing a slit eye or a tubular hair lock is insufficient if the resulting face still misses that target; improvement over a failed predecessor is not stage acceptance.
- On a recognized failure, decide between a supported local repair and a method reassessment. Record cause, intervention and observable expected improvement before another execution. Persistently missing those improvements is evidence against the approach, not a reason for another agent handoff or cosmetic retry.
- Do not impose a fixed retry quota. Repeated reference-image generation is appropriate when each attempt addresses an identified mismatch with a credible correction; change the prompt or method when the same failure persists. Neither a round count nor sunk cost justifies adoption.
- Do not blame missing views or a lower-effort model for failing features already visible in the adopted view without evidence. Multiple views resolve additional design ambiguity; they do not repair a method that fails to reproduce the available reference.
