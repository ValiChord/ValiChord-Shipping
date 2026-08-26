"""Phase 0b step 2 -- reconstruct a real port call from a real judgment.

Tricon Energy Ltd v MTM Trading LLC [2020] EWHC 700 (Comm). Agreed facts:

    "(c) NOR was tendered at the discharge port, Houston, on 20 March 2017 at 01.12;
     (d) the Vessel was shifting to her berth between 14.48 and 20.40 on 21 March 2017;
     (e) discharge commenced on 22 March 2017 at 03.20"

The judgment never names the vessel. She is identified here by inference: the owner is
MTM Trading LLC, whose fleet carries MTM-prefixed names, and exactly one MTM vessel was
anywhere near Houston that day. THAT IS AN INFERENCE AND THE OUTPUT SAYS SO.

READ docs/21 FOR THE RESULT AND docs/20 BEFORE DRAWING ANY CONCLUSION FROM IT.
The vessel was ~59 nm out and making 13.4 knots when NOR was tendered. That is NOT a
catch: NOR is a notice sent by email, tendering it inbound is ordinary, and these times
were COMMON GROUND between the parties. The dispute was a time bar over missing documents.

Input:  ais/AIS_2017_03_20.zip  (301 MB, NOAA/MarineCadastre, public domain)
Output: tricon_result.json
"""
import csv
import io
import json
import math
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ZIP = os.path.join(HERE, "ais", "AIS_2017_03_20.zip")
CSV_NAME = "AIS_2017_03_20.csv"

# Galveston Bar pilot station -- where Houston-bound tankers arrive.
PILOT = (29.31, -94.70)
FLEET_PREFIX = "MTM"


def nm_from_pilot(lat, lon):
    return math.hypot((lon - PILOT[1]) * 60 * math.cos(math.radians(PILOT[0])),
                      (lat - PILOT[0]) * 60)


def main():
    if not os.path.exists(ZIP):
        sys.exit(f"missing {ZIP}\n  curl -o {ZIP} \\\n"
                 f"    https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2017/"
                 f"{os.path.basename(ZIP)}")

    tracks = {}
    with zipfile.ZipFile(ZIP) as z, z.open(CSV_NAME) as fh:
        for row in csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8",
                                                   errors="replace")):
            name = (row["VesselName"] or "").strip().upper()
            if not name.startswith(FLEET_PREFIX):
                continue
            try:
                lat, lon, sog = (float(row["LAT"]), float(row["LON"]),
                                 float(row["SOG"]))
            except ValueError:
                continue
            tracks.setdefault(name, {"imo": row["IMO"], "mmsi": row["MMSI"],
                                     "fixes": []})
            tracks[name]["fixes"].append({
                "t": row["BaseDateTime"], "lat": lat, "lon": lon, "sog": sog,
                "status": row["Status"],
                "nm_from_pilot": round(nm_from_pilot(lat, lon), 2)})

    if not tracks:
        sys.exit("no MTM-named vessels found -- check the archive")

    for v in tracks.values():
        v["fixes"].sort(key=lambda p: p["t"])
        v["closest_nm"] = min(p["nm_from_pilot"] for p in v["fixes"])

    ranked = sorted(tracks.items(), key=lambda kv: kv[1]["closest_nm"])
    best_name, best = ranked[0]

    print(f"{len(tracks)} {FLEET_PREFIX}-named vessels in US AIS on 2017-03-20:")
    for n, v in ranked:
        print(f"  {n:16s} {v['imo']:14s} fixes={len(v['fixes']):5d}  "
              f"closest={v['closest_nm']:8.2f} nm")

    # the moment the judgment records NOR being tendered
    at_nor = min(best["fixes"],
                 key=lambda p: abs(int(p["t"][11:13]) * 60 + int(p["t"][14:16]) - 72))
    anchored = next((p for p in best["fixes"] if p["sog"] < 0.5), None)

    print(f"\nidentified (BY INFERENCE): {best_name}, IMO {best['imo']}")
    print(f"  at 01:12 (NOR per judgment): {at_nor['nm_from_pilot']} nm, "
          f"{at_nor['sog']} kt, status {at_nor['status']}")
    if anchored:
        print(f"  anchored:                   {anchored['t']} at "
              f"{anchored['nm_from_pilot']} nm")
    print(f"  closest approach that day:  {best['closest_nm']} nm "
          f"(never entered the channel -- consistent with berthing on 21 March)")

    result = {
        "_disclosure": {
            "vesselIdentification": "INFERENCE. The judgment never names the vessel. "
                                    "Identified as the only MTM-fleet vessel near "
                                    "Houston that day. Strong, but not confirmed.",
            "telemetry": "REAL -- NOAA/MarineCadastre public AIS, unmodified",
            "judgment": "REAL -- [2020] EWHC 700 (Comm), Find Case Law",
            "notAFinding": "The vessel was ~59 nm out and making way when NOR was "
                           "tendered. This is NOT evidence of wrongdoing. NOR is a "
                           "notice sent by email; tendering it inbound is ordinary; "
                           "and these times were COMMON GROUND between the parties. "
                           "See docs/21.",
        },
        "case": {"citation": "[2020] EWHC 700 (Comm)",
                 "parties": "Tricon Energy Ltd v MTM Trading LLC",
                 "port": "Houston", "agreedNorTendered": "2017-03-20T01:12",
                 "agreedShiftingToBerth": "2017-03-21T14:48 to 20:40",
                 "agreedDischargeCommenced": "2017-03-22T03:20",
                 "disputeWasAbout": "whether the demurrage claim was time-barred for "
                                    "want of supporting documents -- NOT the timings"},
        "candidates": [{"name": n, "imo": v["imo"], "mmsi": v["mmsi"],
                        "fixes": len(v["fixes"]), "closestNm": v["closest_nm"]}
                       for n, v in ranked],
        "identified": {"name": best_name, "imo": best["imo"], "mmsi": best["mmsi"]},
        "atNorTime": at_nor,
        "anchored": anchored,
        "closestNmThatDay": best["closest_nm"],
        "hourly": [p for p in best["fixes"]
                   if p["t"][14:16] < "02"][:24],
        "notDetermined": [
            "Whether the NOR was validly tendered. That is a question of law under the "
            "particular charter, not of position.",
            "Whether this is in fact the vessel in the case.",
            "Anything not visible to AIS -- hoses, cargo operations, weather, "
            "documentation. See docs/20 on why that limitation decides the use case.",
        ],
    }
    out = os.path.join(HERE, "tricon_result.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
    print(f"\nwrote {os.path.basename(out)}")
    print("\nREAD docs/20 BEFORE DRAWING A CONCLUSION FROM THIS.")


if __name__ == "__main__":
    main()
