# What is actually inside a ship's PMS

```bash
python pms_model.py
```

Built from public sources so that [`../record-gap/`](../record-gap/) stops using a schema
invented to fit a magazine article. **Everything here is marked with a confidence level,
because the purpose of this file is to be corrected by someone who knows.**

An expert cannot correct a model that does not admit what it is unsure of, and a plausible
model that is quietly wrong is worse than an honest one that is visibly incomplete.

## The three things this changed about our own demo

**1. Lubricating oil is a *system*, not a component.** SFI primary group 6 is machinery main
components — engines, generators, boilers. Group 7 is the systems that serve them: fuel,
**lubricating oil**, starting air, exhaust, automation.

Our demo filed the contaminated oil batch against a generator in group 6. It belongs in group
7. And the distinction is not pedantry — **the entire causation argument turns on one LO
system being common to three engines**, which is exactly what a group 7 code expresses and a
group 6 code cannot.

**2. The code format was wrong.** SFI is a three-digit group plus a three-digit suffix, where
the suffix says what kind of thing it is: `NNN.000`–`NNN.099` is a *detail* code, a component
bought direct to the ship; `NNN.100`–`NNN.999` is a *material* code, a spare bought to stock.
We were using a three-part code of our own invention.

**3. We cannot publish real SFI codes, and we should stop pretending we know them.** See
below.

## The licence problem, and the honest response to it

**SFI is not free.** An SFI User Licence Certificate must be bought from SpecTec, one per
ship or site, with further charges per manual or database. SpecTec also own AMOS, the most
widely used marine PMS.

So this repository records SFI's **structure**, which is publicly described, and does **not**
reproduce SFI's **code tables**, which are not.

Which leaves us honestly stuck on the detail, and the sources disagree:

- One says group 6 → 60 "diesel engines for propulsion" → 601 "diesel engines" → `601001`
  "main diesel engine".
- Another shows `632.001` as "Main Engine".
- A third places `612`/`613` as high and medium-pressure steam turbines under "61 propulsion
  steam machinery", which is incompatible with the first.

We cannot settle that without the licensed manual. **So every subgroup value in
`pms_model.py` is written as `6XX.001` — SFI-shaped and visibly not SFI.** That is deliberate.
It is the single most correctable thing in this repository, and a superintendent or any AMOS
user could fix it in about ten seconds.

## The field that this whole project is about

Of everything a PMS job record carries — component, job code, intervals, running hours, dates,
criticality, class flag — one field is different:

**`remarks`. Free text. It holds the finding, the reason and the judgement.**

It is the least structured thing in the database and therefore the least portable through a
migration. In the Gard turbocharger case it is precisely what was missing: the *fact* of the
cartridge changes survived, because the purchase orders were in the owner's own accounts. The
*reason* did not.

Everything else in a PMS is a number or a code and survives being exported badly. The reason
does not.

## The finding worth chasing first

**Continuous Machinery Survey.** Rather than a surveyor attending to open up machinery, class
spreads machinery surveys across a five-year cycle. Under an **approved** planned maintenance
scheme, maintenance carried out and recorded on board under the chief engineer's
responsibility **earns survey credit**, with the class surveyor reviewing records and
sampling completed jobs at periodic visits.

Then the numbers:

> Around **85%** of Lloyd's Register classed vessels are on a continuous survey machinery
> cycle. Only around **15%** have an approved Machinery Planned Maintenance Scheme — *"even
> though virtually all operators are using computerised planned maintenance systems."*

**Nearly everyone holds the data. Very few hold it in a form class will credit.**

Why that matters more than anything else in this file: [`../../docs/28`](../../docs/28-prior-art-and-the-general-case.md)
identifies blocker 3 — the party who must adopt loses by adopting — as the whole remaining
risk. Survey credit is a benefit that accrues **to the party doing the writing**. It is the
same shape as the CoverSense answer: the writer benefits, and the asset record is a
by-product.

It also puts class in the network as a natural reader rather than an imposition, because
under CMS class is *already* reading these records.

**Confidence: MEDIUM, single source, and Lloyd's-specific. Verify this before building
anything on it.** If the 85/15 gap is real and the reason is that approval is burdensome,
that is a product. If it is real because operators simply do not want class in their data,
that is the opposite of a product — and it would be much better to learn that early.

## Glossary

For keeping up in a conversation rather than nodding.

| Term | What it means |
|---|---|
| **PMS** | Planned Maintenance System. The software holding the job schedule and history |
| **CMS / CSM** | Continuous (Machinery) Survey. Machinery surveys spread over a five-year cycle rather than done at once |
| **MPMS** | Machinery Planned Maintenance Scheme — a PMS *approved* by class, so recorded work earns survey credit |
| **SFI** | The component coding system. Proprietary, SpecTec |
| **Detail code** | Component bought direct to the ship (`NNN.000`–`NNN.099`) |
| **Material code** | Spare bought to stock (`NNN.100`–`NNN.999`) |
| **Running hours** | The counter on a machine. The usual basis for maintenance intervals |
| **Critical equipment** | Equipment whose sudden failure could cause a hazardous situation. Identified under ISM |
| **ISM Code** | Requires a maintenance programme and records. A change of manager triggers a new DOC and SMC — **but not a transfer of records** |
| **DOC / SMC** | Document of Compliance (the company) / Safety Management Certificate (the ship) |
| **Superintendent** | The shore-based technical manager responsible for a handful of ships |
| **H&M** | Hull and machinery insurance. Covers damage to the ship itself |
| **P&I** | Protection and indemnity. Third-party liabilities. Gard is a P&I club |
| **Deductible** | The amount the owner bears before insurance responds |
| **Subrogation / recovery** | The insurer pursuing a third party after paying a claim |
| **Average adjuster** | Independent professional who determines how a marine loss is apportioned |
| **Class society** | DNV, LR, ABS, BV, ClassNK. Certify the ship against their rules and survey it |
| **SHIPMAN** | BIMCO's standard ship management agreement. 2024 edition, Clauses 21 and 22 |

## What to ask someone who actually knows

In rough order of how much the answer would change:

1. **Is the 85/15 CMS gap real, and why?** Is approval burdensome, or do operators not want
   class inside their data?
2. **What are the correct SFI codes** for an auxiliary generator engine, its turbocharger, and
   the LO system serving all three?
3. **When a manager changes, what actually arrives?** A database export, PDFs, paper, or
   nothing? Does the remarks field survive?
4. **Who reads a maintenance record other than the crew?** Class, insurers' surveyors,
   vetting inspectors, buyers' technical inspectors — and what do they each ask for?
5. **Is criticality a three-way split in practice, or does every operator do it differently?**
