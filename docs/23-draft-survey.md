# 23 — Draft survey: the one candidate that survives, and the question that kills it

**A ship's officer and a shipper's surveyor each estimate how much cargo is aboard, from
the same hull, by judgement. They disagree by design. The ship's figure is its only
defence, and it is written in a notebook that can be revised after the pressure arrives.**

**One question decides whether this is worth anything, and it has not been asked.** It is at
the bottom of this document, and it should be the first thing done.

Assessed 26 August 2026, after [`docs/22`](22-why-shipping-resists-this.md) eliminated four
other candidates and retracted the survey case that three earlier documents had relied on.

---

## What a draft survey is

Bulk cargo is not weighed. The ship's draft is read fore, aft and amidships, corrected for
trim, list, water density, and deducted non-cargo weights (ballast, bunkers, fresh water),
and the cargo quantity is derived from the displacement difference.

It is done on essentially every dry bulk cargo, worldwide, twice — load and discharge.

## Why it is judgement, not measurement

This is the property that killed laytime and it is inverted here.

> "Performing a draft survey is not an exact science and much depends on weather
> conditions, swell, draft mark accuracy, and calculation care."
> — Gard

There is **no sensor that gives the answer.** The shore side has weighbridges or belt
scales, which produce a *different* number — and that difference is the dispute, not its
resolution. Two competent people, same hull, same hour, legitimately different figures.

**A better instrument does not settle this**, which is exactly why the AIS and mass-flow
-meter pattern from `docs/20` and `docs/22` does not repeat here.

## Why the divergence is meaningful rather than noise

There is an agreed tolerance, and it carries a contractual consequence.

> "barring exceptional circumstances, such as a high swell during the survey, if the
> difference between the shore figure and the draft survey figure is greater than 0.5 per
> cent, it may well represent a physical gain or loss"

> "if the draft survey gives a figure which is more than 0.5 per cent below the shipper's
> figure, the Mate's receipt and bill of lading should be claused"
> — both Gard

**A numeric output with an agreed threshold is close to ideal for this mechanism**, because
"did these two independent assessments actually agree" becomes a measurement rather than an
opinion. On a 60,000-tonne cargo, 0.5% is 300 tonnes.

## The pressure, described by the people who pay for it

The ship's own survey is, in Gard's words, **"the only means those on board have of
checking the shipper's figure."**

And on what happens when it disagrees:

> charterers may offer "a LOI holding the shipowner harmless if they agree not to" clause
> the bills of lading

So: the master produces the only independent check, the check disagrees, and the commercial
counterparty offers an indemnity to make the disagreement go away. The P&I club then carries
the shortage claim.

**The artefact worth protecting is the master's own figure, as it stood before that
conversation began.** Today it lives in a notebook.

---

## Why this survives `docs/22`'s cross-cutting objection

`docs/22`'s strongest finding is that in three of four candidate areas, an independent
verification system would have to be **bought by the party it constrains** — which is why
such systems do not get adopted on merit.

**Draft survey inverts it.**

| | |
|---|---|
| Who is constrained | the **shipper**, whose figure is being checked |
| Who wants the verification | the **owner** and the **P&I club**, who carry the shortage claim |
| Who buys | the same |
| Who must adopt | **only the ship** |

### The unilateral property, which is the real finding

**Anchoring-prevention does not require bilateral adoption.** If the master seals their
figure before seeing the shipper's, they capture the entire benefit *whether or not the
other side ever participates.*

There is no counterparty to recruit, no network to join, no platform for anyone else to
adopt. **That dissolves the twelve-counterparty wall that killed TradeLens, killed Holo
Sail, and has blocked this repository since [`docs/04`](04-strategic-assessment.md).**

It took five use cases to notice, and it is domain-independent.

## What exists already

Checked, per the discipline `docs/20` exists to enforce.

