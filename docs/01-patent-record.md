# 01 — The patent record

## Two filings, both dead

Holo Sail Technologies filed twice. Neither was granted.

### Parent application

| Field | Value |
|---|---|
| Publication | US 2021/0174293 A1 |
| Application | 17/074,484 |
| Filed | 19 October 2020 |
| Provisional | 62/916,930, filed 18 October 2019 |
| Published | 10 June 2021 |
| Title | Method and System for Shipping and Receiving Process Automation |
| Applicant / Assignee | Holo Sail Technologies, Omaha, NE |
| Inventors | John Paul Vaughn Walker II; Horence Daus Hernando; Luke Pearse Glaser; Joseph O'Callaghan Glaser Jr. (all of West Caldwell, NJ) |
| Classification | G06Q 10/0833; H04L 9/0643; H04L 2209/38 |
| **Status** | **Abandoned** |

### Continuation-in-part

| Field | Value |
|---|---|
| Publication | US 2022/0156679 A1 |
| Filed | 4 February 2022 |
| Published | 19 May 2022 |
| Priority | Same — 18 October 2019 |
| Relationship | Continuation-in-part of 17/074,484 |
| **Status** | **Abandoned** |

## Verified legal events

Read from USPTO legal-event data as reproduced on Google Patents. Free-format text quoted
exactly.

**Parent (17/074,484):**

| Date | Code | Event |
|---|---|---|
| 2021-07-18 | STPP | `DOCKETED NEW CASE - READY FOR EXAMINATION` |
| 2021-08-02 | STPP | `NON FINAL ACTION MAILED` |
| 2022-02-11 | STCB | `ABANDONED -- FAILURE TO RESPOND TO AN OFFICE ACTION` |

**Continuation-in-part:**

| Date | Code | Event |
|---|---|---|
| 2022-04-12 | STPP | `DOCKETED NEW CASE - READY FOR EXAMINATION` |
| 2023-09-19 | STPP | `NON FINAL ACTION MAILED` |
| 2024-04-04 | STCB | `ABANDONED -- FAILURE TO RESPOND TO AN OFFICE ACTION` |

The pattern is identical both times. The examiner raised objections; no reply was filed; the
application went abandoned at the statutory deadline. This is not a case of losing an argument
on the merits. Nobody argued.

Note the sequencing: the continuation-in-part was filed on **4 February 2022**, one week before
the parent formally went abandoned on **11 February 2022**. The parent was allowed to lapse
while the same specification was refiled.

## What was actually claimed

The application contains **one claim and no dependent claims**. In full:

> **1.** A system for securely and safely shipping goods and services from supply source to a
> final destination using a computer-based Holochain platform, comprising:
> container means;
> Designate means attached to said container, for generating data for real-time geo-tracking
> and status monitoring of conditions both inside and outside of the container;
> communication means for transmitting data streams to and from the Designate means and other
> components of the Holochain platform;
> computer means using Holochain logic means for processing data uploaded from the Designates;
> and
> data stream monitor means by which customers and clients can access their personal manifests
> via HoloSail Designates during transit and receive appropriate payment upon delivery.

Two observations.

**A single claim with no dependents is a thin filing.** Dependent claims are the normal way to
build fallback positions, so that if the broad claim is rejected, a narrower one may still be
allowed. There were none. There was nothing to retreat to.

**Every element is drafted in "means-plus-function" form** — "container means," "Designate
means," "computer means," "data stream monitor means." Under 35 U.S.C. § 112(f), such a claim
is construed to cover only the specific structure disclosed in the specification, plus
equivalents. The specification discloses no structure for the Designate device at all beyond a
list of quantities it would measure. *(Inference: this construction, combined with the G06Q
business-method classification and the abstract-idea problem that follows from it, makes a
§ 101 and § 112 rejection the most probable content of the office action. The file wrapper is
behind USPTO authentication and was not read, so this is reasoning about a document not seen,
not a report of it.)*

## The continuation-in-part added essentially nothing

A continuation-in-part exists to add new matter to a specification. This one did not
meaningfully do so.

**Method.** The description body of the parent was isolated from the extracted PDF text
(from "FIELD OF THE INVENTION" to "What is claimed") and compared word-for-word against the
description of the continuation-in-part.

**Result.**

| | Words in description |
|---|---|
| Parent (US 2021/0174293 A1) | 3,366 |
| Continuation-in-part (US 2022/0156679 A1) | 3,399 |

A net difference of 33 words, roughly one percent. Sentence-level comparison showed the
apparent differences were artefacts of extracting two-column PDF text (hyphenation breaks such
as "auto-mate," "con-tain," "ofthe"), not substantive additions. The single claim is unchanged.

Both source texts are preserved in [`../sources/patent/`](../sources/patent/) so this can be
rechecked independently.

Fifteen months elapsed between the two filings. The technical disclosure did not advance.

## What the specification does and does not describe

**Described in reasonable detail** — the commercial process. The specification walks the
container from factory through freight forwarder, truck, terminal operator, crane, vessel,
destination port, dock, second truck, and final delivery, with a detection event at each
handover propagated to all parties to the transaction. This part reads as though written by
people who have actually worked a terminal, and it is the most credible content in the
document.

**Described as a list, not a design** — the "Designate" device. The specification enumerates
what it would report: ISO container type, shipping line owner, weight and dimensions, internal
temperature against a range, humidity, power draw and fluctuation, personalised manifests,
container opening during transit, off-loading at an incorrect destination, ETA from current
speed and route, and cargo shift alerts to crew. It says nothing about power, physical
mounting, radio, connectivity at sea, key custody, or how a device on a steel box in a stack
mid-ocean reaches a network at all. These are the actual engineering problems and none are
addressed.

**Asserted without support** — the network claims. The specification states that Holochain
makes transaction speeds and volumes "near-limitless," that security is "near impossible to
crack," and reports that "after a conversation with the Network development team, more
transactions we add to the network, the faster it will work." No benchmark, model, or citation
is offered. The payment mechanism is given as "atomic swap utilizing the Holochain networks
cryptocurrency Holofuel," with no design for it. *(What would fill that gap today is
assessed in [`07-unyt-payments-and-the-survey-protocol.md`](07-unyt-payments-and-the-survey-protocol.md)
— and it is not the currency they named.)*

**Not present at all** — anything about governance, onboarding, identity, dispute resolution,
or how competing commercial parties are induced to run nodes. See
[`04-strategic-assessment.md`](04-strategic-assessment.md); this is the omission that matters.

## Consequences for anyone building in this space

1. **No freedom-to-operate obstacle from Holo Sail.** Abandoned applications confer no rights.
2. **A prior-art obstacle to patenting.** Published 10 June 2021, priority 18 October 2019.
   The disclosure is broad and vague, which makes it *worse* as prior art, not better — vague
   disclosures are hard to design around in a patent claim while remaining novel.
3. **The business-method classification is a warning.** G06Q filings in this area face a
   difficult § 101 landscape. Anyone whose plan depends on patent protection for
   "supply chain + distributed ledger" should treat this record as evidence about the
   category, not just about one company.

---

**Sources for this document**

- [US20210174293A1 — Google Patents](https://patents.google.com/patent/US20210174293A1/en)
- [US20220156679A1 — Google Patents](https://patents.google.com/patent/US20220156679A1/en)
- [Holo Sail Technologies patent filings — uspto.report](https://uspto.report/company/Holo-Sail-Technologies)
- Local copies: [`../sources/patent/`](../sources/patent/)
