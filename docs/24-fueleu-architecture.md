# 24 — FuelEU compliance: the first use case where Holochain's validation actually does work

> ## ❌ CLOSED, 27 August 2026 — the incumbent check came back occupied at every layer
>
> This document was written before the check it says at the bottom must be done. The check
> was then done, and **FuelEU is occupied more thoroughly than laytime was.**
>
> | Layer | Who has it |
> |---|---|
> | Compliance calculation | **OceanScore**, Lloyd's Register, DNV, **BetterSea** |
> | Pooling | **OceanScore FuelEU Pooling Marketplace** — live, expanded May 2026, backed by **MSC, Anglo-Eastern, V-Ships, IINO Lines, Nordic Shipping, Döhle Group**. A published price index (OPX, €190–225/tCO₂e). Direct counterparty transactions, *"no additional counterparty risk"* |
> | The pooling *agreement* | OceanScore worked with **Clyde & Co** on a template pooling agreement |
> | Verification | **Statutory.** An accredited verifier confirms each ship's balance by 31 March; the EU's **Thetis** registry holds it. Pooled balances count only once the verifier approves |
> | The owner–charterer dispute mechanism | **BIMCO's clause already requires it**: owners' deficit calculations must be *"independently validated"* before presentation to charterers, and parties may agree *"once verified, that the decision is binding"* |
>
> **The regulation supplies the trusted neutral.** That is the strongest form of the pattern
> that has now killed six candidates: there is a statutory, accredited third party whose whole
> job is to confirm the number, and an EU registry that records it.
>
> The disputes are real — *"shipowners and charterers are still debating who pays, when and
> how,"* and the BIMCO clause is *"still being heavily amended in negotiations."* But that is
> **commercial allocation**, settled by contract negotiation. It is not a verification gap.
>
> **What survives is the technical insight, not the use case.** See the pattern note at the
> end of this document — it is the most portable thing in this repository.

**Every previous candidate in this repository asked peers to *witness* something they could
not check. This one asks them to *verify arithmetic*. That is a different kind of problem and
it is the first one where an integrity zome earns its place.**

Designed 27 August 2026, from the domain rather than from ValiChord's shape.

---

## Why this one is different

Look at what was being verified in each earlier candidate:

| Candidate | Disputed thing | Can a peer check it? |
|---|---|---|
| Notice of Readiness | was she an "arrived ship" | **No** — question of law |
| Cargo damage | was the damage pre-existing | **No** — expert judgement |
| Draft survey | how much cargo is aboard | **No** — judgement from readings |
| Speed and consumption | was it a "good weather day" | **No** — interpretation |
| **FuelEU compliance balance** | **does this figure follow from these inputs** | **Yes — it is arithmetic** |

GHG intensity under FuelEU is a formula: regulated well-to-wake emission factors applied to
fuel mass and energy. **Given the committed inputs and the regulated factors, the answer is
computable and deterministic.**

That matters because Holochain validation *must* be deterministic. Everywhere else in this
project the honest answer was "peers can confirm you committed to something, not that it is
true." Here peers can confirm the number is **right**.

**It does not make the inputs true.** What it does is collapse the argument surface: a
charterer disputing the manager's balance is no longer disputing a calculation — every peer
has already validated that. They can only dispute a specific fuel figure, which usually has a
mass flow meter behind it.

---

## The structural facts that dictate the design

**Liability and control sit in different hands.** The company holding the ISM Document of
Compliance is legally liable to the EU for penalties. The **time charterer** makes the
decisions that create the deficit — fuel purchased, speed, whether onshore power is used.
BIMCO's *FuelEU Maritime Clause for Time Charter Parties 2024* bridges this with a monthly
notification and indemnity, and gives owners the right to suspend on five days' notice.

**So the party who wants the evidence is not the party constrained by it.** That inverts the
objection that killed five earlier candidates in [`docs/22`](22-why-shipping-resists-this.md).

