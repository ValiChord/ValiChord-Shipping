# ValiChord-Shipping

**A recovered record of Holo Sail Technologies' attempt to put container shipping on Holochain (2019–2022), why it stopped, and what — if anything — is worth picking up.**

This repository is research notes, not code. It exists because the primary sources are
disappearing: the Holochain forum has gone offline, Holo Sail's original domain has lapsed
and been re-registered by an unrelated party, and the Internet Archive was intermittently
unavailable during collection. Everything recoverable is preserved in [`sources/`](sources/),
with provenance recorded in [`sources/README.md`](sources/README.md).

Assembled 25 August 2026.

---

## The finding in one paragraph

Holo Sail Technologies filed two US patent applications covering container shipping on
Holochain. **Both were abandoned for failure to respond to an office action** — the first on
11 February 2022, the second on 4 April 2024. There is no granted patent, no enforceable
right, and no public code. The company still exists but has pivoted entirely to encrypted
communications and no longer mentions Holochain or shipping. What survives is a written
description of a system that was never built.

## What that means practically

**The design is free to build.** No patent exists, so there is nothing to infringe.

**The design is no longer patentable — by anyone, including us.** A published application is
prior art from its priority date regardless of whether it was ever granted. The priority date
here is **18 October 2019**. Anyone now attempting to patent container telemetry combined with
an agent-centric distributed network and payment-on-delivery must contend with this document.
Holo Sail's failure closed the door behind them.

**The hard part was never the technology.** See [`docs/04-strategic-assessment.md`](docs/04-strategic-assessment.md).
Holo Sail's own materials name twelve counterparty classes who must all participate before the
system does anything. Maersk and IBM's TradeLens — the competitor Holo Sail's patent explicitly
names as prior art — was shut down in November 2022, and the stated reason was that "the need
for full global industry collaboration has not been achieved." Two very differently resourced
attempts died at the same wall, and it was not the ledger.

**Everything of value this company produced is outside its patent.** The interoperability
standards work (IPCSA, ISO 28005, EDIFACT, IALA S-211) is on the archived home page. The
strategic analysis — including a correct prediction of TradeLens's collapse, published
twenty-two months before it happened — is in a
[gCaptain editorial](https://gcaptain.com/is-blockchains-role-in-supply-chain-logistics-overhyped/)
by the CEO. The patent contains neither, and instead explains what a blockchain is. **Start with
those two documents, not the PDF.**

---

## Contents

| Document | What it covers |
|---|---|
| [`docs/01-patent-record.md`](docs/01-patent-record.md) | Both filings, verified USPTO legal events, what the single claim actually says, and the comparison showing the continuation-in-part added nothing |
| [`docs/02-company-record.md`](docs/02-company-record.md) | Who Holo Sail were, the timeline from 2019 to today, and the documented drift from shipping to cyber-security |
| [`docs/03-community-response.md`](docs/03-community-response.md) | The Holochain community's contemporaneous reading of the patent, including Bob Haugen's hREA assessment |
| [`docs/04-strategic-assessment.md`](docs/04-strategic-assessment.md) | The adoption wall, the TradeLens precedent, and an honest case for and against picking this up |
| [`docs/05-source-inventory.md`](docs/05-source-inventory.md) | Every URL consulted, whether it is still live, and what could not be recovered |
| [`docs/06-nondominium-compatibility.md`](docs/06-nondominium-compatibility.md) | Whether a revived version would run on Nondominium/hREA. It would — and why that matters less than it sounds |
| [`docs/07-unyt-payments-and-the-survey-protocol.md`](docs/07-unyt-payments-and-the-survey-protocol.md) | Unyt answers the patent's payment gap; where a blind commit-reveal protocol actually fits; and why the claims application may be the wedge rather than an extra |
| [`docs/08-external-evidence-and-the-real-gap.md`](docs/08-external-evidence-and-the-real-gap.md) | What the industry is doing in 2026, verified. It is already building neutrality — the gap is claim integrity, not data exchange. Plus the finding that public AIS makes this buildable alone |
| [`docs/09-demo-plan.md`](docs/09-demo-plan.md) | A phased plan for one artefact, with an explicit record of which ecosystem components are deliberately **not** used |
| [`docs/10-phase0-findings.md`](docs/10-phase0-findings.md) | **Phase 0 ran and passed.** Maritime events can be timed to ~70 seconds from free public AIS, and self-reported status diverges from telemetry measurably |
| [`docs/11-phase1-findings.md`](docs/11-phase1-findings.md) | **Phase 1 built and working.** Commit–reveal–verify against a real vessel's real track, with a negative control proving the binding actually holds |
| [`docs/12-phase2-findings.md`](docs/12-phase2-findings.md) | **Phase 2 built.** The report rendered as one page, plus two layout bugs that were invisible in a screenshot and obvious in the numbers |
| [`docs/13-phase3-findings.md`](docs/13-phase3-findings.md) | **Phase 3 built.** A witness with nobody to recruit — and the attack it does not stop |
| [`docs/14-holochain-setup.md`](docs/14-holochain-setup.md) | What Phase 3b would actually cost. The toolchain is not the obstacle — two languages are |
| [`sources/`](sources/) | The recovered primary material itself |
| [`tools/fetch-missing-posts.sh`](tools/fetch-missing-posts.sh) | Retries the four blog posts still missing. Run it when the Internet Archive is healthy |
| [`tools/phase0/`](tools/phase0/) | The Phase 0 code. Regenerates every number in `docs/10` from public data |
| [`tools/phase1/`](tools/phase1/) | The Phase 1 demonstrator. `bash run.sh` reproduces `docs/11` end to end |
| [`tools/phase2/`](tools/phase2/) | Renders the discrepancy record as a single page. Sample output committed under `example_output/` |
| [`tools/phase3/`](tools/phase3/) | The witness layer — drand floor, OpenTimestamps ceiling, and a negative control that names what it cannot prove |

**Known gap.** Four 2020 blog posts remain unrecovered — the Internet Archive returned 503
throughout collection, and archive.today was checked by hand and holds nothing for this domain.
`what-is-a-port-community-system-pcs` is the one worth wanting. Details and the full list of
routes tried are in [`docs/05`](docs/05-source-inventory.md); the retry script above will fetch
them straight into `sources/` if the Archive recovers.

## Method and confidence

Findings are separated by how they were established:

- **Verified** — read directly from a primary source and quoted. Patent status and legal
  events were read from USPTO legal-event data; forum threads and web pages were recovered
  from the Internet Archive with snapshot timestamps recorded.
- **Derived** — a conclusion drawn by comparing sources, with the method stated so it can be
  rechecked. Example: the continuation-in-part comparison in `docs/01`.
- **Inference** — reasoning that goes beyond the documents. Always labelled as such. Example:
  why the examiner's office action was likely fatal.

Where a source could not be recovered, that is stated rather than glossed. Nothing in these
notes rests on an unrecorded source.

## A note on scope and fairness

This repository documents a company's public filings, public website, and public statements.
It reaches critical conclusions about those artefacts. It is not an assessment of the people
involved, several of whom brought deep maritime operational experience that the sector
genuinely lacks in its technology projects. Personal contact details found in archived pages
have been redacted. Corrections are welcome via issue or pull request.

## Licence

Apache License 2.0, matching the rest of the ValiChord organisation. See [`LICENSE`](LICENSE)
and [`NOTICE`](NOTICE). Quoted third-party material remains the property of its authors and is
reproduced here for research, commentary, and preservation.
