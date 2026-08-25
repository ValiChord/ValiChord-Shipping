# 07 — Unyt, payments, and where a commit-reveal protocol actually fits

Two questions this document answers.

1. What actually fills the payment gap the patent left. **Not HoloFuel** — that is mutual credit
   for hosting, and proposing it for cargo invoices was a category error. **Unyt** is the
   settlement infrastructure, it is already shipping, and its limits are a licensing question
   rather than a technical one.
2. Is ValiChord's blind commit-reveal protocol useful here? **Not for the handover chain the
   patent designed. Well matched to marine cargo damage survey**, which is where the disputes and
   the money actually are.

Checked 25 August 2026.

---

## Part 1 — Unyt answers the payment question

### The distinction the patent missed, and these notes repeated

**HoloFuel is a currency. Unyt is the rails.** The patent conflated them, and an earlier draft of
these notes repeated the conflation by treating HoloFuel's availability as the blocker.

"Payment on delivery" is not a currency problem. It is a conditional-execution problem: *when a
verified delivery attestation exists and the consignee accepts, release funds.* That is an
agreement, and it works with whatever unit the parties choose. HoloFuel's launch date is not on
the critical path.

### What HoloFuel actually is — and why the patent's plan was a category error

Checked against Holo's own currency page, 25 August 2026. Their words, not a paraphrase:

> **"A currency built for hosting, not for holding"**

> "HoloFuel is a **mutual-credit** cryptocurrency architecture designed for the Holo ecosystem…
> **Internal accounting**: A system for pricing, payments, and resource allocation **within the
> hosting network**."

> "HoloFuel will serve as the **internal accounting system** for pricing, payments, and resource
> allocation."

And the disclaimer is unusually direct:

> "Any HOT redemption or conversion services would be provided by appropriately licensed
> third-party entities, not Holo Limited. **Holo Limited is a cloud hosting company and does not
> operate token exchange services.**"

So HoloFuel is mutual credit for settling hosting capacity between hosts and customers. It is not
a general tradable currency; Holo explicitly disclaims operating exchange; and mutual credit does
not behave like a bearer asset — balances are credit and debit positions against a network you
have joined, bounded by credit limits.

**The patent proposed settling international cargo invoices in it.** From the specification:
payment "in the seller's local currency vie atomic swap utilizing the Holochain networks
cryptocurrency Holofuel." That is proposing to pay for a container of goods with the unit designed
for buying server time. It was a category error in 2020, it remains one, and no launch date fixes
it.

Note also that Holo currently accepts **HOT and national currencies (USD, EUR)** for hosting,
pending HoloFuel's implementation. Holo does not yet settle Holo in HoloFuel.

*(This correction originated with Ceri John, who queried the "HoloFuel is a currency" framing on
the grounds that it looked like a hosting unit rather than a tradable one. It was checked against
the primary source and he was right.)*

### What Unyt is

A peer-to-peer payments and accounting system on Holochain. Self-custodial, no mandatory fees,
participant-defined currencies, EVM bridging. From their own description: *"Create currencies,
automate payments, and connect networks — without middlemen, platform lock-in, or mandatory
fees."*

Stated use cases include escrow, billing, revenue sharing, proof-of-service billing for
infrastructure networks, and **"atomic multi-currency trades — no trading pairs, liquidity pools,
or crypto exchanges needed."**

Set that last item beside the patent's own sentence:

> "payment of the goods is made immediately in the seller's local currency vie atomic swap"

Unyt's feature list is a closer match to Holo Sail's stated requirement than Holo Sail's own
architecture was.

### What Unyt can and cannot settle

**Can — units of the network's choosing.** From the Currency Design documentation:

> "**Unit of account:** What does your currency represent? Hours, energy, favors, **dollars**?"
> "**Issuance:** Mutual credit, admin-issued, earned-only, **backed by locked assets**, etc"

Each deployment — a "Unyt Alliance" — defines its own currencies, rules and governance. Unyt is
**not** locked to HoloFuel; HoloFuel is one unit among many, and Holo's hosting settlement is built
*on* Unyt rather than the reverse.

**Can — bridged EVM assets.** Bridging is implemented, not aspirational: a two-way HOT ↔
bridged-HOT bridge using a Raindex orderbook vault, with Solidity contracts, a Rust orchestrator,
and lock/claim flows.

**Cannot — fiat.** The full Unyt documentation was searched on 25 August 2026:

| Term | Occurrences |
|---|---|
| `fiat` | 0 |
| `USD` | 0 |
| `stablecoin` | 0 |
| `USDC` | 0 |

