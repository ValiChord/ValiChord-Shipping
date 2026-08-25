"""Phase 1 step 1 — extract one real port call from the Phase 0 AIS data.

Everything this writes is REAL. The vessel, the track, the timings, the speeds are
all from NOAA/MarineCadastre public AIS. Nothing here is invented.

The synthetic part of the demonstrator lives in demo.py and is labelled there.

Output: case.json
"""
import csv, json, math, os, sys
from datetime import datetime, timezone

# CSL SPIRIT, Los Angeles / Long Beach, 15 January 2023.
# Chosen by tools/phase0 analysis: cleanest inbound profile available, with the
# port-limit crossing resolved to +-29 seconds.
MMSI = None                      # resolved from IMO below
IMO = "IMO9138111"
SRC = "../phase0/lalb_2023_01_15.csv"
PORT = {"name": "Los Angeles / Long Beach", "unlocode": "USLAX",
        "lat": 33.720, "lon": -118.190, "limit_nm": 12.0}


def ts(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")


def nm(la, lo):
    return math.hypot((lo - PORT["lon"]) * 60 * math.cos(math.radians(PORT["lat"])),
                      (la - PORT["lat"]) * 60)


def main():
    if not os.path.exists(SRC):
        sys.exit(f"missing {SRC} -- run tools/phase0/fetch.sh first")

    track, meta = [], None
    with open(SRC, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("IMO", "").strip() != IMO:
                continue
            try:
                track.append({
                    "t": r["BaseDateTime"], "lat": float(r["LAT"]), "lon": float(r["LON"]),
                    "sog": float(r["SOG"]), "cog": float(r["COG"] or 0),
                    "status": r.get("Status", ""),
                })
            except ValueError:
                continue
            if meta is None:
                meta = {"name": r.get("VesselName", "").strip(), "imo": IMO,
                        "mmsi": r["MMSI"], "callsign": r.get("CallSign", "").strip(),
                        "vessel_type": r.get("VesselType", ""),
                        "length_m": r.get("Length", ""), "draft_m": r.get("Draft", "")}
    if not track:
        sys.exit(f"no fixes found for {IMO}")
    track.sort(key=lambda p: p["t"])
    for p in track:
        p["dist_nm"] = round(nm(p["lat"], p["lon"]), 3)

    # derive the two events, bracketed -- we know the crossing happened inside the
    # window between two fixes and nowhere else
    events = {}
    for a, b in zip(track, track[1:]):
        if "port_limit_inbound" not in events and \
           a["dist_nm"] > PORT["limit_nm"] >= b["dist_nm"]:
            events["port_limit_inbound"] = {
                "after": a["t"], "before": b["t"],
                "window_s": (ts(b["t"]) - ts(a["t"])).total_seconds(),
                "note": "vessel crossed the 12nm port limit inbound somewhere in this window"}
        if "port_limit_inbound" in events and "stopped" not in events and \
           a["sog"] >= 3.0 and b["sog"] < 0.5:
            events["stopped"] = {
                "after": a["t"], "before": b["t"],
                "window_s": (ts(b["t"]) - ts(a["t"])).total_seconds(),
                "note": "speed over ground fell below 0.5kt somewhere in this window"}

    case = {
        "_provenance": {
            "source": "NOAA / MarineCadastre public AIS, AIS_2023_01_15.zip",
            "url": "https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2023/",
            "status": "REAL DATA -- unmodified public record",
            "extracted": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
        "vessel": meta, "port": PORT,
        "fix_count": len(track),
        "first_fix": track[0]["t"], "last_fix": track[-1]["t"],
        "derived_events": events,
        "track": track,
    }
    with open("case.json", "w", encoding="utf-8") as f:
        json.dump(case, f, indent=2)

    print(f"vessel : {meta['name']} ({IMO}), MMSI {meta['mmsi']}")
    print(f"fixes  : {len(track)}  {track[0]['t']} -> {track[-1]['t']}")
    for k, v in events.items():
        print(f"event  : {k:20s} between {v['after']} and {v['before']}  "
              f"(+-{v['window_s']:.0f}s)")
    print("wrote case.json")


if __name__ == "__main__":
    main()
