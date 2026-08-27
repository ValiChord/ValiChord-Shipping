# 26 — Handover: find a shipping project that genuinely fits Holochain

**Paste this into a fresh session. It replaces [`docs/19`](19-handover-brief.md), which was
written for a narrower task.**

Written 27 August 2026 at the end of a long session that drifted. The drift is described
below because it is the main thing to avoid repeating.

---

## The task

**Find a problem in shipping that Holochain's architecture genuinely fits, and that nobody
has already solved.** If no such problem exists, say so — that is a valid and useful answer,
and this repository already contains ten worked examples of reaching it honestly.

### Three things that are NOT the task

1. **This is not a ValiChord project.** The repository sits under the ValiChord organisation
   for historical reasons only. **Do not assume blind commit–reveal.** Do not assume
   verification, attestation, or dispute resolution. ValiChord is useful only as a worked
   example of *how to build on Holochain* — membrane proofs, integrity/coordinator split,
   sweettest, `must_get_valid_record` chains. It is not a template for the shape.
2. **This is not Holo Sail's vision.** That is documented in `docs/01`–`docs/04`. It died at
   a twelve-counterparty adoption wall, as did TradeLens with Maersk and IBM's money.
3. **This is not laytime, demurrage, or anything in the ruled-out list below.**

---

## The mistake this session made, so you don't repeat it

Every candidate got filtered through *"does blind commit–reveal fit?"* — which is
**ValiChord's mechanism, not Holochain's architecture.** The user said at the outset not to
do this, and it happened anyway across ten candidates.

**Holochain's most useful properties in shipping have nothing to do with trust or disputes.**

| Property | What it is actually good for |
|---|---|
| **No server** | Coordination where nobody wants to pay for, or trust, an operator. The cost floor is zero; a SaaS competitor's is not |
| **Data stays with each party** | Each holds their own signed chain and grants access to slices. A *control* problem, not a trust one |
| **Offline-first** | Sign at sea, gossip on reconnect, sequence intact. ⚠️ **See the correction below — merchant ships are no longer offline** |
| **Cheap ephemeral private groups** | Membraned cloned spaces per group, created and dissolved at no infrastructure cost |
| **Countersigning** | Atomic bilateral commit — both or neither |
| **Peer-enforced deterministic rules** | The DHT enforces, not a server |
| **Accumulating per-agent history** | Held by peers, so forks are detectable and reputation accrues |

Only the last three are about trust. **The first four are about cost, connectivity and
ownership.**

### The question to search with

Not *"who is lying?"* but:

> **Where does coordination currently require someone to run a server that nobody wants to
> pay for or trust with their data — and where does the connection keep dropping?**

---

## Learning Holochain — and facts already established, so you don't re-derive them

**Primary documentation:** `https://developer.holochain.org/build/` — read `dnas/`, `zomes/`,
`validation/`, `cloning/`, `entries/`, `links/`, `callbacks-and-lifecycle-hooks/`. Crate docs
at `docs.rs/hdi` (integrity) and `docs.rs/hdk` (coordinator).

**Verified this session, from primary sources. Trust these:**

- **Validation must be deterministic.** *"Validation rules must always yield the same
  true/false outcome… regardless of who is validating them and when."* Dependencies *"must be
  addressable, retrievable from the same DHT."*
- **`must_get_action`, `must_get_entry`, `must_get_valid_record`, `must_get_agent_activity`**
  are the only deterministic DHT retrieval functions available in validation.
- **`hdi::ed25519::verify_signature` IS available in integrity zomes.** ValiChord's code
  contains a comment claiming otherwise; it is wrong, and it caused ValiChord to move its
  membrane check into `init()`. Do not inherit that mistake.
- **Changing an integrity zome changes the DNA hash**, *"creating a new empty network and
  database."* Keep integrity zomes small and stable. This is a migration, not a patch.
- **Clone data is deleted** when the cell is deleted or the hApp uninstalled. Disabled clones
  retain data. **Do not put long-lived evidence in a short-lived clone.**
- **DNA properties are modifiers** and change the DNA hash. Every party must serialise them
  **byte-identically** to land in the same network. A network seed alone is not enough.
- **`call_remote` does not cross DNAs.** Bridge calls (`call`) work *within one agent's own
  hApp instance* — that is the mechanism for cross-cell work on one node.
