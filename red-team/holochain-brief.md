# Red-team brief: Holochain as the transport for Asset Record Entry

Copy everything below the line into a fresh session with a red-teaming model, along with
`spec/asset-record-entry-v0.1.md`.

Its job is to stop the model inventing Holochain facts — the platform is niche, moves fast,
and most training data about it is either wrong or four years old — and to point the attack at
the transport rather than at the format, which has already been audited three times.

**Written to invite attack, not to defend.** If it starts reading like a case for Holochain,
it has failed and should be rewritten. The section on what Holochain makes *worse* is there
on purpose and must not be trimmed.

---

## Context

I have a draft format, Asset Record Entry v0.1 (attached), for one signed, hash-chained entry
in the life of a physical asset. It has been red-teamed three times already and the findings
are recorded in the spec. **I do not need the format audited again.**

The real problem it exists for: a ship's maintenance record does not survive a change of
technical manager. The record lives in the manager's licensed software; when the management
agreement ends, it goes. Marine insurers have documented this since 2010 and it is still
happening. The top two causes of main engine damage — lubrication failure and incorrect
maintenance, averaging USD 926,000 a claim — are exactly what a maintenance record either
establishes or fails to establish.

The format alone cannot fix it, because its central property — that a missing entry is
provable — only works if a second party actually **received** the entries when they were
written. That is a transport question. **I am considering Holochain as that transport and I
want you to attack that decision.**

## What Holochain is, factually

Verified against primary sources in August 2026. Please work from these rather than from
memory, and tell me if anything here contradicts something you know.

**It is agent-centric, not data-centric.** Every participant has their own append-only,
cryptographically signed source chain of their own actions. There is no global ledger.

**There is no consensus mechanism.** No mining, no staking, no ordering service, no global
agreement about a sequence of events. This is the main way it differs from a blockchain, and
it matters here because this problem has no double-spend and needs no global ordering.

**Data lives in a validating DHT.** When an agent commits, the entry is published to peers
whose hash neighbourhood covers it. Those peers validate it against deterministic rules and
hold a replica. Peers, not a server, enforce the rules.

**One application is one network.** Rules live in an "integrity zome"; changing it changes the
DNA hash, which creates a **new, empty network**. That is a migration, not a patch.

**Membership can be gated** by a membrane proof checked when an agent joins.

**Warrants** let peers block an agent that breaks validation rules, and propagate the fact.

Four things it is **not**, because these confusions are common: it is not a blockchain; it is
not the HOT token or Holo hosting (a separate company); it does not give global consensus; and
it is not mature — see below.

## Maturity, stated plainly

- Current release **0.7.0**, July 2026.
- **0.8** is "stabilize the HDK and support app upgrades". DNA migration is still a *spike* —
  an investigation, not an implementation.
- **1.0** contains the key-rotation work (updating an agent key while still serving history
  under the previous key). **No date is published.** My own estimate from release cadence is
  2028–29 and may be wrong.
- Sharding is three loosely-specified issues in 0.9, two marked "awaiting clarification".
- Countersigning is feature-gated as unstable, and roughly half of the 2.0 milestone is
  countersigning bug fixes — including one where failure rate rises with network size.
- Membrane proofs are **not** enforced during handshaking, so an unauthorised agent can join
  and read briefly before being blocked. Fixing that is a 1.0 item.
- Action timestamps are **self-reported**.
- The intended shape here is one small network per vessel: two to five agents (owner, manager,
  possibly class and an insurer), full replication, tens of thousands of entries over a
  25-year asset life.

## The claims I want attacked

These are **claims, not conclusions.** Please try to break each one.

1. **Tail truncation is mitigated.** The strongest open finding against the format is that a
   chain ending at entry 11 verifies perfectly whether or not entry 12 was written and
   dropped — so the most damaging record can be withheld with no cryptographic trace. The
   claim is that publishing at commit time defeats this, because the counterparty already
   holds the entry before anyone decides it is inconvenient. Is that true in practice, given
   gossip timing, offline peers and small networks?

2. **The merged view is native.** With a bare format, each author keeps a separate chain and a
   reader must discover and merge them. The claim is that a shared DHT makes "everything known
   about this hull" a query rather than an integration problem.

3. **Cross-chain ordering improves.** Entries can reference other agents' action hashes and
   validation can *require* it, which a passive file format cannot.

4. **The network boundary can be the asset, not the company.** One network per vessel;
   managers join and leave; the record persists among remaining members. Does that survive
   contact with reality — key loss, a one-ship owner going quiet, a vessel sale?

5. **Withdrawal becomes impossible rather than merely detectable**, because peers already hold
   a replica.

## What I believe Holochain makes worse

Stated by me so you do not have to find them, and so you can tell me if there are more.

- **Redaction becomes harder, not easier.** A prior red team found that an immutable chain
  over free-text remarks makes it impossible to scrub PII (crew injury detail) or commercial
  pricing without destroying history. Replicating to peers makes erasure worse, not better.
- **Availability is worse than a server.** DHT data lives on peers who are online. A one-ship
  owner whose machine is off may simply not receive entries.
- **Two sources of truth.** Holochain already orders an agent's actions on the source chain.
  Carrying `seq` and `prev` inside the entry as well gives two orderings that can diverge.
- **A 25-year record on a platform that changes network identity when its rules change** is a
  genuine tension, and the migration story is still a spike.
- **Adoption is worse.** Nobody has a conductor installed. The format can be adopted by one
  party unilaterally; the transport cannot.

## What I want from you

1. Break the five claims. Where a mitigation only holds under assumptions, name the
   assumptions.
2. Find things Holochain makes worse that I have not listed.
3. Tell me which of the five could be obtained **without** Holochain, and how cheaply. If a
   plain signed-file exchange with a receipt gets 80% of it, say so.
4. Identify what would have to be true about the ship-management market for this transport
   choice to be right — and how I could test that from a desk.
5. Say plainly if the honest answer is that the transport should be boring and the interesting
   part is elsewhere.

**Do not be agreeable.** I have had three rounds of technical audit and no market contact, so
the failure mode I am most worried about is a well-audited artifact nobody wants. If you think
that is where this is heading, lead with that.
