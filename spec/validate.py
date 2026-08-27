"""Reference validator for Asset Record Entry v0.1.

    python validate.py <file.json> [<file.json> ...]
    python validate.py --selftest

Files may contain one entry or a JSON array of entries. Given several entries by the
same author for the same asset, the chain is checked as well: sequence contiguity,
prev-hash linkage, and where a gap is found, what is provably missing.

This is the executable half of asset-record-entry-v0.1.md. Where the prose and this
file disagree, that is a bug in both -- fix the prose, then fix this.

Depends only on `cryptography` for Ed25519. No network, no registry: an entry is
verified with nothing but the public key it carries.
"""
import base64
import binascii
import hashlib
import json
import sys

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
        Ed25519PublicKey, Ed25519PrivateKey)
    from cryptography.exceptions import InvalidSignature
except ImportError:
    sys.exit("needs `cryptography` -- pip install cryptography")

FMT = "asset-record/0.1"
REQUIRED = ("fmt", "asset", "author", "seq", "prev", "authored_at", "body", "sig")
OPTIONAL = ("attachments",)


# --- strict JSON loading ----------------------------------------------------
# Two parsers must never disagree about which bytes were signed. Python's json
# silently keeps the LAST of a duplicated key, so a document carrying the same
# key twice can mean different things to different readers -- and only one of
# those meanings was signed. Reject it. (Grok red team against v0.1.)

class DuplicateKey(ValueError):
    pass


def _no_dupes(pairs):
    seen = set()
    for k, _ in pairs:
        if k in seen:
            raise DuplicateKey("duplicate key %r" % k)
        seen.add(k)
    return dict(pairs)


def load_strict(fp):
    """json.load, but a duplicated key is an error rather than last-wins."""
    return json.load(fp, object_pairs_hook=_no_dupes)


def loads_strict(text):
    return json.loads(text, object_pairs_hook=_no_dupes)


# --- base64url without padding, used for keys and signatures ----------------

def b64d(s):
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def b64e(b):
    return base64.urlsafe_b64encode(b).decode().rstrip("=")


# --- canonical form ---------------------------------------------------------

