# Astra token-efficiency reference

Load this file only for diagnosing token, quota, or round-trip efficiency. It does not change the approval gates, model/host selection, runtime contracts, or deliverables in `SKILL.md`. Guidance and sources were checked 2026-09-09.

## Evidence and scope

- **Official** means OpenAI API documentation; it does not prove Codex desktop behavior.
- **Observed** means a community report or measurement with its own limits.
- **Hypothesis** means an operational idea to measure on the actual host, never a saving guarantee. Do not add fixed prices or claimed savings.

## Measure the accepted result

Use one ledger for design, handoff, production, repairs, verification, parent and child agents, and new-context startup. Compare only equal approved references, Blender environment, acceptance criteria, save/reload checks, and output format. Record model/tool calls, images, retries, empty waits, processing time, human approval wait, and render time separately.

For cumulative usage, subtract start from end; never add cumulative event totals. Keep input, cached-read, cache-write, output, and reasoning fields separate. Missing data is `null`, never `0`. Do not add reasoning to output when the provider already includes it in an aggregate. Usage/quota telemetry is distinct from API billing and secrets; record non-sensitive metadata only and never persist keys or authentication tokens.

## Official API boundaries

Prompt caching reuses a stable prefix; cache reads and writes are still usage. Keep a stable production contract (axes, dimensions, named parts, fixed properties, acceptance criteria) ahead of changing results, but do not pad prompts merely to create a cache. History rewrites and compaction can reduce reuse; inspect `cached_tokens` and `cache_write_tokens` when available.

The Responses API documents `configuration_update` with a stable request-level effort in Astra standard, single-agent mode. It is incompatible with automatic compaction/truncation and standalone `/responses/compact`; explicit compaction requires a fresh update. Read the linked official compatibility section before implementing it. Do not assume this is the same as changing a Codex setting: API and Codex are different surfaces and accounting systems. A Codex issue about effort changes and cache preservation is an implementation observation, not an API contract.

Images and vision documentation does not establish an Astra-specific image-token conversion factor. Do not import another model's formula or assume fewer images cost less. Use targeted views that answer the current question: silhouette, matched-angle identity close-up, or consistent-lighting material diagnosis. Contact sheets and small previews are useful only when readable.

## Blender hypotheses to measure

1. Batch meaningful scene operations in a rerunnable `bpy` script; return only changed parts, save path, counts/dimensions, checks, and image paths. Fetch verbose geometry or node data only for a failing diagnosis.
2. Diagnose camera, geometry, materials, and shading separately. A targeted image plus precise difference, fixed properties, required view, and repair boundary may reduce rework; measure image cost and repair cost together.
3. Prefer event-driven completion signals or host-side waiting for render/provider jobs. Do not repeatedly call Astra with unchanged long history to ask whether a job is done. Respect host response, timeout, and polling limits; a community wait report is not host policy.
4. Keep scripts, design revision, approved images, `.blend`, checkpoints, and quality results on disk. Resume from state instead of reconstructing the conversation. Required approval, save, reload, and export checks remain mandatory.

The saving from High-for-design and Low-for-production is an **unverified hypothesis**. For this chosen workflow, count High planning, Low execution, repairs, verification, context startup, and parent coordination together. Do not count reasoning twice or call Low cheaper because one short script was generated.

## Minimal diagnostic record

Record date, model/effort, client and Blender versions, API vs Codex surface, reference/design hashes, stage and agent, calls/waits/images, input/cache/output usage, elapsed times, and acceptance result. Compare one change at a time after a baseline; stop when the decision is answered. Do not run paid experiments solely to populate this file.

## Sources (all accessed 2026-09-09)

- [GPT-6 Astra model](https://developers.openai.com/api/docs/models/gpt-6-astra) — Official model/API facts.
- [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) — Official cache behavior and fields.
- [Reasoning updates](https://developers.openai.com/api/docs/guides/reasoning#change-reasoning-mid-conversation) — Official `configuration_update` boundary.
- [Using GPT-6 Astra](https://developers.openai.com/api/docs/guides/latest-model) — Official instruction guidance.
- [Images and vision](https://developers.openai.com/api/docs/guides/images-vision) — Official image limits; no Astra conversion assumption.
- [Architectural visualization with Astra](https://developers.openai.com/blog/architectural-visualization-with-astra) — Official Blender/Python example, not savings evidence.
- [Astra quota investigation](https://www.reddit.com/r/codex/comments/1wa9c9d/i_investigated_why_gpt6_astra_burns_quota_so_fast/) — Observed wait-loop report.
- [Codex issue #42996](https://github.com/openai/codex/issues/42996) — Observed implementation report, not API proof.
- [Astra Blender experiment](https://note.com/glad_frog1869/n/ncf626de0c303) — Observed quota display, not token accounting.
- [Hobby Blender benchmark](https://www.reddit.com/r/OpenAI/comments/1wa5akw/astra_results_on_my_hobby_blender_benchmark/) — Observed batching report.
