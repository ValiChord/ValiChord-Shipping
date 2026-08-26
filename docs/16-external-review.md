# 16 — External review: what survives, what does not, and what to do next

**Verdict: Phases 0–3 and [`docs/08`](08-external-evidence-and-the-real-gap.md)–[`docs/13`](13-phase3-findings.md)
are sound and should stand. [`docs/15`](15-dna-architecture.md) is where the project turns
away from its own conclusions, and the evidence for that is internal to this repository.**

An independent review commissioned 26 August 2026, deliberately conducted by a session
holding none of the prior context. Findings are separated below by how each was
established, following this repository's existing convention.

---

## Method, and what that is worth

| How established | What it covers here |
|---|---|
| **Verified — by hand** | Holochain platform behaviour, read from `developer.holochain.org` and `docs.rs/hdi`; the ValiChord code quoted in Part 4; grant call status, read from the funders' own pages |
| **Verified — delegated, spot-checked** | The `tools/` code reads in Part 3 and the ValiChord survey in Part 4, produced by separate read-only sessions with file and line references. Two claims were re-read by hand after one delegated finding proved wrong — see the correction in Part 2 |
| **Derived** | The diagnosis in Part 1, drawn by comparing this repository's documents and commit history against each other |
| **Inference** | The proposal in Part 7. Labelled as such: it has not been run |

**One delegated finding was wrong and was caught.** A first pass reported that signature
verification is unavailable inside Holochain validation, resting on a code comment in
ValiChord. Checking the crate documentation directly showed the opposite. The wrong
version had already been acted on before it was corrected. Recorded because it is the same
failure mode `docs/08` warns about — an AI-surfaced claim that reads plausibly and is not
true — and because it changed a conclusion in this document rather than a detail.

**A second claim in this document was also wrong, and is corrected in place.** Part 3
originally said the Phase 3 ceiling could be fixed by parsing the OpenTimestamps calendar
receipts, because they carry signed timestamps. They do not. The finding survives; the
proposed remedy did not, and the correction is written into Part 3 rather than quietly
edited out. Two errors in one review, both from asserting before checking, is the argument
of Part 1 turned on the reviewer.

---

## Part 1 — The direction, and the diagnosis

### What is right

`docs/08`'s separation of **backdating** from **anchoring** is the sharpest reasoning in
the repository, and its refusal of the adjudication output — `financialImpactUSD`,
`confidenceScore: 0.99` — is correct for the reason it gives. Whether a vessel was an
"arrived ship" is why London arbitration exists.

[`docs/10`](10-phase0-findings.md) is the strongest artefact here. Its numbers were
regenerated from the real NOAA files during this review and reproduced exactly: geofence
median 70 s, p90 71 s, n=244; 290,276 inter-fix intervals; 0.112% exceeding fifteen
minutes. Nothing was rounded in its favour.

`docs/13` is the best-argued document, and it reaches two conclusions the rest of the
project should be built on:

- *"Detection needs one peer, not an industry."*
- *"In a bilateral handover, the counterparty **is** the peer."*

### What went wrong, and where

Three documents in sequence say the next action is human, not technical:

| Where | What it says |
|---|---|
| `docs/13`, closing line | *"The next useful action is not Phase 4. It is showing this to one person who works cargo claims or a laytime desk."* |
| [`docs/14`](14-holochain-setup.md), Recommendation | *"Do not do Phase 3b before showing someone the Phase 2 page."* |
| [`docs/09`](09-demo-plan.md), Risks | *"Scope creep back into a platform. Every previous attempt in this space became a platform and died."* |

`docs/15` then designs Phase 3b in full, marks `docs/14` superseded, and declares its
effort estimate too low. The Phase 2 page has still not been shown to anyone.

**The commit history records the swing directly.** `9e7d7e4` — *"Design this project's own
DNAs: two, not four"* — is immediately followed by `112b570` — *"Four DNAs: registry,
telemetry, voyage, record."* Same day, reversed.

**Derived: this is anchoring on the parent project, not reasoning from requirements.**
ValiChord has four DNAs. `docs/15` arrives at four and pre-emptively defends the
coincidence in its own text. The external material reviewed alongside it does the same
thing independently — Gemini's validator prompt places the agent *"inside DNA 2 (Validator
Workspace)"*, mapping shipping onto ValiChord's existing four-DNA layout without being
asked to. Two systems reaching four because the parent has four is one bias observed
twice, not corroboration.

