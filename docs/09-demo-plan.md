# 09 — Plan for a demonstrator

**The proposition to test, in one sentence:** *can an independently-sourced record demonstrate
that a consequential operational claim was not recorded when it says it was?*

Not a platform. Not a company. One artefact that either shows this or fails to.

---

## What gets used, and what deliberately does not

Recorded first, because the risk in a project that has surveyed an ecosystem is reaching for
everything surveyed.

| Component | Verdict | Reasoning |
|---|---|---|
| **Public AIS** | **Use** | The only independent, free, machine-readable ground truth available without a counterparty. Without it there is no demo |
| **SHA-256 commitments + signatures** | **Use** | The whole mechanism. Thirty lines of code |
| **DCSA event vocabulary** | **Use** | Costs nothing and makes the output legible to a maritime reader rather than a developer. See [`docs/02`](02-company-record.md) on standards being the thing that makes work real to a port |
| **Unyt** | **Do not use** | No money moves in this demo. Adding a settlement layer to a demonstration about evidence would be decoration. Revisit only if fees or claims are ever actually settled — and note the licensing constraint in [`docs/07`](07-unyt-payments-and-the-survey-protocol.md) |
| **Nondominium / hREA** | **Do not use** | Its primitives are custody transfer of economic resources and governance gating. This demo has neither: no resource changes hands, and nothing is gated. `TransferCustody` would be a vocabulary borrowed to look connected. Revisit only if the work extends to cargo custody chains ([`docs/06`](06-nondominium-compatibility.md)) |
| **ValiChord's blind commit-reveal** | **Do not use — in Phase 1** | This is uncomfortable and it is the honest reading of [`docs/08`](08-external-evidence-and-the-real-gap.md). Laytime is a *backdating* problem, not an *anchoring* problem. Blind commit-reveal solves anchoring. Using it here would be importing the protocol because it is ours, which is the exact error this table exists to prevent. It has a genuine place — see Phase 4 |
| **Holochain** | **Not in Phase 1; justified from Phase 3** | Reasoning below, because it is the one call worth arguing rather than asserting |

### On Holochain specifically

The demo's core requirement is that a commitment provably existed **before** the reveal. That
needs a witness — otherwise a party simply computes the hash afterwards and claims it was earlier.

Three ways to get a witness:

1. **A central timestamp authority** (RFC 3161). Works, is mature, and reintroduces exactly the
   owned-intermediary problem TradeLens died of. Every party must trust one operator.
2. **A public chain anchor** (OpenTimestamps or similar). Works, is neutral, and drags in
   blockchain framing that this sector has specifically soured on.
3. **Holochain.** Each party holds its own append-only signed source chain, and published entries
   are held and validated by peers. Publication is witnessed by the network without any party
   owning it.

Option 3 is a genuinely good fit for the specific property required — witnessed, append-only,
per-agent, no central operator. That is a reason to use it, as distinct from familiarity.

But **Phase 1 does not need a real witness**, because Phase 1 is proving the detection logic, not
the trust model. Simulate it, keep the interface clean, and introduce the real substrate at Phase
3 when the property has to be genuine. Building the trust model first is how demos die unbuilt.

---

## Phase 0 — Try to kill it (days)

**Before writing any demo code.** The premise is that operational claims and physical telemetry
diverge often enough, and measurably enough, to matter. That is an empirical question with a free
dataset attached.