def find_floats(node, path="$"):
    """The format forbids floats, which is what makes canonical JSON deterministic."""
    out = []
    if isinstance(node, float):
        out.append(path)
    elif isinstance(node, dict):
        for k, v in node.items():
            out += find_floats(v, path + "." + str(k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            out += find_floats(v, path + "[" + str(i) + "]")
    return out


def canonical(entry):
    """Canonical bytes: every field but `sig`, keys sorted, no whitespace, UTF-8."""
    body = {k: v for k, v in entry.items() if k != "sig"}
    return json.dumps(body, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def entry_hash(entry):
    return "sha256:" + hashlib.sha256(canonical(entry)).hexdigest()


# --- checks -----------------------------------------------------------------

def check_structure(e):
    errs = []
    for f in REQUIRED:
        if f not in e:
            errs.append("missing required field `%s`" % f)
    for f in e:
        if f not in REQUIRED and f not in OPTIONAL:
            errs.append("unknown field `%s`" % f)
    if errs:
        return errs

    if e["fmt"] != FMT:
        errs.append("fmt is %r, expected %r" % (e["fmt"], FMT))

    a = e["asset"]
    if not isinstance(a, dict) or set(a) != {"scheme", "id"}:
        errs.append("asset must be an object with exactly `scheme` and `id`")
    elif not (isinstance(a["scheme"], str) and isinstance(a["id"], str)):
        errs.append("asset.scheme and asset.id must both be strings")

    if not isinstance(e["seq"], int) or isinstance(e["seq"], bool) or e["seq"] < 1:
        errs.append("seq must be an integer >= 1")

    if e["seq"] == 1:
        if e["prev"] is not None:
            errs.append("prev must be null when seq is 1")
    else:
        if not (isinstance(e["prev"], str) and e["prev"].startswith("sha256:")
                and len(e["prev"]) == 71):
            errs.append("prev must be `sha256:` plus 64 hex chars when seq > 1")

    t = e["authored_at"]
    if not (isinstance(t, str) and len(t) == 20 and t.endswith("Z")
            and t[4] == "-" and t[10] == "T"):
        errs.append("authored_at must be RFC 3339 UTC to the second, e.g. "
                    "2025-01-09T11:04:00Z")

    if not isinstance(e["body"], dict):
        errs.append("body must be an object")

    for i, at in enumerate(e.get("attachments") or []):
        if not isinstance(at, dict) or "hash" not in at:
            errs.append("attachments[%d] needs at least a `hash`" % i)

    try:
        if len(b64d(e["author"])) != 32:
            errs.append("author must be a 32-byte Ed25519 public key")
    except (binascii.Error, ValueError, TypeError):
        errs.append("author is not valid base64url")

    for p in find_floats({k: v for k, v in e.items() if k != "sig"}):
        errs.append("float at %s -- the format forbids floats" % p)

    return errs


def check_signature(e):
    try:
        key = Ed25519PublicKey.from_public_bytes(b64d(e["author"]))
        key.verify(b64d(e["sig"]), canonical(e))
        return []
    except InvalidSignature:
        return ["signature does not verify against `author`"]
    except Exception as exc:
        return ["signature could not be checked: %s" % exc]


def check_chain(entries):
    """Sequence contiguity and prev-hash linkage, per author per asset.

    Reports gaps as findings rather than errors: a holder legitimately may not have
    every entry. The point of the format is that the gap is visible and provable,
    not that it is forbidden.
    """
    errs, findings = [], []
    groups = {}
    for e in entries:
        groups.setdefault((e["author"], e["asset"]["scheme"], e["asset"]["id"]),
                          []).append(e)

    for (author, scheme, aid), group in sorted(groups.items()):
        group.sort(key=lambda x: x["seq"])
        seqs = [x["seq"] for x in group]
        if len(set(seqs)) != len(seqs):
            errs.append("author %s... reuses a seq number for %s:%s"
                        % (author[:8], scheme, aid))
            continue

        by_seq = {x["seq"]: x for x in group}
        missing = [s for s in range(min(seqs), max(seqs) + 1) if s not in by_seq]
        if missing:
            findings.append(
                "author %s... on %s:%s -- holding %d entries, %d MISSING (seq %s). "
                "Their existence is proved by the prev-hash of the following entry."
                % (author[:8], scheme, aid, len(group), len(missing),
                   ", ".join(str(m) for m in missing)))
        if min(seqs) > 1:
            findings.append(
                "author %s... on %s:%s -- chain starts at seq %d, so %d earlier "
                "entries are not held" % (author[:8], scheme, aid, min(seqs),
                                          min(seqs) - 1))

        for e in group:
            want = by_seq.get(e["seq"] - 1)
            if want is None:
                continue
            got = entry_hash(want)
            if e["prev"] != got:
                errs.append("seq %d prev-hash does not match seq %d (chain broken)"
                            % (e["seq"], e["seq"] - 1))
    return errs, findings


# --- runner -----------------------------------------------------------------

def validate(entries):
    errs, findings = [], []
    for i, e in enumerate(entries):
        if not isinstance(e, dict):
            errs.append("entry %d is not an object" % i)
            continue
        label = "seq %s" % e.get("seq", "?")
        for m in check_structure(e):
            errs.append("%s: %s" % (label, m))
        if not check_structure(e):
            for m in check_signature(e):
                errs.append("%s: %s" % (label, m))
    if not errs:
        ce, cf = check_chain(entries)
        errs += ce
        findings += cf
    return errs, findings


def selftest():
    """Build a 3-entry chain, verify it, then drop the middle and prove it shows."""
    priv = Ed25519PrivateKey.generate()
    pub = b64e(priv.public_key().public_bytes_raw())

    chain, prev = [], None
    for n in (1, 2, 3):
        e = {"fmt": FMT, "asset": {"scheme": "imo", "id": "0000000"},
             "author": pub, "seq": n, "prev": prev,
             "authored_at": "2025-01-0%dT11:04:00Z" % n,
             "body": {"job": "TC-CLN", "running_hours": 40000 + n}}
        e["sig"] = b64e(priv.sign(canonical(e)))
        chain.append(e)
        prev = entry_hash(e)

    errs, findings = validate(chain)
    assert not errs, errs
    assert not findings, findings
    print("  intact chain of 3      OK, no findings")

    errs, findings = validate([chain[0], chain[2]])
    assert not errs, errs
    assert any("MISSING (seq 2)" in f for f in findings), findings
    print("  middle entry removed   OK, gap detected and provable")

    tampered = json.loads(json.dumps(chain[2]))
    tampered["body"]["running_hours"] = 999999
    errs, _ = validate([tampered])
    assert any("signature does not verify" in e for e in errs), errs
    print("  body altered           OK, signature refuses it")

    floaty = json.loads(json.dumps(chain[0]))
    floaty["body"]["running_hours"] = 1.5
    errs, _ = validate([floaty])
    assert any("float" in e for e in errs), errs
    print("  float in body          OK, refused")

    try:
        loads_strict('{"a":1,"a":2}')
        raise AssertionError("duplicate key was accepted")
    except DuplicateKey:
        print("  duplicate JSON key     OK, refused")

    scientific = json.loads('{"n":1e5}')["n"]
    assert find_floats(scientific if isinstance(scientific, dict)
                       else {"n": scientific}), "scientific notation slipped through"
    print("  1e5 parsed as float    OK, refused")

    print("\nself-test passed")


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) < 2:
        return sys.exit(__doc__)

    entries = []
    for path in argv[1:]:
        try:
            with open(path, encoding="utf-8") as f:
                doc = load_strict(f)
        except DuplicateKey as exc:
            sys.exit("%s: %s -- refused, because two readers could disagree "
                     "about what was signed" % (path, exc))
        except UnicodeDecodeError:
            sys.exit("%s: not valid UTF-8" % path)
        entries += doc if isinstance(doc, list) else [doc]

    errs, findings = validate(entries)
    print("%d entr%s read" % (len(entries), "y" if len(entries) == 1 else "ies"))
    for f in findings:
        print("  FINDING  " + f)
    for e in errs:
        print("  ERROR    " + e)
    if not errs:
        print("\nvalid" + (" (with findings above)" if findings else ""))
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main(sys.argv)
