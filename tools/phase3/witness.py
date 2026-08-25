"""Phase 3 — the witness layer. No humans, no port, no recruitment.

THE PROBLEM
-----------
Phase 1 bound a party to WHAT it committed. It could not bind WHEN, because commit and
reveal happened in one process. Without a witness, a party simply computes the hash
afterwards and claims it was earlier. That is the backdating the whole project is about.

A witness is NOT a validator. This distinction is the thing:

  VALIDATOR  forms a judgement about evidence. Human or AI. Expensive to recruit,
             expensive to trust, and the thing ValiChord was built around.
  WITNESS    attests that some data existed at some time. Not a judgement at all.
             Free, public, machine-only, and available right now.

You cannot solve witnessing with validators of any kind, because witnessing is not a
judgement task. And crucially: an AI validator you run yourself has no reputation at
stake, so what makes its finding credible to a hostile counterparty is that the INPUTS
were provably pinned before anyone knew the answer. AI validators make the witness more
important, not less.

THE MECHANISM -- a two-sided time sandwich
------------------------------------------
FLOOR ("this was not made earlier")
    drand, the League of Entropy public randomness beacon, publishes an unpredictable
    value every 30 seconds, signed by a threshold of independent organisations. Embed
    the current round in the payload before hashing. Nobody can know round N's
    randomness before round N exists, so any commitment containing it was necessarily
    created after that moment. Backdating becomes impossible, not merely detectable.

CEILING ("this was not made later")
    OpenTimestamps aggregates a digest into the Bitcoin blockchain via independent
    calendar servers. The block timestamp proves the digest existed before that block.

Together the commitment is pinned inside a window by public systems that the committing
party does not control, that require no counterparty, and that do not care where anyone
lives.

HONEST LIMITS
-------------
* The floor is verifiable IMMEDIATELY and independently -- anyone re-fetches that drand
  round from a public API and checks the value matches.
* The ceiling is NOT immediate. At stamp time you hold signed receipts from calendar
  servers -- a promise to include the digest in Bitcoin. Confirmation takes hours. Until
  upgraded, the ceiling rests on the calendars' signatures, which is why this submits to
  three independent operators rather than one.
* drand liveness is assumed. If the beacon is unreachable, there is no floor and the run
  should say so rather than pretend.
"""
import json, subprocess, hashlib

DRAND = "https://api.drand.sh"
CALENDARS = [
    "https://b.pool.opentimestamps.org",
    "https://finney.calendar.eternitywall.com",   # Eternity Wall
    "https://btc.calendar.catallaxy.com",         # Catallaxy
]
UA = "valichord-shipping-phase3"


def _curl(args, timeout=25):
    return subprocess.run(["curl", "-s", "-m", str(timeout), "-A", UA] + args,
                          capture_output=True)


def beacon_floor():
    """Fetch the current drand round. Embed the result in a payload before hashing."""
    r = _curl([f"{DRAND}/public/latest"])
    if r.returncode != 0 or not r.stdout:
        return None
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        return None
    info = _curl([f"{DRAND}/info"])
    chain = json.loads(info.stdout) if info.stdout else {}
    genesis, period = chain.get("genesis_time"), chain.get("period", 30)
    return {
        "source": "drand / League of Entropy",
        "api": DRAND,
        "chainHash": chain.get("hash"),
        "round": d["round"],
        "randomness": d["randomness"],
        "signature": d["signature"],
        "roundUnixTime": (genesis + (d["round"] - 1) * period) if genesis else None,
        "meaning": "this commitment could not have been constructed before this round "
                   "was published, because its randomness was unpredictable until then",
        "verifyBy": f"GET {DRAND}/public/{d['round']} and compare 'randomness'",
    }


def verify_floor(floor):
    """Re-fetch the cited round from the public beacon. Anyone can run this."""
    if not floor:
        return {"checked": False, "reason": "no floor recorded"}
    r = _curl([f"{DRAND}/public/{floor['round']}"])
    if r.returncode != 0 or not r.stdout:
        return {"checked": False, "reason": "beacon unreachable at verification time"}
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"checked": False, "reason": "unparseable beacon response"}
    return {"checked": True, "round": floor["round"],
            "randomnessMatches": d.get("randomness") == floor["randomness"],
            "signatureMatches": d.get("signature") == floor["signature"]}


def anchor(digest_hex):
    """Submit a digest to several independent OpenTimestamps calendars."""
    raw = bytes.fromhex(digest_hex)
    import tempfile, os
    fd, path = tempfile.mkstemp()
    os.write(fd, raw)
    os.close(fd)
    out = []
    try:
        for cal in CALENDARS:
            r = _curl(["-X", "POST", "--data-binary", f"@{path}",
                       "-H", "Accept: application/vnd.opentimestamps.v1",
                       "-w", "\n__HTTP:%{http_code}__", f"{cal}/digest"], timeout=30)
            body = r.stdout.split(b"\n__HTTP:")[0]
            code = (r.stdout.split(b"__HTTP:")[-1].rstrip(b"__\n").decode()
                    if b"__HTTP:" in r.stdout else "?")
            out.append({
                "calendar": cal,
                "accepted": code == "200" and len(body) > 0,
                "httpStatus": code,
                "receiptBytes": len(body),
                "receiptSha256": hashlib.sha256(body).hexdigest() if body else None,
                "receiptHex": body.hex() if body else None,
            })
    finally:
        os.unlink(path)
    return {
        "protocol": "OpenTimestamps",
        "submittedDigest": digest_hex,
        "calendars": out,
        "accepted": sum(1 for c in out if c["accepted"]),
        "meaning": "each accepting calendar has signed a commitment to include this "
                   "digest in Bitcoin. Until a block confirms, the ceiling rests on "
                   "these signatures, which is why several independent operators are "
                   "used rather than one.",
        "bitcoinConfirmed": False,
    }