| Product | What it does |
|---|---|
| DoSurvey! (DS Marinesoft) | draft survey calculation for officers and surveyors, fleet data management |
| SurveyorMates | draft, bunker and oil survey calculation |
| Draft Survey Professional 3.1 | mobile calculator and report generator (updated Sept 2025) |
| SGS Draft Survey Tool | patented draft-reading measurement, proprietary calculation |
| Control Union Draft Survey Software System | proprietary, standardised protocol |

**Every one is a single-user calculator.** They help one person produce their own figure
faster and more accurately. **None addresses two parties arriving at figures independently,
and none makes a figure tamper-evident once recorded.**

That is a narrow, specific gap — which is the right shape, and the opposite of what `docs/20`
found for laytime.

## What Holochain would and would not add

Stated honestly, because [`docs/16`](16-external-review.md) exists to stop this repository
claiming more than it has.

**Not needed for the core.** Sealing a figure and anchoring it to independent timestamp
authorities is [`docs/13`](13-phase3-findings.md)'s Phase 3, already built and running. It
needs no DHT.

**What Holochain adds:** the master's figures accumulate on a chain that peers hold, so a
*pattern* becomes visible across voyages rather than one figure at a time — a master whose
sealed figures consistently end up matching the shipper's after the fact is a pattern that
only a persistent, peer-held record can show. And the record survives the owner changing
manager, IT system, or flag.

That is `docs/13`'s **"detection is the deterrent"** doctrine, and it is a genuine argument.
It is not an overwhelming one, and the honest sequence is to prove the premise before
building any of it.

---

## The question that decides everything

`docs/22` retracted the cargo-survey case because nobody had checked what surveyors
actually do — established joint-survey practice is *deliberately convergent*, and blinding
would damage it.

**The identical risk applies here and has not been tested:**

> **Is a joint draft survey — the master and the shipper's surveyor working the figure out
> together on deck — standard practice?**
>
> If it is, then sealing the master's figure first damages a convergence mechanism the
> industry believes in, and draft survey dies exactly as the cargo-survey case did.

Everything else in this document is contingent on that answer. **Ask it first.**

Two supporting questions, in the same conversation:

- When the ship's figure and the shipper's differ by more than 0.5%, what happens in
  practice — is the bill claused, or is an LOI taken?
- Has anyone ever suggested the master's figure was written *after* seeing the shore
  figure?

## Who to ask — no introduction required

- **IIMS** — the International Institute of Marine Surveying. 1,000+ members in 100
  countries, and *The Report* magazine explicitly invites member submissions, four times a
  year.
- **Named authors of P&I loss-prevention guidance** on draft survey and bulk shortage
  claims — **Gard**, **Britannia**, **Maritime Mutual**, **Steamship Mutual**. They have
  publicly declared an interest in this exact problem, and their clubs pay the claims.
- **Master mariners and chief officers**, who have actually done this on deck at 3am.

**Three conversations. No code.** If the answer to the question above is "yes, we do it
jointly," this document is the end of the line for shipping, and that is worth knowing for
the price of three emails.

---

**Sources**

- [Gard — Draft surveys, a critical tool to defend dry bulk cargo shortage claims](https://gard.no/en/insights/draft-surveys-critical-tool-to-defend-dry-bulk-cargo-shortage-claims/)
- [Britannia P&I — Preventing bulk shortage claims](https://britanniapandi.com/2025/03/loss-prevention-guidance-preventing-bulk-shortage-claims/)
- [Maritime Mutual — Draft Survey Defence of Dry Bulk Cargo Short Delivery Claims](https://maritime-mutual.com/risk-bulletins/draft-survey-defence-of-dry-bulk-cargo-short-delivery-claims/)
- [DS Marinesoft — DoSurvey!](https://www.dsmarinesoft.com/products/dosurvey-draft-survey-calculation-software/)
- [SGS — Draft Survey and Marine Services](https://www.sgs.com/en/services/draft-survey-and-marine-services-for-agricultural-commodities)
- [Control Union — Draft survey](https://www.controlunion.com/service/inspections/commodity-inspections/draft-survey-cargo/)
- [IIMS — The Report magazine archive](https://www.iims.org.uk/report-magazines/)
