"""Phase 1 — commit, reveal, verify, and report a discrepancy.

WHAT IS REAL AND WHAT IS NOT
----------------------------
REAL       The vessel (CSL SPIRIT, IMO 9138111), its entire track, every position,
           speed and timestamp. Public AIS from NOAA/MarineCadastre, unmodified.
SYNTHETIC  The four parties' event records, their keys, and the carrier's claim.
           Nobody has given us their operational logs. These are constructed to
           exercise the mechanism.

The demonstrator therefore shows that the MECHANISM works against real telemetry.
It does not show that any real carrier misreported anything. Every output carries
this disclosure; do not remove it.

WHAT THIS DELIBERATELY DOES NOT DO
-----------------------------------
No adjudication. No monetary figure. No confidence score. No interpretation of any
charterparty clause. Whether a Notice of Readiness was validly tendered is a
contested question of law (the "arrived ship" line of authority); this reports where
the vessel physically was and stops. See docs/08.

Phase 1 has NO EXTERNAL WITNESS to commitment ordering -- commit and reveal both
happen in this process. That is Phase 3's job. The output says so.
"""
import hashlib, json, secrets, sys
from datetime import datetime, timezone
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey)
from cryptography.exceptions import InvalidSignature

UTC = timezone.utc


def canonical(obj) -> bytes:
    """Deterministic serialisation -- the hash must be reproducible by anyone."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


# ---------------------------------------------------------------- parties

class Party:
    """One organisation. Holds a keypair, commits to a payload, later reveals it."""

    def __init__(self, role, name, payload):
        self.role, self.name, self.payload = role, name, payload
        self._sk = Ed25519PrivateKey.generate()
        self.pubkey = self._sk.public_key().public_bytes_raw().hex()
        self._nonce = secrets.token_bytes(32)
        self.commitment = hashlib.sha256(canonical(payload) + self._nonce).hexdigest()
        # signs the COMMITMENT, not the payload: binds the party without disclosing
        self.signature = self._sk.sign(bytes.fromhex(self.commitment)).hex()

    def commit_record(self, seq):
        return {"seq": seq, "role": self.role, "party": self.name,
                "commitment_sha256": self.commitment,
                "pubkey_ed25519": self.pubkey, "signature_ed25519": self.signature}

    def reveal_record(self):
        return {"role": self.role, "party": self.name,
                "nonce_hex": self._nonce.hex(), "payload": self.payload}


def verify_commitment(commit_rec, reveal_rec):
    """Recompute the hash and check the signature. Anyone can run this."""
    recomputed = hashlib.sha256(
        canonical(reveal_rec["payload"]) + bytes.fromhex(reveal_rec["nonce_hex"])
    ).hexdigest()
    hash_ok = secrets.compare_digest(recomputed, commit_rec["commitment_sha256"])
    try:
        Ed25519PublicKey.from_public_bytes(
            bytes.fromhex(commit_rec["pubkey_ed25519"])
        ).verify(bytes.fromhex(commit_rec["signature_ed25519"]),
                 bytes.fromhex(commit_rec["commitment_sha256"]))
        sig_ok = True
    except (InvalidSignature, ValueError):
        sig_ok = False
    return {"role": commit_rec["role"], "party": commit_rec["party"],
            "commitment_matches_reveal": hash_ok, "signature_valid": sig_ok,
            "commitment_sha256": commit_rec["commitment_sha256"],
            "recomputed_sha256": recomputed}


# ------------------------------------------------------- telemetry bracket

def bracket(track, when):
    """Where was the vessel at `when`? Return the fixes either side.

    The vessel was between these two points and nowhere else. That is the whole
    epistemic claim -- no interpolation, no smoothing, no inference.
    """
    t = datetime.strptime(when, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    before = after = None
    for p in track:
        pt = datetime.strptime(p["t"], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=UTC)
        if pt <= t:
            before = p
        elif after is None:
            after = p
            break
    return before, after


STATUS = {"0": "under way using engine", "1": "at anchor", "2": "not under command",
          "3": "restricted manoeuvrability", "4": "constrained by draught",
          "5": "moored", "8": "under way sailing", "15": "undefined"}


def main():
    case = json.load(open("case.json", encoding="utf-8"))
    track, vessel, port = case["track"], case["vessel"], case["port"]
    ev = case["derived_events"]

    # ---- the four parties -------------------------------------------------
    # The carrier's claim is the injected discrepancy: it asserts the vessel was
    # an arrived ship at 05:30, when the real AIS shows it 17nm out at 12 knots.
    NOR = "2023-01-15T05:30:00Z"
    parties = [
        Party("CARRIER", "Global Ocean Line (synthetic)", {
            "specVersion": "DCSA-JIT-1.2", "eventType": "TRANSPORT",
            "eventClassifierCode": "ACT", "eventTypeCode": "ARRI",
            "transportCallID": "TC-2023-USLAX-0042",
            "vesselIMONumber": vessel["imo"].replace("IMO", ""),
            "UNLocationCode": port["unlocode"], "facilityTypeCode": "BRTH",
            "eventDateTime": NOR,
            "operationalDetails": {"noticeOfReadinessTendered": True,
                                   "norTenderDateTime": NOR,
                                   "vesselStatusAsserted": "arrived ship, awaiting berth"}}),
        Party("PORT_AUTHORITY", "USLAX VTS (synthetic)", {
            "specVersion": "DCSA-JIT-1.2", "eventType": "TRANSPORT",
            "eventClassifierCode": "ACT", "eventTypeCode": "ARRI",
            "transportCallID": "TC-2023-USLAX-0042",
            "vesselIMONumber": vessel["imo"].replace("IMO", ""),
            "UNLocationCode": port["unlocode"], "facilityTypeCode": "ANCH",
            "eventDateTime": ev["port_limit_inbound"]["before"] + "Z",
            "operationalDetails": {"vesselAction": "ENTERED_PORT_LIMITS",
                                   "portLimitNm": port["limit_nm"]}}),
        Party("TERMINAL_OPERATOR", "Delta Marine Terminal (synthetic)", {
            "specVersion": "DCSA-JIT-1.2", "eventType": "OPERATIONS",
            "eventClassifierCode": "ACT", "eventTypeCode": "MOOR",
            "transportCallID": "TC-2023-USLAX-0042",
            "vesselIMONumber": vessel["imo"].replace("IMO", ""),
            "UNLocationCode": port["unlocode"], "facilityTypeCode": "BRTH",
            "eventDateTime": ev["stopped"]["before"] + "Z",
            "operationalDetails": {"vesselAction": "WAY_OFF"}}),
        Party("TELEMETRY", "NOAA/MarineCadastre public AIS (REAL)", {
            "specVersion": "AIS-BULK-1.0",
            "transportCallID": "TC-2023-USLAX-0042",
            "vesselIMONumber": vessel["imo"].replace("IMO", ""),
            "sourceStatus": "REAL -- unmodified public record",
            "fixCount": case["fix_count"],
            "coverage": {"from": case["first_fix"], "to": case["last_fix"]},
            "trackSha256": hashlib.sha256(canonical(track)).hexdigest()}),
    ]

    # ---- commit phase -----------------------------------------------------
    commit_log = [p.commit_record(i + 1) for i, p in enumerate(parties)]
    commit_time = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

    # ---- reveal phase -----------------------------------------------------
    reveals = [p.reveal_record() for p in parties]
    reveal_time = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

    # ---- verification -----------------------------------------------------
    integrity = [verify_commitment(c, r) for c, r in zip(commit_log, reveals)]

    findings, undetermined = [], []
    for rv in reveals:
        if rv["role"] == "TELEMETRY":
            continue
        claimed = rv["payload"]["eventDateTime"]
        b, a = bracket(track, claimed)
        if b is None:
            findings.append({"role": rv["role"], "claimedEventDateTime": claimed,
                             "telemetry": "NO COVERAGE -- claim precedes first AIS fix",
                             "finding": "UNDETERMINED"})
            continue
        limit = port["limit_nm"]
        outside = b["dist_nm"] > limit
        making_way = b["sog"] >= 3.0
        f = {
            "role": rv["role"], "party": rv["party"],
            "claimedEventDateTime": claimed,
            "claimedFacilityTypeCode": rv["payload"].get("facilityTypeCode"),
            "telemetryBracket": {
                "lastFixAtOrBefore": {"t": b["t"] + "Z", "distanceFromPortNm": b["dist_nm"],
                                      "speedOverGroundKt": b["sog"],
                                      "vesselBroadcastStatus": STATUS.get(b["status"], b["status"])},
                "firstFixAfter": ({"t": a["t"] + "Z", "distanceFromPortNm": a["dist_nm"],
                                   "speedOverGroundKt": a["sog"]} if a else None),
                "note": "the vessel was between these two fixes and nowhere else"},
        }
        if outside and making_way:
            f["finding"] = "CONTRADICTED_BY_TELEMETRY"
            f["basis"] = (
                f"at the claimed time the vessel was {b['dist_nm']:.2f} nm from the port "
                f"reference point, outside the stated {limit} nm port limit, making "
                f"{b['sog']:.1f} knots, and its own AIS broadcast status was "
                f"'{STATUS.get(b['status'], b['status'])}'")
        else:
            f["finding"] = "CONSISTENT_WITH_TELEMETRY"
            f["basis"] = (f"vessel {b['dist_nm']:.2f} nm from port reference point at "
                          f"{b['sog']:.1f} knots at the claimed time")
        findings.append(f)

    undetermined = [
        "Whether Notice of Readiness was validly tendered. That turns on whether the "
        "vessel was an 'arrived ship', a contested question of law, not of position.",
        "Whether any laytime or demurrage consequence follows, and in what amount.",
        "Whether any divergence was deliberate. Nothing here speaks to intent.",
        "Commitment ordering relative to any external clock. Phase 1 has no external "
        "witness; commit and reveal occur in one process. See docs/09 Phase 3.",
    ]

    record = {
        "_disclosure": {
            "telemetry": "REAL -- NOAA/MarineCadastre public AIS, unmodified",
            "partyRecords": "SYNTHETIC -- no operational logs were supplied by any "
                            "real organisation. Constructed to exercise the mechanism.",
            "carrierClaim": "SYNTHETIC -- the discrepancy is deliberately injected",
            "implication": "This demonstrates the mechanism against real telemetry. It "
                           "is not evidence that any real party misreported anything.",
        },
        "protocolRun": {"id": "P1-" + secrets.token_hex(4),
                        "committedAt": commit_time, "revealedAt": reveal_time,
                        "externalWitness": None},
        "case": {"vessel": vessel, "port": port,
                 "telemetryProvenance": case["_provenance"],
                 "derivedEvents": ev},
        "commitmentIntegrity": integrity,
        "claimsVersusTelemetry": findings,
        "notDetermined": undetermined,
    }

    with open("discrepancy_record.json", "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2)
    with open("commit_log.json", "w", encoding="utf-8") as f:
        json.dump({"committedAt": commit_time, "entries": commit_log}, f, indent=2)

    # ---- console summary --------------------------------------------------
    print(f"\nvessel: {vessel['name']} ({vessel['imo']})   port: {port['name']}")
    print(f"telemetry: {case['fix_count']} REAL AIS fixes, "
          f"{case['first_fix']} -> {case['last_fix']}\n")
    print("commit phase")
    for c in commit_log:
        print(f"  {c['seq']}. {c['role']:18s} {c['commitment_sha256'][:24]}...")
    print("\nverification")
    for i in integrity:
        ok = "OK  " if (i["commitment_matches_reveal"] and i["signature_valid"]) else "FAIL"
        print(f"  [{ok}] {i['role']:18s} hash={'match' if i['commitment_matches_reveal'] else 'MISMATCH'} "
              f"sig={'valid' if i['signature_valid'] else 'INVALID'}")
    print("\nclaims against telemetry")
    for f in findings:
        print(f"  {f['role']:18s} {f['finding']}")
        if f.get("basis"):
            print(f"       {f['basis']}")
    print("\nnot determined by this record:")
    for u in undetermined:
        print(f"  - {u}")
    print("\nwrote discrepancy_record.json, commit_log.json")


if __name__ == "__main__":
    main()