The only appearance of "dollars" is the rhetorical line above about what a unit may *represent*.

**This distinction is load-bearing: denominating a unit in dollars is not moving dollars.** Unyt
supplies accounting, agreements, and atomic multi-currency trades. It does not supply a bank
connection.

### The real barrier is a licence, not a technology

For the patent's actual promise — *immediate payment in the seller's local currency upon
delivery* — moving real money across borders requires a licensed money transmitter or payment
institution at the boundary. That is a regulated business, not a missing feature.

Holo's disclaimer is them identifying this exact line and declining to cross it: they are "a cloud
hosting company" and do "not operate token exchange services."

**Nothing in Holochain, Unyt, Nondominium or ValiChord addresses this, and nothing was ever going
to.** Holo Sail bolted settlement to provenance because HoloFuel made it sound like a solved
problem. It was not.

### The primitive: RAVE

From the Smart Agreement Code Library:

> "A **Smart Agreement** is a recorded agreement, verifiably executed… an executor runs the
> agreement's code against the inputs each party has parked, and every peer re-runs it to validate
> the result. The record of one execution is a **RAVE** — a Record of Agreement Verifiably
> Executed."

Agreements are written in Rhai with JSON Schemas for inputs, output, and the creation form.

### Relevant templates already exist

The library ships these, among others:

| Template | Relevance |
|---|---|
| `lockbox` | Escrow — funds held pending a condition |
| `conditional_forward` | Conditional payment release |
| `aggregate_payment` / `aggregate_requests` | Batching, for many small handover events |
| `_lane_proof_of_service` | Proof-of-service billing |
| `_lane_proof_of_service_rideshare` | **Proof of service for a movement of something from A to B** — the nearest existing analogue to proof of custody transfer |
| `test_verify_signatures` | Signature verification inside an agreement |

"Payment on delivery" is `lockbox` plus `conditional_forward`, with a delivery attestation as the
parked input. That is not speculative engineering; it is composition of existing templates.

### Maturity

- 11 releases since September 2025; latest milestone *Blockchain Bridging v0.54.0*, February 2026.
- Repositories across the org pushed within the last week, including `unytctl`, `heart`,
  `migration-service`, `watchtower`, `pricing_oracle`, `raindex-orders`.
- Holo's own hosting settlement is being built on it.

### The architectural precedent already exists

ValiChord's Nondominium notes record that their Unyt governance rule **does not trust a locally
written tag — it queries the Unyt DHT cross-DNA and validates the real RAVE.**

So the pattern *"an externally verified record triggers a state change"* is already implemented in
this ecosystem, with Unyt as the verified party. "Verified delivery releases payment" is that
pattern with different nouns.

### What this does and does not correct

Checked before asserting: **the earlier documents in this repository did not make the error.**
[`docs/01`](01-patent-record.md) says of the patent that "the payment mechanism is given as
'atomic swap utilizing the Holochain networks cryptocurrency Holofuel,' with no design for it."
That remains exactly right, and nothing here supersedes it.

The error was made in conversation, not in these notes: treating HoloFuel's launch status as the
blocker, and describing the payment mechanism as a missing keystone. It is recorded here because
it shaped an earlier recommendation, not because a document needs amending.

**The distinction that matters:** the gap Holo Sail left was a *design* gap, not an *availability*
gap. They wrote one sentence where a mechanism was needed. Six years on, the mechanism is
available off the shelf — and it is not the currency they named.

---

## Part 2 — Where blind commit-reveal fits

ValiChord's protocol solves one specific problem: **correlated judgement among independent
assessors.** Each assessor commits a hash of their verdict before seeing any other; then all
reveal. Nobody can anchor on anybody. The record preserves genuine agreement *and* genuine
disagreement rather than manufactured consensus.

The question is whether that problem occurs in this domain.

### Where it does not — the handover chain

A custody transfer is **bilateral**. One party hands over, one receives, their interests are
opposed, and both sign. What that needs is non-repudiation: a signed, timestamped, tamper-evident
receipt binding both parties.

There are no independent assessors at a terminal gate and nothing to herd toward. Commit-reveal
would be ceremony.

**For the seven `TransferCustody` events in the patent's process narrative, plain attestation is
the right tool.** The protocol adds nothing.

### Where it might — marine cargo damage survey

When cargo arrives damaged, the cargo insurer appoints a surveyor and the carrier or its P&I club
appoints another. They assess cause, extent, apportionment and quantum. These assessments are
**sequential and partisan**: whoever reports first frames the dispute, and the second is written
in knowledge of the first.

