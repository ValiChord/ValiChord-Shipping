"""Phase 1 — negative control.

A verifier that always says "OK" is worthless. This proves the mechanism actually
binds, by attempting the fraud it is supposed to prevent: commit to one time, then
reveal a different one.

Three attacks, all of which must fail:
  1. Alter the revealed payload after committing        -> hash mismatch
  2. Alter the payload AND recompute the commitment     -> signature invalid
  3. Alter payload, recompute hash, forge the signature -> signature invalid
"""
import hashlib, json, secrets
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey)
from cryptography.exceptions import InvalidSignature
from demo import canonical, Party, verify_commitment

honest = {"eventTypeCode": "ARRI", "eventDateTime": "2023-01-15T05:30:00Z",
          "vesselIMONumber": "9138111"}
backdated = dict(honest, eventDateTime="2023-01-15T13:00:00Z")

print("PHASE 1 NEGATIVE CONTROL -- the mechanism must refuse these\n")
print(f"honest payload committed : {honest['eventDateTime']}")
print(f"payload later substituted: {backdated['eventDateTime']}\n")

p = Party("CARRIER", "test", honest)
commit = p.commit_record(1)

# --- attack 1: swap the payload at reveal, keep the original commitment
r1 = p.reveal_record(); r1["payload"] = backdated
v1 = verify_commitment(commit, r1)
print(f"attack 1  swap payload only")
print(f"          hash match : {v1['commitment_matches_reveal']}   "
      f"signature valid : {v1['signature_valid']}")
assert not v1["commitment_matches_reveal"], "hash check failed to catch substitution"

# --- attack 2: swap payload AND recompute commitment, reuse the old signature
nonce = bytes.fromhex(p.reveal_record()["nonce_hex"])
forged_commit = dict(commit,
                     commitment_sha256=hashlib.sha256(canonical(backdated) + nonce).hexdigest())
v2 = verify_commitment(forged_commit, r1)
print(f"attack 2  swap payload + recompute hash, reuse signature")
print(f"          hash match : {v2['commitment_matches_reveal']}   "
      f"signature valid : {v2['signature_valid']}")
assert not v2["signature_valid"], "signature check failed to catch forged commitment"

# --- attack 3: as attack 2, but sign with an attacker key while presenting the
#     original party's public key
attacker = Ed25519PrivateKey.generate()
forged2 = dict(forged_commit,
               signature_ed25519=attacker.sign(
                   bytes.fromhex(forged_commit["commitment_sha256"])).hex())
v3 = verify_commitment(forged2, r1)
print(f"attack 3  swap payload + recompute hash + forge signature with another key")
print(f"          hash match : {v3['commitment_matches_reveal']}   "
      f"signature valid : {v3['signature_valid']}")
assert not v3["signature_valid"], "signature check failed to catch key substitution"

# --- control: the honest path still verifies
v0 = verify_commitment(commit, p.reveal_record())
print(f"\ncontrol   untampered")
print(f"          hash match : {v0['commitment_matches_reveal']}   "
      f"signature valid : {v0['signature_valid']}")
assert v0["commitment_matches_reveal"] and v0["signature_valid"]

print("\nALL THREE ATTACKS REFUSED, honest path accepted.")
print("\nNote the limit: this binds a party to WHAT it committed. It does not by")
print("itself prove WHEN, because commit and reveal happen in one process here.")
print("Ordering needs an external witness -- see docs/09 Phase 3.")
