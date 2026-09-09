# Blender Image to 3D

`blender-image-to-3d` turns an approved reference image into an editable Blender scene. Invoke it with:

```text
$blender-image-to-3d /path/to/image
```

The default result is a static, editable `.blend` that preserves the source style, proportions, visible asymmetry, and identity-critical features. The skill records what is observed, what is inferred, and what remains undecided. It can choose direct Blender construction, a suitable base mesh, image-to-3D, or a hybrid route.

## Approval model

Production starts only after a human approves a complete design revision: scope, identity locks, proportions, parts, joins, materials, expressions, and inferred areas. After blockout, representative materials, and coarse geometry are shown, a second human gate is required before finish work. An already authorized external provider may create the coarse candidate after design approval; any new service, data transfer, or cost requires specific approval.

The skill prefers GPT-6 Astra at high reasoning for design and review when an explicit host configuration provides it, then delegates production to GPT-6 Astra at low reasoning with no fork when that host is available. This is a host-side choice; the skill never changes the active model by itself. If a manual switch is needed, confirm the configured model and host first. MCP is optional. The official Blender MCP reference is <https://projects.blender.org/lab/blender_mcp>.

## What it delivers

- editable `.blend` with semantic objects and checkpoints;
- GLB exchange file by default, with import and re-render verification;
- source-match, face close-up, oblique, side/back, and conditional top/bottom review renders;
- a record of assumptions, provider jobs, material decisions, known limits, and unverified claims.

Expressions, animation, VRM/game delivery, and 3D printing add their own acceptance checks. A generated image, accepted provider job, or attractive render is not treated as a finished model until the mesh is imported, inspected, saved, and rendered.

## Installation

For a normal local skill installation from a checkout, install only the nested skill directory. Inspect the destination first and do not overwrite an existing skill:

```bash
git clone https://github.com/usedhonda/blender-image-to-3d.git
mkdir -p ~/.codex/skills
if [ -e ~/.codex/skills/blender-image-to-3d ] || [ -L ~/.codex/skills/blender-image-to-3d ]; then
  echo "Existing installation preserved; inspect before updating."
else
  cp -R ./blender-image-to-3d/skills/blender-image-to-3d ~/.codex/skills/blender-image-to-3d
fi
```

For hosts that use `~/.agents/skills`, repeat the same checked copy with that destination. If a destination exists, inspect it and preserve it; merge only intended files. The bundled `.codex-plugin/plugin.json` is the distribution manifest for the repository root. A configured marketplace or supported GUI import may consume that manifest; this repository does not claim a direct plugin installer command. Blender itself and the optional official MCP server are separate dependencies.

## Runtime files

- `skills/blender-image-to-3d/SKILL.md`: invocation, gates, workflow, and completion criteria.
- `skills/blender-image-to-3d/references/`: route selection, diagnostics, provider state, runtime interface, and export QA.
- `skills/blender-image-to-3d/templates/`: brief, state, Astra plan, handoff, quality record, and external-job record.
- `skills/blender-image-to-3d/scripts/`: approval-gated local state and Blender entry operations, when the runtime is available.

The source manual used to design this skill is research material, not a required user dependency.

## Current verification status

The verified baseline includes a Blender 5.2.1 environment where direct Blender work and the official MCP produced identical cube renders and save/reopen checks. R2 produced front, back, side, oblique, top, and sole views, a neutral/smile pair, and four material references; design approval remains pending. No Astra Low character production run has been completed. See [`docs/verification.md`](docs/verification.md) for the evidence matrix and pending checks.

## License

MIT. See [`LICENSE`](LICENSE).