That is the correlated-judgement problem, with money attached.

The same structure appears in:

- **Equipment interchange disputes** — who caused damage between gate-out and gate-in
- **Reefer temperature-excursion adjudication** — was the consignment compromised
- **Draft survey quantity disputes** in bulk cargo

**Convergence worth noting:** [`docs/04`](04-strategic-assessment.md) identified cargo insurers as
the most plausible buyer by a completely different route — disputed liability at handover as a
direct cost centre. Two independent lines of reasoning arriving at the same counterparty is
stronger evidence than either alone.

### Red team

**The adversarial structure may be a feature.** Each side appoints its own surveyor partly
*because* they want an expert who understands their position. "Independence through blindness"
competes with "independence through opposition," and some parties want leverage rather than a
neutral finding. This is the serious objection, and it is commercial-cultural rather than
technical.

**Joint surveys already exist** as the instrument when both sides want a shared finding. This
would compete with an incumbent mechanism, not fill a void.

**It is a licensed, institutional profession** — Lloyd's agents, IIMS, salvage associations,
centuries of settled practice. Changing professional practice is slow.

**A survey finding is not a scalar.** ValiChord commits a verdict. A surveyor produces a report
with photographs, measurements and narrative. *What exactly gets committed* — a conclusion, a hash
of the full report, an apportionment percentage — is a genuine design question, not a detail.

**Volume is modest.** Damage claims are a minority of shipments.

### Epistemic status — weak, and deliberately flagged

Everything in Part 2's marine-survey argument is reasoned from general knowledge of claims
practice. **No primary source, and nobody who works marine claims, has been consulted.** It should
be held as a hypothesis worth one conversation, not as a finding. The specific question to put to
a practitioner is in the open questions below.

---

## Part 3 — Direction, and why the "extra" may be the wedge

### The direction

Set by Ceri John, 25 August 2026, in response to the assessment above:

> "I'd still like to go for the global supply chain ambition of the original Holo Sail, but with
> the nice added extra of the marine cargo damage app."

Recorded plainly because it differs from what [`docs/04`](04-strategic-assessment.md) recommends.
That document argues against the platform play and for a narrow start; the project direction is
the broader ambition with the survey application included. Both are on the record so the
reasoning stays legible either way.

### Why the survey application may be more than an extra

Working through the implications, there is a case that the cargo damage application is not a side
component but **the mechanism by which the global ambition becomes reachable.** Three reasons.

**1. It requires a slice of the handover chain anyway.** A damage survey is meaningless without
provenance: what was handed over, when, by whom, in what condition. Building the survey
application forces you to build custody attestation for the legs in question. The "extra" and the
"ambition" share a foundation.

**2. Insurers and surveyors touch every party in the chain.** Carriers, terminals, forwarders,
consignees — a claims process already reaches all of them. That is a distribution channel the
platform play never had. TradeLens had to persuade twelve counterparty classes to join something;
a claim already summons them.

**3. It supplies the adoption incentive that was always missing — and this is the important
one.**

TradeLens died because carriers would not publish operational data into a rival's platform. There
was no reason to contribute. Holo Sail's CEO diagnosed exactly this in gCaptain in January 2021
(see [`docs/04`](04-strategic-assessment.md)).

But a claim inverts the incentive. **In a dispute, every party wants evidence that exonerates
them.** A terminal operator who can prove the container left their gate undamaged has a direct,
self-interested reason to publish a signed handover attestation — not cooperation, not altruism,
not a platform strategy. Self-defence.

That is the first mechanism in this whole record that makes parties *want* to contribute to a
shared evidence layer. It does not require them to trust each other, join a consortium, or accept
a rival's infrastructure. It requires only that they prefer not to be blamed.

If that holds, the sequencing writes itself: **the claims application is not downstream of the
supply chain platform — it is the reason anyone would populate one.**

*(Inference, clearly labelled. It rests on the marine-survey reading in Part 2, which is
unverified. If practitioners are content with adversarial appointment, this argument does not
start.)*

### What this implies for build order

Retaining the full ambition, the order the above suggests:

1. **Custody attestation for one lane.** Signed, non-repudiable handover receipts. hREA
   `TransferCustody` vocabulary; no Designate hardware; verifiable by a non-participant.
2. **Blind survey on top.** ValiChord's commit-reveal where multiple assessors are genuinely
   involved — used on merit, not imported wholesale.
