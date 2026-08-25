# 08 — External evidence, and what the gap actually is

Earlier documents in this repository reasoned from Holo Sail's own record and from the TradeLens
post-mortem. This one tests those conclusions against what the maritime industry is doing **now**,
in 2026.

The research was produced with AI assistance (ChatGPT and Gemini) and is recorded as such. Every
load-bearing claim was then checked against the primary source, because AI-surfaced citations are
a category that requires it. The verification results are below, including one claim that did not
fully survive.

Checked 25 August 2026.

---

## Verification

| Claim | Status |
|---|---|
| DCSA: five eBL platforms adopt the interoperability annex, June 2026 | **Verified exactly.** 4 June 2026. CargoX, edoxOnline, TradeGo, WaveBL, eTEU. IGP&I approval confirmed. Three components: Platform Interoperability (PINT), a Control Tracking Registry (CTR), and a legal framework for jurisdictions without eBL legislation |
| IPCSA Network of Trusted Networks | **Verified.** Two-year trial, up to 70 ports, ten airports, multiple inland terminals. Connects existing Port Community Systems and Single Windows rather than replacing them. "Trusted and neutral" is their own framing |
| BIMCO 2026 declaration on fragmentation | **Verified, near-verbatim.** *Declaration on Shared Principles for Maritime Digitalisation and Harmonised Information Exchange*, following a March 2026 workshop: "digital solutions continue to develop in isolation, resulting in fragmented implementation, limited interoperability, and poor scalability. Maritime stakeholders rely on diverging data models, formats, interfaces, and interpretations" |
| BIMCO FuelEU Maritime Clause for Time Charter Parties 2024 | **Partly verified.** The clause is real, adopted 25 November 2024, and obliges owners to notify charterers of the vessel's aggregated Compliance Balance monthly, with surcharges attached. **The quoted phrase "independently validated information" did not surface in checking** and should be treated as paraphrase, not quotation |
| US AIS historical data is free and public | **Verified.** NOAA / MarineCadastre publishes bulk AIS for US coastal waters, 2009–2025, as zipped CSV and GeoParquet, described as "complete and analysis-ready," with no application required. Denmark's DMA also publishes historical AIS free, though it requires an application |

---

## What the evidence establishes

**The industry has the problem and knows it.** BIMCO's declaration is an industry body stating
plainly that maritime digitalisation is fragmenting and that solutions built in isolation do not
scale.

**And it is already solving the part we thought was the insight.** This matters, and earlier
documents in this repository should be read in its light.

[`docs/04`](04-strategic-assessment.md) argued that TradeLens died as an *owned* platform, and that
a neutral, non-owned layer was the untried proposition. That analysis stands — but the conclusion
that it is untried does not. IPCSA's Network of Trusted Networks is precisely a
"don't-make-everyone-join-one-network" architecture, connecting existing trusted systems. DCSA's
eBL annex does the same for bills of lading: an eBL can now move between platforms without every
party using the same one.

**We did not discover the need for neutral infrastructure. The industry got there first, and is
building it.** Any framing that presents neutrality as our contribution is wrong and would be
recognised as wrong by anyone in the sector.

## Where the actual gap is

What PINT, NoTN and the IMO Compendium solve is **pipe and schema neutrality**: A can send a
standardised message to B without a shared platform.

What they do not solve is whether the assertion inside the message is true — or, more precisely,
whether it was recorded when it claims to have been recorded.

An operational log generated on a ship, at a weighbridge, or in a terminal office can be adjusted,
delayed, or retrospectively amended before transmission. Moving an unverified assertion over a
standardised API does not make it true. It standardises the format.

That is the gap: **not data exchange, but claim integrity at the point of origin.**

---

## The distinction that decides what gets built

The external research treats all its examples as applications of blind commit-reveal. They are
not. Two different cryptographic properties are in play, and conflating them would produce a
product that does not do what it claims.

**Blind commit-reveal prevents *anchoring*.** Several assessors judge the same thing at the same
time; each commits before seeing any other. It stops herding and preserves genuine disagreement.
This is what ValiChord's protocol is built for.

**Commit-at-observation prevents *backdating*.** A single party records its own event and publishes
a hash immediately, so the record cannot be massaged afterwards. This is secure timestamping, or
notarisation.

Sorting the candidate use cases by which property they actually need:

| Use case | Problem | Property needed |
|---|---|---|
| Notice of Readiness / laytime | Carrier writes 06:00 when telemetry says 08:45 | **Timestamping** — parties record their own events at different times; nobody is judging anybody |
| FuelEU / EU ETS noon reports | Consumption figures "smoothed or adjusted after the fact" | **Timestamping** |
| SOLAS VGM / dangerous goods | Declared weight versus weighbridge versus crane load-cell | **Cross-source reconciliation** — arguably neither |
| Marine cargo damage survey | Two surveyors, same cargo, each waiting to see the other's position | **Anchoring** — the genuine fit |

The external research's own language gives this away: "pencil-pitching," "retrospectively doctor,"
"smoothed after the fact." Every one describes backdating, not herding.

