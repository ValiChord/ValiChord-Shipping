"""Phase 0 step 5: do reported claims actually diverge from physical telemetry?

docs/09 assumed this could not be tested without carrier logs. It can, partially,
because a single AIS message carries BOTH:

  * NavigationalStatus -- set by the crew. A CLAIM about what the vessel is doing.
  * SOG / LAT / LON     -- GPS derived. TELEMETRY.

So every AIS fix is a miniature version of the exact comparison the demo proposes:
somebody's assertion, next to independent physical evidence, in one record.

Hard contradictions only -- claiming to be stationary while demonstrably making way:

    status 1 (at anchor) or 5 (moored), with SOG >= 3.0 kt

Soft cases (status 0 "under way" while stopped) are excluded: a vessel under way
using engine can legitimately be stopped in the water, so that is not a contradiction.

This measures sloppiness and staleness as much as dishonesty. It is NOT evidence of
fraud, and must not be reported as such. What it establishes is narrower and still
useful: that self-reported operational status and physical reality do come apart in
the wild, at a measurable rate.
"""
import csv, glob, statistics as st
from collections import defaultdict
from datetime import datetime

STATUS = {0: "under way using engine", 1: "at anchor", 2: "not under command",
          3: "restricted manoeuvrability", 4: "constrained by draught",
          5: "moored", 6: "aground", 7: "fishing", 8: "under way sailing",
          15: "undefined"}
STATIONARY_CLAIM = {1, 5}
MOVING_KT = 3.0
CARGO_TANKER = range(70, 90)

tot = contradictions = 0
per_vessel = defaultdict(int)
fixes_per_vessel = defaultdict(int)
meta = {}
examples = []
speeds = []

for path in sorted(glob.glob("*_2023_*.csv")):
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                vt = int(float(r["VesselType"]))
                if vt not in CARGO_TANKER:
                    continue
                sog = float(r["SOG"])
                stat = int(float(r["Status"]))
                m = r["MMSI"]
            except (ValueError, KeyError, TypeError):
                continue
            if sog > 102.2:            # AIS sentinel for "not available"
                continue
            tot += 1
            fixes_per_vessel[m] += 1
            meta.setdefault(m, (r.get("VesselName", "").strip(),
                                r.get("IMO", "").strip()))
            if stat in STATIONARY_CLAIM and sog >= MOVING_KT:
                contradictions += 1
                per_vessel[m] += 1
                speeds.append(sog)
                if len(examples) < 10:
                    examples.append((r.get("VesselName", "").strip()[:22],
                                     r.get("IMO", "").strip(),
                                     r["BaseDateTime"], STATUS.get(stat, stat),
                                     sog, path.split("_", 1)[0]))

print("PHASE 0 -- CLAIM vs TELEMETRY DIVERGENCE (cargo/tanker only)\n")
print(f"AIS fixes examined:              {tot:,}")
print(f"vessels:                         {len(fixes_per_vessel):,}")
print(f"hard contradictions:             {contradictions:,} "
      f"({100*contradictions/max(tot,1):.3f}% of fixes)")
print(f"vessels showing >=1:             {len(per_vessel)} "
      f"({100*len(per_vessel)/max(len(fixes_per_vessel),1):.1f}% of vessels)")
if speeds:
    print(f"speed while claiming stationary: median {st.median(speeds):.1f} kt, "
          f"max {max(speeds):.1f} kt")

if per_vessel:
    print("\nmost persistent (contradicting fixes / total fixes):")
    for m, n in sorted(per_vessel.items(), key=lambda kv: -kv[1])[:8]:
        nm_, imo = meta[m]
        print(f"  {nm_[:24]:24s} {imo:11s} {n:>5d}/{fixes_per_vessel[m]:<6d} "
              f"({100*n/fixes_per_vessel[m]:.0f}%)")

print("\nexamples:")
for nm_, imo, t, stat, sog, port in examples:
    print(f"  {port:8s} {nm_:22s} {imo:11s} {t}  claims '{stat}'  "
          f"but SOG {sog:.1f} kt")
