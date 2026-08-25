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

[`docs/09`](09-demo-plan.md) argued Holochain would earn its place at Phase 3, on the
grounds that witnessed append-only per-agent publication without a central operator is
exactly what the trust model needs. **That reasoning was sound and the conclusion was
wrong, for a practical reason the plan did not consider.**

Holochain's witnessing property depends on *independent peers actually running nodes*. In
a demonstrator where one person operates every node, there is no independence — it is
theatre with extra steps. Getting genuinely independent nodes means recruiting
participants, which is the exact problem this phase existed to route around.

drand and OpenTimestamps supply real independence today, at zero recruitment cost,
because other people already run them for their own reasons.

**Holochain becomes the right answer when there are genuinely independent parties** —
which is a later problem, and a commercial one rather than a technical one. Recorded as a
revision rather than quietly dropped.

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
