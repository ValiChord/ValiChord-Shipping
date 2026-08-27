# Asset Record Entry, version 0.1

**Status: draft. Nothing depends on this yet, and it has no outside adopters.**

A file format for one event in the life of a physical asset, signed by whoever recorded it,
chained so that a removed entry leaves a hole you can point at.

It is designed to be the *same file* whether it travels as an email attachment, a blob in a
peer-to-peer store, or an entry in a Holochain DHT. That portability is the whole point: the
platform question stays open, and nothing built on this format has to be thrown away when it
is answered.

## Why a format and not a product

The problem this comes from is documented in
[`../docs/28`](../docs/28-prior-art-and-the-general-case.md): a physical asset outlives the
organisations that maintain it, but the maintenance record belongs to whichever organisation
happened to hold the software. When they leave, it goes.

Aviation prices that at 10–20% of an aircraft's value. UK law now mandates it for higher-risk
buildings. The EU mandates it for batteries from February 2027. In shipping, lubrication
failure and incorrect maintenance are the top two causes of main engine damage — a lube oil
failure claim averages USD 926,000 — and both are exactly what a maintenance record either
establishes or fails to.

**A format can be adopted by one party without anyone's permission.** A platform cannot.

## Prior art, and why this is small

**Nothing in this format is novel, and it would be dishonest to imply otherwise.** Signed,
hash-chained, per-author statements about a thing are a well-worn pattern with several mature
implementations:

- **GS1 EPCIS** — an international standard for visibility events about physical objects
  across their lifecycle, structured as what / when / where / why, and explicitly covering
  fixed and returnable assets. It is more complete than this, it is widely deployed, and it
  is the obvious thing to adopt if a heavier standard is acceptable.
- **IETF SCITT** (Supply Chain Integrity, Transparency and Trust) — an active working group
  building exactly this: signed statements made non-repudiable, immutable and auditable
  through transparency services.
- **W3C Verifiable Credentials**, **in-toto / SLSA attestations**, **C2PA**, **Certificate
  Transparency**, and **git** all solve overlapping pieces.

So this document is not a claim to have invented anything. It is **the smallest thing that
carries the one property we actually need** — that a missing entry is provable — with no
registry, no server, no schema negotiation and no membership in a standards body. If it grows
past a few pages, adopt EPCIS instead.

**The corollary matters more than the format.** If the format was never the hard part — and
it plainly was not, given how many exist — then the reason asset records still do not survive
their custodians lies somewhere else entirely: in who is willing to write, and who receives a
copy at the moment of writing. That is an incentive and distribution problem, and no
specification solves it. See [`../docs/28`](../docs/28-prior-art-and-the-general-case.md).

## Design rules

1. **The format carries no domain vocabulary.** It knows about assets, authors, order and
   signatures. It does not know what a turbocharger is. Domain content lives in `body`,
   which this specification treats as opaque.
2. **No floating-point numbers anywhere.** This removes the hard part of canonical
   serialisation, and every quantity worth recording (running hours, cycles, counts) is an
   integer or a string.
3. **An entry is immutable.** There is no edit and no delete. A correction is a new entry
   that references the one it corrects.
4. **Verifiable with nothing but a public key.** No network, no server, no registry.

## The entry

```json
{
  "fmt": "asset-record/0.1",
  "asset": { "scheme": "imo", "id": "0000000" },
  "author": "3v0kQ2p...",
  "seq": 47,
  "prev": "sha256:9f2c...",
  "authored_at": "2025-01-09T11:04:00Z",
  "body": { },
  "attachments": [],
  "sig": "base64url..."
}
```

| Field | Required | Meaning |
|---|---|---|
| `fmt` | yes | Exactly `asset-record/0.1` |
| `asset` | yes | What this entry is about. `scheme` names the identifier space (`imo`, `easa-msn`, `uprn`, `serial`), `id` is the identifier within it |
| `author` | yes | The signer's Ed25519 public key, 32 bytes, base64url unpadded. **The key is the identity** — there is no registry to consult |
| `seq` | yes | This author's entry number for this asset. Starts at 1, increments by exactly 1, never reused |
| `prev` | yes | `sha256:` plus hex digest of the canonical bytes of this author's entry at `seq - 1`. `null` when `seq` is 1 |
| `authored_at` | yes | RFC 3339 UTC, `Z`, second precision. **Self-reported and not evidence of time** — see below |
| `body` | yes | The domain payload. Opaque here |
| `attachments` | no | Content-addressed references to files held elsewhere |
| `sig` | yes | Ed25519 signature over the canonical bytes of every other field, base64url unpadded |

