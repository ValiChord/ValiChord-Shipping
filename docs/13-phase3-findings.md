# 13 — Phase 3: a witness with nobody to recruit

**The question was "how do I get a witness when I don't live near a port and humans are
too hard to organise?" The answer is that a witness was never a human role.**

Code: [`../tools/phase3/`](../tools/phase3/). Sample output:
[`../tools/phase3/example_output/`](../tools/phase3/example_output/). Run 25 August 2026.

---

## The distinction the phase turns on

ValiChord was designed around human validators, and has since moved to AI validators.
Neither can do this job, and that is not a limitation — it is a category difference.

| | Does | Cost |
|---|---|---|
| **Validator** | Forms a *judgement* about evidence | Recruitment, expertise, trust |
| **Witness** | Attests that data *existed at a time* | Free, public, machine-only |

Witnessing is not a judgement task. It cannot be delegated to a validator of any kind,
because the property required is independence and ordering, not expertise. A witness that
you operate is not a witness.

**And AI validators make the witness more important, not less.** A human expert signing a
finding stakes their reputation on it. An AI you run yourself stakes nothing — so a
hostile counterparty has no reason to believe its output. What makes a machine finding
credible against an adversary is that the *inputs were provably pinned before anyone knew
the answer*. Remove the witness and an AI validator's verdict is just an assertion by the
party that owns the model.

---

## What was built

A two-sided time sandwich, using two live public services, neither operated by this
project.

