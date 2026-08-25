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
"""
import hashlib, json, sys, os, time
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "phase1"))
from demo import canonical, Party, verify_commitment    # noqa: E402
from witness import beacon_floor, verify_floor, anchor, _curl, DRAND  # noqa: E402

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

# ---- 2. omit the beacon --------------------------------------------------
p2 = Party("CARRIER", "test", dict(base))
v2 = verify_floor(p2.payload.get("_timeFloor"))
print("attack 2  omit the beacon entirely")
print(f"          checked={v2['checked']}  reason={v2.get('reason')}")
assert v2["checked"] is False, "missing beacon not flagged"
print("          REFUSED -- no floor, record is unwitnessed and must say so\n")

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
r = _curl([f"{DRAND}/public/{old_round}"])
old = json.loads(r.stdout) if r.stdout else None
print(f"attack 4  embed a genuine but OLD beacon round ({OLD_ROUNDS_BACK} rounds back)")
if not old:
    print("          could not fetch the historical round; attack untested")
else:
    period, genesis = 30, 1595431050
    old_floor = dict(floor, round=old["round"], randomness=old["randomness"],
                     signature=old["signature"],
                     roundUnixTime=genesis + (old["round"] - 1) * period)
    p4 = Party("CARRIER", "test", dict(base, _timeFloor=old_floor))
    v4 = verify_floor(p4.payload["_timeFloor"])
    print(f"          re-fetched round {v4.get('round')}  "
          f"randomnessMatches={v4.get('randomnessMatches')}")
    print("          NOT REFUSED -- the round is genuine, so the floor verifies")

    now_unix = int(time.time())
    honest_width = now_unix - floor["roundUnixTime"]
    attack_width = now_unix - old_floor["roundUnixTime"]
    print()
    print("          what exposes it is the INTERVAL, not the floor:")
    print(f"            honest commitment : floor->now = {honest_width:>7d} s "
          f"({honest_width/60:.1f} min)")
    print(f"            backdated attempt : floor->now = {attack_width:>7d} s "
          f"({attack_width/3600:.1f} h)")
    print(f"          a {attack_width/3600:.0f}-hour interval establishes almost nothing "
          f"about when the")
    print("          commitment was actually made. Report the width, never a boolean.")

print("\n" + "-" * 68)
print("THREE ATTACKS REFUSED. ONE NOT, AND NAMED.")
print("The witness proves an INTERVAL, not an instant. Its usefulness is entirely a")
print("function of how narrow that interval is, which depends on anchoring promptly")
print("after committing. Any output that says 'witnessed: true' without the width is")
print("misleading, and docs/13 says so.")
