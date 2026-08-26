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
    created after that moment.

CEILING ("this was not made later")
    OpenTimestamps aggregates a digest into the Bitcoin blockchain via independent
    calendar servers. The block timestamp proves the digest existed before that block.

CORRECTION, 26 August 2026 -- THE CEILING WAS NOT WHAT THIS FILE CLAIMED
------------------------------------------------------------------------
An earlier version computed the interval as `int(time.time()) - roundUnixTime` and the
record declared the commitment "provably exists somewhere inside this window and nowhere
outside it". That was false. The top of that interval was THIS MACHINE'S OWN CLOCK, which
a backdating party controls. See docs/16 Part 3.

It also assumed the calendar receipts carried signed times. They do not. A calendar
returns a PendingAttestation, whose definition is explicit: "Nothing other than the URI
is recorded." There is no time and no calendar signature in it.

So the ceiling is now handled honestly:

  * Calendar responses are parsed with the real `opentimestamps` library into Timestamp
    objects, merged, and written to a proper `.ots` file that anyone can verify with the
    standard `ots` CLI.
  * `ceiling_state()` reports PENDING until a Bitcoin block confirms. Pending is not a
    ceiling and is no longer described as one.
  * `upgrade()` completes the ceiling later by asking the calendars for the confirmed
    timestamp. When a BitcoinBlockHeaderAttestation appears, there is a real, independent
    upper bound -- a block height -- and only then does an interval exist.

HONEST LIMITS
-------------
* The floor is verifiable IMMEDIATELY and independently -- anyone re-fetches that drand
  round from a public API and checks the value matches. `verify_floor` now asks SEVERAL
  independent relays rather than re-asking the one that supplied it.
* drand's BLS threshold signature is NOT verified here. No BLS library is available in
  this environment, so agreement across independent relays is the substitute. That is
  weaker than signature verification and is reported as such -- see `verify_floor`.
* The ceiling is NOT immediate and is not faked in the meantime. Confirmation takes
  hours. Until then the record says so.
