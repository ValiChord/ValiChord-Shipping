# Phase 0 — is a maritime event timeable precisely enough?

Findings: [`../../docs/10-phase0-findings.md`](../../docs/10-phase0-findings.md).
Plan and kill criteria: [`../../docs/09-demo-plan.md`](../../docs/09-demo-plan.md).

```bash
bash fetch.sh          # ~1.3 GB, a few minutes, no credentials needed
python aggregate.py    # test 1 -- timing resolution
python divergence.py   # test 2 -- claim vs telemetry divergence
```

| File | Does |
|---|---|
| `fetch.sh` | Downloads four 2023 dates from NOAA/MarineCadastre, extracts two port bounding boxes, deletes the archives |
| `extract_box.py` | Streams a daily AIS zip and keeps only rows inside the LA/Long Beach and Houston boxes |
| `aggregate.py` | Timing resolution: how tightly can a geofence crossing or a stop be bounded |
| `divergence.py` | Claim vs telemetry: crew-set navigational status against GPS speed |

Pure standard library — no pandas, no pyarrow. The filtered CSVs are not committed;
`fetch.sh` regenerates them.

**Two things to preserve if this is edited.** Events are derived from kinematics, never
from navigational status — that field is a claim, and conflating the two would destroy
test 2. And `divergence.py` counts only hard contradictions (claiming stationary while
making way); it measures staleness as much as dishonesty and its output must never be
described as evidence of fraud.