**The compliance period is annual; the parties change inside it.** A ship may have several
charterers in a compliance year. **The balance attaches to the ship, not to the party.**

**The data is created at sea, offline.** Intermittent VSAT is normal.

**Pooling is multi-party and adversarial.** After verification, surpluses can be transferred
between vessels of different companies. *"All participating companies must approve the
pool."* Surplus has cash value.

---

## The design

### One DNA, cloned per vessel — not per voyage

`network_seed = hash(IMO number)`. `CellProvisioning::CloneOnly`.

**The peer group is the hull.** This is forced by the domain, not chosen by analogy: the
liability attaches to the ship and survives every change of charterer and manager, so the
network must too.

This also repairs [`docs/16`](16-external-review.md)'s finding 2 against
[`docs/15`](15-dna-architecture.md). Per-voyage clones gave every party a fresh source chain
each voyage and destroyed the accumulating history that `docs/13`'s deterrent depends on. A
per-vessel cell accumulates for the life of the ship — **exactly as the liability does.**

Membership changes over time. Charterers join for their period and leave. The chain persists.

```yaml
name: vessel_compliance
integrity:
  network_seed: ~                    # per clone: hash(imo_number)
  properties:
    imo_number: "9228320"
    compliance_regime: FuelEU-2025
    emission_factors: { ... }        # regulated WtW factors, canonically serialised
    credential_issuers: [uhCAk...]
  zomes: [{ name: compliance_integrity }]
coordinator:
  zomes: [{ name: compliance_coordinator, dependencies: [compliance_integrity] }]
```

**One DNA, two zomes.** Not four DNAs. There is one peer group, one lifetime, and one set of
validation rules — so there is one network.

### Entries

```
BunkerDelivery      fuel type, mass, supplier, BDN reference, claimed WtW factors
ConsumptionRecord   period, per-fuel mass burned, energy, signed by the vessel
PortStay            berth, duration, onshore power available / used
ComplianceBalance   derived figure for a period, referencing the entries above by hash
HandoverAttestation countersigned: balance to date, fuel remaining on board, composition
```

### What validation actually enforces

This is the part that has never been available before:

- **`ComplianceBalance` must reference its inputs by action hash**, retrieved with
  `must_get_valid_record` — same DHT, deterministic, platform-legal.
- **The arithmetic must be correct.** SHA-256 and ordinary computation are available in an
  integrity zome; the regulated emission factors live in DNA properties, so every validator
  computes the same answer from the same inputs.
- **Signatures are checkable.** `hdi::ed25519::verify_signature` is available in validation —
  corrected in `docs/16` Part 2 after this review initially claimed otherwise.
- **No double-counting**: a `ConsumptionRecord` may be referenced by at most one
  `ComplianceBalance` for a period.

**A regulated factor changing is a new regulatory period, which legitimately deserves a new
DNA hash.** That turns Holochain's most awkward constraint — integrity changes create a new
network — into an accurate reflection of the domain.

### Countersigning finally earns its place

The charterer handover mid-compliance-year is the moment both parties have opposite
incentives about the same number: the balance so far, and the fuel remaining aboard with its
composition.

**It is inherently bilateral and simultaneous — either both commit or neither does.** That is
what countersigning is for, and nothing else in the toolkit provides it.

`docs/13` identified it; `docs/15` deferred it as "not in the first build." Here it is the
first build.

*Caveat, unchanged: it is feature-gated `unstable-countersigning`, sessions are time-bounded
with a six-second clock-skew limit, and stuck sessions need explicit abandonment.*

### Offline-first is load-bearing, and we had missed it

Consumption is recorded at sea. A source chain signs offline and gossips on reconnect with
the sequence intact — no live connection to a cloud database required.

**Credit where due: this came from Gemini and none of this repository's documents had made
the point.** For anything recorded shipboard it is a genuine advantage over any SaaS
platform, and it is not a claim about cryptography.

### No public DNA — export instead

