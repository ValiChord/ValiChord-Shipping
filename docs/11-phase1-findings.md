# 11 — Phase 1: the mechanism works

**A working commit–reveal–verify pipeline, running against a real vessel's real track,
producing a discrepancy record that reports facts and refuses to adjudicate.**

Code: [`../tools/phase1/`](../tools/phase1/). Sample output:
[`../tools/phase1/example_output/`](../tools/phase1/example_output/).
Built 25 August 2026.

---

## The case

Chosen from the Phase 0 data as the cleanest inbound profile available — its port-limit
crossing is resolved to ±29 seconds.

| | |
|---|---|
| Vessel | **CSL SPIRIT**, IMO 9138111, MMSI 311000368 |
| Port | Los Angeles / Long Beach (USLAX) |
| Date | 15 January 2023 |
| Telemetry | **460 real AIS fixes**, 05:17:01 → 23:57:33 |
| Port limit crossed | between 05:59:33 and 06:00:02 (±29 s) |
| Way off | between 12:49:22 and 12:51:30 (±128 s) |

**Real:** the vessel, the track, every position, speed, timestamp and broadcast status.
Unmodified public NOAA/MarineCadastre AIS.

**Synthetic:** the four parties, their keys, and the carrier's claim. No organisation
supplied operational logs. The discrepancy is deliberately injected.

Every output file carries a `_disclosure` block saying so. It is not decoration — a demo
that implied real carrier data it does not have would end a conversation with an insurer
permanently.

---

## What it does

Four parties — carrier, port authority/VTS, terminal operator, telemetry — each holding a
DCSA-shaped event record.

1. **Commit.** Each computes `SHA-256(canonical_payload ‖ 32-byte nonce)` and signs *the
   commitment* with a real Ed25519 key. Signing the commitment rather than the payload binds
   the party without disclosing what it said.
2. **Reveal.** Payloads and nonces published.
3. **Verify.** Anyone recomputes the hashes and checks the signatures.
4. **Bracket.** Each claimed event time is placed against the real track: the last fix at or
   before, the first fix after. *The vessel was between those two points and nowhere else.*
   No interpolation, no smoothing, no inference.

Canonical serialisation is sorted-key JSON with no whitespace, so the hash is reproducible
by anyone holding the payload.

## The result

```
verification
  [OK] CARRIER            hash=match sig=valid
  [OK] PORT_AUTHORITY     hash=match sig=valid
  [OK] TERMINAL_OPERATOR  hash=match sig=valid
  [OK] TELEMETRY          hash=match sig=valid

claims against telemetry
  CARRIER            CONTRADICTED_BY_TELEMETRY
       at the claimed time the vessel was 17.35 nm from the port reference
       point, outside the stated 12.0 nm port limit, making 12.2 knots, and
       its own AIS broadcast status was 'under way using engine'
  PORT_AUTHORITY     CONSISTENT_WITH_TELEMETRY
  TERMINAL_OPERATOR  CONSISTENT_WITH_TELEMETRY
```

The carrier's synthetic claim asserts an arrived ship at 05:30. The real track puts the
vessel 17.35 nm out at 12.2 knots at that moment, with the vessel's own AIS status field
reading *under way using engine*.

**Three independent contradictions from one real record: position, speed, and the vessel's
own broadcast.** That last one matters — it means the contradiction does not depend solely
on our geofence choice.

## The negative control

A verifier that always returns OK is worthless, so `tamper_test.py` attempts the fraud the
mechanism exists to prevent — commit to one time, reveal another:

| Attack | Result |
|---|---|
| Swap the revealed payload, keep the commitment | **hash mismatch** |
| Swap payload *and* recompute the commitment, reuse the signature | **signature invalid** |
| Swap payload, recompute the hash, forge the signature with another key | **signature invalid** |
| Control: untampered | hash match, signature valid |

All three refused. The honest path accepted.

---

## What this establishes, and what it does not

**Establishes:** a party can be cryptographically bound to *what* it asserted, and that
assertion can be checked against independent physical evidence by anyone, with the
uncertainty stated rather than hidden.

**Does not establish — and the output says all of this in a `notDetermined` block:**

- **Whether NOR was validly tendered.** That turns on whether the vessel was an "arrived
  ship" — a contested question of law, not of position. Per
  [`docs/08`](08-external-evidence-and-the-real-gap.md), reporting a monetary figure here
  would be a liability, not a feature.
- **Whether any laytime or demurrage consequence follows, or in what amount.**
- **Whether any divergence was deliberate.** Nothing here speaks to intent.
- **When anything was committed, relative to any external clock.** This is the real
  limitation and it is structural: commit and reveal both happen inside one process. The
  mechanism binds a party to *what* it said, not yet to *when* it said it. Ordering needs an
  external witness, which is Phase 3.

That last point is worth stating plainly rather than burying. Phase 1 is half the property
the project needs. It is the half that had to work first.

---

## Dependency discipline

[`docs/09`](09-demo-plan.md) opened with a table of what would deliberately not be used. Held
to:

| | |
|---|---|
| `cryptography` (Ed25519) | **Used** — real signatures, not simulated ones |
| Unyt | **Not used** — no money moves |
| Nondominium / hREA | **Not used** — nothing changes custody, nothing is gated |
| ValiChord blind commit-reveal | **Not used** — this is a backdating problem, not an anchoring one |
| Holochain | **Not used in Phase 1** — no external witness needed to prove detection logic |

The whole thing is one dependency and about 300 lines.

---

## Next

**Phase 2 — legibility.** Everything above convinces a developer. The test now is whether
someone who runs a laytime desk understands the output without narration. That means one
page: the timeline, the track, the divergence in minutes, the sealed commitments, and a
visible statement of what is real and what is synthetic.

If it needs explaining, it has failed, and correctness will not rescue it.
