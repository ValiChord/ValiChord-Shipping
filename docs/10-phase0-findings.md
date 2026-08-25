# 10 — Phase 0 findings: can a maritime event be timed precisely enough?

**Verdict: PASS, by a wide margin.** The kill criterion in [`09-demo-plan.md`](09-demo-plan.md)
was fifteen minutes. The measured figure is **seventy seconds**.

A second test, which the plan assumed impossible without carrier logs, turned out to be possible
and also came back positive: **self-reported operational status and physical telemetry do come
apart in the wild, at a measurable rate.**

Run 25 August 2026. Code in [`../tools/phase0/`](../tools/phase0/); it regenerates everything
below from public data.

---

## What was done

| | |
|---|---|
| Source | NOAA / MarineCadastre bulk AIS, free, no application |
| Dates | 15 Jan, 16 Apr, 16 Jul, 15 Oct 2023 — spread to catch seasonal variation |
| Ports | **Los Angeles / Long Beach** (open coast, breakwater, large offshore anchorage) and **Houston** (long dredged ship channel into Galveston Bay) — deliberately different geometries |
| Raw volume | ~1.3 GB compressed; ~8.1M AIS fixes per day nationally |
| After filtering | 682 cargo/tanker vessel-days, 290,276 inter-fix intervals |
| Vessel filter | AIS vessel type 70–89 (cargo and tanker) with ≥20 fixes — excludes tugs, fishing, pleasure craft |

**Events are derived from kinematics — position and speed — never from the vessel's
self-reported navigational status.** That field is set by the crew, which makes it a claim rather
than ground truth. Keeping the two apart matters, and it is what made the second test possible.

---

## Test 1 — timing resolution

The question is not "how often does AIS report" but "how tightly can a specific event be bounded."
For any threshold crossing, the answer is the gap between the last fix before and the first fix
after: the vessel crossed somewhere inside that window and nowhere else.

| Event | n | median | p90 | max | ≤5 min | ≤15 min |
|---|---|---|---|---|---|---|
| **GEOFENCE** — crossing a port limit, underway | 244 | **70 s** | 71 s | 2,351 s | 99.2% | 99.6% |
| **STOP** — anchor down / all fast | 267 | **71 s** | 182 s | 899 s | 95.1% | 100% |

Consistent across both ports and all four dates.

**Why the geofence result is the important one.** Notice of Readiness turns on whether the vessel
had arrived — a boundary crossing that happens *while the vessel is underway*, which is exactly
when AIS reports most frequently (roughly every 70 seconds, against 180 seconds when stopped). The
event that matters commercially is the one the data times best. That is a fortunate alignment and
not something that had to be true.

**Coverage:**

| | |
|---|---|
| Median interval between fixes | 180 s |
| Intervals exceeding 15 minutes | 326 of 290,276 — **0.112%** |
| Longest single gap | 22.6 hours |

Gaps exist. They are rare, and terrestrial AIS reception is imperfect at range. Any claim built on
this must state the gap rather than average it away.

---

## Test 2 — do claims and telemetry actually diverge?

[`09-demo-plan.md`](09-demo-plan.md) listed "no independent record of claimed times obtainable" as
a possible reason to stop. That was wrong, and pleasingly so.

**A single AIS message carries both a claim and its own contradiction material.**
`NavigationalStatus` is set by the crew. `SOG`, `LAT` and `LON` are GPS-derived. Every fix is a
miniature of the exact comparison the demonstrator proposes: an assertion sitting next to
independent physical evidence.

Counting only hard contradictions — a vessel claiming **at anchor** or **moored** while making
**≥3 knots**:

| | |
|---|---|
| Fixes examined (cargo/tanker) | 289,305 |
| Distinct vessels | 622 |
| Hard contradictions | **1,077 — 0.372% of fixes** |
| Vessels showing at least one | **40 — 6.4%** |
| Speed while claiming stationary | median 6.5 kt, max 58 kt |

Some vessels do it persistently: `MTM DUBLIN` on 31% of its fixes, `VICKI ANN` on 25%,
`HAMPSHIRE` on 23%.

A clean worked example — `QUEEN ZENOBIA`, Houston, 15 January 2023:

```
04:19:28  claims 'at anchor'  SOG 3.1 kt
04:20:39  claims 'at anchor'  SOG 4.0 kt
04:22:59  claims 'at anchor'  SOG 5.1 kt
04:24:09  claims 'at anchor'  SOG 5.4 kt
04:27:38  claims 'at anchor'  SOG 5.9 kt
04:31:08  claims 'at anchor'  SOG 6.2 kt
04:32:19  claims 'at anchor'  SOG 6.3 kt
```

A vessel heaving up and departing while continuing to broadcast that it is anchored.

### What this does and does not show

**It does not show fraud, and must never be presented as showing fraud.** The overwhelmingly
likely explanation is staleness: a crew updates the status field late, or not at all. Nobody gains
from misdeclaring AIS navigational status; there is no money attached to that particular field.

**What it does establish** is narrower and still load-bearing: *self-reported operational state and
physical reality come apart routinely, at a rate around 0.4% of observations and touching 6% of
vessels, in a field where nobody even has an incentive to lie.*

The reasonable inference — and it is an inference — is that fields where money **is** attached
would not diverge less.

---

## Limitations, stated plainly

**AIS times physical events. The claims that matter commercially are documentary.** Notice of
Readiness is a document tendered by the master; AIS cannot say when an email was sent. What it can
do is establish whether the claimed time was *physically possible* — a vessel cannot validly tender
NOR as an arrived ship while making 12 knots thirty miles out. That constrains the claim rather
than proving it, and every downstream statement must be phrased that way.

**The divergence proxy is weak.** Navigational status is not a commercial claim. It is the best
available stand-in and should be labelled as one.

**Data quality is imperfect.** A cargo vessel logged at 58 knots is not real, and one persistent
offender carries an invalid IMO number (`IMO0622325`). Bad records exist and must be filtered, not
trusted.

**Outliers survive the median.** 99.2% of geofence crossings fall within five minutes; the worst
was 39 minutes. A single dispute could land on a bad window.

**Narrow sample.** US waters, 2023, two ports, four days, 682 vessel-days. Enough to clear a kill
criterion, not enough to publish.

**AIS itself can be spoofed** — flagged in [`09-demo-plan.md`](09-demo-plan.md) and unaddressed
here. Nothing in Phase 0 tested for manipulation.

---

## Verdict

| Kill criterion from `docs/09` | Result |
|---|---|
| Arrival cannot be pinned within ~15 minutes | **Passed** — 70 s median, 99.2% within 5 min |
| Coverage gaps make approach and anchorage unusable | **Passed** — 0.112% of intervals exceed 15 min |
| No independent record of claimed times obtainable | **Passed** — navigational status serves as a partial proxy, and diverges measurably |

Phase 0 does not show anyone will pay. It shows the evidence layer is technically possible and the
premise is not obviously false — which is exactly what it was for, and it cost an afternoon rather
than a year.

**Proceed to Phase 1.**

---

## Reproducing this

```bash
cd tools/phase0
bash fetch.sh          # downloads four dates, extracts two port boxes, deletes the archives
python aggregate.py    # test 1 -- timing resolution
python divergence.py   # test 2 -- claim vs telemetry
```

Roughly 1.3 GB of transfer and a few minutes. No credentials, no application, no counterparty.
