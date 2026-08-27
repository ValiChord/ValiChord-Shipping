# 27 — What Holochain 1.0 actually contains, and what to design for

Written 27 August 2026. Read [`26`](26-handover-find-a-holochain-project.md) first, including
its correction.

## Where this comes from

The public roadmap page at `holochain.org/roadmap` **stops at 0.9 and shows no 1.0 at all.**
That is misleading. The real planning lives on a public GitHub project board, which needs no
login and which anyone can re-check:

- Board: `https://github.com/orgs/holochain/projects/11`
- Filter one release: append `?filterQuery=roadmap:"__Holochain 1.0"` (two underscores for
  1.0 and 2.0, one for 0.8 and 0.9 — the underscores are just sort-order prefixes)

Everything below is read off that board on 27 August 2026. Item counts and statuses move, so
re-read before relying on any single line.

## The shape of it

| Release | Items | Theme |
|---|---|---|
| 0.7.0 | released 30 Jul 2026 | Kitsune2 integration, Iroh transport. **What we are on** |
| 0.7.1 | 13 | Backup/restore, data model consistency |
| 0.8 | 100 | **"Stabilize the HDK and support app upgrades"** |
| 0.9 | 46 | Mobile builds, per-app network infrastructure, first sharding items |
| 1.0 | 69 | Key management (Deepkey), security hardening, migrations, production infra |
| 2.0 | 14 | Countersigning repairs, pub/sub, ephemeral store |

**There is no published date for any of these.** Release cadence has been roughly one minor
version every six to twelve months (0.3.6 Dec 2024 → 0.4.4 Jul 2025 → 0.5.6 Sep 2025 →
0.6.2/0.7.0 Jul 2026). On that cadence 1.0 lands somewhere in **2028–2029**. That is my
arithmetic, not their statement, and it should be treated as a guess.

## The four things that actually matter to a vessel-record system

### 1. Sharding is not our feature, and we should stop waiting for it

The Sharding epic is in 0.9 and contains **three issues**, two of them "Awaiting
clarification":

- `#4176` Configure gossip arc clamping at runtime — *Ready for refinement*
- `#4348` Partially connected, full arc nodes — *Awaiting clarification*
- `#5372` Fix `get_by_op_type` routing to use correct op-basis location for sharding —
  *Awaiting clarification*

It is barely specified and years out. **But the more useful finding is that we do not want
it.** A per-vessel network has two to five agents and perhaps a few tens of thousands of
entries across the ship's whole life. What we want is the opposite of sharding: **every
member holds everything, always.** Full arc. That is precisely the property that makes an
entry impossible to withdraw — the manager cannot take back what four other nodes already
hold in full.

`Configure arc size clamping per cell` (`#4452`) sits in **0.8** and is the knob we care
about. Design for full replication, state it as a requirement, and treat sharding as
irrelevant to us.

See also the parked [`../../polite-shrink/`](../../polite-shrink/) work — that was about
large networks, which this is not.

### 2. Key rotation is the sleeper feature, and it is the one to actually wait for

The largest single cluster in 1.0 is Deepkey / DPKI:

- `#4138` Add DPKI call to update agent key
- `#4046` Serving agent activity for **updated and previous** agent keys
- `#4105` Combine `agent_initial_pubkey` and `agent_latest_pubkey`
- `#4126` Adapt `InstallApp` to allow for agent **and DNA** migration
- `#4128` Align DNA migration with Agent Key Update

**Over twenty-five years, people lose laptops and staff leave.** A vessel record that cannot
survive a superintendent replacing their machine is not a vessel record. Key rotation while
keeping the history attributable is not a nice-to-have for us; it is the difference between
a lifetime record and a five-year one.

This is more important to our design than sharding and warrants combined, and it is the one
genuine reason to care about 1.0 specifically.

### 3. The migration problem is real, acknowledged, and unfinished

