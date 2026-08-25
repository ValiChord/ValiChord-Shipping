# 14 — What the Holochain setup actually involves

**Short answer: you already have it. The obstacle is not setup, and it is not this
laptop. It is that Phases 1–3 are written in Python and a hApp is written in Rust.**

Checked against the ValiChord repository on 25 August 2026, not from memory.

---

## What already exists

ValiChord is a working Holochain 0.7.0 project, not a plan for one:

| | |
|---|---|
| DNAs | four — `attestation`, `governance`, `researcher_repository`, `validator_workspace` |
| Tests | 150 automated, run in CI on every push |
| Multi-node | integration tests launch up to 7 independent conductors, each with its own agent identity, source chain and DHT participation |
| Toolchain | plain `cargo install` — **no nix, no holonix, no flake** |

That last point is worth dwelling on, because it contradicts the usual assumption.
Holochain development is commonly described as requiring a nix environment. ValiChord's
does not:

```bash
rustup target add wasm32-unknown-unknown
cargo install holochain            --version 0.7.0 --locked
cargo install holochain_cli        --version 0.7.0 --locked   # the `hc` CLI
cargo install kitsune2_bootstrap_srv --version 0.5.0 --locked
```

And `setup_holochain.sh` in the ValiChord repo already automates it — Rust, the wasm
target, all three installs, PATH, and a `holochain-dev` Claude Code skill. Its own banner
reads *"ValiChord Codespace Setup"*, and it budgets **~10 minutes** for the Holochain
compile.

## Where it runs, and where it does not

**Not on this Windows laptop.** Verified: no `cargo`, no `rustc`, no `nix`, no `npm`, and
WSL is installed with no distribution. Nothing about the shipping work changes that.

**It runs where ValiChord already runs** — GitHub Codespaces (what `setup_holochain.sh`
is written for), the Oracle Ubuntu host, and CI on `ubuntu-latest`. That is the existing
workflow and Phase 3b should simply join it.

So "setting up Holochain" is not a project. It is opening a Codespace and running a
script that already exists.

---

> **Superseded by [`15-dna-architecture.md`](15-dna-architecture.md).** The sketch below
> assumed a single DNA. The design is **four** — `registry`, `telemetry`, `voyage`,
> `record` — driven by four genuinely different peer groups and by a platform constraint
> this document did not account for: validation cannot read across DNA boundaries, so the
> membrane verifies signed credentials rather than performing lookups. The effort estimate
> further down is therefore too low. Read `docs/15` for the design.

## What Phase 3b actually needs — less than first estimated

**ValiChord already implements this protocol.** From
`ValiChord/docs/Holochain_complete.md`, the Attestation DNA runs:

> **Round 1 Commit:** validator creates `CommitmentEntry` (blinded hash of their
> assessment) — written to Attestation DHT
> **Round 2 Reveal:** validator creates `RevealEntry` (actual assessment + nonce) — DHT
> validates hash matches commitment

That is precisely the shape Phase 1 built in Python. Phase 3b is therefore **reuse of a
tested pattern**, not new protocol design — a different entry payload on an existing
mechanism.

What it needs:

- **one DNA**, integrity zome plus coordinator zome
- **one entry type** — a sealed claim carrying the commitment hash, the public key, the
  signature, and the time floor
- **each party is an agent**, with its own source chain and identity
- **sweettest** for verification, matching how ValiChord is already tested

A few hundred lines of Rust, and much of the logic has a working precedent to copy.

> **What it does not buy, corrected.** An earlier draft claimed each agent's source chain
> would supply trustworthy ordering without any external witness. That is wrong — fork
> detection is performed by *peers* holding the `RegisterAgentActivity` replica, so a
> single-operator hApp gets no adversarial ordering guarantee at all. Holochain action
> timestamps are also self-reported. **External time anchors remain necessary whatever the
> substrate.** See the retraction in [`docs/13`](13-phase3-findings.md).

## The actual obstacle — two languages

This is the cost nobody would guess from the setup instructions.

**Phases 1–3 are Python.** The parties, the commitments, the Ed25519 signing, the
verification, the AIS bracketing, the report generator. All of it.

**A hApp is Rust.** Source chains, countersigning, and the DHT live inside a conductor.

Bridging them means one of three things, and the choice matters more than the setup:

**Rewrite the party logic in Rust.** Cleanest architecturally, and everything ends up in
one place. Costs the most, and throws away working Python that is doing its job.

**Drive the conductor from Python over its websocket API.** Keeps Phases 1–3 intact and
adds a thin client. Means maintaining a message-encoding layer against an API that
changes between Holochain versions — and 0.6→0.6.1 alone broke the transport and the
HDK.

**Split by role.** The hApp owns the commit log and nothing else; Python keeps the AIS
work, the verification, and the report. They meet at a file — the hApp exports its chain
state, Python reads it. Ugly at the seam, but each side stays in the language that suits
it, and neither has to know about the other.

The third is the least elegant and probably the right one for a demonstrator. It also
degrades gracefully: if the Holochain side is unavailable, Phases 1–3 still run.

---

## An honest estimate

| | |
|---|---|
| Environment | **~15 minutes** — open a Codespace, run `setup_holochain.sh`, ~10 min of which is the compile |
| The zome | **a day or two**, given the `holochain-dev` skill already in the repo |
| The bridge | **the real work** — genuinely unknown until the approach is chosen, and the most likely place to lose a week |
| This laptop | **not viable**, and no reason to make it so |

## What Phase 3b would and would not buy

**Would:** agent-centric identity, with each party holding its own chain and key.
Countersigning, so a handover commits for both parties or neither — with the caveat that
it is feature-gated `unstable-countersigning` and time-bounded. Reuse of a commit–reveal
mechanism ValiChord already runs in production. And — the strategic point from
[`docs/13`](13-phase3-findings.md) — it makes this a ValiChord artefact rather than an
orphan that happens to share an author.

**Would not:** trustworthy ordering on its own. Fork detection needs peers who are not
you; a single-operator hApp has none, and Holochain's own action timestamps are
self-reported. External anchors stay necessary regardless, and Phase 3 already has them
working.

**Would not:** independent witnessing. Same reason — it needs peers who are not you,
which is a commercial problem rather than a technical one.

**Would not:** move the question that has been unanswered since
[`docs/04`](04-strategic-assessment.md) — whether anyone will pay.

---

## Recommendation

**Do not do Phase 3b before showing someone the Phase 2 page.**

Not because the architecture is wrong — [`docs/13`](13-phase3-findings.md) concedes it is
right, and that the earlier dismissal was too sweeping. But the setup is cheap and stays
cheap; it will be exactly as easy in a month. The demonstrator already runs, already uses
real data, and already produces something a claims person could read.

Phase 3b makes the artefact architecturally honest. It does not make it more persuasive
to the one audience that matters, and that audience has still not seen it.
