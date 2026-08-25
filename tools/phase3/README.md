# Phase 3 — the external witness

Findings: [`../../docs/13-phase3-findings.md`](../../docs/13-phase3-findings.md).
Plan: [`../../docs/09-demo-plan.md`](../../docs/09-demo-plan.md).

```bash
bash ../phase1/run.sh   # once -- produces case.json
bash run.sh             # needs network: contacts drand and OpenTimestamps
```

## A witness is not a validator

This is the distinction the phase turns on.

**Validator** — forms a *judgement* about evidence. Human or AI. Expensive to recruit,
expensive to trust.

**Witness** — attests that data *existed at a time*. Not a judgement at all. Free,
public, machine-only, available right now.

You cannot solve witnessing with validators of any kind, because witnessing is not a
judgement task. And an AI validator you run yourself has no reputation at stake — so what
makes its finding credible to a hostile counterparty is that the inputs were provably
pinned *before anyone knew the answer*. **AI validators make the witness more important,
not less.**

## The mechanism

| | | |
|---|---|---|
| **Floor** | [drand](https://drand.love/) / League of Entropy | Unpredictable value every 30 s, threshold-signed by independent organisations. Embedded in the payload before hashing, so a commitment containing round N was necessarily made after round N existed |
| **Ceiling** | [OpenTimestamps](https://opentimestamps.org/) | Digest aggregated into Bitcoin via three independent calendar operators — OpenTimestamps pool, Eternity Wall, Catallaxy |

Neither is operated by this project. Neither requires a counterparty, an introduction, or
proximity to a port.

## What it proves, and what it does not

**An interval, not an instant.** The negative control runs four attacks:

| Attack | Outcome |
|---|---|
| Fabricate the beacon value | refused — re-fetch from the public API disagrees |
| Omit the beacon | refused — no floor, flagged unwitnessed |
| Alter the payload after committing | refused — hash mismatch |
| **Embed a genuine but stale round** | **not refused** |

The fourth is real and named. A floor proves *not before*; it does not prove *was then*.
What exposes a stale round is the **width** of the floor-to-ceiling interval — seconds
for an honest run, hours for a backdating attempt. Every party record therefore carries
`timeInterval.seconds`, and any output reporting `witnessed: true` without the width
would be misleading.

## Do not

Report a boolean where the width belongs. Drop the disclosure block. Let the run continue
silently when drand is unreachable — an unwitnessed record produced by a witnessed
protocol is worse than a failure.
