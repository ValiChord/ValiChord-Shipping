# 22 — Four more use cases, and the structural reason shipping resists all of them

**Scanned four candidate disputes before building anything, which is the discipline
[`docs/20`](20-is-this-already-solved.md) was written to enforce. Three are occupied. The
fourth turns out to be occupied by a *contract clause* nobody uses. And the cross-cutting
finding is worse than any of them individually.**

**It also overturns `docs/20`'s own conclusion about what survives.** That is corrected
below rather than quietly amended.

Run 26 August 2026, immediately after [`docs/21`](21-tricon-run.md).

---

## The one-line verdict on each

| Area | Verdict |
|---|---|
| Charterparty speed and performance | **Partly occupied — and the gap is legal-cultural, not technical** |
| Marine cargo damage surveys | **The blinding premise is backwards.** See the correction below |
| Bunker quantity / quality | **Occupied (quantity). Open but wrong-shaped (quality)** |
| Container condition at interchange | **Occupied and closing fast** |

---

## The cross-cutting finding, which matters more than the four

**In three of the four, an independent verification system would have to be bought by the
party it constrains.**

- **Speed and performance.** The *owner* controls the sensors and the data. The
  *charterer* wants the measurement and cannot get it without the owner's consent.
- **Cargo surveys.** Each surveyor is appointed and paid by the party whose interest they
  advance. A club buying a blinding system blinds its *own* surveyor first.
- **Containers.** The terminal owns the gate cameras and is also the party most often
  alleged to have caused the damage. The trucker carrying the exposure has no purchasing
  leverage at the gate.

**And the single counterexample is the most useful fact in the scan.** Bunker mass flow
meters *were* forced on the measured party — the barge operator — but not by a sale.
Singapore made them a condition of the **bunker licence** in 2017; Rotterdam and
Antwerp-Bruges followed from **1 January 2026**, tied to the vessel licence, with fines or
licence revocation for breach.

> **The only adoption path that worked in this entire scan was a sovereign gatekeeper
> mandating it. Not a product sale.**

That is a strategic finding about the industry, not about any one use case, and it should
outlive every specific idea in this repository.

## The sharpest single fact

**BIMCO Energy Efficiency Data Sharing Clause 2025, sub-clause (k):**

> "The Charterers expressly waive any right to use the Data as a basis for or in support of
> a claim against the Owners regarding any off-hire period… and/or existing warranties as to
> speed and consumption."

Owners will hand charterers high-frequency sensor telemetry **only on condition that it
cannot be used in a performance claim.**

Better evidence exists. The party who holds it has contracted it out of the dispute. That is
not a technology gap and no protocol closes it.

---

## ❌ Correction to `docs/20`: the survey case does not survive either

[`docs/20`](20-is-this-already-solved.md) concluded that the marine cargo survey case was
*"the one"* that survives, inheriting that judgement from
[`docs/08`](08-external-evidence-and-the-real-gap.md) and
[`docs/09`](09-demo-plan.md). **All three were wrong, and for a reason none of them
checked: what the industry actually does.**

Established practice is **the joint survey** — surveyors representing all interests are
invited to attend together, explicitly *"without prejudice"*, and the stated goal is that
they **work together at the scene to agree quantum and cause** so that litigation is
avoided. Failing to invite the other side's surveyor can *prejudice* recovery.

**Blind independent capture would deliberately destroy the convergence the industry relies
on to settle cheaply.**

You could still argue the agreed facts are contaminated by anchoring — that is a real and
plausible claim. But it is now a claim you must *prove*, against an entrenched practice
that everyone involved believes already works, before anyone will pay to disrupt it. That
is a research programme, not a product.

**This was the repository's fallback position for four documents. It is gone.**

---

## The area that looked most promising, and why it is not

Charterparty speed and performance disputes are judgement-shaped, frequent, and
adversarial. No product occupies "neutral pre-committed adjudicator."

**But the contract clause does.** London Arbitration 9/23 turned on wording already in use:

> "In the event of a dispute over a breach of speed and consumption warranty in this Charter
> Party, a mutually agreed weather routing company to be appointed to analyse the vessel's
> performance whose findings will be final and binding"

Similar architecture sits in BIMCO's Weather Routeing Clause 2006 and in club-recommended
clauses escalating to a mutually-agreed third router. **The industry already knows how to
write "neutral, pre-agreed, binding analyst" into a contract.** It largely does not, and
where it does, tribunals still second-guess it.

The economics explain why: claim values cluster around **USD 15k–250k**. High volume, low
value. Nobody will fund a heavyweight adjudication process for a dispute that settles by
horse-trading.

**Building a technical solution here means fighting a problem that is not technical.**

---

## What actually survives — and it is one thing

Per the standing discipline of pairing a red team with a blue team, here is what the scan
does *not* kill.