3. **Settlement via Unyt.** `lockbox` + `conditional_forward` for surveyor fees first, claim
   settlement much later or never.

   This was originally proposed on stakes — start small. The fiat finding above gives a second
   and better reason: **start where you do not need a licence.** Surveyor fees are modest, between
   a handful of known parties, and can run as a mutual-credit or dollar-denominated unit inside an
   alliance — or simply be invoiced conventionally, with Unyt holding the verifiable record rather
   than moving the money. Claim settlement is large, cross-border and regulated. Do not design for
   it early, and treat "we settle claims" as a thing to earn, not to promise.
4. **Standards surface.** ISO 28005, UN/EDIFACT, IALA S-211, IPCSA — from
   [`docs/02`](02-company-record.md). This is what makes any of it legible to a port, and matters
   more than any Holochain version question.
5. **Widen from the claims footprint** into the general supply chain as parties who joined to
   defend themselves stay for the visibility.

Steps 1–3 need one insurer and a panel of surveyors, not an industry.

### Decouple the evidence layer from the payment layer

A structural consequence of the fiat finding, and arguably the most useful thing in this document.

**The verifiable part needs no licence.** Who held what, when, in what condition, and what
independent assessors concluded — none of that touches regulated money movement. It can be built,
shipped and sold without becoming a financial institution.

**The money can settle however the parties already settle it.** Letters of credit, open account,
existing claims processes. The evidence layer produces a record those processes consume; it does
not have to move the funds.

Holo Sail welded settlement onto provenance because HoloFuel made settlement sound like a solved
problem. It was not, and the welding added the one component that requires a licence to operate.
**Separating them removes the project's only regulatory dependency** — and loses nothing, because
provenance was always the part with no substitute.

---

## Open questions

The load-bearing ones, in order of how much they decide:

1. **Is surveyor independence a live grievance in marine claims, or is adversarial appointment
   considered to work?** Everything in Parts 2 and 3 rests on this. One conversation with a claims
   practitioner settles it.
2. **What would a surveyor commit to?** The verdict shape has to be defined before the protocol
   can be applied.
3. **Do insurers currently pay for provenance, or only for adjustment?** Is there an existing
   budget line, or would this be a new one?
4. **Would a terminal operator publish an exonerating attestation?** The self-defence incentive in
   Part 3 is inferred, not observed.
5. **What survived TradeLens?** Its participants and integrations went somewhere.

---

**Sources**

- [holo.host/currency](https://holo.host/currency/) — read 25 Aug 2026; local copy at
  [`../sources/ecosystem/2026-08-25-holo-host-currency-page.txt`](../sources/ecosystem/2026-08-25-holo-host-currency-page.txt)
- [unyt.co/docs](https://unyt.co/docs/) — read 25 Aug 2026; local copy at
  [`../sources/ecosystem/2026-08-25-unyt-documentation.txt`](../sources/ecosystem/2026-08-25-unyt-documentation.txt)
- [unyt.co](https://unyt.co/) — read 25 Aug 2026; local copy at
  [`../sources/ecosystem/2026-08-25-unyt-homepage.txt`](../sources/ecosystem/2026-08-25-unyt-homepage.txt)
- [unytco/raindex-orders](https://github.com/unytco/raindex-orders) — the implemented HOT bridge
- [unytco/smart_agreement_library](https://github.com/unytco/smart_agreement_library) — README and template listing
- [unytco GitHub organisation](https://github.com/unytco) — repository activity
- [HOT to HoloFuel Technical Migration Test — Holo](https://holo.host/blog/hot-to-holofuel-technical-migration-test-ha2gtr4RkYV/)
- Local: `ValiChord/nondominium_integration/NONDOMINIUM_ARCHITECTURE.md` (Unyt RAVE verification pattern)
- Local: [`../sources/website/2021-01-22-gcaptain-is-blockchains-role-overhyped.txt`](../sources/website/2021-01-22-gcaptain-is-blockchains-role-overhyped.txt)

**Note on the HoloFuel timeline.** A launch date of 1 November 2026 at the latest has been
reported to this project; it could not be independently confirmed here. What is public is a Holo
blog post of 3 July 2026 announcing a 30 July livestream at which the official migration date
would be revealed.

The date matters less than it appears, and for a stronger reason than "the rails already exist."
HoloFuel is mutual credit for hosting. Even fully launched on schedule, it would not be the
instrument for settling cargo invoices — so its timeline is not a dependency of this project in
either direction. It is not dismissed: a hosting-backed mutual-credit unit may yet be useful for
something here, most plausibly for paying network participants rather than for trade settlement.
But it is not the answer to "payment on delivery," and the patent was wrong to treat it as one.
