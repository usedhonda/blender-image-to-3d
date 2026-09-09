# Lessons from running this workflow

Load the relevant entry when its observed failure appears. Preserve the failing command/result locally, apply the smallest correction, and rerun only the check that failed. These entries describe reproduced failures, not assumptions about every Blender installation.

## Blender cannot import a sibling Python module

**Observed:** `blender --background --python scripts/blender_entry.py` raised `ModuleNotFoundError: No module named 'runtime'` although both files were in the same directory. Blender's script execution did not add that directory to Python's module search path.

**Fix:** the bundled entry script resolves its own directory from `__file__` and adds it to `sys.path` before importing the bundled runtime. Task-specific scripts that import a sibling helper must do the same, or explicitly load that helper from its file. Never rely on the shell's current directory or install an unrelated package named `runtime` to fix this failure.

**Proof:** rerunning the corrected entry in Blender 5.2.1 returned scene JSON with three default objects, one mesh, eight vertices, and six polygons. This proves the entry/import path; it does not prove character geometry or rendering quality. Plain-Python mocks did not expose this Blender-specific failure, so one real Blender entry call is part of initial capability verification.

## A Python traceback can accompany Blender exit status zero

**Observed:** the same failed import printed a traceback while the Blender process returned zero.

**Fix:** direct batch commands must include `--python-exit-code 1` before `--python`, and callers must also inspect the expected JSON result/artifact. Use this form:

```bash
blender --background --python-exit-code 1 --python /absolute/skill/scripts/blender_entry.py -- \
  --operation inspect --state /absolute/job/state.json
```

A zero process status alone is insufficient. A saved file or render must exist and satisfy the operation's acceptance check. Do not repeat an unchanged successful baseline unless the version, code, or relevant environment changes.

## Blender arguments reach the script parser

Blender passes its own command-line arguments in `sys.argv`. Parse only the arguments following `--`. The bundled entry supports that boundary and also accepts an explicit argument list for MCP callers. Do not maintain separate direct/MCP copies of the geometry program. The argv boundary is covered by a synthetic test; distinguish that from a real Blender invocation.

## MCP transport success contains an operation error

The official MCP path can return `isError: false` while `structuredContent.status` is `error`. Check both the outer tool envelope and the operation payload, including embedded JSON text. Use `mcp_status_error` for the supported response shapes. Investigate the returned operation error before retrying; do not convert transport acceptance into scene success.

## Background extraction draws a checkerboard into RGB pixels

**Observed:** a requested transparent cutout was an RGB image with a painted checkerboard. It also changed the source's color intensity.

**Fix:** inspect the image mode and alpha values before calling it transparent, then visually compare silhouette, proportions, and color with the immutable original. Reject a painted checkerboard. In the trial, a targeted image edit produced a clean white-background reference; this was disclosed as RGB, not alpha. White is adequate for a modeling reference when no transparency-dependent downstream process is required. If real alpha is required, continue with an authorized image-editing route that actually supplies it; do not relabel the RGB output.

## A material design sheet exaggerates surface texture

**Observed:** the initial robot material closeups introduced swirling, embossed grain much stronger than the intended subtle vinyl finish.

**Fix:** keep the geometry, palette, views, and expressions fixed and request a material-only image revision. Inspect the corrected swatches and whole-object views together. Register the corrected board as a new candidate and ask the human to approve that exact candidate. Do not blindly translate generated texture artifacts into Blender bump/displacement.

## State summaries confuse approval with file validity

An unapproved source can still be intact. Report input validity, design approval, coarse approval, and checked production plan independently. The trial caught a resume summary that incorrectly reported `input_valid: false` solely because design approval was pending; the runtime now checks these separately. Byte changes to the original or approved assets must invalidate the relevant gate even when the filename stays the same. Generate state using `init`; a documentation template is not a replacement for live state.

## Evidence boundaries from the trial

The trial established image-reference iteration, explicit pending approval, state contracts, local skill discovery, and a live Blender read-only entry. Earlier cube save/render/reopen parity established the direct and official-MCP transport baseline. None of those proves an Astra Low character handoff, finished character fidelity, a rig, or a token saving. Record each only after that step actually runs.
