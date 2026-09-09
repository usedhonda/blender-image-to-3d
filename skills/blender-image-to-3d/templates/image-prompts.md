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

## Material detail

```text
Create a material reference for [part] while preserving its approved color and shape. Show separate swatches or close-ups for base color, roughness/gloss character, and fine bump or relief. Keep lighting neutral and disclose whether a mark is painted color, a geometry relief, or a light/shadow effect. Do not bake cast shadows into the base color.
```

## Expression reference

```text
Create the approved neutral expression and [requested expression] for the same head. Keep head size, landmarks, ears, neck, hairline, camera, and materials fixed. Change only the expression. If continuous topology cannot be inferred, provide a separate aligned expression reference and do not claim it is shape-key compatible.
```
