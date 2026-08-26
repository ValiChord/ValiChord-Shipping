"""Phase 3 negative control — including the attack the witness does NOT stop.

Four attacks. Three are refused. One is not, and pretending otherwise would be the
kind of overclaim that gets a project dismissed by the first person who reads it
properly.

  1. Fabricate the beacon value            -> REFUSED (re-fetch from public API)
  2. Omit the beacon entirely              -> REFUSED (no floor, flagged unwitnessed)
  3. Alter the payload after committing    -> REFUSED (hash mismatch)
  4. Embed a deliberately OLD beacon round -> NOT REFUSED

Attack 4 is the honest one. A floor proves "not before". It does not prove "was then".
A party wanting to look old embeds an old round, and the floor happily accepts it.

What exposes attack 4 is not the floor but the WIDTH of the interval between floor and
ceiling. A commitment with a five-minute interval is strong evidence of when it was
made. One with a three-day interval proves almost nothing. So the honest output is the
interval, not a boolean -- and a verifier that reports "witnessed: true" without the
width is misleading.

CORRECTED 26 August 2026
------------------------
Two defects in this file, both found by outside review (docs/16 Part 3):

* Attack 2 called `verify_floor(None)` and hit an early-return guard. It exercised an
  `if` statement, not the pipeline. It now builds a party with no floor and runs the
  same verification phase3.py runs, asserting the party's record comes out NOT OK.

* The attack-4 arithmetic measured floor->NOW using this machine's clock, which is
  exactly the thing an adversary controls. The width that actually exposes a stale
  round is floor->CEILING, and no ceiling exists until Bitcoin confirms. The comparison
  below is therefore labelled as a diagnostic proxy, and the real measurement is
  deferred to upgrade.py rather than faked here.
"""
import hashlib, json, sys, os, time
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "phase1"))
from demo import canonical, Party, verify_commitment    # noqa: E402
from witness import (beacon_floor, verify_floor, anchor,  # noqa: E402
                     _get_json, DRAND)

UTC = timezone.utc
print("PHASE 3 NEGATIVE CONTROL\n")

floor = beacon_floor()
if not floor:
    sys.exit("drand unreachable")
base = {"eventTypeCode": "ARRI", "eventDateTime": "2023-01-15T05:30:00Z",
        "vesselIMONumber": "9138111"}

# ---- 1. fabricate the beacon value --------------------------------------
fake = dict(floor, randomness="de" + "ad" * 31)
p1 = Party("CARRIER", "test", dict(base, _timeFloor=fake))
v1 = verify_floor(p1.payload["_timeFloor"])
print("attack 1  fabricate the beacon randomness")
print(f"          re-fetched round {v1.get('round')}  "
      f"randomnessMatches={v1.get('randomnessMatches')}")
assert v1.get("randomnessMatches") is False, "fabricated beacon not caught"
print("          REFUSED -- the public beacon disagrees\n")

# ---- 2. omit the beacon from ONE party's payload -------------------------
# Runs the pipeline phase3.py runs, rather than poking a guard clause. A party that
# quietly drops its floor while its counterparties keep theirs must come out NOT OK.
p2 = Party("CARRIER", "test", dict(base))          # no _timeFloor
c2, r2 = p2.commit_record(1), p2.reveal_record()
integ2 = verify_commitment(c2, r2)
v2 = verify_floor(r2["payload"].get("_timeFloor"))
# the exact expression phase3.py uses to decide whether a party record is acceptable
party_ok = (integ2["commitment_matches_reveal"] and integ2["signature_valid"]
            and v2.get("randomnessMatches"))
print("attack 2  omit the beacon from one party's payload")
print(f"          hash={integ2['commitment_matches_reveal']} "
      f"sig={integ2['signature_valid']} floorChecked={v2['checked']} "
      f"-> partyRecordOK={bool(party_ok)}")
assert integ2["commitment_matches_reveal"] and integ2["signature_valid"], \
    "the honest parts of the record should still verify"
