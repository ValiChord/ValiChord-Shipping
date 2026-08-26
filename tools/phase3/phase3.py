"""Phase 3 — the same protocol as Phase 1, but with a real external witness.

Run order per party:
  1. fetch the current drand round                  -> the FLOOR
  2. embed it in the payload, hash, sign            -> the COMMITMENT
  3. get signed tokens from independent timestamp authorities -> the CEILING
  4. (later) reveal
  5. verify: hash, signature, floor re-fetched from independent relays, ceiling tokens

What this establishes is an INTERVAL, not an instant. Fabricating or omitting the beacon
is refused outright. Embedding a genuine but STALE round is not refused -- it verifies
perfectly and proves nothing, and the only thing that exposes it is how wide the
resulting interval is. So every party record carries the width, and a boolean
"witnessed: true" would be misleading. See negative_control.py.

CORRECTED 26 August 2026 -- THE CEILING WAS THIS MACHINE'S CLOCK
----------------------------------------------------------------
This file previously computed the interval as `int(time.time()) - roundUnixTime` and
declared that the commitment "provably exists somewhere inside this window and nowhere
outside it". The top of that window was this machine's own clock. A party wanting to
appear prompt sets both ends: a stale beacon round for the floor, and whatever it likes
for the ceiling. The one honest limitation the phase was built around -- that interval
WIDTH is what exposes a stale round -- was therefore not enforced by anything.

The record now separates three different things, and calls each what it is:

  timeFloor            established, independent, verifiable immediately
  localAnchorRequest   SELF-REPORTED. Evidence of nothing. Recorded for operations only
  timeCeiling          signed by independent RFC 3161 authorities, immediately

An interval is reported only when a real ceiling exists. See docs/16 Part 3.

WHY NOT BITCOIN
---------------
The first fix used OpenTimestamps, which pins the digest into Bitcoin. It works, but the
ceiling takes HOURS -- so in the meantime there was no interval, and the one attack this
phase could not refuse (a genuine but STALE beacon round) stayed unmeasurable. It also
means saying "blockchain" to a sector that watched TradeLens fail.

RFC 3161 timestamp authorities return a signed token in about a second, from independent
operators in different jurisdictions. The interval is real and narrow immediately. Bitcoin
is still available -- set VALICHORD_OTS=1 -- but it is no longer the default and is not
what anyone gets shown.
"""
import hashlib, json, os, secrets, sys, time
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "phase1"))
from demo import canonical, Party, verify_commitment, CLAIM_TIMES   # noqa: E402
from witness import (beacon_floor, verify_floor, tsa_ceiling,       # noqa: E402
                     anchor, TSAS)

