"""Phase 3 — the same protocol as Phase 1, but with a real external witness.

Run order per party:
  1. fetch the current drand round                  -> the FLOOR
  2. embed it in the payload, hash, sign            -> the COMMITMENT
  3. submit the commitment digest to 3 calendars    -> the CEILING
  4. (later) reveal
  5. verify: hash, signature, floor re-fetched independently, calendar receipts

What this establishes is an INTERVAL, not an instant. Fabricating or omitting the beacon
is refused outright. Embedding a genuine but STALE round is not refused -- it verifies
perfectly and proves nothing, and the only thing that exposes it is how wide the
resulting interval is. So every party record carries the width, and a boolean
"witnessed: true" would be misleading. See negative_control.py.
"""
import hashlib, json, os, secrets, sys, time
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "phase1"))
from demo import canonical, Party, verify_commitment          # noqa: E402
from witness import beacon_floor, verify_floor, anchor         # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.join(HERE, "..", "phase1", "case.json")
UTC = timezone.utc


def now():
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def main():
    case = json.load(open(CASE, encoding="utf-8"))
    vessel, port, ev = case["vessel"], case["port"], case["derived_events"]

    print("Phase 3 -- witnessed commitments\n")
    print("fetching floor from drand (League of Entropy) ...")
    floor = beacon_floor()
    if not floor:
        sys.exit("drand unreachable -- refusing to run. A witnessed protocol with no "
                 "witness should fail loudly, not quietly produce an unwitnessed record.")
    print(f"  round {floor['round']}  randomness {floor['randomness'][:24]}...\n")

    NOR = "2023-01-15T05:30:00Z"
    specs = [
        ("CARRIER", "Global Ocean Line (synthetic)",
         {"eventTypeCode": "ARRI", "eventDateTime": NOR,
          "operationalDetails": {"noticeOfReadinessTendered": True}}),
        ("PORT_AUTHORITY", "USLAX VTS (synthetic)",
         {"eventTypeCode": "ARRI",
          "eventDateTime": ev["port_limit_inbound"]["before"] + "Z",
          "operationalDetails": {"vesselAction": "ENTERED_PORT_LIMITS"}}),
        ("TERMINAL_OPERATOR", "Delta Marine Terminal (synthetic)",
         {"eventTypeCode": "MOOR", "eventDateTime": ev["stopped"]["before"] + "Z",
          "operationalDetails": {"vesselAction": "WAY_OFF"}}),
    ]

    parties, commit_log = [], []
    for role, name, body in specs:
        payload = dict(body, specVersion="DCSA-JIT-1.2",
                       transportCallID="TC-2023-USLAX-0042",
                       vesselIMONumber=vessel["imo"].replace("IMO", ""),
                       UNLocationCode=port["unlocode"],
                       # the floor lives INSIDE the payload, so it is covered by the hash
                       _timeFloor=floor)
        p = Party(role, name, payload)
        parties.append(p)
        commit_log.append(p.commit_record(len(commit_log) + 1))

    print("anchoring commitments to OpenTimestamps calendars ...")
    anchors = {}
    for c in commit_log:
        a = anchor(c["commitment_sha256"])
        anchors[c["role"]] = a
        print(f"  {c['role']:18s} {a['accepted']}/3 calendars accepted")

    anchored_at = int(time.time())

    print("\nrevealing and verifying ...")
    reveals = [p.reveal_record() for p in parties]
    results = []
    for c, r in zip(commit_log, reveals):
        integ = verify_commitment(c, r)
        f = r["payload"].get("_timeFloor")
        fv = verify_floor(f)
        a = anchors[c["role"]]
        # The honest metric. A floor proves "not before"; a ceiling proves "not after".
        # What the pair establishes is an INTERVAL, and its usefulness is entirely a
        # function of how narrow it is. See negative_control.py attack 4: a genuine but
        # stale beacon round verifies perfectly and proves nothing.
        width = (anchored_at - f["roundUnixTime"]) if (f and f.get("roundUnixTime")) else None
        results.append({
            "role": c["role"], "party": c["party"],
            "commitmentSha256": c["commitment_sha256"],
            "hashMatches": integ["commitment_matches_reveal"],
            "signatureValid": integ["signature_valid"],
            "timeFloor": {"round": f["round"] if f else None,
                          "roundUnixTime": f.get("roundUnixTime") if f else None,
                          "independentlyReVerified": fv},
            "timeCeiling": {"calendarsAccepted": a["accepted"],
                            "of": len(a["calendars"]),
                            "bitcoinConfirmed": a["bitcoinConfirmed"]},
            "timeInterval": {
                "seconds": width,
                "meaning": "the commitment provably exists somewhere inside this "
                           "window and nowhere outside it",
                "strength": (None if width is None else
                             "tight" if width <= 300 else
                             "loose" if width <= 3600 else
                             "weak -- proves little about when it was actually made"),
            },
        })
        ok = (integ["commitment_matches_reveal"] and integ["signature_valid"]
              and fv.get("randomnessMatches") and a["accepted"] > 0)
        print(f"  [{'OK  ' if ok else 'FAIL'}] {c['role']:18s} "
              f"hash={'match' if integ['commitment_matches_reveal'] else 'MISMATCH'} "
              f"sig={'valid' if integ['signature_valid'] else 'INVALID'} "
              f"floor={'re-verified' if fv.get('randomnessMatches') else 'UNVERIFIED'} "
              f"ceiling={a['accepted']}/3 interval={width}s")

    record = {
        "_disclosure": {
            "telemetry": "REAL -- NOAA/MarineCadastre public AIS, unmodified",
            "partyRecords": "SYNTHETIC -- no real organisation supplied logs",
            "witnesses": "REAL -- drand and OpenTimestamps are live public services, "
                         "contacted at run time. Neither is operated by this project.",
        },
        "protocolRun": {"id": "P3-" + secrets.token_hex(4), "at": now()},
        "witnessModel": {
            "floor": {"what": "drand / League of Entropy public randomness beacon",
                      "proves": "the commitment was not constructed before this round",
                      "round": floor["round"], "chainHash": floor["chainHash"],
                      "verifyBy": floor["verifyBy"]},
            "ceiling": {"what": "OpenTimestamps calendars, Bitcoin-anchored",
                        "proves": "the commitment existed before the confirming block",
                        "calendars": [c["calendar"] for c in
                                      anchors[commit_log[0]["role"]]["calendars"]],
                        "bitcoinConfirmed": False,
                        "note": "until a block confirms, the ceiling rests on the "
                                "calendars' signatures -- hence three independent "
                                "operators rather than one"},
            "humansRequired": 0,
            "whatItProves": "an INTERVAL, not an instant. A genuine but stale "
                            "beacon round verifies perfectly while proving "
                            "nothing, so the interval width -- not a boolean -- "
                            "is the measure. See negative_control.py attack 4.",
        },
        "case": {"vessel": vessel, "port": port},
        "parties": results,
        "anchors": anchors,
        "notDetermined": [
            "Whether Notice of Readiness was validly tendered -- a contested question "
            "of law, not of position or of timing.",
            "Any laytime or demurrage consequence, or amount.",
            "Whether any divergence was deliberate.",
            "Bitcoin confirmation of the ceiling, which takes hours. At the moment of "
            "writing, the ceiling is three independent calendar signatures.",
        ],
    }
    out = os.path.join(HERE, "witnessed_record.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2)
    print(f"\nwrote {os.path.basename(out)}")
    print(f"floor: drand round {floor['round']}   ceiling: "
          f"{results[0]['timeCeiling']['calendarsAccepted']}/3 calendars   humans: 0")


if __name__ == "__main__":
    main()
