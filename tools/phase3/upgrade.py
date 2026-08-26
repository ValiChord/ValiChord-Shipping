"""Complete the ceiling once Bitcoin has confirmed.

Run this HOURS after phase3.py -- typically the next day. It asks the OpenTimestamps
calendars for the confirmed timestamp of each commitment and merges it into the .ots
file. When a BitcoinBlockHeaderAttestation appears, the commitment has a genuine upper
bound: it existed before that block was mined.

Why this exists
---------------
Until 26 August 2026 there was no upgrade step. phase3.py used its own system clock as
the top of the "interval" and the record claimed the commitment "provably exists
somewhere inside this window and nowhere outside it". A backdating party controls that
clock, so the claim was false and the phase's own headline limitation -- that interval
WIDTH is what exposes a stale beacon round -- was not enforced by anything.

See docs/16 Part 3.

The .ots files this upgrades are standard. Anyone can check them without this code:

    ots verify carrier.ots
"""
import glob
import json
import os
import sys

from witness import upgrade

HERE = os.path.dirname(os.path.abspath(__file__))
OTS_DIR = os.path.join(HERE, "ots")


def main():
    paths = sorted(glob.glob(os.path.join(OTS_DIR, "*.ots")))
    if not paths:
        sys.exit(f"no .ots files in {OTS_DIR} -- run phase3.py first")

    print(f"upgrading {len(paths)} timestamp(s) against the calendars\n")
    results, confirmed = [], 0
    for p in paths:
        r = upgrade(p)
        results.append(r)
        if r["ceilingEstablished"]:
            confirmed += 1
            print(f"  {r['otsFile']:24s} CONFIRMED  bitcoin block(s) "
                  f"{r['bitcoinBlockHeights']}")
        else:
            print(f"  {r['otsFile']:24s} still pending -- try again later")

    out = os.path.join(HERE, "ceiling_status.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"upgraded": results,
                   "ceilingsEstablished": confirmed,
                   "of": len(paths)}, fh, indent=2)

    print(f"\n{confirmed}/{len(paths)} ceilings established")
    if confirmed < len(paths):
        print("Bitcoin confirmation usually takes a few hours. Nothing is wrong;\n"
              "the record correctly reports that no upper bound exists yet.")
    print(f"wrote {os.path.basename(out)}")


if __name__ == "__main__":
    main()