`26` records that changing an integrity zome changes the DNA hash and creates a new empty
network. That is the strongest objection to putting a *lifetime* record on Holochain, and it
is not answered yet:

- `#4396` **SPIKE: What is needed for DNA migration** — 0.8, epic "DNA migration"
- `#4397` **SPIKE: Conductor migrations** — 1.0
- A whole "Coordinator Updates" epic in 0.8: `update_app`, manifest refactor,
  `init_upgrade` callback, capability tokens, remote calls, applying updates to clone cells

Both of the load-bearing items are still **spikes** — investigations, not implementations.

**Design consequence, and it is the main one:** keep the integrity zome as small and as
boring as humanly possible. Entry types, signatures, sequence, membership. Every rule that
can live in a coordinator zome must live there, because coordinator zomes can be swapped
without killing the network and integrity zomes cannot. This is a constraint to accept at
the start, not to discover in year three.

### 4. Warrants are maturing, but they are not what protects us

Warrants are how a peer that breaks validation rules gets blocked, with other peers learning
why. They exist today; `Warrants v2` (`#5370`) is in 0.8, and 1.0 adds `#5793` "Warrant
authorities that respond with invalid signatures on records".

Worth having. But note that **our security model barely depends on them.** We are not
detecting liars. The protection is that entries were copied to the other members when they
were written, and an append-only chain makes an absence visible. That works whether or not
anyone gets warranted. Warrants are a bonus, not a foundation — which is a good position to
be in, because they are the part still being rebuilt.

## Two corrections to things this project already believes

### Countersigning is worse than `26` implies — do not build the handover on it

`26`'s surviving point 4 says *"countersigning fits handovers, and only handovers."* A
management handover is exactly that, so this looked like the obvious place to use it.

**It is the least stable thing on the board, and its repairs are the furthest out.** Nearly
half of 2.0 — the most distant milestone published — is countersigning:

- `#4080` Enzymatic countersigning session failure rate **increases with network size**
- `#4144` Prevent changing app state during a countersigning session
- `#4680` Actions committed during countersigning sessions are served before publish
- `#4832` Countersigning must not send to participants in non-enzymatic

Add that it is still feature-gated behind `unstable-countersigning`, with a six-second
clock-skew limit and stuck sessions needing explicit abandonment.

**So: do not design the management-change ceremony as a countersigning session.** Model the
handover as ordinary signed entries from both parties. It is weaker in theory and it will
actually work.

### The membrane read hole is known and slated for 1.0

`26` notes that membrane proofs are not enforced during handshaking, so an unauthorised agent
can read briefly before being blocked. Confirmed, and tracked: `#4705` "Prevent DHT read
access until membrane proofs validated", 1.0, General Security.

Until that ships, **a brief unauthorised read is possible** — and for a fleet's defect
history that is a commercially real concern, not a theoretical one. It is a question an
insurer's IT reviewer will ask. Either accept it explicitly with the customer, or encrypt
entry contents at the application layer and treat the DHT as carrying ciphertext plus
signatures.

## Peerkit — the same foundation, a different bet

`github.com/holochain/peerkit`, with a `SPECIFICATIONS.md` that is worth reading in full.

**A TypeScript peer-to-peer data synchronisation framework**, built by the Holochain
Foundation as an explicit experiment alongside Holochain rather than a part of it. It is
libp2p-based, deliberately carries **no Rust dependency**, and layers deep validation on top
rather than building it in.

Its shape fits this problem almost uncannily well:

| What we need | What Peerkit does |
|---|---|
| Everyone holds everything | **`FullReplicationPolicy` is the MVP default** — all blobs on every peer |
| Publish at write time | Push module streams newly authored blobs to connected peers as they are authored |
| Repair after being offline | Pull module runs periodic anti-entropy over epoch boundaries with XOR hash reconciliation |
| Closed membership | **Networks are closed by default.** Every connection must present valid `NetworkAccessBytes` *before any messages are exchanged*, and rejected agents are sticky |
| Per-author ordering | Blobs carry a hash, an author `AgentId`, and a **monotonic `authoredAt` per author** |
| Identity without a registry | `AgentId` is the hex of the raw Ed25519 public key — self-describing, verified by reconstructing the key |

