"""Generate spec/example-entry.json from the record-gap case.

    python make_example.py

Emits the three entries that answer the question Gard's surveyor could not: the
contaminated lube oil batch, the lab result against it, and the DG2 cartridge
replacement that cites both. That is the causation trail, in the format.

The signing key is derived from a fixed seed so the output is byte-identical on
every run. It is a demonstration key published in this repository -- it protects
nothing and must never be used for anything real.
"""
import base64
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate import canonical, entry_hash, b64e, validate  # noqa: E402

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

HERE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.join(HERE, "..", "tools", "record-gap", "case.json")
OUT = os.path.join(HERE, "example-entry.json")

SEED = hashlib.sha256(b"asset-record/0.1 example key -- NOT SECRET").digest()
WANTED = ("LO-BNK", "LO-SMP", "TC-REP")


def main():
    with open(CASE, encoding="utf-8") as f:
        case = json.load(f)

    rows = [r for r in case["records"]["truth"]
            if r["job_code"] in WANTED and r["manager"] == "A"]
    rows = [r for r in rows if r["job_code"] != "TC-REP" or r["dg"] == "DG2"]
    rows.sort(key=lambda r: r["seq"])

    priv = Ed25519PrivateKey.from_private_bytes(SEED)
    pub = b64e(priv.public_key().public_bytes_raw())

    out, prev = [], None
    for n, r in enumerate(rows, start=1):
        e = {
            "fmt": "asset-record/0.1",
            "asset": {"scheme": "imo", "id": case["vessel"]["imo"]},
            "author": pub,
            "seq": n,
            "prev": prev,
            "authored_at": r["done_date"] + "T00:00:00Z",
            "body": {
                "component": r["component"],
                "component_name": r["component_name"],
                "job_code": r["job_code"],
                "job_title": r["job_title"],
                "running_hours": r["done_rh"],
                "remarks": r["remarks"],
                "order_no": r["order_no"],
            },
        }
        if r["job_code"] == "LO-SMP":
            e["attachments"] = [{
                "hash": "sha256:" + hashlib.sha256(
                    b"synthetic lab report placeholder").hexdigest(),
                "media_type": "application/pdf",
                "name": "lab-report-LAB-24-3312.pdf",
            }]
        e["sig"] = b64e(priv.sign(canonical(e)))
        out.append(e)
        prev = entry_hash(e)

    errs, findings = validate(out)
    if errs:
        sys.exit("generated an invalid example: " + "; ".join(errs))

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
        f.write("\n")
    print("wrote " + OUT + "  (%d entries, valid, %d findings)"
          % (len(out), len(findings)))


if __name__ == "__main__":
    main()
