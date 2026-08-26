# 19 — Handover brief

**For any session picking this up, including the one that wrote `docs/14` and `docs/15`.**
Read this before writing anything. It is short on purpose.

Written 26 August 2026, after the review in [`docs/16`](16-external-review.md) and the work
in [`docs/17`](17-phase0b-case-candidates.md) and [`docs/18`](18-outreach-and-funding.md).

---

## The one instruction that was missing

The standing brief was to avoid recruiting people at this stage and to be creative about
routing around them. **That was a good instruction and it worked** — Phases 0 to 3 exist
because of it, and `docs/13` is the best document in the repository.

It had no expiry condition, so nothing stopped when it should have. `docs/13` reached the
point where the answer was human and said so in its closing line. `docs/14` said it again
in its recommendation. `docs/15` then designed four DNAs instead.

**So: this brief carries the stopping condition that was missing.**

> Routing around people has stopped being the right move. The next useful action is an
> email, not an architecture. If you find yourself designing rather than building or
> writing to someone, say so out loud and stop.

A related pattern worth holding: *"find a way around X"* will essentially never return
*"there is no way around X."* It always finds something, long after the constraint has
stopped binding.

---

## Four corrections to carry forward

**1. `verify_signature` IS available in integrity zomes, and it is callable inside
`validate`.** Settled since: Holochain's `ValidateHostAccess` sets
`keystore_deterministic: Permission::Allow`, which is exactly the permission the host
function requires. ValiChord's `attestation_integrity` carries a comment asserting the
opposite and has built around it, putting the real Ed25519 check in the coordinator's
`init()`. That is a bug **in ValiChord**, not here. It arrived in `73c3e9b` (11 Mar 2026),
five months before the 0.7 merge — so it is not upgrade staleness, it was false when
written. `docs/15`'s credential mechanism is sound.

**2. ValiChord's commit-reveal is coordinator code — but the fix is a schema change, not a
code move.** `docs/14`'s "reuse of a tested pattern" is unfounded for the part that
matters: the hash check is not enforced by validators and has a dev bypass. **The obstacle
is not the missing `sha2` dependency**, which is trivial — it is that **the nonce is never
published**, so no peer can recompute the hash. Publishing it at reveal is harmless but
changes the entry schema. `docs/16` Finding 1 originally implied otherwise and is corrected
there.

**2b. The credential layer is coordinator-enforced throughout — the membrane is not an
outlier.** `certification_tier` is not checked in the integrity zome either, and the
live-`StudyClaim` guard is coordinator-side. The right question is not "fix the membrane"
but *"what do we say is validated, versus what a peer actually checks?"*

**3. Per-voyage clones destroy the deterrent.** Each clone gives every party a fresh source
chain. `docs/13`'s contagion argument — a carrier caught once has its whole book reopened —
needs a persistent network where the same key writes voyage after voyage. This is the
deepest problem with `docs/15` and it is an argument between two documents in this
repository, not an outside objection.

**4. Two claims in `docs/16` were themselves wrong** and are corrected in place. Both came
from asserting before checking. The review's own Part 1 diagnosis applied to the reviewer.

---

## What is true about the code as of today

| | |
|---|---|
| Phase 0 | Real NOAA AIS. Re-run during review; reproduces every published figure exactly |
| Phase 1 | Real Ed25519, persistent keys, four-assertion tamper test. **Circularity fixed** — claim times are literals in `CLAIM_TIMES`, and the verifier derives what a claim implies from its DCSA codes |
| Phase 2 | Renders every assertion tested against its verdict. `example_output/report.html` is now actually committed; `*.html` had been excluding it |
| Phase 3 | **The ceiling was this machine's clock and is now honest.** Real `.ots` files, `upgrade.py` completes the ceiling once Bitcoin confirms, and the record says NO INTERVAL YET until it does |
| Phase 0b | Case-mining tools and 43 scored candidates. **No case has been run against AIS yet** |
| Holochain | **None. No Rust anywhere in this repo, and none in its history** |

---

## What to do next, and what not to

**Do, in this order:**

1. Run the Tricon case — [`docs/17`](17-phase0b-case-candidates.md) step 2. One 301 MB
   download and the existing Phase 0 code.
2. Send two emails from [`../outreach/draft-emails.md`](../outreach/draft-emails.md). Two,
   not ten. Then wait.
3. Only after someone has replied: build **one** persistent DNA with two agents — claimant
   and counterparty — per [`docs/16`](16-external-review.md) Part 8 item 8.

**Do not:**

- Design more DNAs. `docs/15` is parked with seven findings recorded against it; adding an
  eighth document of architecture is the failure mode this brief exists to prevent.
- Write another analysis document. Including a rebuttal of this one — if something here is
  wrong, fix the thing and say so in a commit message.
- Add Unyt, Nondominium or hREA. [`docs/09`](09-demo-plan.md)'s exclusion table still
  holds for all three.
- Report a phase as verified because the prose says so. Check the code. Two of this
  repository's own claims did not survive that check, and one of the review's did not
  either.

---

## The question that has not moved

Unanswered since [`docs/04`](04-strategic-assessment.md): **whether anyone will pay.**

Five phases of engineering have not moved it a millimetre and no further engineering will.
The demonstrator exists so the question can be asked while holding something that runs.
That was the stated purpose from the start, and it has now been met twice over.

Ask it.