1. Pull real historical AIS from [MarineCadastre](https://marinecadastre.gov/accessais/) — US
   coastal waters, 2009–2025, analysis-ready, no application required.
2. Pick a busy port and a window. Derive, from AIS alone, per-vessel events: entry into port
   limits, speed profile, anchoring, mooring.
3. Establish **resolution**: how precisely can arrival be pinned? Minutes, or hours?
4. Compare against any independently published port record obtainable — port authority arrival
   lists, published berth schedules, anything.

**Kill criteria — stop if any is true:**

- AIS-derived arrival cannot be established to within ~15 minutes for a usable share of calls.
  Laytime disputes turn on minutes; an hour of uncertainty makes the evidence worthless.
- Coverage gaps make the picture unusable at the moments that matter — approach and anchorage.
- No independent record of claimed times can be obtained at all, even one, making the divergence
  question untestable rather than merely unanswered.

**Deliverable:** a short written finding — go or no-go, with the numbers.

This phase costs a weekend and can end the project. That is its purpose.

---

## Phase 1 — The mechanism (about a week)

A script, not a product. Four parties, one port call.

- Each party has an event record in DCSA-shaped JSON — carrier, port authority/VTS, terminal
  operator, telemetry.
- Each commits `SHA-256(payload ‖ nonce)` and signs it. Commitments recorded with a sequence.
- Reveal: payloads published.
- Verifier: (a) recompute each commitment and confirm it matches; (b) derive events from **real**
  AIS; (c) report where the revealed claims and the telemetry disagree.

**Data honesty.** The AIS is real. The party claims are synthetic — nobody has given us their
logs. **The artefact must say so on its face.** A demo that implies real carrier data it does not
have is the kind of thing that ends a conversation with an insurer permanently.

**Output is a discrepancy record, never an adjudication.** Per [`docs/08`](08-external-evidence-and-the-real-gap.md):
report that the carrier committed 06:00 while telemetry shows the vessel underway 35nm out; do
**not** report that $4,010.42 is therefore owed. No `confidenceScore`. No clause interpretation.
The facts are ours; the law is theirs.

---

## Phase 2 — Make it legible (about a week)

Phase 1 convinces a developer. This phase is for someone who runs a laytime desk.

One page, self-contained:

- A timeline with the four claimed events and the AIS track on the same axis
- The divergence marked plainly, in minutes
- The sealed commitments, with what was sealed and when
- DCSA field names throughout — `transportCallID`, `eventTypeCode`, `UNLocationCode`,
  `facilityTypeCode` — so it reads as native rather than foreign
- A visible statement of which data is real and which is synthetic

**The test of this phase:** a maritime professional understands what they are looking at without
anyone explaining it. If it needs narration, it has failed and no amount of correctness rescues
it.

---

## Phase 3 — Make the trust model real (only if Phase 2 lands)

Now the witness has to be genuine, and this is where Holochain earns its place: separate parties,
each with their own source chain, publication witnessed by peers, no central operator.

Scope: two or three real parties. That is the point at which the claim "nobody can backdate this"
becomes true rather than illustrated.

Do not start here.

---

## Phase 4 — The survey extension (optional, and where ValiChord genuinely fits)

Everything above solves backdating. Blind commit-reveal solves **anchoring** — which is the marine
cargo damage survey case in [`docs/07`](07-unyt-payments-and-the-survey-protocol.md): two
surveyors, the same cargo, each waiting to see the other's position.

If the earlier phases find an audience, this is the natural second capability and the one where
ValiChord's actual protocol is the right tool rather than an available one.

It is listed last deliberately. It requires surveyors, which requires relationships, which is the
thing we do not have.

---

## Risks worth naming now

**AIS can itself be spoofed.** This is documented and not rare — vessels manipulate AIS to conceal
positions. The ground truth is not perfectly ground. Two responses: AIS is one source among
several rather than an oracle, and manipulation tends to leave signatures (implausible kinematics,
gaps, duplicate MMSI). But any claim that AIS *proves* anything must be qualified, and a
counterparty who works in this sector will raise it in the first five minutes. Better to raise it
first.

**Synthetic party data limits the claim.** The demo shows the mechanism works, not that carriers
actually misreport. Only Phase 0 can speak to the latter, and only weakly.

**Resolution may not survive contact.** AIS reporting intervals vary with speed and equipment
class. A vessel at anchor reports infrequently. The precision needed for laytime may not be
available at exactly the moments that matter. This is what Phase 0 is for.

**Building a developer artefact.** The likeliest failure is a technically correct thing that no
maritime professional can read. Phase 2 exists to prevent this and should not be skipped because
Phase 1 feels finished.

**Scope creep back into a platform.** Every previous attempt in this space became a platform and
died. The artefact is an artefact.

---

## What this is not

Not a Port Community System. Not a transport layer. Not an eBL platform. Not a competitor to
DCSA, IPCSA or the Maritime Single Window — those are further along than we are and solving a
different problem ([`docs/08`](08-external-evidence-and-the-real-gap.md)).

If it works, it is a thing that sits underneath any of them and answers a question none of them
currently answers.

---

## Sequence, and the one number that matters

| Phase | Effort | Ends with |
|---|---|---|
| 0 — Falsify | A weekend | Go / no-go, with numbers |
| 1 — Mechanism | ~1 week | A working verifier and a discrepancy record |
| 2 — Legibility | ~1 week | One page a maritime professional can read unaided |
| 3 — Real witness | Longer | The trust claim becomes true |
| 4 — Survey | Later | Where blind commit-reveal belongs |

Phases 0–2 are roughly two to three weeks and need **no partner, no introduction and no
permission**. That is the whole reason this is worth doing now and was not worth doing before
[`docs/08`](08-external-evidence-and-the-real-gap.md) established that AIS is free.

The number that decides everything is still the one from
[`docs/04`](04-strategic-assessment.md): whether anyone will pay. Phases 0–2 do not answer it.
They buy the right to ask it while holding something that runs.
