# 20 — Is this already solved? Mostly yes, and here is exactly what is left

**Short answer: AIS-derived port event timing is a mature commercial product, sold today by
at least two integrated vendors, and the industry's own account of where demurrage money is
lost does not mention disputed facts. The laytime framing this repository has been building
towards is occupied. What survives is narrower than Phases 0–3 assumed, and it is not the
part that was built.**

Asked directly by Ceri John on 26 August 2026 — *"is this really a thing no one else has
solved… I don't want a patronising response to any email"* — which is the correct question
and should have been asked before `docs/16` Part 7 proposed Phase 0b.

---

## What already exists

**Marcura** — PortLog, DA-Desk, and Claims PDMS:

> PortLog "combines digitised Statements of Facts, agent data, DA-related information, AIS,
> and weather into an anonymised, cleansed dataset focused at the terminal level."

> "Marcura Claims' PDMS tracks port calls by AIS and chases agents until a verified bundle
> arrives."

> SOFs "are processed through an AI pipeline trained on more than 700,000 documents, then
> validated by a specialist QA team."

**Veson Nautical** — IMOS, integrated with Marcura's PortLog, and owner of **Oceanbolt**,
whose AIS-derived port congestion data feeds Veson's estimated-demurrage calculations.

So: **AIS event detection, reconciled against Statements of Facts, feeding a demurrage
calculation, is a shipped product with an AI pipeline and human QA behind it.** At the scale
of 700,000 documents.

That is, with precision, the capability Phases 0–2 demonstrate.

Add the wider AIS analytics layer — Windward, Spire, Kpler, Lloyd's List Intelligence,
Signal Ocean, Pole Star — and a claim of *"I can time a vessel's arrival from AIS"* lands in
a room where everyone present already buys that.

## What the industry says the problem actually is

Marcura's own account of demurrage leakage names four causes. **None of them is a
disagreement about when the vessel arrived.**

| | Cause | Their figure |
|---|---|---|
| 1 | Incomplete calculations — analyst workload forces selective transcription | *"At $15,000–$30,000 per day, each unrecovered detail compounds"* |
| 2 | **Missed time bars** — deadlines tracked informally | *"One real portfolio documented $450,000 in time bar failures in a single year"* |
| 3 | Data that cannot be queried — SOFs exist but not in structured form | *"SOFs exist, but not in a form that makes them useful"* |
| 4 | Expertise leaving — institutional memory walks out with the analyst | — |

And the headline number: **"99% of statements of facts are still processed manually across
the industry, consuming an estimated 12 million hours per year."**

**The pain is transcription labour and process discipline, not contested facts.**

## Our own evidence already said this and it was not heard

[`docs/17`](17-phase0b-case-candidates.md) found that the one runnable real case — *Tricon
Energy Ltd v MTM Trading LLC* [2020] EWHC 700 (Comm) — had **times that were common
ground.** The dispute was whether the demurrage claim was time-barred for missing
documents. That is cause 2 in the table above, in a real judgment, and it was recorded as a
"structural tension" rather than as what it was: the premise failing.

Three independent sources now agree — a vendor's product line, a vendor's problem
statement, and a court record.

---

## The strongest case against this conclusion, stated fairly

Per [[differential red-teaming]]: having argued the negative, here is the positive.

- **Laytime disputes are reported as roughly 30% of all charterparty arbitrations, average
  claim above $200,000.** *(Attributed to LMAA 2024–25 data by a vendor page; not verified
  against LMAA directly. Treat as indicative.)* That is a large, live, expensive category.
- **Competing Statements of Facts genuinely happen.** In head- and sub-charter chains,
  different agents present different SOFs to the Master, and the Master may produce their
  own. **London Arbitration 6/17** turned on SOFs containing different rainfall evidence.
- Small wording and timestamp differences in an SOF do shift real money.

So factual disagreement is not imaginary. The question is whether *telemetry* resolves it.

## Why telemetry mostly does not — the limitation that decides everything

**AIS sees position, speed, heading and navigational status. That is all it sees.**

A Statement of Facts is a list of thirty-odd operational events. AIS can speak to perhaps
four to six of them:

| AIS can establish | AIS cannot see |
|---|---|
| Arrival at port limits | Hoses connected / disconnected |
| Anchor down, anchor aweigh | Cargo operations commenced / suspended / resumed |
| Berthing and unberthing | Rain stopping work |
| Departure | Pumping rates, tank inspections, ullage |
| | Documentation, surveyor attendance, free pratique |