**The strongest single tell:** `docs/15` is the only document in the sequence with no kill
criterion. Every other one names what would stop it.

### The instruction that produced this, which was a good instruction

The operator's standing brief was to avoid recruiting people at this stage and to be
creative about routing around them. `docs/13` opens by quoting it almost verbatim and
answers it well — drand, OpenTimestamps, zero humans. Phases 0–3 exist because of that
push. A weaker constraint would have produced a plan stalled behind an introduction.

**But it removed every alternative to `docs/15` rather than pointing at it.** Under "no
people," architecture is the only work a solo operator can do indefinitely without
permission. A process that must keep producing will produce the thing it can produce
alone.

**And `docs/15` does not honour the constraint anyway — it defers it.** `docs/13` got the
requirement down to *one* person. `docs/15` reintroduces a registry the industry joins,
oracle operators, credential issuers, and four authorised parties per transport call.
Deferred people read as no people. They are not.

**Recorded for reuse:** *"find a way around X"* will essentially never return *"there is no
way around X."* The instruction needs an expiry condition attached. `docs/13` and `docs/14`
both reached that point and said so; nothing was listening for a stop.

---

## Part 2 — `docs/15`, checked against the platform

Each finding below was read from Holochain's own documentation, not from memory.

### What survives, including one thing this review initially got wrong

**The core constraint is correctly stated.** Validation must be deterministic —
*"Validation rules must always yield the same true/false outcome for a given operation
regardless of who is validating them and when"* — and dependencies *"must be addressable,
retrievable from the same DHT."* The four `must_get_*` functions are the deterministic
retrieval set. `docs/15` has this right.

**`call_remote` across DNAs is correctly ruled out.** *"Bridging between different cells
only happens within one agent's hApp instance, and remote calls only happen between two
agents in one DNA's network."*

**Credential verification at validation time is legal, and this review first said it was
not.** `hdi::ed25519` exports `verify_signature` and `verify_signature_raw`. Signature
checking is deterministic and is available to integrity zomes. **`docs/15`'s central
mechanism — a signed credential verified against `credential_issuers` in DNA properties,
with no network call — is sound.** The correction matters because the opposite claim was
briefed before it was checked.

### Finding 1 — the precedent `docs/14` relies on does not exist

`docs/15` lists *"a reveal must hash to its commitment"* as an integrity rule, and
`docs/14` calls Phase 3b *"reuse of a tested pattern"* on the strength of ValiChord's
Attestation DNA.

**Verified by hand:** `attestation_integrity/Cargo.toml` has no `sha2` dependency and the
integrity zome contains no SHA-256 anywhere. The check lives in
`attestation_coordinator/src/lib.rs:284-302`, and is skipped entirely when the joining
issuer key and the nonce are both empty. Its own inline comment claims the flow is
*"enforced on-chain, not just by policy"* — coordinator code is not DHT validation, and a
modified hApp bypasses it.

The mechanism is real and tested. It is not validated by peers, and the precedent being
cited does not do the thing being claimed of it. This is the pattern `docs/08` names: our
documents describe intent.

### Finding 2 — per-voyage clones destroy the deterrent `docs/13` is built on

**A cell is a DNA–agent pair, and each cell has its own source chain.** Cloning per
transport call therefore gives every party a fresh chain each voyage. There is no
cross-voyage record.

That is in direct tension with `docs/13`'s economics:

> *"A carrier caught backdating one Notice of Readiness has not lost one claim — every
> other NOR it has filed becomes worth re-examining."*

> *"This permanence is not a secondary safeguard — it is the primary deterrent, and it gets
> stronger the longer the system runs."*

Contagion across claims requires a persistent network in which the same key writes voyage
after voyage and peers hold the accumulated record. `docs/15`'s architecture resets that
every port call.

**And the data does not survive the cell.** Holochain retains a *disabled* clone's data,
but *"Holochain will clean up its data when the hApp is uninstalled."* `docs/15` gives
`voyage` a *"bounded lifetime — ends with the claim window."* English limitation periods
for contract claims run six years. The evidence would be gone before the arbitration that
needs it.