Note the membership row in particular. **Peerkit rejects before any messages are exchanged,
which is stronger than Holochain's behaviour today** — where, per `26`, an unauthorised agent
can join and read briefly before being warranted. That fix is a Holochain 1.0 item (`#4705`).
Peerkit has the property now.

### The catch, and it is exactly where our argument lives

Straight from the specification, listed twice as a stated design principle:

> **"Not append-only at the protocol level. Supports destructive edits for scalability and
> privacy."**

Higher layers make blobs **prunable**, including their metadata. This is a deliberate goal,
not an oversight, and it is the precise opposite of what a maintenance record needs.

Read carefully, though, the position is better than that quote alone suggests:

- **Layers 2–4 deal with immutable blobs.** Mutable state and destructive edits arrive at
  Layer 5. The MVP implements Layers 0–2 only.
- So we would live at Layer 2, with full replication, and simply never adopt pruning.
- **Append-only would be our property to build and defend**, not one we inherit: each entry
  carries its author's previous-entry hash and a sequence number, exactly as the
  [`../tools/record-gap/`](../tools/record-gap/) census assumes.
- And the guarantee we actually rely on never came from the protocol anyway. **An entry
  cannot be withdrawn because other peers already hold it** — which push-on-author plus full
  replication delivers directly.

### What it does not give us

- **No peer-enforced validation.** Nobody refuses a bad entry; validation is the app's job.
  Membership rules would be application-level and therefore weaker than a membrane proof.
- **No warrants.** No immune system, no blocking of misbehaving peers.
- **Persistence is not there yet.** The MVP ships in-memory stores; persisted backends are
  planned. The interfaces are pluggable, so this is ours to write — but it is not a box we
  can tick today.
- **It is an experiment.** 145 commits, 2 stars, 1 fork, and the Foundation describes it as
  something they will "continue to explore as capacity allows". Betting a twenty-five-year
  record on that would be reckless.

### The conclusion that matters

Peerkit does not replace the plan in `26`; it improves the middle step. The three-step
sequence becomes:

1. **Define the data model once, and make it portable.** Signed, hash-chained,
   per-author-sequenced entries. That format travels over an email attachment, over Peerkit
   blobs, or as Holochain entries without change.
2. **Peerkit for the working prototype.** TypeScript, no Rust, no conductor, full
   replication and closed networks out of the box. Far less to build than hand-rolling
   transport, far less to install than Holochain.
3. **Holochain when peer-enforced rules and key rotation start to matter** — which is when
   class societies and insurers join, and when the record has to outlive the people who
   made it.

**The portable data format is the thing to get right, and it is the thing that survives all
three.** It is also the move that has already worked once on this project: the ValiChord
attestation format found outside adopters precisely because it was a format and not a
platform. Do that again here.

## What already exists in the org that we should not rebuild

267 repositories under `github.com/holochain`, of which roughly 100 are live and the rest
archived legacy from 2019–2023. Read off the public API on 27 August 2026 (`sort=pushed`).

**These are repository descriptions and, where noted, specs — not code I have read.** Treat
each as a lead to check, not a component to assume works.

### The two that answer "but nobody will install a node"

This is the biggest practical objection to the whole design, and the org has both halves:

- **`hc-http-gw`** (Rust, active Aug 2026) — *"The Holochain HTTP Gateway for providing a way
  to bridge from the web2 world into Holochain."* A claims adviser at a P&I club, a surveyor,
  an insurer's IT department: **none of them will ever run a conductor.** A gateway means
  they read the vessel record over ordinary HTTP from an ordinary browser.
- **`kangaroo-electron`** — bundle a hApp as a standalone Electron app with a built-in
  conductor. That is how the owner and the manager get a node without knowing what a
  conductor is.