assert not party_ok, "a party with no floor was accepted by the pipeline"
print("          REFUSED -- hash and signature are fine, but with no floor the party\n"
      "          record fails the pipeline's own acceptance test\n")

# ---- 3. alter the payload after committing -------------------------------
p3 = Party("CARRIER", "test", dict(base, _timeFloor=floor))
c3 = p3.commit_record(1)
r3 = p3.reveal_record()
r3["payload"] = dict(base, _timeFloor=floor, eventDateTime="2023-01-15T13:00:00Z")
v3 = verify_commitment(c3, r3)
print("attack 3  swap the revealed payload after committing")
print(f"          hashMatches={v3['commitment_matches_reveal']}")
assert not v3["commitment_matches_reveal"], "payload substitution not caught"
print("          REFUSED -- hash mismatch\n")

# ---- 4. embed an OLD round to appear older -------------------------------
OLD_ROUNDS_BACK = 2880          # 30s period -> 24 hours earlier
old_round = floor["round"] - OLD_ROUNDS_BACK
try:
    old = _get_json(f"{DRAND}/public/{old_round}")
    chain = _get_json(f"{DRAND}/info")
except Exception:
    old, chain = None, {}
print(f"attack 4  embed a genuine but OLD beacon round ({OLD_ROUNDS_BACK} rounds back)")
if not old:
    print("          could not fetch the historical round; attack untested")
else:
    # read the chain parameters rather than hardcoding them -- a hardcoded genesis
    # silently produces wrong widths on any other drand chain
    genesis, period = chain.get("genesis_time"), chain.get("period", 30)
    old_floor = dict(floor, round=old["round"], randomness=old["randomness"],
                     signature=old["signature"],
                     roundUnixTime=genesis + (old["round"] - 1) * period)
    p4 = Party("CARRIER", "test", dict(base, _timeFloor=old_floor))
    v4 = verify_floor(p4.payload["_timeFloor"])
    print(f"          re-fetched round {v4.get('round')}  "
          f"randomnessMatches={v4.get('randomnessMatches')}")
    print("          NOT REFUSED -- the round is genuine, so the floor verifies")

    # DIAGNOSTIC PROXY, NOT EVIDENCE. The width that exposes a stale round is
    # floor -> CEILING, and the ceiling is a Bitcoin block that has not confirmed yet.
    # Using local time here shows the SHAPE of the exposure; it does not measure it,
    # because our own clock is precisely what an adversary controls. The real
    # measurement is upgrade.py's job.
    now_unix = int(time.time())
    honest_gap = now_unix - floor["roundUnixTime"]
    attack_gap = now_unix - old_floor["roundUnixTime"]
    print()
    print("          what exposes it is the INTERVAL floor->ceiling, not the floor:")
    print(f"            honest commitment : floor age = {honest_gap:>7d} s "
          f"({honest_gap/60:.1f} min)")
    print(f"            backdated attempt : floor age = {attack_gap:>7d} s "
          f"({attack_gap/3600:.1f} h)")
    print(f"          a {attack_gap/3600:.0f}-hour gap establishes almost nothing about "
          f"when the")
    print("          commitment was actually made. Report the width, never a boolean.")
    print()
    print("          NOTE: the two figures above are measured against THIS MACHINE'S")
    print("          clock and are a diagnostic proxy only. The real ceiling is a")
    print("          Bitcoin block. Until upgrade.py confirms one, no interval exists")
    print("          and this attack cannot actually be measured -- only described.")

print("\n" + "-" * 68)
print("THREE ATTACKS REFUSED. ONE NOT, AND NAMED.")
print("The witness proves an INTERVAL, not an instant -- once both ends exist. Today")
print("only the floor does. Its usefulness is entirely a function of how narrow that")
print("interval turns out to be, which depends on anchoring promptly after committing.")
print("Any output that says 'witnessed: true' without the width is misleading, and")
print("docs/13 says so. Any output that computes the width from its own clock is worse,")
print("which is what docs/16 caught.")