### Attachments

An attachment names a file without containing it, so a 40MB photograph of a failed
turbocharger does not have to travel with the record:

```json
{ "hash": "sha256:1a2b...", "media_type": "image/jpeg", "name": "tc-rotor-contact.jpg" }
```

The hash is over the file's bytes. Whether the bytes are available is a separate question
from whether the record is intact — which is deliberate, because in practice the record
survives and the attachments do not.

## Canonical form

To hash or sign an entry:

1. Remove `sig`.
2. Serialise as JSON with **keys sorted** at every level, **no whitespace**, UTF-8, no
   trailing newline.
3. The result is the canonical bytes.

Because floats are forbidden, this is deterministic across languages and is compatible with
RFC 8785 for the value types the format permits. Implementations must reject any entry
containing a float.

## What this buys you: absence has a shape

An author's entries form a chain. Entry 47 contains the hash of entry 46, which contains the
hash of 45.

So if a holder has entries 1–46 and 48, three things are true and all of them are checkable
offline:

- **Something is missing.** `seq` 47 is absent.
- **It cannot be denied.** Entry 48's `prev` is the hash of an entry the holder does not
  have, so 47 existed and its content hashed to a known value.
- **It cannot be forged after the fact.** Any replacement for 47 must hash to that value and
  carry the author's signature.

**That is the difference between "we do not have the records" and "we know exactly what is
missing."** In a claim, the second is worth a great deal even when the content is gone,
because it establishes that the absence is not the holder's doing.

### Three limits on that claim, stated here rather than in the small print

**"When" means order, not time.** An earlier draft of this section said "missing, and when",
which over-sold it. The chain orders **one author's own entries relative to each other**. It
says nothing about wall-clock time, and `authored_at` is self-reported. If a claim depends on
"this was recorded *before* the incident", the format does not carry it — anchor it
externally.

**Only internal gaps have a shape. The tail does not.** A chain ending at `seq` 11 is
cryptographically perfect whether or not `seq` 12 was written and dropped. So the most
damaging entry — the one written last, showing the fault — can be withheld with no
cryptographic footprint. Detecting that needs either publication at write time (so the
counterparty already holds it) or an expectation of regular entries, so that **silence is
itself evidence**. Neither is in v0.1.

**A chain that was never shared proves nothing to a later holder.** The absence property
depends entirely on someone else having received the entries. A format cannot make anyone
publish; that is the transport's job. This is the reason the sequencing exists, and it is
also the reason the format alone is not a product.

## What this format does not do

Stated plainly, because a specification that only lists its strengths is advertising.

- **It does not make an entry true.** A signature proves who wrote it, not that they were
  right or honest. This is custody, not verification.
- **`authored_at` is self-reported.** An author can backdate. The chain constrains *order*,
  not *time*. If wall-clock time matters, anchor it externally — the tooling in
  [`../tools/phase3/`](../tools/phase3/) already does this with OpenTimestamps.
- **It does not stop a second private record.** It only means the entries that *were* written
  cannot later be withdrawn.
- **It is forward-only.** The first holder to adopt it still inherits whatever blank history
  came before.
- **Key loss is unsolved at version 0.1.** The author's key is their identity, so rotation
  needs a link between old and new keys. That is the single largest gap in this draft, and
  it matters most for exactly the long-lived assets this exists for.

## Mapping onto the three transports

| | Email attachment | Peer-to-peer blob | Holochain |
|---|---|---|---|
| Entry is | a `.json` file | one authored blob | one entry + action |
| `author` | the key in the file | the peer's agent key | the agent key |
| `seq` / `prev` | in the file | in the file | in the file, and mirrored by the source chain |
| Published when | someone sends it | on author, to all peers | on commit, to the DHT |

The format does not change across the columns. **Only the answer to "who else has a copy, and
when did they get it" changes** — which is the thing actually being bought.

## Validating

```bash
python spec/validate.py spec/example-entry.json
```

