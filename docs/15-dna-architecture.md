# 15 — DNA architecture for this project

**Two DNAs, with a named seam where a third would attach.** Not ValiChord's four, and the
places it differs are the interesting part.

Designed against [Holochain's own DNA guidance](https://developer.holochain.org/build/dnas/),
which is deliberately conservative: split for **separate peer groups**, **privileged or
cloned spaces**, or **bounded data lifetimes** — *"keep functionality unified otherwise."*

---

## The correction that shapes everything

The four parties — carrier, port authority, terminal operator, telemetry — are **four
agents in one DNA**, not four DNAs. Exactly as ValiChord's validators are N agents in the
Attestation DNA.

This is where the shipping case diverges from ValiChord, and it diverges *downward*:
fewer DNAs, not more.

---

## Why there is no private per-party DNA

ValiChord has two private DNAs — Researcher Repository and Validator Workspace — because
a researcher's files and a validator's intermediate reasoning are sensitive, and because
those participants are individuals working on documents.

Neither reason survives translation.

**The carrier's raw record already lives in their own system.** Their TOS, their ERP,
their ops database. Asking a shipping line to migrate operational data into a Holochain
private cell is asking them to replace working infrastructure, which nobody will do. The
private space already exists and is not ours. **The boundary is the moment a party chooses
to make a claim** — before that, it is their system's business.

**And the validator's work has nothing to hide.** ValiChord's DNA 2 exists partly because
a validator's intermediate calculations would leak their verdict before reveal. Here the
check runs *after* reveal, on data that is already public, and it is deterministic —
compare a revealed claim against a public AIS track. **Anyone can re-run it and get the
same answer.**

That last point matters beyond DNA layout. It is why [`docs/08`](08-external-evidence-and-the-real-gap.md)
concluded this is a *backdating* problem rather than an *anchoring* one: blind
commit-reveal exists to stop assessors influencing each other, and a reproducible
computation cannot be influenced.

---

## DNA 1 — `voyage`, cloned per transport call

The shared, credentialed space where the protocol runs. **One cloned cell per voyage.**

Justified on two of Holochain's three grounds at once: parties to voyage A are a different
peer group from voyage B, and per-voyage isolation is precisely the "privileged spaces via
cloning" case.

```yaml
name: voyage
integrity:
  network_seed: ~          # supplied per clone
  properties:
    transport_call_id: TC-2023-USLAX-0042
    vessel_imo: "9138111"
    unlocode: USLAX
    authorised_parties:    # role -> AgentPubKey, from the charterparty
      CARRIER: uhCAk...
      PORT_AUTHORITY: uhCAk...
      TERMINAL_OPERATOR: uhCAk...
      TELEMETRY: uhCAk...
  zomes:
    - name: voyage_integrity
coordinator:
  zomes:
    - name: voyage_coordinator
      dependencies: [voyage_integrity]
```

**Provisioning:** `CellProvisioning::CloneOnly` with a high `clone_limit`. There is no base
cell — only clones are ever instantiated. Nondominium already runs this pattern with one
clone per NDO at `clone_limit: 512`, so it is proven in the ecosystem rather than novel.

**Deriving the seed.** `network_seed = hash(transport_call_id)`, so any party holding the
transport call reference computes the same cell and needs no directory to find it.
Transport call IDs are not secret, so **the seed is addressing, not security** — the
membrane is the security.

**The membrane is the confidentiality mechanism.** `validate_agent_joining` checks the
joining key against `authorised_parties` in the DNA properties, which are baked into the
DNA hash and therefore tamper-evident. A party to another voyage cannot join, and cannot
quietly alter the guest list either.

That is the direct answer to what IPCSA names as the cornerstone of its Network of Trusted
Networks — commercial confidentiality, with parties exchanging only what they authorised.

**Entry types:**

| Entry | Holds |
|---|---|
| `SealedClaim` | commitment hash, role, agent key, signature, embedded time floor |
| `RevealedClaim` | payload, nonce — validated against the matching `SealedClaim` |
| `TimeAnchor` | drand round and the external timestamp receipts for a commitment |

**Integrity rules:** a reveal must hash to its commitment; one claim per role per call; no
updates and no deletes on any of the three. Immutability is the deterrent, per
`ValiChord/docs/1_ValiChord_Vision&Architecture.md`.

**Lifetime.** Voyage cells are bounded — the claim window closes, the dispute resolves, the
cell can be disabled. This is Holochain's third split criterion (isolating old data into
bounded networks) arriving for free.

## DNA 2 — `record`, one shared public network

The finding. Open read, no membrane, HTTP gateway so a claims manager with no Holochain
can read it.

A different peer group in the strongest sense — the readership is everyone, including
people who will never run a node.

| Entry | Holds |
|---|---|
| `DiscrepancyRecord` | the finding, the voyage cell's DNA hash, the anchor proofs, and the explicit `notDetermined` list |

Published only once a voyage cell's protocol completes. Immutable. **This is what
[`docs/12`](12-phase2-findings.md) rendered as a static page** — the Phase 2 artefact is
DNA 2's read view, built before the DNA existed.

---

## The third DNA — a real choice, deliberately deferred

Two candidates, and it is worth being honest that this is a fork rather than a settled
question.

**Candidate A — `telemetry`.** A shared public space where AIS oracles publish signed
attestations over track extracts, referenced by voyage cells rather than duplicated into
each one. It has a genuine case: oracles are a different peer group from commercial
parties, their data is public rather than confidential, and one day's track may serve many
voyages.

**Candidate B — `identity`.** A long-lived registry answering *"which agent key is
authorised to act as CARRIER for this company?"* Real problem, and currently hand-waved
into DNA 1's properties.

**Recommendation: neither yet.**

Against A: AIS is already public and external. The oracle's job is to attest *"this hash
is the AIS for this period"*, and that attestation fits in DNA 2 today. A telemetry DNA is
a **deduplication optimisation, not a correctness requirement** — and optimising storage
before anyone uses the system is the definition of premature.

Against B: shipping already has identity infrastructure — IMO numbers, company registries,
P&I club membership, charterparty documents naming the parties. Building a new identity
layer for the industry is a larger project than this one, and referencing what exists beats
recreating it. For now the charterparty names the parties and DNA 1's properties record
them.

**And a design asymmetry worth respecting: adding a DNA later is far easier than removing
one.** Holochain's own guidance says keep it unified until a reason forces the split.
Neither reason has arrived.

The seam is named so that when one does, it attaches somewhere obvious rather than being
retrofitted.

---

## What this changes about Phase 3b

[`docs/14`](14-holochain-setup.md) costed Phase 3b as building a new DNA and treated the
two-language bridge as the main risk. Both estimates need revising:

- **DNA 1 is ValiChord's Attestation DNA with a different entry payload and a cloned
  provisioning strategy.** The commit-reveal mechanism, the membrane pattern, and the
  immutability rules all have working, tested precedent in the same codebase.
- **DNA 2 is simpler than ValiChord's Governance DNA** — one immutable entry type and a
  read gateway.
- **There is no third and fourth DNA to build**, because the private tiers do not
  translate.

The Python-to-Rust bridge remains the real work, and [`docs/14`](14-holochain-setup.md)'s
three options for it still stand.

## What it does not change

Nothing here answers whether anyone will pay. A cleaner architecture is still architecture.
The Phase 2 page has still not been shown to anyone who works a laytime desk, and that
remains the only outstanding question that matters.