### Finding 3 — the network seed alone does not put parties in the same cell

`docs/15` states that `network_seed = hash(transport_call_id)` means *"any party holding
the voyage reference computes the same cell."*

Properties are DNA modifiers too, and *"because it's a DNA modifier, it changes the DNA
hash, which results in a new network."* The properties include the entire
`authorised_parties` map. Every party must therefore serialise it byte-identically or land
in separate networks. The voyage reference has to be the full property set, or its hash —
not the transport call ID.

### Finding 4 — DNA 4 cannot be validated, by `docs/15`'s own argument

`docs/15` applies the cross-DNA constraint to `registry → voyage` and then does not apply
it to `voyage → record`. `record` is open-write with no membrane, and validation there
cannot confirm that a referenced voyage cell exists or that its parties committed anything.
As specified, anyone can publish a `DiscrepancyRecord` about any voyage.

The schema carries `findings[]`, `telemetry_refs[]` and `anchors[]`, and no party
signatures — so a reader cannot verify it offline either. That is fixable by carrying the
parties' signatures in the record, and it is not currently in the design.

### Finding 5 — bridge calls are the missing mechanism, not a gap

`docs/15` correctly says validation cannot reach DNA 2, and correctly moves telemetry
verification to *"the coordinator or by the reader."* It does not name how: `call`
(bridging) works between cells within one agent's own hApp instance. That is the
mechanism, and it should be written down before someone re-derives the constraint as a
blocker.

### Finding 6 — the membrane is leakier than presented

`docs/13` already quotes the platform caveat: *"Membrane proof checking is currently only
enforced via normal validation, not during handshaking, so unauthorised agents are able to
join a network and access it for a short time before being warranted and blocked."*
Holochain's own documentation adds that *"the membrane proof record can't be
self-validated... because it's written before the agent joins the network."*

`docs/15` does not carry this across. For a DNA whose entire purpose is that only the
parties can see the sealed claims, a window of readable access by an unauthorised joiner is
a material property, not a footnote.

### Finding 7 — the cloning precedent is Nondominium's, not ValiChord's

**Verified:** ValiChord contains no `create_clone_cell`, no `clone_limit`, and no
`CellProvisioning::CloneOnly`. All roles in all three hApp manifests use
`provisioning: { strategy: create }`. `docs/15`'s claim that the pattern is *"proven rather
than novel"* cites Nondominium at `clone_limit: 512`, which was not verified in this
review. Whatever its status there, `docs/14`'s comfort that Phase 3b is reuse of tested
ValiChord machinery does not extend to cloning.

---

## Part 3 — The code, against what the documents claim

Delegated read with file and line references; the Phase 0 aggregate was re-executed.

### Materially weaker than claimed

**The Phase 3 ceiling is the committing machine's own clock.** `phase3.py:77` sets
`anchored_at = int(time.time())` and `:91` computes the interval width from it. The record
then asserts (`phase3.py:104-106`, rendered at `example_output/witnessed_record.json:75`)
that *"the commitment provably exists somewhere inside this window and nowhere outside
it."*

That is not true as implemented. `bitcoinConfirmed` is a hardcoded `False`
(`witness.py:143`), no `.ots` file is written, and the calendar receipts are stored as hex
blobs that nothing parses.

**This is the finding that matters most in Part 3**, because it undercuts the argument
`docs/13` is most proud of. `docs/13` names one attack it cannot refuse — a genuine but
stale drand round — and argues that *interval width* exposes it: 9 seconds honest against
86,409 backdating. If the top of the interval is self-reported, a backdating party sets
both ends and the width proves nothing.

**The remedy first proposed in this document was wrong, and is corrected here.** It said the
calendar receipts already carry signed timestamps and merely go unread. They do not. An
OpenTimestamps calendar returns a `PendingAttestation`, whose own definition is explicit:
*"Nothing other than the URI is recorded, nor is there provision made to add extra metadata
(other than the URI) in future upgrades."* There is no time and no calendar signature in it.

**`docs/13` understood this correctly** — *"The ceiling is a promise at first... Confirmation
takes hours"* — so the defect is narrower than first stated. It is not a misunderstanding of
OpenTimestamps. It is that `phase3.py` computes the interval from the local clock and then
the record's prose claims a proven bound the code has not established.