The EU verifier needs the annual figure. That is not a network problem, it is an export: a
signed bundle carrying the balance and the chain of committed inputs, verifiable offline by
anyone holding the DNA properties.

This deliberately avoids `docs/16`'s finding 4, where `docs/15`'s public `record` DNA could
not be validated at all and anyone could publish anything into it.

---

## What is honestly unresolved

**Incumbents not yet ruled out.** OceanScore, Lloyd's Register and others sell FuelEU
compliance calculation. **What has not been found is anything addressing the multi-party
*dispute* layer** — the indemnity cascade, the handover, the pooling agreement. That is
currently contract law and spreadsheets. **This is the check that killed laytime and it is
not finished. Do it before building.**

**Pooling is multi-party in a way this design does not yet cover.** *"All participating
companies must approve the pool"* — across different owners, in Thetis. That is a second,
harder problem and possibly the more valuable one.

**The membrane is still leaky.** Holochain's own caveat stands: membrane proof checking is
not enforced during handshaking, so an unauthorised agent can join briefly and read.

**Properties must serialise byte-identically** for every party to land in the same cell —
`docs/16` finding 3. With emission factors in properties this needs a canonical encoding
fixed up front.

**Nobody has been asked whether they want this.** Unchanged since
[`docs/04`](04-strategic-assessment.md), and no amount of architecture moves it.

---

## Why this is worth more than the four DNAs of `docs/15`

| | `docs/15` | Here |
|---|---|---|
| DNAs | four | **one** |
| Peer group | chosen by analogy to ValiChord | **forced by where the liability sits** |
| Clone lifetime | per voyage — history destroyed | **per vessel — history accumulates with the liability** |
| Validation | witnesses commitments | **verifies arithmetic** |
| Countersigning | deferred | **the handover, which is the point** |
| Public record DNA | unvalidatable | **replaced by a signed export** |

ValiChord was a guide to *how to build on Holochain* — membrane proofs, integrity/coordinator
split, sweettest, `must_get_valid_record` chains. It was not a template for the shape, and
the shape here came from the regulation.

---

## The pattern, after six candidates — and this is what to keep

Six use cases, investigated properly, all closed:

| | Candidate | What already occupies it |
|---|---|---|
| 1 | Laytime / Notice of Readiness | Marcura PortLog and Claims PDMS, Veson IMOS, Oceanbolt — AIS reconciled against digitised SOFs, 700,000 documents through an AI pipeline |
| 2 | Marine cargo damage survey | **Joint survey practice** — surveyors attend together, without prejudice, and are *meant* to converge |
| 3 | Bunker quantity | **Mass flow meters**, mandated by Singapore 2017, Rotterdam and Antwerp-Bruges 2026 |
| 4 | Container condition at interchange | Automated gate cameras — Camco ARGUS/ADI, AllRead and others |
| 5 | Speed and consumption | **BIMCO Weather Routeing Clause 2006** — "a mutually agreed weather routing company… final and binding". Exists; largely unused |
| 6 | FuelEU / EU ETS | **A statutory accredited verifier**, the Thetis registry, OceanScore's pooling marketplace, and a BIMCO clause already requiring "independently validated" calculations |

**Six for six is not bad luck.** It is a finding.

### What the finding is

**Shipping already has trusted-neutral machinery for every dispute worth having one for.**
Sometimes commercial (Marcura, SGS, Control Union, OceanScore), sometimes contractual (BIMCO
clauses), sometimes statutory (accredited verifiers, port authority licensing), and sometimes
social (the joint survey).

**Cryptographic trust-minimisation solves a problem this industry solved socially and legally
a long time ago.** That is why every candidate is occupied, and it will be true of the
seventh.

Three corollaries, each earned:

- **Where the dispute is factual, a sensor arrives and wins.** AIS, mass flow meters, gate
  cameras. Every time.
- **Where the dispute is judgemental, the industry has built convergence, not verification** —
  and it prefers it, because convergence settles cheaply.
