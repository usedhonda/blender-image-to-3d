# Quality record

- Scene/artifact revision and relevant camera/material/environment conditions: `...`
- Changed parts/properties and invalidated evidence: `...`
- Reused passing evidence and why it remains valid: `...`

## Evidence
- Source-match: `...`
- Face close-up: `...`
- Oblique/side/back: `...`
- Top/bottom if required: `...`
- Coarse geometry/material approval: `...`
- Export re-import/render: `...`

## Findings
| Issue/target and discrepancy | Class | Evidence/view | Decision and fixed properties |
|---|---|---|---|
|  | camera / geometry / join / material / shading / motion |  |  |

## Limits
- Observed vs inferred: `...`
- Unverified: `...`
- Provider/model/version/usage: `...`
- Known defects and next repair: `...`

## Available usage

Record observed values only; use `unknown` for unavailable fields, never zero.

| Stage/agent | Model/effort and host/version | Input | Cached read | Cache write | Output total | Reasoning subset | Calls/empty waits |
|---|---|---|---|---|---|---|---|
| design / handoff / production / repair / verification | | | | | | | |

- Measurement source, start/end boundaries, per-call or cumulative: `...`
- Aggregate all stages and agents once. Difference cumulative counters; never sum their snapshots. Reasoning is a subset of total output: do not add it again.
- API cost, currency, pricing source/date and additional tool charges, if available: `...`
- Codex quota window, start/end readings, used/remaining convention and concurrent activity: `...` (separate from tokens and API cost)
- Elapsed execution/render time and human approval waiting time separately: `...`
- Final acceptance and failed/unfinished work: `...`
- Missing measurements and limits on comparison: `...`

Usage counts are not authentication tokens. Never record credentials or private request contents. Consult `references/token-efficiency.md` only for consumption diagnosis or comparison.