**London Arbitration 6/17 turned on rainfall.** AIS has nothing to say about rainfall.

This is the objection a laytime professional raises in the first two minutes, and the
repository has no answer to it. `docs/09` anticipated a version of it under "resolution may
not survive contact" but framed it as a precision problem. It is not a precision problem. It
is a **coverage** problem, and precision does not help.

---

## What actually survives

Being strict about it, three things — and only the third is worth much.

**1. The blind pre-commitment property is genuinely unsold.** Nobody offers "both parties
seal their version before either sees the other's." Marcura reconciles *after the fact*, as
a vendor engaged by a party. But — the evidence above says facts are not the main dispute,
so there is no demonstrated demand for solving them better. **An unmet need is not the same
as an unsold product.**

**2. Neutrality of the reconciler.** Marcura's output is Marcura's. It has not been
committed to in advance by both sides. This is a real structural difference and the industry
shows no sign of minding.

**3. The marine cargo survey case — and this is the one.** Two surveyors, one appointed by
the P&I club and one by the cargo underwriter, board the same vessel, inspect the same
cargo, and each waits to see what the other will argue before finalising. That is
**anchoring**, not telemetry. No AIS product touches it, because no telemetry exists for
"was this damage pre-existing." The evidence is human judgement, and the failure mode is
that the judgements are not independent.

**[`docs/08`](08-external-evidence-and-the-real-gap.md) identified this correctly and
[`docs/09`](09-demo-plan.md) placed it last.** Both were right. It was deferred because it
requires surveyors, which requires relationships — the same wall everything else in this
repository has been routing around since Phase 0.

---

## What this means, plainly

**Phases 0–3 built a working, honest demonstration of a capability that is already
commercially available.** The engineering is sound and the numbers reproduce. The market
position does not exist.

**The kill criteria in `docs/09` were about resolution and coverage of the data.** They
should have included a competitive one: *does anyone already sell this?* Nobody asked until
Ceri did, five documents later.

**This does not kill ValiChord.** It kills laytime as the wedge. The distinction matters:
ValiChord's actual mechanism — blind commit-reveal to prevent anchoring between independent
assessors — was never what the laytime demo needed. `docs/08` said so in its own table:
laytime is a *backdating* problem, and *"the anchoring property is the scarce one, and only
the survey case requires it."*

**The repository has been building the wrong half of its own analysis for four phases.**

## What to do

1. **Do not send the Tier 1 emails as drafted.** They lead with seventy-second AIS timing,
   which reads as naive to anyone who has met Marcura. Rewritten in
   [`../outreach/draft-emails.md`](../outreach/draft-emails.md).
2. **The Lloyd's Register email is fine** — it asks whether the work fits their remit and
   does not claim novelty.
3. **Change the question being asked.** Not *"would independent arrival times be useful?"*
   but *"when two surveyors disagree about cargo damage, does anything today stop the second
   one waiting to see the first one's position?"* That is answerable, it is not served by
   any product found here, and it is where the mechanism actually fits.
4. **Keep the demonstrator.** It works, it is honest, and it shows the mechanism to a
   technical audience in ninety seconds. It is a credential, not a product.

---

**Sources**

- [Marcura — The Four Causes of Demurrage Leakage](https://marcura.com/resources/blog/demurrage-claims-leakage)
- [Marcura — Port Call Management / DA-Desk](https://marcura.com/manage-port-calls)
- [Marcura — PortLog](https://www.portlog.com/)
- [Veson Nautical and Marcura integration](https://veson.com/news/commodity-shipping-to-optimize-port-time-financials-in-digital-solution-by-veson-and-marcura/)
- [Veson IMOS — Estimated Demurrage](https://help.veson.com/imos/imos-estimated-demurrage) (Oceanbolt / PortLog webhook import)
- [CharterPartyDisputes — Statement of Facts](https://www.charterpartydisputes.com/laytime-and-demurrage/sof) (competing SOFs; London Arbitration 6/17)
- [*Tricon Energy Ltd v MTM Trading LLC* [2020] EWHC 700 (Comm)](https://caselaw.nationalarchives.gov.uk/ewhc/comm/2020/700)
