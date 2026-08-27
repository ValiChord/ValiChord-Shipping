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
missing, and when."** In a claim, the second is worth a great deal even when the content is
gone, because it establishes that the absence is not the holder's doing.

This works because each entry was published when it was written. A format alone does not
make anyone publish — that is the transport's job, and the reason for the sequencing here.

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