**Why this matters commercially.** Timestamping is a crowded field — RFC 3161 timestamp
authorities, OpenTimestamps, and every blockchain ever built. A product whose headline capability
is tamper-evident timestamping competes in a solved category. The **anchoring** property is the
scarce one, and only the survey case requires it.

The honest position is that these are two distinct services sharing plumbing. Saying so is better
than letting the phrase "commit-reveal" paper over the difference — because a technically literate
counterparty will notice.

---

## Adjudication is a liability, not a feature

The external research includes a worked example: a validator that reads charterparty clauses,
detects a false Notice of Readiness, and outputs
`"financialImpactUSD": 4010.42` with `"confidenceScore": 0.99`.

**The arithmetic is correct.** Valid NOR at 08:45 plus six hours' turn time gives laytime
commencing 14:45; the claimed 06:00 would have given 12:00; the delta is 2.75 hours; 2.75/24 of
$35,000 per day is $4,010.42. The clause-15 tender-hours window is also handled correctly.

**The legal conclusion is not a computation.** Whether NOR was validly tendered turns on whether
the vessel was an "arrived ship" — a contested question under English law — and on whether WIBON
applies, which the scenario's own clause conditions on berth unavailability due to congestion that
is never established. London arbitration exists because these questions are genuinely arguable.

A system that emits a confident monetary figure on a contested legal question invites attack from
whichever party it disadvantages, and `confidenceScore: 0.99` on a legal determination is
unfalsifiable decoration.

**The defensible output is the discrepancy, not the adjudication:**

> Carrier committed 06:00 UTC. Independent AIS shows the vessel underway at 12.4 knots, 35nm
> outside port limits, at that timestamp. Anchor down 08:45. All four commitments verified intact
> and pre-dating reveal.

Stop there. "We establish the facts; you argue the law" is a position saleable to both sides of a
dispute. "Our model decides your demurrage" is saleable to one.

---

## The finding that changes feasibility

**AIS is public, free, historical, and machine-readable.**

NOAA's MarineCadastre publishes bulk AIS for US coastal waters covering 2009–2025 in analysis-ready
form, at no cost and with no application. Denmark's DMA publishes historical Danish AIS on
application.

Every previous document in this repository has flagged the same obstacle: **no maritime domain
access, and that was Holo Sail's only genuine asset** — two founders with twenty years on terminal
floors. See [`docs/02`](02-company-record.md) and [`docs/04`](04-strategic-assessment.md).

Public AIS is a partial substitute for that asset, available immediately. It means a working
demonstration of "a claimed operational event contradicted by independent telemetry" can be built
with **no partner, no pilot customer, no NDA and no introductions.**

It also makes the underlying premise cheaply falsifiable. Run real historical port calls against
real AIS and see whether divergence occurs often enough to matter. If it does not, the idea dies
for the cost of a weekend rather than a year.

This is the most consequential practical fact established anywhere in this repository.

---

## Revised position

[`docs/04`](04-strategic-assessment.md) recommended against picking this up, on the grounds that
the demand question was unanswered and domain access was missing. That recommendation is now
partially superseded:

- **Domain access** — partially solved by public AIS, for this class of question.
- **The problem's existence** — no longer speculation. BIMCO says it, the IMO's digitalisation
  work says it, and the eBL and NoTN programmes are the industry spending money on the adjacent
  layer.
- **The demand question** — still unanswered. Nobody has been asked whether they would pay.

What has changed is the cost of finding out. A falsification test is now days of work rather than
a business.

**Position: proof-of-concept, not a company.** Not a shipping platform, not a Port Community
System, not a transport layer — the industry is building those and is further along than we are.
A narrow, buildable artefact that tests one proposition: *can an independently-sourced record
demonstrate that a consequential operational claim was not recorded when it says it was?*

The plan for that artefact is [`09-demo-plan.md`](09-demo-plan.md).

---

**Sources**

- [DCSA — Five eBL platforms adopt DCSA interoperability annex](https://dcsa.org/newsroom/five-ebl-platforms-adopt-dcsa-interoperability-annex) (4 June 2026)
- [IPCSA — Network of Trusted Networks](https://notn.ipcsa.international/initiatives/network-of-trusted-networks/)
- [BIMCO — Declaration on Shared Principles for Maritime Digitalisation](https://www.bimco.org/news-insights/trending-topics/maritime-digitalisation/shared-principles/)
- [BIMCO — FuelEU Maritime Clause for Time Charter Parties 2024](https://www.bimco.org/contractual-affairs/bimco-clauses/current-clauses/fueleu-maritime-clause-for-time-charter-parties-2024/)
- [IMO — Maritime Single Window](https://www.imo.org/en/ourwork/facilitation/pages/maritimesinglewindow-default.aspx)
- [MarineCadastre — AccessAIS](https://marinecadastre.gov/accessais/) and [bulk vessel traffic data](https://hub.marinecadastre.gov/datasets/vessel-traffic-ais-1)
- [Danish Maritime Authority — download data](https://www.dma.dk/safety-at-sea/navigational-information/download-data)