"""
import json
import os
import subprocess
import urllib.request

from opentimestamps.calendar import RemoteCalendar
from opentimestamps.core.notary import (BitcoinBlockHeaderAttestation,
                                        PendingAttestation)
from opentimestamps.core.op import OpSHA256
from opentimestamps.core.serialize import (BytesSerializationContext,
                                           BytesDeserializationContext)
from opentimestamps.core.timestamp import DetachedTimestampFile, Timestamp

DRAND = "https://api.drand.sh"

# Independent relays for the beacon. api/api2/api3 share the drand.sh domain and may
# share an operator; Cloudflare's is a genuinely separate one. Agreement across these
# is weaker evidence than verifying the threshold signature, and is labelled that way.
DRAND_RELAYS = [
    "https://api.drand.sh",
    "https://api2.drand.sh",
    "https://api3.drand.sh",
    "https://drand.cloudflare.com",
]

CALENDARS = [
    "https://b.pool.opentimestamps.org",
    "https://finney.calendar.eternitywall.com",   # Eternity Wall
    "https://btc.calendar.catallaxy.com",         # Catallaxy
]
UA = "valichord-shipping-phase3"


def _get_json(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)


def _curl(args, timeout=25):
    return subprocess.run(["curl", "-s", "-m", str(timeout), "-A", UA] + args,
                          capture_output=True)


# --------------------------------------------------------------------- floor

def beacon_floor():
    """Fetch the current drand round. Embed the result in a payload before hashing."""
    try:
        d = _get_json(f"{DRAND}/public/latest")
        chain = _get_json(f"{DRAND}/info")
    except Exception:
        return None
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
    """Re-fetch the cited round from SEVERAL independent public relays.

    The earlier version re-fetched from the single API that supplied the round and
    string-compared. A compromised or spoofed endpoint would have agreed with itself.
    Asking independent relays does not prove the threshold signature -- that needs a BLS
    library this environment does not have -- but it does mean one bad endpoint no longer
    passes unchallenged. The distinction is recorded in the result rather than glossed.
    """
    if not floor:
        return {"checked": False, "reason": "no floor recorded"}

    relays, agree, disagree, unreachable = [], 0, 0, 0
    for base in DRAND_RELAYS:
        try:
            d = _get_json(f"{base}/public/{floor['round']}")
        except Exception as exc:
            relays.append({"relay": base, "reachable": False,
                           "error": type(exc).__name__})
            unreachable += 1
            continue
        ok = (d.get("randomness") == floor["randomness"]
              and d.get("signature") == floor["signature"])
        relays.append({"relay": base, "reachable": True, "matches": ok})
        agree += 1 if ok else 0
        disagree += 0 if ok else 1

    return {
        "checked": agree + disagree > 0,
        "round": floor["round"],
        "relaysAgreeing": agree,
        "relaysDisagreeing": disagree,
        "relaysUnreachable": unreachable,
        "relays": relays,
        # kept for backward compatibility with existing readers of this record
        "randomnessMatches": agree > 0 and disagree == 0,
        "signatureMatches": agree > 0 and disagree == 0,
        "thresholdSignatureVerified": False,
        "limitation": "drand's BLS threshold signature is NOT verified here -- no BLS "
                      "library is available. Agreement across independent relays is a "
                      "weaker substitute and should not be described as a signature "
                      "check.",
    }


# ------------------------------------------------------------------- ceiling

def anchor(digest_hex, ots_dir=None, label=None):
    """Submit a digest to independent OpenTimestamps calendars.

    Returns a PENDING ceiling. Submitting is not proof of time -- it is a set of
    promises to include the digest in Bitcoin. The real ceiling arrives later, via
    `upgrade()`. This function no longer claims otherwise.
    """
    digest = bytes.fromhex(digest_hex)
    merged = Timestamp(digest)
    per_calendar = []

    for url in CALENDARS:
        entry = {"calendar": url}
        try:
            cal = RemoteCalendar(url, user_agent=UA)
            ts = cal.submit(digest, timeout=30)
            merged.merge(ts)
            uris = [a.uri for a in ts.all_attestations()
                    if isinstance(a, PendingAttestation)]
            entry.update(accepted=True, pendingUris=uris)
        except Exception as exc:
            entry.update(accepted=False, error=f"{type(exc).__name__}: {exc}")
        per_calendar.append(entry)

    ots_path = None
    if ots_dir and label:
        os.makedirs(ots_dir, exist_ok=True)
        ots_path = os.path.join(ots_dir, f"{label}.ots")
        _write_ots(ots_path, digest, merged)

    state = ceiling_state(merged)
    return {
        "protocol": "OpenTimestamps",
        "submittedDigest": digest_hex,
        "calendars": per_calendar,
        "accepted": sum(1 for c in per_calendar if c.get("accepted")),
        "otsFile": os.path.basename(ots_path) if ots_path else None,
        "meaning": "each accepting calendar has undertaken to include this digest in "
                   "Bitcoin. A pending attestation carries a URI and NOTHING ELSE -- no "
                   "time, no calendar signature. It is not yet a ceiling.",
        "verifyBy": (f"ots verify {os.path.basename(ots_path)}" if ots_path else
                     "no .ots written"),
        **state,
    }


def _write_ots(path, digest, timestamp):
    """Write a standard detached .ots file, verifiable with the ordinary `ots` CLI."""
    detached = DetachedTimestampFile(OpSHA256(), timestamp)
    ctx = BytesSerializationContext()
    detached.serialize(ctx)
    with open(path, "wb") as fh:
        fh.write(ctx.getbytes())


def _read_ots(path):
    with open(path, "rb") as fh:
        ctx = BytesDeserializationContext(fh.read())
    return DetachedTimestampFile.deserialize(ctx)


def ceiling_state(timestamp):
    """Is there an actual upper bound yet, or only promises?"""
    blocks = [a.height for a in timestamp.all_attestations()
              if isinstance(a, BitcoinBlockHeaderAttestation)]
    if blocks:
        return {
            "ceilingEstablished": True,
            "bitcoinConfirmed": True,
            "bitcoinBlockHeights": sorted(blocks),
            "ceilingNote": "the digest is committed in the named Bitcoin block, so it "
                           "existed before that block was mined. This is an independent "
                           "upper bound.",
        }
    pending = [a.uri for a in timestamp.all_attestations()
               if isinstance(a, PendingAttestation)]
    return {
        "ceilingEstablished": False,
        "bitcoinConfirmed": False,
        "pendingCalendars": pending,
        "ceilingNote": "PENDING -- no upper bound exists yet. Bitcoin confirmation "
                       "typically takes hours. Run upgrade.py once it has.",
    }


def upgrade(ots_path):
    """Complete the ceiling: ask the calendars for the confirmed timestamp.

    This is the step the earlier implementation never had, and its absence is why the
    ceiling was being faked with a local clock reading.
    """
    detached = _read_ots(ots_path)
    ts = detached.timestamp
    upgraded = False

    for url in CALENDARS:
        try:
            cal = RemoteCalendar(url, user_agent=UA)
            newer = cal.get_timestamp(ts.msg, timeout=30)
            ts.merge(newer)
            upgraded = True
        except Exception:
            continue

    if upgraded:
        _write_ots(ots_path, ts.msg, ts)

    return {"otsFile": os.path.basename(ots_path), "queriedCalendars": len(CALENDARS),
            **ceiling_state(ts)}