Two real fixes, either of which works:

- **Complete the upgrade path.** Write `.ots` files, and upgrade once Bitcoin confirms. That
  yields a `BitcoinBlockHeaderAttestation` carrying a block height — a genuine, independent
  ceiling. Costs hours of waiting, not effort.
- **Add an RFC 3161 timestamp authority.** Returns a signed time token immediately.
  **`docs/13` already argued for this** — legal recognition, eIDAS presumption, no blockchain
  framing — and recorded that the code was unchanged. It still is.

> ### ✅ Both were done, and the second is now the default — 26 August 2026
>
> The first fix shipped `.ots` files and `upgrade.py`. Ceri John then asked whether Bitcoin
> was necessary at all, which turned out to be the better question.
>
> Phase 3 now takes its ceiling from **three independent RFC 3161 authorities in three
> jurisdictions** — DigiCert (US), FreeTSA (DE), BOSA (BE) — all three granting on the live
> run in about a second. Bitcoin sits behind `VALICHORD_OTS=1`.
>
> **This review framed it as presentation. It was correctness.** With a Bitcoin ceiling
> hours away there was no interval at all in the meantime, and interval width is the only
> thing that exposes `docs/13`'s unrefused attack. The negative control now *measures* that
> attack instead of describing it: **11 seconds honest against 86,412 backdated**, both ends
> set by parties this project does not operate.
>
> This is a third place where the review's own reasoning was weaker than the thing it was
> reviewing. `docs/13` had already argued for RFC 3161 on its own merits and simply never
> acted on it.

Until one is done, the record should say *"floor → self-reported anchoring time, with three
calendar receipts pending"* and nothing stronger.

**Phase 1 is partly circular.** The PORT_AUTHORITY and TERMINAL_OPERATOR payloads are
constructed *from* the telemetry-derived events (`demo.py:135`, `demo.py:144`) and then
checked against that same track, returning `CONSISTENT_WITH_TELEMETRY` by construction.
Only the injected carrier discrepancy (`demo.py:117`) is a real comparison.
[`docs/12`](12-phase2-findings.md) concedes *"one case, one vessel, one port"* but not
this. A technically literate counterparty will notice, which is precisely the risk
`docs/09` names under data honesty.

### Smaller, all worth fixing before anything is sent

| Issue | Where |
|---|---|
| `verify_floor` string-compares drand against a re-fetch of the same API — no BLS verification against the chain key, despite `docs/13` describing it as threshold-signed | `witness.py:103-105` |
| `docs/13` reports the interval as 28 seconds in one place and 9 seconds in another, from two different runs, presented as one result | `docs/13` |
| Ed25519 keys are generated fresh per run, so signatures bind to no persistent organisational identity | `demo.py:47` |
| drand genesis time hardcoded rather than read from `chain.get("genesis_time")` as `witness.py:80` does | `negative_control.py:75` |
| Negative-control attack 2 calls `verify_floor(None)` and exercises a guard clause, not the pipeline | `negative_control.py:49` |
| `claimedFacilityTypeCode` is rendered into the report but never evaluated — a berth claim 3.52 nm from the port reference goes untested | `render.py:134`, `demo.py:179-180` |

### Confirmed sound

Phase 0 downloads real NOAA bulk AIS and computes every published figure. Phase 1's Ed25519
is genuine `cryptography` with a real four-assertion tamper test including a forged-key
attack. Phase 2 derives every rendered value from Phase 1 output. Phase 3 makes real
network calls to drand and to three OpenTimestamps calendars, and its fourth
negative-control attack deliberately carries no assertion because the point is that it
succeeds. That is more honest than most demonstrator code.

**There is no Rust or Holochain code in this repository, in the working tree or anywhere in
its history.** The README says so; recorded here because `docs/14` and `docs/15` read as
though a build is underway.

---

## Part 4 — A bug in ValiChord, found on the way

**Verified by hand.** `attestation_integrity/src/lib.rs` carries this, twice:

> *"`verify_signature` is an HDK host function that is NOT available in HDI integrity
> zomes."*

