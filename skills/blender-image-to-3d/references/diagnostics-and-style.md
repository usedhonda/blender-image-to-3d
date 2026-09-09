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

## Topology, UV, and materials

Decimate reduces density; voxel remesh joins or regularizes volume; quad remesh helps rebuild flow; none supplies character-specific facial or joint topology. Copy before any operation that may affect UVs, attributes, shape keys, or rigs. Use controlled retopology or fit a good base where deformation matters. Check texture projection for leaks, seams, and front details appearing on the back.

Start with simple toon bands/masks. Use custom normals only when a controlled shadow is needed; flat normals are not a universal anime rule. Keep Blender-only shading separate from exchange-format capabilities (for example, Shader to RGB is EEVEE-specific). Match materials to the target format and re-import it.
