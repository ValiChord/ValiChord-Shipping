# 06 — Would this run on Nondominium?

**Question:** Bob Haugen's 2021 assessment (see [`03-community-response.md`](03-community-response.md))
was that hREA could already do everything Holo Sail's patent described. Nondominium is built on
hREA. So: is a revived version of this design compatible with Nondominium?

**Short answer: yes, and more cleanly than expected. But compatibility is not the binding
constraint, and finding that out does not lower the barrier — it relocates it.**

---

## How this was checked

Two sources, deliberately kept apart.

**Nondominium's structure** was read from ValiChord's own architecture notes at
`nondominium_integration/NONDOMINIUM_ARCHITECTURE.md`, which record repeated re-verification
against Sensorica's repository (most recently against the `dev` trunk, August 2026). These are
*our reading of their code*, not their documentation, and they carry their own corrections where
earlier readings were wrong. Treat specifics as accurate-as-of-last-recon and re-check before
building.

**hREA's upstream health** was checked directly against the repository and API on 25 August 2026,
because a claim about dependency risk should not rest on recollection.

Where something is inference rather than observation, it is labelled.

---

## Where it fits

### Haugen's claim is now structural, not aspirational

In 2021 he was arguing that hREA *could* model this. Nondominium's v1.0 commits to dual-DNA hREA
delegation (ADR-006) — hREA is **vendored as a DNA**, supplying the ValueFlows core types. The
claim is no longer an outside opinion about an adjacent project. It is inside the codebase.

### The handover primitive already exists

Nondominium extends the standard ValueFlows action set with three actions, one of which is
**`TransferCustody`**.

Every step in the Holo Sail specification is one of these:

| Patent step | Nondominium event |
|---|---|
| Factory → truck | `TransferCustody` |
| Truck → terminal operator | `TransferCustody` |
| Terminal → vessel | `TransferCustody` |
| Vessel → destination dock | `TransferCustody` |
| Dock → destination truck | `TransferCustody` |
| Truck → consignee | `TransferCustody` |
| Payment on acceptance | `Transfer` |

This is not an analogy. Custody transfer of a physical resource between agents is the same
operation whether the resource is a shared workshop tool or a forty-foot container.

### The obvious objection does not bite

*Nondominium* means not-owned; a container is very much owned. This looked fatal and is not.
`PropertyRegime` has four variants — `Private`, `Commons`, `Nondominium`, `CommonPool` — and
`ResourceNature` includes `Physical`. A privately-owned steel box is representable in the model
as it stands, with no change to their integrity zome.

### The contribution accounting already speaks freight

This is the strongest single point and it was not expected.

The Participation Receipt system generates cryptographically-signed
`PrivateParticipationClaim` entries automatically whenever `log_economic_event()` is called.
`ParticipationClaimType` has 16+ variants covering, among others, **custody transfer, storage,
and transport**. Each claim can carry a `PerformanceMetrics` struct recording **timeliness,
quality, reliability, communication, and overall satisfaction**.

That is carrier performance measurement, signed per event, already in the vocabulary. It is also
a direct hit on the one commercial question [`04-strategic-assessment.md`](04-strategic-assessment.md)
identifies as worth testing: disputed liability at handover, which is a cargo insurer's cost
centre.

### External verification is a house pattern, not a special case

The capability-slot design is two-tier, with two worked external integrations already serving as
templates — Unyt and Flowsta. Unyt's rule does the hard part correctly: it does not trust the
slot tag written by the interested party, it queries the other DHT and verifies the real record.

ValiChord is already lined up as the third instance of that pattern. A maritime attestation would
be a fourth of the same shape — not a new architecture.

### hREA claims this use case in its own words

hREA describes itself as affording "most functionality commonly used in supply chain systems,
project management software, logistics management and enterprise resource planning," and says
that from hREA data you can "do tracking and tracing through a supply chain."

And `pospi` — the developer Haugen name-checked in the 2021 thread for having run
"experiments somewhat like that for BeefLedger" — is hREA's dominant contributor. BeefLedger is
agricultural supply-chain provenance. The nearest existing precedent to this idea sits inside the
same project.

---

## Where it strains

### The enforcement machinery is not built

ValiChord's July 2026 recon found governance-as-operator — the rule-enforcement layer — still
unimplemented on Nondominium's side (their issues #41–#44), and re-verified that finding in
August 2026. **No gate rule of any kind can be enforced yet.**

For an evidence layer this may not matter: a signed, verifiable record of a handover has value
even when nothing automatically gates on it. For anything that must *block* a transition on a
failed attestation, it is a hard blocker until they build it.

