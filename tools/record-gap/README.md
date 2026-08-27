# Record gap — what the missing maintenance records cost

```bash
bash run.sh
```

Opens nothing and downloads nothing. Pure Python, standard library only.

| File | Does |
|---|---|
| `build_case.py` | Builds one vessel's turbocharger history three ways: what was actually done, what the incoming manager received, and what the owner would hold had every entry been copied to them as it was written. Writes `case.json` |
| `analyse.py` | Asks all three records the four questions Gard's surveyor could not answer, mechanically. Writes `gap_report.json` |
| `render.py` | One page. Writes `report.html` (standalone) and `artifact.html` (fragment, for publishing) |
| `example_output/` | A committed run, so the output can be read without running anything |

## The case this is built from

Gard published a claim on **21 July 2026** — *"The risk of taking over a vessel
without its history"*, by Svend Leo Larsen (Senior Claims Adviser) and Kristin
Urdahl (Loss Prevention Specialist). A turbocharger fails on one of three diesel
generators. The other two had recent turbocharger changes. Without running hours,
overhaul history **and the reasons for those changes**, the surveyor could not
determine whether the damage was *"part of a wider issue affecting all three
generators or a separate issue affecting only that turbocharger"*. Some of the
gaps, Gard notes, may date back to previous ownership.

That is the shape reconstructed here. Not the case — the shape.

## What is real and what is not

**Real** — the problem, its age, and that it is unresolved. Gard raised it in a
2010 loss prevention circular. IUMI raised it again in its position paper *Loss of
ship records*, 8 September 2015, and asked IACS — jointly with the London Joint
Hull Committee — to make record retention a condition of classification, calling
non-transfer and destruction of records *"commonplace"*. Cefor's 2018 statistics
record higher claims frequency on vessels that change ownership. SHIPMAN 2024
added Clause 22 on owners' data and Clause 21 giving owners access *via the
manager's platform*. Sixteen years on, Gard is still writing it up.

**Synthetic** — everything else. The vessel, both managers, every date, every
running hour, every one of the 73 entries, and the lube oil batch. Gard published
no data at all: no vessel, no dates, no hours. `IMO 0000000` is deliberately not a
valid IMO number so it cannot collide with a real ship.

**Not claimed** — that co-holding would have changed the outcome of Gard's case.
Nobody outside Gard knows what was in that file. This shows what the *arrangement*
changes, on a record built to the published shape.

Do not remove the `_disclosure` block from either JSON, and do not remove the
"what is real" section from the page. Every number on the page is computed from
`case.json`; nothing is typed in.

## The finding

Of 50 entries written by the outgoing manager, 2 survived the handover — and both
survived only because the owner had paid the invoices, so they arrived stripped of
the remarks field that said *why*.

But the number is not the point, and a reader who takes only the number has missed
it. **The difference is not what you hold. It is whether you can count what you
don't.** A handover pack arrives as a pile of rows, where an absent row and a job
that was never done are indistinguishable. Entries published to the owner as they
are written form a per-author sequence, so an absence has a shape.

## Why this is not ValiChord

ValiChord is blind commit–reveal: it exists so that a claim can be verified. This
is not that, and reaching for it here would be the mistake
[`docs/26`](../../docs/26-handover-find-a-holochain-project.md) was written to
prevent. Nothing here is verified, nobody commits to anything, and there is no
dispute. The problem is **custody** — a record that has to outlive the company
that wrote it, where no neutral custodian is acceptable to anyone. Owners will not
hand a full defect history to class, who also regulate them, and will not put it
in a competitor-adjacent cloud.

The Holochain properties that carry this are the unglamorous ones: entries are
published to peers at write time, each author's chain is append-only and
sequential, and the network boundary can sit on the hull rather than on any
company. Managers join and leave; the record stays. It works with two parties —
owner and manager — so there is no adoption wall to climb first.

## What this does not show, and the honest limits

These are in `gap_report.json` under `not_fixed_by_coholding`, and they are
findings, not disclaimers:

- It cannot recover a reason that was never written down.
- It does not make an entry true. A wrong entry co-held is a wrong entry held by
  two parties. **Custody is not verification.**
- It is forward-only. The first owner to adopt it still inherits a blank history.
- It needs the owner's node to have been online to receive the entry. Solving that
  with an always-on peer quietly reintroduces the operator the design avoided.
- It does not stop a manager keeping a second, private record. It only means the
  entries they did write cannot later be withdrawn.

Two more that belong to the market rather than the mechanism:

- **Nobody will type into two systems.** This has to mirror off the existing PMS —
  AMOS, BASSnet, ShipNet, STAR Suite, NavFleet — not replace it. If it cannot
  ingest automatically it has no users, and no amount of being right about custody
  fixes that.
- **Sixteen years, insurer backing, no movement.** The barrier may be incentive
  rather than technology, in which case this changes nothing. That is the question
  to put to Gard and to IUMI, and it is not answerable from a desk.

- **Someone does sell a version of this.** An earlier draft of this file said
  nobody is paid to prevent the problem, only to remediate it. That was too
  strong. **CoverSense sells a Vessel Passport** — *"the permanent digital
  identity for your boat… stays with the vessel for life"*, entries that *"cannot
  be altered or deleted after verification"*, transferring to the buyer on sale.
  It is recreational rather than commercial, and it is hosted by CoverSense, but
  it is prior art and it is real. See
  [`../../docs/28-prior-art-and-the-general-case.md`](../../docs/28-prior-art-and-the-general-case.md).

## Two rules for anyone editing this

**Report what the record can and cannot establish. Never adjudicate.** No monetary
figures, no confidence scores, no view on whether an insurer should pay. Whether
damage falls within a wear-and-tear exclusion is contested, and this stops well
short of it. Inherited from [`../phase1/README.md`](../phase1/README.md) and it
still applies.

**Keep the negative section.** `not_fixed_by_coholding` is the first thing a
sceptical reader should be able to find. A demo that only shows the win is an
advertisement, and this repository has spent ten candidates learning to tell the
difference.
