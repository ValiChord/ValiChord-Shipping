"""Phase 0 step 4: aggregate the resolution finding across dates and ports."""
import csv, glob, math, statistics as st
from collections import defaultdict
from datetime import datetime

STOPPED, MOVING, HOLD_MIN = 0.5, 3.0, 30
CARGO_TANKER = range(70, 90)

# geofence centre + radius (nm) per port -- any boundary crossed while underway
# gives the same measurement answer; these are plausible port-limit proxies
FENCE = {
    "lalb":    (33.720, -118.190, 12.0),   # LA/LB breakwater
    "houston": (29.340,  -94.770,  8.0),   # Bolivar Roads entrance
}


def ts(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")


def nm(la, lo, cla, clo):
    return math.hypot((lo - clo) * 60 * math.cos(math.radians(cla)), (la - cla) * 60)


def pct(v, p):
    v = sorted(v)
    return v[min(int(len(v) * p / 100), len(v) - 1)] if v else float("nan")


def load(path):
    rows, meta = defaultdict(list), {}
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                m, sog = r["MMSI"], float(r["SOG"])
                t, la, lo = ts(r["BaseDateTime"]), float(r["LAT"]), float(r["LON"])
            except (ValueError, KeyError, TypeError):
                continue
            rows[m].append((t, sog, la, lo))
            meta.setdefault(m, (r.get("VesselName", "").strip(),
                                r.get("VesselType", ""), r.get("IMO", "").strip()))
    comm = {}
    for m, pts in rows.items():
        try:
            vt = int(float(meta[m][1]))
        except (ValueError, TypeError):
            continue
        if vt in CARGO_TANKER and len(pts) >= 20:
            comm[m] = sorted(pts)
    return comm, meta


agg = {p: {"stop": [], "geo": [], "gaps": [], "vessels": 0, "days": 0}
       for p in FENCE}

for port in FENCE:
    cla, clo, rad = FENCE[port]
    for path in sorted(glob.glob(f"{port}_2023_*.csv")):
        comm, meta = load(path)
        agg[port]["vessels"] += len(comm)
        agg[port]["days"] += 1
        for m, pts in comm.items():
            for a, b in zip(pts, pts[1:]):
                agg[port]["gaps"].append((b[0] - a[0]).total_seconds())
            # STOP
            for i in range(len(pts) - 1):
                (t1, s1, *_), (t2, s2, *_) = pts[i], pts[i + 1]
                if s1 < STOPPED or s2 >= STOPPED:
                    continue
                held = [q for q in pts[i + 1:]
                        if (q[0] - t2).total_seconds() <= HOLD_MIN * 60]
                if held and all(q[1] < MOVING for q in held) and \
                   (held[-1][0] - t2).total_seconds() >= HOLD_MIN * 48:
                    g = (t2 - t1).total_seconds()
                    if g < 3600:
                        agg[port]["stop"].append(g)
                    break
            # GEOFENCE inbound
            for i in range(len(pts) - 1):
                (t1, s1, la1, lo1), (t2, s2, la2, lo2) = pts[i], pts[i + 1]
                if nm(la1, lo1, cla, clo) > rad >= nm(la2, lo2, cla, clo):
                    g = (t2 - t1).total_seconds()
                    if g < 3600:
                        agg[port]["geo"].append(g)
                    break

print("PHASE 0 -- AIS TIMING RESOLUTION, aggregated\n")
print(f"{'port':9s} {'days':>4s} {'vessel-days':>11s} {'event':9s} {'n':>4s} "
      f"{'median':>7s} {'p90':>6s} {'max':>6s}  {'<=5min':>7s} {'<=15min':>8s}")
allgeo, allstop = [], []
for port, d in agg.items():
    for label, key in (("GEOFENCE", "geo"), ("STOP", "stop")):
        v = d[key]
        if not v:
            continue
        (allgeo if key == "geo" else allstop).extend(v)
        f5 = 100 * sum(1 for x in v if x <= 300) / len(v)
        f15 = 100 * sum(1 for x in v if x <= 900) / len(v)
        print(f"{port:9s} {d['days']:>4d} {d['vessels']:>11d} {label:9s} {len(v):>4d} "
              f"{st.median(v):>7.0f} {pct(v,90):>6.0f} {max(v):>6.0f}  "
              f"{f5:>6.1f}% {f15:>7.1f}%")

print("\n--- combined ---")
for label, v in (("GEOFENCE (port-limit crossing, underway)", allgeo),
                 ("STOP (anchor down / all fast)", allstop)):
    if not v:
        continue
    print(f"{label}")
    print(f"   n={len(v)}  median={st.median(v):.0f}s ({st.median(v)/60:.1f} min)  "
          f"p90={pct(v,90):.0f}s  max={max(v):.0f}s")
    for th, lbl in ((60, " 1 min"), (300, " 5 min"), (900, "15 min")):
        print(f"   within {lbl}: {100*sum(1 for x in v if x<=th)/len(v):5.1f}%")

gaps = [g for d in agg.values() for g in d["gaps"]]
long_ = [g for g in gaps if g > 900]
print(f"\n--- coverage across all ports/days ---")
print(f"inter-fix intervals: {len(gaps):,}   median {st.median(gaps):.0f}s")
print(f"gaps > 15 min: {len(long_)} ({100*len(long_)/len(gaps):.3f}%)   "
      f"max {max(gaps)/3600:.1f} h")