`validate.py` checks structure, canonical form, chain linkage across a sequence, the float
prohibition, and Ed25519 signatures. It is roughly two hundred lines and depends only on
`cryptography`. Treat it as the specification's executable half — where the prose and the
validator disagree, **the validator is wrong and should be fixed**, but the disagreement is a
bug in this document too.

## Read this before the backlog: the backlog is a trigger, not a to-do list

A fourth red team made the observation that matters most, and it is about the **trajectory**
rather than any single item.

Take the backlog below at face value — key rotation, detachable bodies with hash linkage,
`causal_refs`, key-to-role delegation, `same_as`/`supersedes`, `corrects`, counter-signed
receipts — and this stops being a small JSON format. It becomes **an ad-hoc, unstandardised
reimplementation of IETF SCITT plus W3C Data Integrity**, without their formal proofs, their
tooling or their SDKs, and without the one advantage that justified not using them: being
small.

**This document already tells you what to do about that.** The design rules say: *if it grows
past a few pages, adopt EPCIS instead.* The backlog below breaks that rule and I did not
notice until it was pointed out.

So the backlog is **a trip-wire**. Each item is a reason to reconsider adopting a standard,
not a feature to add. Implement two or three and the honest move is to stop and either align
with SCITT — probably as a profile over COSE-signed statements, keeping only the domain
specifics — or write down explicitly why SCITT's envelopes were rejected. **Do not walk to a
standard one bespoke header field at a time.**

### The other findings from that fourth pass

**Detachable bodies create bad-faith withholding disguised as privacy.** This is the strongest
argument against the redaction fix listed as blocking below. If the body detaches, a manager
who recorded severe bearing wear can publish the header, keep the payload, and later say "we
purged it under GDPR." **Offline verification cannot distinguish lawful redaction from
never-disclosed.** The fix is not to abandon detachability but to make the signed header
declare *what kind* of record was redacted — a `payload_type`, or better a Merkleised body so
a crew member's name can be zeroised while the bearing clearance survives. Note this is also
the same family as tail truncation: the format cannot tell absence-by-right from
absence-by-bad-faith.

**In-chain key rotation cannot survive compromise or loss, only planned handover.** A dual-
signed `rotate` entry handles the orderly case. It fails twice otherwise. If a key is stolen,
the thief can sign a valid rotation to their own key and no verifier can tell which party
rotated — the real author is locked out of their own chain permanently. If a key is lost, the
dual signature is impossible and the chain simply stops, forcing a new chain at `seq` 1 with
no continuity to genesis. **Both need an external trust anchor.** Worth noting for the
transport question: Holochain's DPKI is exactly such an anchor — but not before 1.0.

**History is not state, and opacity destroys the interoperability it was meant to protect.**
A causal DAG proves what happened; it does not answer *"is this engine cleared for
operation?"*. If one author logs "cracked liner" and another "within tolerance", the DAG shows
both and nothing decides which governs. Because `body` is fully opaque, **100% of conflict
resolution is pushed into proprietary application logic** — which defeats the cross-system
interoperability that opacity was chosen for. EPCIS solved this with event types and a
business-step vocabulary. We did not, and that is another point on the scoreboard for adopting
rather than extending.

**Organisational keys are an anonymous shield. This corrects earlier advice in this file.**
The backlog below says to bind keys to an organisation rather than an individual, on the
grounds that it is easier and closer to what matters. **That was wrong.** A company-level key
ends up in a CI/CD pipeline or an ERP sync agent, and the defence writes itself: *"an
automated script logged that from a faulty database trigger; no human certified it."* Maritime
and aviation both rest on the **personal licence** of the Chief Engineer or the A&P mechanic.
The answer is probably an individual signature plus an organisational delegation — which, note,
is one more item making the format bigger.

**"The same file across transports" is only true of the entry, not of the proof.** A
counterparty receipt cannot live inside the signed entry without changing its hash. So there
are two artefacts: the raw entry and a proof bundle of receipts and timestamps. Portability at
the entry layer says nothing about the proof layer — and **the absence property, which is the
entire value, lives in the proof bundle.** The transport table below is therefore weaker than
it looks and should be read as covering the entry only.

## The v0.2 backlog, from three independent red teams