**Together they are the deployment story: Kangaroo for the two or three parties who write,
the gateway for everyone who only reads.** That split maps exactly onto who actually needs
what, and it is worth designing around from the start.

### Two that matter for this box and this way of working

- **`holochain-client-python`** (Python, 34★) — a Python client for the Conductor API. **We
  have Python here and no Rust.** This does not remove the need for a Codespace to build a
  DNA, but it means the tooling around it can be written in the language already installed.
- **`ai-tools`** — *"skills and other tools to aid in developing holochain hApps."* Given how
  this project is actually built, Holochain-specific skills are worth an hour of
  investigation before writing any zome.

### Reuse before building

- **`portal-dna`** — *"A DNA for providing cross-DHT zome function access."* [`26`](26-handover-find-a-holochain-project.md)
  records that `call_remote` does not cross DNAs. If we go per-vessel and later want a
  fleet-level view, **this is the existing answer to a constraint we already documented.**
- **`hc-cooperative-content`** — zomes providing *"patterns for collaborative content
  management."* Multi-party write permissions is our owner / manager / class problem.
- **`zome-mere-memory`** — storing large or small byte values. Our own demo already implies
  attachments: the oil sample entry references a lab report, and a turbocharger claim means
  photographs. Note that **`file-storage-zome` is archived**, so this is the live option.
- **`deepkey`** — the DPKI implementation behind the key-rotation work described above.
- **`hcSeedBundle`** (TypeScript) — seed bundle parsing and generation, i.e. key backup and
  recovery. Over twenty-five years this is not optional.
- **`rust-hdi-extensions`, `rust-hdk-extensions`, `rust-hc-crud-caps`** — the last implements
  a *"CAPS pattern (Chained, Action ID, Permalink, State-based)"*, which sounds close to the
  chained-entry model we need. Worth reading before designing our own.

### Tooling and, more usefully, showing

- **`holochain-playground`** — visualises DHT state. Being able to *show* someone the record
  replicating to the owner's node as it is written is worth more than any explanation of it.
  That is the same instinct that made the record-gap page work.
- `scaffolding`, `tryorama`, `hc-spin`, `holonix`, `wind-tunnel` — the standard build, test
  and performance kit.
- **`HOW`** — Holochain Improvement Proposals. A better place to watch direction than the
  roadmap page, which as noted above omits 1.0 entirely.

### Two cautions found while reading

- **`hc-chc-service` is archived.** CHC is the Chain Head Coordinator — the mechanism for
  coordinating one agent's source chain across devices, and so for detecting forks. The 1.0
  board still lists a Wind Tunnel scenario *"Read/write with CHC enabled"*, so the capability
  appears to live on in core even though the standalone service repo is retired. **Check its
  status before relying on it**, because multi-device access for one company is a plausible
  requirement for us.
- **`cryptographic-autonomy-license`** (250★, not archived) — the CAL. We are Apache 2.0, and
  this project has already had licence friction elsewhere. Not a recommendation, just a flag
  that the Foundation maintains a licence with different obligations to ours.

## What this means for sequencing

**Do not gate the project on 1.0.** No date is published, my estimate is 2028–29, and the
customer conversation does not need any of it — [`../tools/record-gap/`](../tools/record-gap/)
makes the argument without naming a platform.

Build in this order:

1. **Now** — the two-party version. Signed entries, append-only, copied to the owner as
   written. This needs nothing from the roadmap and can be demonstrated to a manager.
2. **0.8** — per-cell arc clamping and coordinator updates make a real Holochain version
   sensible. Integrity zome stays tiny from day one.
3. **1.0** — key rotation and the membrane read fix are what make it a *lifetime* record
   rather than a demonstration.

The honest summary: **1.0 is not a feature release we are waiting on. It is the point at
which the platform stops changing underneath a record that has to last twenty-five years.**
That is a different reason to care, and a better one.