### The model would be used without its purpose

Nondominium exists for capture-resistant governance of resources held in common. `Private` is
supported, but the surrounding apparatus — roles, validation, capture-resistance — is designed
around commons stewardship. Modelling Maersk's container in it works structurally and means
nothing philosophically. *(Inference: this is a mismatch of intent rather than of code. It costs
nothing technically and may cost something in the relationship, since it borrows a commons
project's machinery for straightforwardly commercial cargo.)*

### It would be the third thing before the second is finished

ValiChord's own integration notes open with: *"Pre-implementation. Design decisions open. No
integration code written yet."* A maritime use case stacked on top would be a third project
depending on a second that does not yet exist.

### Dependency concentration — real, but smaller than it looks

Checked rather than assumed, 25 August 2026:

| | |
|---|---|
| Repository | `h-REA/hREA` — active, not archived |
| Default branch (`sprout`) last commit | **24 June 2025** — quiet for ~14 months |
| Latest release | **`happ-0.4.0-beta`, 27 July 2026** — one month old |
| Contributor spread | pospi 2,301 commits; next contributor 213 |

The quiet default branch looks alarming in isolation and is misleading: work has moved to
branches and releases are still shipping. The bus factor is real — one contributor dominates by
an order of magnitude — but this is not a dead dependency.

**A separate and unverified claim:** project notes record that the hREA dependency *within
Sensorica's stack* is carried by one person (Sacha). That is a different proposition from
upstream health and has not been confirmed here. It should be checked with Sensorica directly
rather than assumed from these notes.

### The adoption problem is untouched

Making the design hREA-shaped does not make twelve classes of commercial counterparty join it.
Nothing in this document addresses the wall described in
[`04-strategic-assessment.md`](04-strategic-assessment.md).

---

## What the compatibility actually buys

If the technical path is largely off-the-shelf, then **the build was never the risk.**

Establishing compatibility does not lower the barrier. It relocates all remaining risk onto the
single question already identified: *will a cargo insurer or port authority pay for verified
handover attestations?*

That is good news rather than bad. It means the question can be tested with conversations before
any maritime code is written, and that if the answer is yes, the distance from yes to working is
unusually short.

**The strongest argument in favour**, stated fairly: a Nondominium-shaped layer is neutral and
non-owned by construction. That is precisely the property TradeLens lacked and died for want of —
carriers would not publish operational data into a rival's platform. Holo Sail's own CEO
identified platform-ownership conflict as the binding constraint in January 2021, in print, two
years before events confirmed it. An architecture whose central commitment is that nobody owns
the substrate is aimed exactly at that failure.

**The counterweight:** that argument is still downstream of someone wanting to buy the thing.
Correct architecture is not demand. Holo Sail is the standing proof — right diagnosis, no
product.

---

## Recommendation

**Do not start a maritime Nondominium project.** The sequencing is wrong and the demand question
is unanswered.

**Do carry the compatibility finding into the Sensorica conversation.** It is concrete, checkable,
and says something useful about their stack's reach that they may not have articulated: their
custody and contribution vocabulary already covers commercial freight, complete with transport
claim types and timeliness metrics. That costs nothing to raise and is not a request for anything.

**If the insurer conversations come back warm**, revisit this document before designing anything
independently. Most of the substrate exists.

## Open questions for Sensorica

Framed as questions rather than asks:

1. Is `PropertyRegime::Private` intended for genuinely commercial resources, or is it there for
   transitional states on the way into a commons?
2. Is there a timeline for governance-as-operator (#41–#44)? Everything gate-shaped waits on it.
3. Does the `ParticipationClaimType` transport/storage vocabulary come from a real logistics use
   case, or was it modelled speculatively? If real, who was it built with?
4. Who else besides Sacha can maintain the hREA dependency inside the stack?

---

**Sources**

- Local: `ValiChord/nondominium_integration/NONDOMINIUM_ARCHITECTURE.md` and `README.md`
- [h-REA/hREA repository](https://github.com/h-REA/hREA) — activity and release data read 25 Aug 2026
- [hREA project site](https://hrea.io/)
- [hApps spotlight: hREA — Holochain Blog](https://blog.holochain.org/happs-spotlight-hrea/)
- [Sensorica/true_commons](https://github.com/Sensorica/true_commons)
- [BeefLedger](https://good-design.org/projects/beefledger-streamlining-transactions-in-the-beef-supply-chain/)
- Bob Haugen's 2021 assessment: [`03-community-response.md`](03-community-response.md) and
  [`../sources/forum/6532-questions-about-the-patent.txt`](../sources/forum/6532-questions-about-the-patent.txt)
