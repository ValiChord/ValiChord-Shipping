# 29 — UR Z20, and a candidate answer to blocker 3

Written 27 August 2026. Read after [`28`](28-prior-art-and-the-general-case.md), whose
scorecard puts the entire remaining risk on **blocker 3: the party who must adopt loses by
adopting.**

This document is about a clause that appears to answer it.

## Source

**IACS Unified Requirement Z20, "Planned Maintenance Scheme (PMS) for Machinery"**, adopted
May 2001, Rev.1 July 2018, Rev.2 May 2019. Extracted from the consolidated UR Z document
published by IACS. Four pages. Confidence: **HIGH** — this is the primary text, not a summary
of it.

UR Z20 is what a class-approved PMS must satisfy, and it binds all IACS member societies —
DNV, LR, ABS, BV, ClassNK and the rest. An approved PMS is the alternative to Continuous
Machinery Survey: instead of a surveyor attending to open up machinery, the operator's own
recorded maintenance is credited.

## The clause

> **2.3.6** — *"The case of sale or change of management of the ship or transfer of class
> shall cause the approval to be reconsidered."*

**The exact event this whole project is about — sale or change of management — is written
into the international requirement as a trigger that puts the PMS approval at risk.**

And what does reconsideration rest on? The documentation listed in 2.2, which must be
available on board, including:

> **2.2.2(iv)** — *"records of maintenance including repairs and renewals carried out"*

Approval can also be withdrawn outright:

> **2.3.5** — *"The survey arrangement for machinery under PMS can be cancelled by the Society
> if PMS is not being satisfactorily carried out either from the maintenance records or the
> general condition of the machinery, or when the agreed intervals between overhauls are
> exceeded."*

## Why this answers blocker 3

Blocker 3 says the manager loses by adopting a portable record, because portability destroys
their leverage. That reasoning holds only while the record's value is purely defensive.

Z20 makes it operational. Follow the chain:

1. A vessel on an approved PMS avoids having a surveyor attend to open up machinery.
2. On a change of management, **the approval is reconsidered** (2.3.6).
3. Reconsideration depends on records of maintenance being available (2.2.2).
4. If those records did not survive the handover, the incoming manager cannot demonstrate
   the scheme, and the vessel drops back to CMS — surveyor attendance, opening up machinery,
   time alongside.

**So the incoming manager has a direct operational interest in receiving a complete record,
and the owner has one in the approval surviving.** The outgoing manager still has no
incentive — but this is the first version of the argument where the pain lands on someone at
a *predictable moment*, with a *known consequence*, rather than diffusely and years later.

It also reframes the pitch. Not *"your records might matter one day if there is a claim"* but
*"your PMS approval is reconsidered the day your manager changes, and reconsideration needs
records your outgoing manager has no reason to give you."*

**Confidence that the clause says this: HIGH. Confidence that it bites in practice: UNKNOWN,
and this is the question to ask.** A society might reconsider and wave it through as a
formality. If so, the argument collapses and we should know. That is now the single best
question in the file:

> When a vessel changes manager, what actually happens to the PMS approval? How often is it
> withdrawn, and what does the incoming manager have to produce?

## Three further findings from the same four pages

### The regulation already requires a personal signature

> **1.3.1** — *"The chief engineer shall be the responsible person on board in charge of the
> PMS."*
>
> **1.3.2** — *"Documentation on overhauls of items covered by the PMS shall be reported and
> signed by the chief engineer."*
>
> **1.3.3** — *"Access to computerized systems for updating of the maintenance documentation
> and maintenance program shall only be permitted by the chief engineer or other authorized
> person."*

This settles an argument the red teams had about
[`../spec/asset-record-entry-v0.1.md`](../spec/asset-record-entry-v0.1.md). I advised binding
signing keys to an **organisation** rather than an individual; the fourth red team said that
was wrong, because a company key ends up in a CI/CD pipeline and destroys individual
culpability.

**The red team was right and the regulation is already on its side.** Maritime requires the
chief engineer to sign personally, and requires access control on the system that holds it.
A format for this domain should bind to the individual, with organisational delegation on top
— because that is what the domain already does.

### Class is already an annual reader of these records

> **3.2.4** — *"The performance and maintenance records shall be examined to verify that the
> machinery has functioned satisfactorily since the previous survey…"*
>
> **3.2.5** — *"Written details of break-down or malfunction shall be made available."*
>
> **3.3.2** — *"Any repair and corrective action… shall be recorded in the PMS logbook and
> repair verified by the Society's surveyor at the Annual Audit."*

An Annual Audit by a surveyor is a condition of keeping the scheme. So on any vessel with an
approved PMS, **class already reads the maintenance record every year, by requirement.**
Putting class in the network is not an imposition to be argued for; it is a description of
what already happens.

### The backup requirement is twenty-five years out of date

> **2.1.3** — *"Computerized systems shall include back-up devices, such as disks/tapes, CDs,
> which are to be updated at regular intervals."*

Written in 2001 and untouched through two revisions. **There is already a requirement that
the record be backed up — it just describes tape and CDs.** That is a hook worth noticing:
we are not asking for a new obligation, only for a better answer to one that exists.

## What this does to the 85/15 gap

[`../tools/pms-model/`](../tools/pms-model/) records Lloyd's Register's figures: around 85%
of LR-classed vessels on a continuous survey cycle, only around 15% with an approved
Machinery Planned Maintenance Scheme, *"even though virtually all Operators are using
computerised planned maintenance systems."* **Now verified as LR's own words, published 21
June 2021** — so five years old, and LR-specific.

Z20 explains part of the gap. Approval requires submitting six categories of documentation,
an Implementation Survey by a surveyor within a year of approval, an annual report reviewed
by the Society, and an Annual Audit. That is real burden, and it is ongoing rather than
one-off.

Which sharpens the question into two competing explanations, with opposite consequences:

- **Approval is burdensome** → the 85/15 gap is a cost problem, and anything that makes
  approval and its maintenance cheaper is a product.
- **Operators do not want class inside their data** → the gap is a *preference*, blocker 3 is
  worse than we thought, and this whole direction is wrong.

Both are consistent with the evidence so far. **Distinguishing them is the highest-value
thing left**, and it may be answerable from class societies' own approval procedure documents,
which are published per society under 2.1.2.

## What has changed, honestly

Blocker 3 now has a **candidate** answer resting on a primary source rather than on
inference. That is a real improvement on this morning, when the only answer was "make the
writer benefit somehow."

It is not a validated answer. It rests on 2.3.6 biting in practice, and nobody in this
repository has ever spoken to anyone who has been through a PMS reconsideration. The kill
criteria in [`28`](28-prior-art-and-the-general-case.md) still stand unchanged.