v0.1 was red-teamed by Gemini and by Grok, alongside my own pass. **All three converged on
the same top item, and none of the three challenged whether anyone wants this** — which is
worth knowing about what a technical red team does and does not give you.

Ordered by whether it blocks real use.

### Blocking

**Key rotation.** Grok's framing is right and stronger than the draft's: this is not the
largest gap, it is *existential*. Long-lived assets outlive key material and the people
holding it, so "the key is the identity" gives the format a hard cliff. Needs care — does the
new key continue the sequence or start a new chain, how does a reader discover the rotation,
what happens to `seq`. **Until this exists the format cannot serve the assets that motivate
it.**

**Detachable body, for redaction.** Gemini's best catch and a v0.1 design error. Crew injury
reports, PII, commercial pricing and export-controlled detail all end up in free-text
remarks. Because `prev` covers the canonical bytes of `body`, that content can never be
scrubbed without destroying the chain — forcing a choice between breaking history and a
continuing regulatory breach. **Fix: chain over a `body_hash`, keep `body` detachable**, so
the payload can be zeroized while the structure survives.

**Tail truncation.** See above. Needs expected-cadence entries, counter-signed receipts, or
both.

### Important

**Key-to-role attestation.** A raw Ed25519 key has no legal standing. In a USD 926,000
arbitration, counsel will say the key was on a shared bridge laptop. Bind the key to an
*organisation* (the manager) rather than an individual engineer — easier, and closer to what
actually matters here.

**Asset identity continuity.** Ships are renamed and reflagged; other schemes reuse serial
numbers. IMO numbers happen to be stable, which flatters our example. Probably needs a
first-class `same_as` / `supersedes` relation rather than letting `asset` mutate mid-chain.

**Cross-chain causal links.** Author B logs "inspected, no issues" an hour after author A logs
"repaired crack", and nothing proves the order. Both red teams proposed the same fix: an
optional `causal_refs` naming the latest known hashes of other authors' chains.

**Bounds.** `body` is unbounded and attachments carry no `size`, so a reader cannot tell a
10KB lab report from a 10GB video before fetching. (Grok's related DoS concern is overstated
— Ed25519 verification is ~50µs, so 50,000 entries is a couple of seconds, and it streams.
The missing bounds are real regardless.)

**Merged views.** Each author keeps their own chain, so a reader wanting "everything known
about this hull" must discover, fetch and merge several. Grok is right that in insurance,
sale and regulatory contexts **the merged view is the product people actually need**, and
v0.1 pushes the hardest part into "an application question".

### Corrections to make now, not later

Some of these are already handled and were simply undocumented:

- **Duplicate JSON keys** must be rejected, not silently collapsed — two parsers can disagree
  about which value was signed. *Fixed in `validate.py`.*
- **Strict UTF-8**, and integers only, including rejecting scientific notation that parsers
  return as floats. *Already covered by the float ban; now tested.*
- **Unknown fields are rejected.** That was the validator's behaviour and an undocumented
  decision. It is deliberate — silent tolerance lets meaning drift — but it means forward
  compatibility must come through `fmt`.
- **A chain starting above `seq` 1** is reported as a finding, so a reader knows the history
  is not complete from genesis. *Already implemented.*
- **`corrects` should be a first-class field** rather than a convention inside `body`, so the
  relationship is machine-checkable.

### One that changes the architecture, not the format

**Holochain would give two sources of truth.** Holochain already has its own source chain and
action model. Carrying `seq` and `prev` *inside* the entry while the source chain also orders
it means two orderings that can diverge. Neither red team was told this was the intended
target and both flagged it independently. The likely answer is that the in-entry chain is
authoritative and the source chain is a coincidence of transport — but it needs deciding
before anything is built, not after.

## Open questions for version 0.2

1. **Key rotation.** The largest gap. Probably a `rotate` entry signed by both old and new
   keys.
2. **Should `asset` be allowed to change?** Ships are renamed and reflagged; IMO numbers are
   not reissued, but not every asset class has an IMO number.
3. **Corrections.** A `corrects` field referencing a prior entry, or leave it to `body`.
4. **Should the author declare who they are acting for?** The manager writes, but the owner
   owns. That relationship is real and currently unrepresented.
5. **Multiple authors, one asset.** Handled today by each author keeping their own chain.
   Whether a reader needs a merged view is an application question, for now.