- **Countersigning is feature-gated** `unstable-countersigning`, sessions are time-bounded
  with a six-second clock-skew limit, and stuck sessions need explicit abandonment.
- **Membrane proofs are not enforced during handshaking** — an unauthorised agent can join and
  read briefly before being warranted and blocked.
- **Holochain action timestamps are self-reported.** Fork detection is done by *peers* holding
  the `RegisterAgentActivity` replica. A single-operator hApp gets no ordering guarantee.
  External time anchors remain necessary. See [`docs/13`](13-phase3-findings.md).
- **ValiChord runs Holochain 0.7.0** (`hdi` 0.8.0, `hdk` 0.7.0), installed by plain
  `cargo install` — no nix, no holonix, no flake.

---

## What has already been ruled out, and why

**Ten candidates. Do not re-open these without new information.**

| Candidate | Why it closed |
|---|---|
| Laytime / Notice of Readiness | Marcura PortLog and Claims PDMS, Veson IMOS, Oceanbolt — AIS reconciled against digitised SOFs, 700,000 documents through an AI pipeline |
| Marine cargo damage survey | **Joint survey practice is deliberately convergent.** Blinding would destroy what the industry uses to settle cheaply |
| Bunker quantity | Mass flow meters. Mandated by Singapore 2017, Rotterdam and Antwerp-Bruges 2026 |
| Container condition at interchange | Automated gate cameras — Camco ARGUS/ADI, AllRead |
| Speed and consumption | **BIMCO Weather Routeing Clause 2006** already provides a binding neutral expert. Exists; unused. Claims are only $15k–250k |
| FuelEU / EU ETS | **Statutory accredited verifier**, Thetis registry, OceanScore's pooling marketplace (MSC, V-Ships, Anglo-Eastern), Clyde & Co template agreement |
| Seafarer hours of rest | **Failed on ethics.** *"A culture of adjustment"* (WMU / ITF Seafarers' Trust): everyone including inspectors adjusts because the rules cannot be met at current manning. An honest record produces a detention, and the crew wear it |
| Vessel vetting | RightShip and OCIMF SIRE are the trusted neutral |
| Crew certification fraud | Flag states issue; IMO GISIS holds |
| Confidential near-miss reporting | CHIRP Maritime already is the confidential neutral |

**The pattern:** maritime has spent two centuries building trusted neutrals — class
societies, P&I clubs, SGS, flag states, CHIRP, accredited verifiers, port authorities — and
they work. **Anything framed as "verify a claim" will hit one of them.**

---

## The seven tests, and their limitation

[`docs/25`](25-seven-tests.md) sets out seven tests, ordered cheapest first. **Use tests 1 and
2 on everything — they are free and kill most ideas in ten minutes:**

1. **Measurement or judgement?** If a sensor could settle it, one will, and you arrive second.
2. **Who buys it, and who does it constrain?** If those are the same party, it is not adopted
   on merit. The only route that ever worked was a gatekeeper mandating it.

**But be aware of what `docs/25` gets wrong for this task.** All seven tests are
*verification-shaped* — every one assumes the problem is a dispute. If the candidate is about
**cost, connectivity or data ownership**, tests 4, 5 and 6 ask irrelevant questions and will
close doors that were never the right doors. Use judgement. Test 3 ("does anyone already sell
this?") always applies.

**One trap `docs/25` does not yet name:** maritime grants — TRIG, CMDC, Lloyd's Register
Foundation, EMFAF — fund **decarbonisation, autonomy and safety *technology*, not evidence
integrity**. Chasing that money means building something else. Verified against the funders'
own pages; every named UK call was closed as of 26 August 2026.

---

## Where to search

- **Incumbents first, always.** Marcura, Veson Nautical, OceanScore, SGS, Control Union,
  Lloyd's Register, DNV, ClassNK, Windward, Spire, Kpler, Nexxiot, ZeroNorth, Q88.
- **P&I club loss-prevention publications** — Gard, Britannia, Steamship Mutual, Skuld, West
  of England, NorthStandard. Named authors, publicly reachable, and they describe real
  problems because they pay for them.
- **BIMCO clauses** — `bimco.org/contractual-affairs/bimco-clauses`. If a coordination
  mechanism is wanted, check whether a clause already exists.
- **Find Case Law** — `caselaw.nationalarchives.gov.uk`, Atom API, Open Justice Licence.
  Tooling in [`tools/phase0b/`](../tools/phase0b/) already mines it.
- **NOAA / MarineCadastre AIS** — free bulk US AIS, 2009–2025 in daily CSV from 2015.
- **IIMS** — 1,000+ marine surveyors, quarterly magazine that invites member submissions.

---

## Environment and working facts

- **Python works here** (3.14.7, `cryptography`, `opentimestamps`), `curl`, `openssl` 3.5
  with `ts`. `tools/` runs and reproduces its published numbers.
- **No Rust, no cargo.** Holochain work needs a Codespace. ValiChord has
  `setup_holochain.sh`.
- **`gh` is not authenticated.** Issues and PRs must be pasted by the user.
- **The repo is public** at `github.com/ValiChord/ValiChord-Shipping` and pushes go to `main`.
- **The user is non-technical, dyslexic, and solo.** Lead with the point. Strip jargon. Short
  paragraphs. He is funding this himself.

---

## What not to do

- **Do not design DNAs before checking the market.** [`docs/15`](15-dna-architecture.md) is
  four DNAs of architecture for a use case that was already occupied. It is parked, with
  seven findings against it.
- **Do not write another analysis document instead of asking a person.** This repository has
  twenty-six of them and has spoken to nobody in the industry.
- **Do not assume a gap exists.** Ten for ten says otherwise.
- **Do not manufacture an eighth candidate to be encouraging.** A clean "no" is worth more
  than a hopeful maybe, and the user has said so explicitly.
- **Pair every red-team pass with a blue-team pass.** Demolition alone produces the belief
  that nothing is viable, which is as wrong as the opposite. Always finish with *what
  survived?*

---

## What survived ten candidates, and is portable

1. **Validation can verify computation, not merely witness commitment** — where the disputed
   quantity is arithmetic over committed inputs, peers can enforce correctness.
2. **Anchoring-prevention works unilaterally** — one party sealing before exposure captures
   the whole benefit alone. **This dissolves the twelve-counterparty adoption wall.**
3. **Put the network boundary where the obligation lives**, not where the transaction is.
4. **Countersigning fits handovers, and only handovers.**
5. **Offline-first requires no argument about trust at all** — and in shipping it may be the
   strongest card in the deck. ⚠️ **Withdrawn. See below.**

**Start from 5, not from 1.** That is the correction this handover exists to make.

---

## CORRECTION, 27 August 2026 — point 5 is withdrawn

**Do not start from offline-first. It has expired, and a session that starts there is
building for 2019.**

Verified against connectivity market data on 27 August 2026: roughly **67,000 commercial
vessels were on Starlink by early 2026**, with 40,000+ merchant ships expected by the end of
2025, and per-gigabyte costs down more than 95% since before LEO. The deep-sea merchant
fleet is going always-on, quickly, and in one direction only.

Offline-first still holds for **fishing, inland waterways, workboats and small operators**.
It does not hold for merchant shipping, which is what the rest of this document is about.

**The property that is strengthening instead is data ownership and custody** — points 2 and
3 on the surviving list. Start there.

This correction produced candidate 11, the first to survive the three cheap tests:

> **A ship's technical record does not survive the company that created it.** IUMI called
> non-transfer and destruction of records *"commonplace"* in its position paper of 8
> September 2015 and asked IACS, jointly with the London Joint Hull Committee, to make
> record retention a condition of class. Gard had already raised it in a 2010 circular and
> was **still writing it up on 21 July 2026**. SHIPMAN 2024 added Clause 22 giving owners
> their data, and Clause 21 giving them access *through the manager's own platform*.
>
> **The clause exists and the problem persists**, which means the missing piece was never
> agreement. It is that nobody can tell what was deleted, because the only record of what
> was written is held by the party who benefits from deleting it.

Worked demo and the full set of objections against it, including the two that could still
kill it: [`../tools/record-gap/`](../tools/record-gap/).

**Note what candidate 11 is not.** It is not a verification problem, and reaching for blind
commit–reveal here would repeat exactly the mistake this document was written to prevent.
Nothing is verified and nobody commits to anything. It is custody.