**Floor — "this was not made earlier."**
[drand](https://drand.love/), the League of Entropy beacon, publishes an unpredictable
value every 30 seconds, threshold-signed by independent organisations. The current round
is embedded *inside* the payload before hashing, so it is covered by the commitment.
Nobody can know round N's randomness before round N exists, so a commitment containing it
was necessarily constructed afterwards.

**Ceiling — "this was not made later."**
[OpenTimestamps](https://opentimestamps.org/) aggregates the commitment digest into
Bitcoin. Submitted to **three independent calendar operators** — the OpenTimestamps pool,
Eternity Wall, and Catallaxy. All three accepted.

**Result from the live run:**

```
floor    drand round 6408713, randomness independently re-fetched and matched
ceiling  3/3 calendars accepted
interval 28 seconds
humans   0
```

Nobody was recruited. Nothing was scheduled. No introductions were needed, and where the
operator lives is irrelevant to every part of it.

---

## What it proves — an interval, not an instant

The negative control runs four attacks. **Three are refused. One is not**, and recording
that honestly matters more than the three that pass.

| Attack | Outcome |
|---|---|
| Fabricate the beacon randomness | **refused** — re-fetching the round from the public API disagrees |
| Omit the beacon entirely | **refused** — no floor; the record is flagged unwitnessed |
| Alter the payload after committing | **refused** — hash mismatch |
| **Embed a genuine but stale beacon round** | **not refused** |

The fourth attack works. A floor proves *not before*. It does not prove *was then*. A
party wanting its commitment to look old simply embeds a round from 24 hours ago; the
round is genuine, so the floor verifies perfectly, and nothing about the cryptography
objects.

**What exposes it is the width of the interval, not the floor.** From the live run:

| | floor → ceiling |
|---|---|
| Honest commitment | **9 seconds** |
| Backdating attempt (stale round) | **86,409 seconds — 24 hours** |

A 24-hour interval establishes almost nothing about when a commitment was made. A
28-second interval establishes a great deal.

So every party record carries `timeInterval.seconds` and a strength label, and **a system
reporting `witnessed: true` without the width would be misleading**. The usefulness of the
whole mechanism is a function of anchoring promptly after committing — which is an
operational discipline, not a cryptographic guarantee.

This is the most important finding in the phase, and it is a limitation rather than a
capability.

---

## Honest limits

**The ceiling is a promise at first.** At stamp time you hold signed receipts from
calendar servers — commitments to include the digest in Bitcoin. Confirmation takes
hours. Until then the ceiling rests on those signatures, which is precisely why three
independent operators are used rather than one. `bitcoinConfirmed` is `false` in the
record and stays false until upgraded.

**drand liveness is assumed.** If the beacon is unreachable the run exits rather than
producing an unwitnessed record. A witnessed protocol that quietly produces unwitnessed
output is worse than one that fails.

**This witnesses claims, not evidence.** The telemetry side needs no witness of ours:
public AIS is continuously published by third parties and cannot be retroactively
altered. What needed pinning was the *claim*, and that is what this does.

**Still synthetic parties.** As with Phases 1 and 2, the vessel and track are real and
the four parties are not.

---

## What this means for the Holochain question

> **Corrected 25 August 2026, after challenge from Ceri John.** The section below
> originally dismissed Holochain for Phase 3 and overstated the case considerably. The
> correction follows the original so the reasoning stays auditable.

### The original argument

[`docs/09`](09-demo-plan.md) argued Holochain would earn its place at Phase 3, on the
grounds that witnessed append-only per-agent publication without a central operator is
exactly what the trust model needs.

Phase 3 rejected that: Holochain's witnessing property depends on *independent peers
actually running nodes*, and in a demonstrator where one person operates every node there
is no independence — it is theatre with extra steps. Getting genuinely independent nodes
means recruiting participants, the exact problem this phase existed to route around.
drand and OpenTimestamps supply real independence today at zero recruitment cost.

### Why that was too sweeping

**The argument is sound about one property and was applied to all of them.** The
"one operator, no independence" objection is correct about the *validating DHT*. It says
nothing about two other things Holochain provides, both of which were skated past
entirely:

**Countersigning.** Holochain supports atomic multi-party commit — either both parties
commit to a shared entry or neither does. A custody handover is inherently bilateral, so
this maps directly onto the actual use case, and plain signed files cannot do it.
*Caveat, checked against the Holochain reference: it is feature-gated
`unstable-countersigning`, sessions are time-bounded with a 6-second maximum clock skew,
and stuck sessions require explicit abandonment. It is a real primitive, not a
turnkey one.*

> ### ⚠️ A claim in this section was wrong, and is retracted
>
> This correction originally also asserted that **"source chains give ordering for free,
> with a single agent — you can prove event A preceded event B with no external witness at
> all."** That is false, and checking it against
> `ValiChord/docs/Holochain_complete.md` is what established it.
>
> Fork detection is not intrinsic to a source chain. It is performed by the DHT
> authorities for the author's public key, via the `RegisterAgentActivity` op — which
> "appends to replica of author's source chain; **detects forks**." `ChainStatus` can
> return `Forked(warrant)` precisely because *peers* noticed.
>
> **With one operator and no independent peers, a fork is undetectable.** An agent can
> rewrite or branch their own chain and nobody holds the earlier state to contradict them.
> A source chain proves ordering to an adversary only if somebody else witnessed the
> earlier entries.
>
> Holochain action **timestamps are self-reported**. The reference says so directly, in
> the context of rate limiting: *"note timestamps are self-reported."* That alone means
> Holochain cannot supply trustworthy time on its own, whoever runs the nodes.
>
> #### Warrant status — corrected again, 25 Aug 2026
>
> An earlier version of this note said "the network does **not** block them automatically
> — on roadmap but not current behaviour," quoting
> `ValiChord/docs/Holochain_complete.md`. **That is out of date, and the ValiChord
> reference should be updated too.**
>
> Checked against the Holochain 0.6 release announcement: transport-level blocking
> already works. *"Validation is now correctly hooked into the network transport to ensure
> that invalid actions are responded to with network-level blocking,"* and *"warrants are
> delivered to anyone who queries a bad agent's public key."*
>
> What genuinely remains open, in Holochain's own words:
>
> * *"Warrants are currently only delivered to the agent public key authorities, so you
>   have to check for warrants using `get_agent_activity`"* — dissemination is narrow, so
>   the application must still query rather than being told.
> * *"Membrane proof checking is currently only enforced via normal validation, not during
>   handshaking, so unauthorised agents are able to join a network and access it for a
>   short time before being warranted and blocked."*
>
> The 0.8.x roadmap carries a **Warrants** epic — *"enable warranting and blocking of
> nodes that violate validation rules"* — still in planning, no date, roughly 14 weeks
> estimated at current velocity.
>
> **Net effect on this project: the consequences of forking are real today, not pending.**
> But they are consequences imposed by *peers*, so the conclusion below is unchanged.
>
> **This reverses the direction of the correction on that specific point.** Holochain does
> not remove the need for independent witnesses, even for ordering — which means Phase 3's
> original conclusion was right for a better reason than the one it gave, and external
> time anchors remain necessary regardless of substrate.
>
> What survives: countersigning, agent-centric identity, and the strategic argument below.
> What does not: the idea that a single-operator hApp gets trustworthy ordering for free.

### How hard is forking, really — and can the UI stop it?

The reasonable objection: forking sounds theoretical, and a well-built client could make
it very awkward. Worth answering properly, because half of it is right.

**Making a fork is not hard.** The agent runs their own conductor; the source chain is a
local database and the signing key is in their own keystore. Rolling back is: stop the
conductor, restore an earlier copy of the state, restart, author something different. No
cryptography is broken and nothing is exploited — it is file operations by someone with
administrator access to their own machine.

**The UI is not the security boundary.** It sits above the conductor, and the conductor's
state is on disk. A client can make forking inconvenient; it cannot make it infeasible,
because the party the client is protecting against is the party running the client.

**And the adversary here is not casual.** The scenario that motivates the whole project is
a demurrage dispute at tens of thousands of dollars a day, contested by an operations
department with IT staff and a direct financial interest. "The interface makes it
difficult" does not survive that question, and a P&I lawyer will ask it early.

**But the objection is half right, and the half that is right matters.** Phase 0 measured
divergence between claims and telemetry at 0.372% of fixes, and concluded it was staleness
at least as much as dishonesty — crews not updating a field nobody is paid to fake. A
client that makes the honest path easy and the careless path hard genuinely addresses the
dominant real-world case. It is worth building. It is simply not what answers the
adversarial question.

### The reframe that actually helps: detection needs one peer, not an industry

The goal is not to prevent forks. It is to make them **detectable**, and detection has a
much lower bar than it first appears.

If a single independent node has seen and receipted entry *N*, and the author later
presents a chain in which *N* differs, that node's copy contradicts them. One honest peer
holding the `RegisterAgentActivity` replica is enough — and since 0.6, the consequence is
network-level blocking rather than a note in a log.

**One peer.** Not consensus, not a quorum, not an industry. A cargo insurer running a
node, a neutral body, a class society, or simply a cheap host under a different legal
entity with a different set of incentives.

That reframes an impossible problem — *recruit the shipping industry* — into a plausible
one: *persuade a single counterparty to run a node*. It is the same insight Phase 3
reached about time anchors, arriving from the other direction: you do not need many
witnesses, you need one you do not control.

**A related design question that has not been decided.** If each party self-hosts its
conductor, each controls its own chain and the analysis above applies. If conductors are
hosted — Holo hosting, or edge nodes — the host holds the state, which changes the threat
model substantially and may be better *or* worse for the neutrality argument depending on
who the host is. Recorded as open.

**"Not needed for the demonstrator" was conflated with "not the right architecture."**
Those are different claims. The first is defensible; the second was not argued for and is
probably false.

### The architecture that should have been proposed

Source chains and external anchors are complementary rather than competing:

- **Source chains** establish ordering *within* each party — free, no witness required
- **External time anchors** pin the chain *head* at intervals
- Everything between anchor N and anchor N+1 is therefore provably ordered *and* pinned
  to that window
- Anchoring becomes periodic rather than per-event — considerably cheaper than what this
  phase actually built
- **Countersigning** handles handovers, where both sides must commit together

That uses Holochain for what it is genuinely good at, with external time filling the one
gap it cannot fill alone: independent proof of *when*, before independent peers exist.

### The strategic objection, which is the stronger one

**If this work never touches Holochain, it is not a ValiChord demonstrator.** It is a
well-built separate artefact that happens to share an author — and the stated purpose of
the whole exercise was to get people interested in what ValiChord can do.

[`docs/09`](09-demo-plan.md)'s exclusion table was a good discipline that prevented real
bloat, and it holds for Unyt (no money moves) and Nondominium (nothing changes custody).
Applied to Holochain it went too far, and a rule against shoehorning can quietly become a
rule against ever integrating anything — leaving an orphan demonstrator with no path back
into the main project.

**Standing position:** Holochain belongs in the system, and its absence from Phases 1–3
is a statement about the demonstrator's scope, not about the architecture. Phase 3b is
the source-chain commit log. Setup cost is documented in
[`14-holochain-setup.md`](14-holochain-setup.md).

---

## A related correction: ValiChord is not trustless

Phase 3's write-up contrasted Bitcoin ("you don't have to trust anyone") with RFC 3161
timestamp authorities ("you must trust the authority"), implying the second was a
compromise of the project's principles.

That framing was wrong, because **ValiChord has never been trustless.** Its own
description specifies *"independent credentialed validators"*, and credentialing is a
trust operation. ValiChord is **trust-distributed**: individual validators are trusted to
be competent, and the structure — blind commit-reveal — prevents them colluding or
anchoring on one another.

That is the same shape as several independent timestamp authorities in different
jurisdictions, each with a business built on not backdating, all of whom would have to
collude. Bitcoin occupies a stricter category; ValiChord and multi-authority timestamping
occupy the same one.

So moving the ceiling to RFC 3161 would be *consistent* with the project's trust model
rather than a departure from it, and the "trustless versus trusted" framing should not be
used to argue against it.

**Status: not yet implemented.** Phase 3 as committed uses OpenTimestamps and Bitcoin.
The case for RFC 3161 — legal recognition, eIDAS presumption of accuracy, instant
issuance, and no blockchain framing in front of an industry that watched TradeLens die —
is argued but the code is unchanged. Recorded as an open decision, not a silent one.

---

## Where the project now stands

Phases 0 to 3 are complete and none of them required a counterparty:

| | |
|---|---|
| **0** | Maritime events can be timed to ~70 seconds from free public AIS |
| **1** | Parties can be bound to *what* they asserted, with a working negative control |
| **2** | The result renders as one page pitched at a laytime desk |
| **3** | Commitments can be pinned in time by public witnesses, with no humans involved |

What remains unanswered is what has been unanswered since
[`docs/04`](04-strategic-assessment.md): **whether anyone will pay.** Four phases of
engineering have not moved that question a millimetre, and no further engineering will.

The demonstrator now exists precisely so that question can be asked while holding
something that runs. That was the stated purpose from the beginning, and it is now met.

**The next useful action is not Phase 4. It is showing this to one person who works cargo
claims or a laytime desk.**