**The premise is false.** `hdi::ed25519` exports `verify_signature` and
`verify_signature_raw`.

The consequence is architectural. Believing it could not check the signature, the integrity
zome performs a length check only — the proof must be at least 64 bytes — and the real
Ed25519 verification against the DNA-properties issuer key was moved into the coordinator's
`init()`. So ValiChord's membrane is enforced by the honest code path rather than by
validators, when it need not be.

**This should be raised in the ValiChord repository, not here.** It is worth noting that
this is a second instance of the same class as Finding 1: both the commit-reveal hash check
and the membrane check sit in coordinator code and are described as though they were
validated by peers.

For related context, `ValiChord/PROJECT_STATUS.md` already flags that *"the 150-pass claim
is asserted, not yet CI-confirmed as one sweep."*

---

## Part 5 — The external suggestions, assessed

`docs/08` already handled this material well and its conclusions stand. Additions only:

**Gemini's Gap C (SOLAS VGM) is the weakest.** `docs/08`'s table says "arguably neither"
property is needed, and that is right — it is multi-sensor reconciliation, and no
cryptography is required to compare three weights.

**Gap A (FuelEU noon reports) is worth keeping alive for a reason Gemini did not give.** It
is where the grant money is. See Part 6.

**Gap B (blind survey) remains the only genuine fit for ValiChord's actual protocol**, and
`docs/09` is right to place it last, because it requires surveyors.

**ChatGPT's contribution was the correct framing and it is already absorbed.** Its own
warning is the one to keep: *nobody in shipping is asking for SHA-256 commitments.*

---

## Part 6 — Grants: corrected

**Verified against the funders' own pages, 26 August 2026.** The list circulated was of
*programmes*, not of *open calls*. Every UK one named is currently shut.

| Programme | Status | Note |
|---|---|---|
| **TRIG 2026** (Connected Places Catapult / DfT) | **Closed** | £2.385m across 53 projects, up to £45k each. Tracks were Maritime Decarbonisation (25), Digital Twins (10), Freight Innovation (5). No evidence-integrity track |
| **CMDC Round 7** (Innovate UK / DfT) | **Closed 15 July 2026** | Three strands, up to £10.5m / £4.2m / £700k. Priority favours combining vessel or infrastructure themes *with* Smart Shipping — a pure data-integrity project fits poorly |
| **Lloyd's Register Foundation — Maritime Connected** | **Closed** | The best fit by a distance. Their remit is safety and evidence, and the call was about *"connections where risks are hidden or emerging"* |

**Two consequences.**

The available money is decarbonisation-framed. If a grant is the route, Gemini's FuelEU gap
fits the funding better than laytime does — which is a genuine reason not to discard Gap A.

And both UK competitions want a consortium partner: a trust port, a terminal operator, a
survey firm. **The grants do not route around the recruitment problem. They converge on the
same single action this project has deferred for four phases.** The next deadline is the
reason to make the call, not a substitute for it.

---

## Part 7 — Phase 0b: the retrospective test

**Inference. This has not been run, and it may not yield.**

`docs/10`'s second test compares a crew-set AIS field against GPS within the same message.
`docs/13` concedes the divergence it found is *"staleness at least as much as dishonesty."*
It does not test the thing that matters — whether *carrier NOR timestamps* diverge from
telemetry — because that needs carrier logs.

**There is a source of real disputed times that requires no counterparty: published
judgments.**

English Commercial Court laytime and Notice of Readiness decisions name the vessel, the
port and the disputed times — *The Happy Day*, *The Tres Flores*, *The Sebat* are all
reported that way, and are freely available. US federal maritime courts do the same. LMAA
arbitration awards are anonymised and are **not** usable; court judgments are.

NOAA bulk AIS covers 2009–2025.

**The test:** find judgments naming a vessel and a US port inside that window; re-derive
arrival from AIS with the existing Phase 0 code; see whether it settles the fact question
the case spent years arguing.

**The honest limitation, stated first.** Free AIS is US waters only. Many English-law
charterparty disputes concern other ports. The usable intersection may be a handful of
cases rather than a study, and it may be zero.