### Draft survey, and the property that makes it different

Determining bulk cargo quantity from the ship's draft. Not covered by the scan above; assessed
separately in [`docs/23`](23-draft-survey.md).

It survives the cross-cutting objection, and it is the only candidate that does:

- **The buyer is not the constrained party.** The ship's master checks the *shipper's*
  figure. The owner and the P&I club want the verification; the shipper is the one
  constrained. That inverts the trap that kills the other three.
- **Adoption is unilateral.** The master sealing their own figure before seeing the
  shipper's gets the entire anchoring benefit *even if nobody else ever participates.*
  There is no counterparty to recruit and no network to join.
- **It is judgement, not measurement.** Gard: *"not an exact science and much depends on
  weather conditions, swell, draft mark accuracy, and calculation care."*
- **The existing software is single-user calculators** — DoSurvey!, SurveyorMates, Draft
  Survey Professional, SGS's and Control Union's in-house tools. None addresses two parties
  arriving at figures independently.

> ⚠️ **The cargo-survey correction above is the exact risk to test here.** If joint draft
> survey — master and shipper's surveyor working the figure together on deck — is
> established practice, then blinding damages a convergence mechanism in the same way, and
> draft survey dies for the same reason. **Nobody has checked. That is the first question to
> ask, not the last.**

### The unilateral insight itself

**Anchoring-prevention does not require bilateral adoption.** One party committing before
exposure captures the benefit alone.

This dissolves the twelve-counterparty wall that killed TradeLens, killed Holo Sail, and has
blocked this repository since [`docs/04`](04-strategic-assessment.md). It is
domain-independent, it is the most portable thing found in this whole line of work, and it
was not noticed until the fifth use case.

### The gatekeeper route

If anything here is worth pursuing at scale, the scan says the path is a **mandating
gatekeeper** — a port authority, a class society, a P&I pooling agreement, a BIMCO standard
clause — not a SaaS sale. That is a multi-year play and not one a solo founder runs.

---

## What this means

**Shipping is structurally hostile to this class of product, for four independent reasons:**

1. The party who would be verified usually controls both the evidence and the purchase.
2. Where pre-commitment is genuinely wanted, it already exists as a contract clause and is
   not adopted — so the missing thing is not a tool.
3. Where the dispute is factual, sensors have arrived or are arriving, and they win.
4. Where the dispute is judgemental, the industry has built social convergence mechanisms
   it believes already work.

**That is not a reason to stop. It is a reason to stop guessing.** Draft survey is worth
three conversations because it inverts reason 1 and sidesteps reasons 2–4. If those
conversations say joint drafting is standard practice, it dies, and the honest conclusion is
that the mechanism's home is not shipping.

---

## Sourcing caveat

Claim-frequency and accuracy figures below are largely from vendor blogs, P&I circulars and
trade press rather than audited data, and should be treated as directional. **The
load-bearing primary facts are** the BIMCO 2025 clause text, the Singapore and Rotterdam MFM
mandates, and the London Arbitration 9/23 clause wording.

**Sources**

- [BIMCO Energy Efficiency Data Sharing Clause 2025](https://www.bimco.org/contractual-affairs/bimco-clauses/current-clauses/energy-efficiency-data-sharing-clause/) — sub-clause (k)
- [BIMCO Weather Routeing Clause for Time Charter Parties 2006](https://www.bimco.org/contracts-and-clauses/bimco-clauses/current/weather_routeing_clause_for_time_charter_parties_2006)
- [Steamship Mutual — Speed and Performance, Pitfalls and Practice](https://www.steamshipmutual.com/publications/articles/speedandperformance062018)
- [Watson Farley & Williams — underperformance disputes, currents and swell](https://www.wfw.com/articles/vessel-underperformance-disputes-how-are-currents-and-swell-treated/)
- [Van Ameyde Marine — the role and challenges of a P&I surveyor](https://www.ameydemarine.com/news/cargo-damage-the-role-and-challenges-of-a-p-and-i-surveyor/)
- [Cargo damage survey guideline — joint survey practice](https://bulkcarrierguide.com/cargo-damage-survey.html)
- [Port of Rotterdam — mass flow meter mandatory from 1 January 2026](https://www.portofrotterdam.com/en/news-and-press-releases/mass-flow-meter-bunker-measurement-system-mandatory-as-of-1-january-2026)
- [Skuld — Singapore mass flow metering](https://www.skuld.com/topics/ship/bunkers/singapore-mass-flow-metering-for-bunkering/)
- [Camco Technologies — Automated Damage Inspection](https://camco.be/automated-damage-inspection-adi/)
- [Gard — draft surveys and dry bulk shortage claims](https://gard.no/en/insights/draft-surveys-critical-tool-to-defend-dry-bulk-cargo-shortage-claims/)
