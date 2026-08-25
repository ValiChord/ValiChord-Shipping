# Phase 1 — commit, reveal, verify

Findings: [`../../docs/11-phase1-findings.md`](../../docs/11-phase1-findings.md).
Plan: [`../../docs/09-demo-plan.md`](../../docs/09-demo-plan.md).

```bash
bash ../phase0/fetch.sh     # once -- pulls the public AIS
bash run.sh
```

| File | Does |
|---|---|
| `build_case.py` | Extracts one real port call (CSL SPIRIT, IMO 9138111, LA/Long Beach, 15 Jan 2023) from the Phase 0 AIS into `case.json`. Everything it writes is real |
| `demo.py` | Four parties commit SHA-256(payload ‖ nonce), sign the commitment with Ed25519, reveal, and are checked against the real track. Emits `discrepancy_record.json` |
| `tamper_test.py` | Negative control. Three substitution attacks, all of which must be refused |
| `example_output/` | A committed sample run, so the output can be read without running anything |

## What is real and what is not

**Real** — the vessel, its 460-fix track, every position, speed, timestamp and
broadcast status. Public NOAA/MarineCadastre AIS, unmodified.

**Synthetic** — the four parties, their keys, and the carrier's claim. No real
organisation supplied operational logs. The discrepancy is deliberately injected.

So this shows the *mechanism* works against real telemetry. It does **not** show that
any real carrier misreported anything, and every output file repeats that. Do not
remove the `_disclosure` block.

## Two rules for anyone editing this

**Report discrepancies, never adjudications.** No monetary figures, no confidence
scores, no charterparty interpretation. Whether a Notice of Readiness was validly
tendered is a contested question of law; this reports where the vessel physically was
and stops. The `notDetermined` list in the output is load-bearing — see
[`../../docs/08-external-evidence-and-the-real-gap.md`](../../docs/08-external-evidence-and-the-real-gap.md).

**Do not add dependencies that are not doing work.** Phase 1 uses `cryptography` for
real Ed25519 and nothing else. Not Unyt, not Nondominium/hREA, not Holochain, not
ValiChord's blind commit-reveal — the reasoning for each exclusion is in
[`../../docs/09-demo-plan.md`](../../docs/09-demo-plan.md).