- **Where a pre-commitment mechanism is genuinely wanted, it already exists as a clause** and
  is not adopted. The missing thing was never a tool.

### What survives, and it is worth more than any of the six

**1. Validation can verify computation, not merely witness commitment.** FuelEU was the first
candidate where the disputed quantity was arithmetic over committed inputs, so an integrity
zome could enforce correctness rather than just recording that somebody said something. That
distinction is real, it is portable to any domain, and it is where Holochain's validation
model is genuinely strong.

**2. Anchoring-prevention works unilaterally.** One party sealing their position before
exposure captures the whole benefit with nobody else participating. This dissolves the
twelve-counterparty wall that killed TradeLens and Holo Sail. Found in
[`docs/23`](23-draft-survey.md), and it is domain-independent.

**3. Peer group should be forced by where the liability sits.** The per-vessel clone in this
document was right for its reason — the compliance balance attaches to the hull — and it is
the correct correction to [`docs/15`](15-dna-architecture.md)'s per-voyage design. **The rule
generalises: find where the obligation lives, and put the network boundary there.**

**4. Countersigning fits handovers, and only handovers.** Where two parties have opposite
incentives about one number at one moment, atomic bilateral commit is the primitive nothing
else provides.

**5. Offline-first is a real advantage** for anything recorded away from connectivity, and it
requires no argument about trust at all.

### The honest conclusion

**Shipping is not the home for this mechanism**, and six investigations is enough evidence to
stop looking. The five findings above are the return on that work, and they are portable.

Anyone picking this up should read this section and then choose a different industry — one
where the trusted neutral does **not** already exist by statute, by contract, or by
professional custom.

---

## Candidate 7 — seafarer hours of rest, and the seventh rule

Checked 27 August 2026, following the observation that maritime **grants** target
decarbonisation, safety and welfare — never commercial dispute resolution — because grants
fund market failure and vendors fund markets. Seafarers have no purchasing power, so no
vendor serves them. That made hours of rest the right *shape*.

**The problem is real and severe.** Rest-hour records are among the most common Port State
Control deficiencies, and are detainable under the Paris and Tokyo MOUs. Fatigue kills.

**The vendors serve the company, not the seafarer.** Sealogic E-CMS, Sealogical, Manage My
Vessel, ShipAdmin HOWAR and others sell rest-hour recording — and the pitch is *"flag
nonconformities"* and *"help vessels pass audits."* Nothing found gives the seafarer a record
their employer cannot alter, and MLC already has them countersign the company's version.

So on the criteria that have governed every other candidate, this one passed: real problem,
no incumbent serving the affected party, unilateral adoption, offline-first, and a record
that must not live on the employer's system.

### And it still fails, for a reason none of the others did

**"A culture of adjustment"** — World Maritime University, funded by the ITF Seafarers'
Trust — found *"widespread malpractices in hours of work reporting"*, and identified the
mechanism:

> the regulations are so difficult to comply with that **"seafarers and inspectors alike…
> collude in an adjustment to suit the rules rather than reflect the realities on board."**

**Everyone adjusts. The seafarer, the master, and the inspector.** Not because anyone is
dishonest, but because the rules cannot be met at current manning levels.

**So a record the seafarer controls and the company cannot alter is a weapon pointed at the
seafarer.** An honest log does not create rest — it creates a detention, and the crew are the
ones who suffer it. The person the tool is meant to protect is the person who would refuse to
use it, and would be right to.

**The falsification is a symptom. The disease is manning levels and regulatory design.** No
amount of evidence integrity touches either.

### The seventh rule, and it is the most useful one here

> **Before building verification, ask whether the false record is a symptom of an impossible
> rule.**
>
> If it is, better evidence makes things *worse* for the person you are trying to help, and
> the honest response is to say so rather than to ship it.

This is the only candidate of the seven that failed on ethics rather than on economics, and
it is the one most likely to have been built by someone who did not check.
