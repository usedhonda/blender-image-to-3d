# Reference image prompts

Attach the immutable original to every edit. Replace bracketed fields with the approved brief. These prompts produce design references, not proof of hidden geometry.

## Background cleanup

```text
Preserve the attached character exactly: face, hair silhouette, colors, asymmetry, proportions, and visible accessories. Remove only the background and replace it with a uniform white background. Do not add a checkerboard, grid, shadow plate, text, or new object. Keep the full subject inside the frame. If transparency is unavailable, return a clean white RGB reference and do not simulate alpha.
```

## Consistent views

```text
Using the immutable original and approved design brief, draw the same character from [front/back/side/oblique]. Preserve [identity locks], [head/body anchors], [palette], [asymmetry], and [part count]. Use the same scale, margins, neutral pose, and front direction as the approved reference. Invent only the listed inferred areas: [inferred areas]. No text, labels, frames, or extra props.
```

## Identity-locked edit

```text
Use the attached original as the sole identity authority. Preserve the approved pose, camera angle, head and body proportions, feature ratios and spacing, asymmetry, hair silhouette, palette, and every original delicate mark. Preserve the subject's source-specific contour, lineweight/contrast, and shading character; do not make the face prettier, sharper, or more detailed as a substitute for fidelity. Change only [explicit change]. Infer only these occluded areas: [enumerated areas]. Do not infer visible features, ancestry, or details from any rejected candidate. Return one candidate with the full subject visible and no collage, labels, or comparison panel.
```

For review, compare the original, previous candidate (with its accepted/rejected status), and current candidate as separate images at the same angle and comparable face scale. Keep the full originals; label any crop or zoom. The prompt increases constraints but does not prove preservation, and an accepted candidate remains a scoped reference rather than canonical promotion or 3D-quality approval.

Do not call a candidate unchanged because extraction succeeded. If a visible lock drifts, restart from the original and isolate that correction; never chain from a failed candidate. If source evidence is insufficient, mark the area unknown instead of inventing it.

## Material detail

```text
Create a material reference for [part] while preserving its approved color and shape. Show separate swatches or close-ups for base color, roughness/gloss character, and fine bump or relief. Keep lighting neutral and disclose whether a mark is painted color, a geometry relief, or a light/shadow effect. Do not bake cast shadows into the base color.
```

## Expression reference

```text
Create the approved neutral expression and [requested expression] for the same head. Keep head size, landmarks, ears, neck, hairline, camera, and materials fixed. Change only the expression. If continuous topology cannot be inferred, provide a separate aligned expression reference and do not claim it is shape-key compatible.
```