**Why it is still the highest-value next step.** A handful is enough. It converts *"the
mechanism works on synthetic parties"* into *"here are real disputes, with real money, where
this settles the fact in seconds"* — which answers the question unanswered since
[`docs/04`](04-strategic-assessment.md). It removes the circularity in Part 3. And it solves
the problem that has actually been blocking the human step: **the case tells you who to
write to.**

A letter saying *"I re-derived the arrival time in your matter from public AIS — here is
what it shows"* is not a pitch. It is a specific artefact about the recipient's own work.

---

## Part 8 — What to do, in order

### Now, before anything is shown to anyone

1. **Fix the Phase 3 ceiling.** Either complete the OpenTimestamps upgrade path or add an
   RFC 3161 authority as `docs/13` already recommended — and until then, weaken the record's
   own wording, which currently claims a bound the code has not established.
2. **Fix the Phase 1 circularity.** Make the port and terminal claims independent, or state
   plainly on the page which comparisons are real.
3. **Clear the six smaller items** in Part 3.

### Next

4. **Run Phase 0b.** Highest-value item on this list.
5. **Write to the firms in those cases.** Specific, about their own work.
6. **If Phase 0b yields nothing usable**, fall back to publicly reachable authors: P&I and
   defence club guidance, maritime solicitors' case notes, demurrage consultancies, maritime
   law academics. All self-identified as interested; none require an introduction.

### Then

7. **Park `docs/15` as design, not decided.** Keep it. Record Findings 1–7 against it so the
   reasoning is not re-derived, and record that its credential mechanism is sound.
8. **Build one DNA, not four.** Persistent, two agents — claimant and counterparty — with
   external anchors pinning the chain head periodically. `registry`, `telemetry` and
   `record` stay as signed files and a web page until there is an industry to justify a DHT.
   This is `docs/13`'s own architecture, which it found and then did not use. **After step
   5**, so that the second agent is a person rather than a placeholder.

### Keep warm

9. **Email Lloyd's Register Foundation.** The call is shut; a conversation is not. Funders
   are professional introducers, which is the shortest route past "I do not know anyone."
10. **Diary the next TRIG and CMDC rounds**, and note that the FuelEU framing fits their
    money better than laytime does.
11. **Give any continuing session a stopping condition** — an explicit instruction to say
    when routing around people has stopped being the right move.

**If only three are done: 4, 5 and 1.** The rest will change shape depending on what Phase
0b turns up.

---

## Part 9 — What this review did not check

Stated so that its silence is not read as endorsement.

- **Nondominium's `clone_limit: 512`** — cited by `docs/15`, not verified here.
- **Whether `hdi::ed25519::verify_signature` is callable from inside a `validate` callback
  specifically.** The crate that exists solely for validation exports it, and it is
  deterministic, so it should be. That is inference, and it should be settled by a compile
  before Finding 1's remedy is relied on.
- **The recovered Holo Sail material** in `sources/` and `docs/01`–`docs/07`. Out of scope.
- **Whether anyone will pay.** Unchanged since `docs/04`. Nothing in this document moves it,
  and no further engineering will.

---

**Sources**

- [Holochain — DNAs](https://developer.holochain.org/build/dnas/)
- [Holochain — Validation](https://developer.holochain.org/build/validation/)
- [Holochain — Cloning](https://developer.holochain.org/build/cloning/)
- [Holochain — Callbacks and lifecycle hooks](https://developer.holochain.org/build/callbacks-and-lifecycle-hooks/)
- [Holochain — Zomes](https://developer.holochain.org/build/zomes/)
- [`hdi::ed25519`](https://docs.rs/hdi/latest/hdi/ed25519/index.html)
- [TRIG 2026 competition — Cohort 19](https://cp.catapult.org.uk/opportunity/trig-2026-competition-cohort-19/)
- [Clean Maritime Demonstration Competition 7](https://iuk-business-connect.org.uk/opportunities/clean-maritime-demonstration-competition-7/)
- [Lloyd's Register Foundation — Maritime Connected funding offer](https://www.lrfoundation.org.uk/maritime-connected-funding-offer)
- [Steamship Mutual — Notice of Readiness: FAQs](https://www.steamshipmutual.com/publications/articles/notice-readiness-faqs)
- [Shipowners' Club — Laytime & Demurrage](https://www.shipownersclub.com/latest-updates/publications/laytime-and-demurrage/)