# Bitcoin anchoring is OFF by default. The ceiling comes from RFC 3161 timestamp
# authorities, which are immediate and do not require explaining a blockchain to a
# laytime desk. Set VALICHORD_OTS=1 to additionally anchor to Bitcoin.
USE_OTS = os.environ.get("VALICHORD_OTS") == "1"

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

    # Claim times come from Phase 1's CLAIM_TIMES literals, not from `ev`. Deriving a
    # claim from the telemetry and then checking it against that telemetry is the
    # circularity corrected in docs/16 Part 3.
    specs = [
        ("CARRIER", "Global Ocean Line (synthetic)",
         {"eventTypeCode": "ARRI", "eventDateTime": CLAIM_TIMES["CARRIER"]["at"],
          "operationalDetails": {"noticeOfReadinessTendered": True}}),
        ("PORT_AUTHORITY", "USLAX VTS (synthetic)",
         {"eventTypeCode": "ARRI",
          "eventDateTime": CLAIM_TIMES["PORT_AUTHORITY"]["at"],
          "operationalDetails": {"vesselAction": "ENTERED_PORT_LIMITS"}}),
        ("TERMINAL_OPERATOR", "Delta Marine Terminal (synthetic)",
         {"eventTypeCode": "MOOR",
          "eventDateTime": CLAIM_TIMES["TERMINAL_OPERATOR"]["at"],
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

    print(f"getting ceilings from {len(TSAS)} independent timestamp authorities "
          f"({', '.join(t[2] for t in TSAS)}) ...")
    tok_dir = os.path.join(HERE, "timestamps")
    ceilings, anchors = {}, {}
    for c in commit_log:
        t = tsa_ceiling(c["commitment_sha256"], out_dir=tok_dir,
                        label=c["role"].lower())
        ceilings[c["role"]] = t
        print(f"  {c['role']:18s} {t['granted']}/{len(TSAS)} granted"
              f"  ceiling={t['ceilingNote'][:34] if not t['ceilingEstablished'] else 'established'}")

    if USE_OTS:
        print("\nalso anchoring to Bitcoin via OpenTimestamps (VALICHORD_OTS=1) ...")
        ots_dir = os.path.join(HERE, "ots")
        for c in commit_log:
            a = anchor(c["commitment_sha256"], ots_dir=ots_dir,
                       label=c["role"].lower())
            anchors[c["role"]] = a
            print(f"  {c['role']:18s} {a['accepted']}/3 calendars, "
                  f"{a['ceilingNote'][:40]}")

    # SELF-REPORTED. This is when this machine says it asked for the anchors. It proves
    # nothing to an adversary and is NOT the ceiling. Kept only so an operator can see
    # whether anchoring followed the floor promptly -- the discipline the phase depends on.
    local_anchor_request = int(time.time())

    print("\nrevealing and verifying ...")
    reveals = [p.reveal_record() for p in parties]
    results = []
    for c, r in zip(commit_log, reveals):
        integ = verify_commitment(c, r)
        f = r["payload"].get("_timeFloor")
        fv = verify_floor(f)
        tc = ceilings[c["role"]]
        a = anchors.get(c["role"])
        floor_unix = f.get("roundUnixTime") if f else None

        # An interval requires BOTH ends to be established by someone other than us.
        # Both now are, immediately: an unpredictable beacon below, signed timestamp
        # authorities above. Neither is this machine's clock.
        if tc["ceilingEstablished"] and floor_unix:
            width = tc["ceilingUnix"] - floor_unix
            interval = {
                "established": True,
                "floorUnix": floor_unix,
                "ceilingUnix": tc["ceilingUnix"],
                "seconds": width,
                "meaning": "the commitment was made after the drand round and before "
                           "the earliest timestamp authority signed for it. Both bounds "
                           "are set by parties this project does not operate.",
                # docs/13's unrefused attack -- a genuine but STALE beacon round --
                # is exposed by this number and nothing else. Which is why the ceiling
                # had to be immediate rather than pending.
                "strength": ("tight" if width <= 300 else
                             "loose" if width <= 3600 else
                             "weak -- a stale beacon round would look like this"),
            }
        else:
            interval = {
                "established": False,
                "floorUnix": floor_unix,
                "meaning": "NO INTERVAL. The floor holds; no timestamp authority "
                           "granted a ceiling. This record proves the commitment was "
                           "not made EARLIER than the drand round, and nothing about "
                           "how much later.",
            }

        # Self-reported, and labelled as such wherever it appears.
        elapsed = (local_anchor_request - floor_unix) if floor_unix else None

        results.append({
            "role": c["role"], "party": c["party"],
            "commitmentSha256": c["commitment_sha256"],
            "hashMatches": integ["commitment_matches_reveal"],
            "signatureValid": integ["signature_valid"],
            "timeFloor": {"round": f["round"] if f else None,
                          "roundUnixTime": floor_unix,
                          "independentlyReVerified": fv},
            "timeCeiling": {"protocol": "RFC3161",
                            "authoritiesGranting": tc["granted"],
                            "of": len(TSAS),
                            "established": tc["ceilingEstablished"],
                            "ceilingUnix": tc["ceilingUnix"],
                            "authorities": tc["authorities"],
                            "note": tc["ceilingNote"],
                            "limitation": tc["limitation"],
                            "verifyBy": tc["verifyBy"],
                            "bitcoinAlsoAnchored": bool(a)},
            "localAnchorRequest": {
                "secondsAfterFloor": elapsed,
                "selfReported": True,
                "provesNothing": "this is our own clock. An adversary sets it freely. "
                                 "It is operational hygiene -- did we anchor promptly "
                                 "after committing -- not evidence.",
            },
            "timeInterval": interval,
        })
        ok = (integ["commitment_matches_reveal"] and integ["signature_valid"]
              and fv.get("randomnessMatches") and tc["ceilingEstablished"])
        print(f"  [{'OK  ' if ok else 'FAIL'}] {c['role']:18s} "
              f"hash={'match' if integ['commitment_matches_reveal'] else 'MISMATCH'} "
              f"sig={'valid' if integ['signature_valid'] else 'INVALID'} "
              f"floor={fv.get('relaysAgreeing')}/{len(fv.get('relays', []))} relays "
              f"ceiling={tc['granted']}/{len(TSAS)} TSAs "
              f"interval={interval.get('seconds')}s")

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
            "ceiling": {"what": "RFC 3161 timestamp authorities, independent operators "
                                "in different jurisdictions",
                        "proves": "the commitment existed before the earliest authority "
                                  "signed for it",
                        "authorities": [f"{n} ({j})" for n, _u, j in TSAS],
                        "established": ceilings[commit_log[0]["role"]]["ceilingEstablished"],
                        "bitcoinAlsoUsed": USE_OTS,
                        "note": "A pending calendar attestation carries a URI and "
                                "NOTHING ELSE -- no time, no signature over a time. It "
                                "is a promise, not a bound. Until a block confirms "
                                "there is no ceiling, and this record does not pretend "
                                "there is one. Corrected 26 Aug 2026, docs/16 Part 3."},
            "humansRequired": 0,
            "whatItProves": "TODAY: a FLOOR only -- the commitment was not made before "
                            "the drand round. That refutes backdating to any point "
                            "earlier than the round, and nothing else. Once the .ots "
                            "files are upgraded, floor and ceiling together give an "
                            "interval. A genuine but stale round still verifies "
                            "perfectly while proving little, so interval width -- not a "
                            "boolean -- remains the measure. See negative_control.py "
                            "attack 4.",
        },
        "case": {"vessel": vessel, "port": port},
        "parties": results,
        "anchors": anchors,
        "notDetermined": [
            "Whether Notice of Readiness was validly tendered -- a contested question "
            "of law, not of position or of timing.",
            "Any laytime or demurrage consequence, or amount.",
            "Whether any divergence was deliberate.",
            "Whether the timestamp authorities told the truth about the time. RFC 3161 "
            "is trusted, not trustless; several independent operators in different "
            "jurisdictions would have to collude. An earlier version of this record "
            "answered the WHEN question using its own system clock, which was not "
            "evidence at all.",
            "Whether drand's threshold signature is valid. Independent relays agree on "
            "the round, which is weaker than verifying the signature.",
        ],
    }
    out = os.path.join(HERE, "witnessed_record.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2)
    print(f"\nwrote {os.path.basename(out)}")
    print(f"floor: drand round {floor['round']}   ceiling: "
          f"{results[0]['timeCeiling']['authoritiesGranting']}/{len(TSAS)} authorities"
          f"   interval: {results[0]['timeInterval'].get('seconds')}s   humans: 0")


if __name__ == "__main__":
    main()
