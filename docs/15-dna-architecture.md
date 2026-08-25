# 15 — DNA architecture

**Four DNAs: `registry`, `telemetry`, `voyage`, `record`.**

Designed from this project's own requirements. An earlier version of this document reached
two DNAs by reasoning against ValiChord's shape and by invoking "adding a DNA later is
easier than removing one" — an argument about migration cost in a deployed system, applied
to a project with nothing deployed. Both were wrong and the document was replaced rather
than patched.

Design inputs: [Holochain's DNA guidance](https://developer.holochain.org/build/dnas/) —
split for separate peer groups, privileged or cloned spaces, or bounded data lifetimes —
and two platform constraints that turn out to decide the shape.

---

## The two constraints that dictate everything

**Validation cannot read across DNA boundaries.** The `must_get_*` family are, in the
Holochain reference's words, *"the ONLY DHT retrieval functions available in validation"*,
because validation must be deterministic. They operate inside one DNA.

**`call_remote` is blocked across DNA networks.** Different DNAs are different networks;
an agent in one cannot reach into another.

Together these mean **a voyage cell can never look up the registry to decide whether to
admit someone.** Any check performed at validation time must be computable offline, from
data the validator already holds.

That single fact determines how the four DNAs connect, and it is why the design below
leans on *signed credentials* rather than *lookups*.

---

## The peer groups, which are what actually decide the boundaries

| | Who is in it | How long it lives | Who may read |
|---|---|---|---|
| `registry` | The industry | Permanent | Anyone |
| `telemetry` | Observers and anyone verifying them | Continuous | Anyone |
| `voyage` | Parties to **one** transport call | Bounded — ends with the claim window | Only those parties |
| `record` | Everyone, including people who will never run a node | Permanent | Anyone |

Four genuinely different populations, on four different clocks. That is the justification;
the resemblance to ValiChord's count is coincidence, and the reasons are unrelated —
ValiChord splits by privacy tier between individuals, this splits by peer group and
lifetime between institutions.

---

## DNA 1 — `registry`

**An index, not an authority.** This is the design call: shipping already has identity
infrastructure — IMO company numbers, LEIs, P&I club membership, charterparty documents
naming parties. A startup declaring itself the root of trust for maritime identity would
be both presumptuous and unusable.

So `registry` answers a narrower question: *which agent key claims to be which existing
legal entity, and who vouches for that claim?*

```
PartyIdentity {
  agent_key, legal_name,
  external_ids: { imo_company_number, lei, p_and_i_club, ... },
  evidence_refs
}
IdentityAttestation {  // one attestor vouching for one binding
  subject: PartyIdentity, attestor_key, signature, time_anchor
}
IdentityDispute { subject, disputant_key, grounds, signature }
```

**Strength is not binary.** A binding is as good as the number and standing of its
independent attestors. One self-assertion is weak; a P&I club and a terminal operator
both vouching is strong. Nothing is prevented — a false claim of identity can be
published, and then contested. That is
[`docs/13`](13-phase3-findings.md)'s *detect over prevent* applied to identity.

**Also issues the joining credentials** that DNA 3 verifies. See "How they connect".

## DNA 2 — `telemetry`

**This DNA exists because the oracle cannot be a party to every voyage.** An AIS observer
watches continuously and belongs to no transport call. Putting it inside the per-voyage
DNA would require it to join every clone — thousands of networks. That is not an
inefficiency, it is an architecture that does not run, and getting this wrong is what made
the earlier two-DNA design invalid.

**It stores attestations about evidence, never the evidence.** AIS is already public and
already hosted by NOAA. Copying it into a DHT would duplicate a public dataset for no gain.

```
TelemetryAttestation {
  source: "NOAA/MarineCadastre", period, coverage_bbox,
  dataset_sha256, retrieval_url,
  oracle_key, signature, time_anchor
}
```

Published once per period and referenced by any number of voyages. An oracle's write
access is gated by a credential from DNA 1; reads are open, because the whole point is
that anyone can check.

## DNA 3 — `voyage` — cloned per transport call

The protocol. Qualifies on two of Holochain's grounds at once — separate peer group *and*
privileged cloned space — and picks up the third, bounded lifetime, for free.

```yaml
name: voyage
integrity:
  network_seed: ~                 # per clone: hash(transport_call_id)
  properties:
    transport_call_id: TC-2023-USLAX-0042
    vessel_imo: "9138111"
    unlocode: USLAX
    credential_issuers: [uhCAk...]   # registry attestor keys, baked into the DNA hash
    authorised_parties:
      CARRIER: uhCAk...
      PORT_AUTHORITY: uhCAk...
      TERMINAL_OPERATOR: uhCAk...
      TELEMETRY: uhCAk...
  zomes: [{ name: voyage_integrity }]
coordinator:
  zomes: [{ name: voyage_coordinator, dependencies: [voyage_integrity] }]
```

`CellProvisioning::CloneOnly`, high `clone_limit` — no base cell, only clones. Nondominium
runs this pattern at `clone_limit: 512` per NDO, so it is proven rather than novel.

**Seed derivation replaces a directory.** `network_seed = hash(transport_call_id)` means
any party holding the voyage reference computes the same cell. Transport call IDs are not
secret, so **the seed is addressing, not security.**

**Entries:** `SealedClaim` (commitment, role, key, signature, embedded drand floor),
`RevealedClaim` (payload, nonce), `TimeAnchor` (external timestamp receipts),
`TelemetryRef` (a `dataset_sha256` from DNA 2).

**Integrity rules:** a reveal must hash to its commitment; one claim per role per call; no
updates, no deletes. Immutability is the deterrent.

### The guest-list problem, and why it is survivable

Whoever creates a clone fixes `authorised_parties` in its properties. So the creator picks
who is watching — and if the carrier creates the cell, the carrier chooses its own
auditors. That appears to hollow out the membrane.

It does not, for three reasons:

- Properties are **baked into the DNA hash**, so the guest list is fixed at creation and
  tamper-evident thereafter.
- Every joining party **sees the full list** and can refuse. A cell with the wrong
  counterparty is a cell nobody joins.
- **A voyage cell with only one real party is worthless.** The output is a comparison
  between independently committed claims. A carrier alone in a cell has produced a signed
  note to itself.

Prevention is not available here and is not needed. Detection is, and it is immediate.

## DNA 4 — `record`

The public finding. Open read, no membrane, HTTP gateway so a claims manager with no
Holochain can read it.

```
DiscrepancyRecord {
  voyage_dna_hash, transport_call_id,
  findings[], telemetry_refs[], anchors[],
  not_determined[]        // load-bearing -- see docs/08
}
```

Immutable, published once a voyage cell's protocol completes. **This is what
[`docs/12`](12-phase2-findings.md) already renders** — the Phase 2 page is DNA 4's read
view, built before the DNA existed.

Separate from `registry` despite both being public and permanent: different write
authority, different validation rules, and a record referencing an identity should not be
able to alter it.

---

## How they connect, given that validation cannot look across

**Registry → voyage: signed credentials, not lookups.** A registry attestor issues a
credential — a signature over *(agent key, role, transport call id)*. The joining agent
presents it as a membrane proof. `validate_agent_joining` verifies the signature against
`credential_issuers` in the DNA properties. **No network call, fully deterministic,
platform-legal.** It is the pattern ValiChord already uses with
`authorized_joining_certificate_issuer`, and here it is forced by the constraint rather
than chosen.

**Telemetry → voyage: reference by hash, verify at read time.** A `TelemetryRef` records a
`dataset_sha256`. Validation cannot confirm the attestation exists in DNA 2 — so it does
not try. Verification happens in the coordinator or by the reader, who fetches the
attestation, fetches the dataset from NOAA, and hashes it. This mirrors Nondominium's Unyt
rule, which verifies the real cross-DNA record outside validation rather than trusting a
local tag.

**Voyage → record: publish on completion**, carrying the voyage DNA hash so a reader can
confirm which network produced it.

---

## Deliberately not decided

**Whether `registry` is one global network or federated per region or per club.** One
network is simpler; federation matches how the industry actually organises. Deferred until
someone real needs to join.

**Whether parties self-host conductors or are hosted.** Self-hosting means each party
controls its own chain; hosting means the host holds the state. It changes the threat model
substantially and interacts with [`docs/13`](13-phase3-findings.md)'s "detection needs one
peer" — a host might *be* that peer.

**Countersigning for handovers.** A custody transfer is bilateral and countersigning fits,
but it is feature-gated `unstable-countersigning` with a 6-second clock-skew limit and
sessions that can need manual abandonment. Not in the first build.

---

## What this changes, and what it does not

**Changes:** [`docs/14`](14-holochain-setup.md)'s estimate assumed one DNA. Four is more
work — though `voyage` carries most of it, and its commit–reveal has tested precedent in
ValiChord's Attestation DNA.

**Does not change:** whether anyone will pay. Four well-argued DNAs are still architecture,
and the Phase 2 page has still not been shown to anyone who works a laytime desk.
