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
| [`docs/15-dna-architecture.md`](docs/15-dna-architecture.md) | The DNA design — `registry`, `telemetry`, `voyage`, `record`, and the platform constraint that dictates how they connect. **Read alongside [`docs/16`](docs/16-external-review.md), which finds seven problems with it and recommends parking it** |
| [`docs/16-external-review.md`](docs/16-external-review.md) | **An outside review, 26 Aug 2026.** Phases 0–3 stand; `docs/15` is where the project turned away from its own conclusions. Seven Holochain findings, two places the code is weaker than the write-up, a bug in ValiChord, corrected grant status, and a retrospective test that needs no counterparty |
| [`docs/17-phase0b-case-candidates.md`](docs/17-phase0b-case-candidates.md) | **Phase 0b ran.** 290 published judgments mined for real disputed times; 43 mention a US port, three survive reading, and the false positives are the instructive part |
| [`docs/18-outreach-and-funding.md`](docs/18-outreach-and-funding.md) | Who to contact and why they are reachable without an introduction, plus the funding calendar — every named UK call is currently shut |
| [`docs/19-handover-brief.md`](docs/19-handover-brief.md) | **Read first if you are picking this up.** The stopping condition that was missing, four corrections to carry, and what not to do |
| [`docs/20-is-this-already-solved.md`](docs/20-is-this-already-solved.md) | **⚠️ READ BEFORE WRITING TO ANYONE IN THE INDUSTRY.** Marcura and Veson already sell AIS-to-SOF reconciliation at scale, and the industry's own account of demurrage leakage never mentions disputed facts. What survives, and why it is the survey case |
| [`docs/21-tricon-run.md`](docs/21-tricon-run.md) | **A real judgment reconstructed from real AIS.** The method works end to end with no counterparty — and corroborates rather than contradicts, which is the finding |
| [`docs/22-why-shipping-resists-this.md`](docs/22-why-shipping-resists-this.md) | **Four more use cases scanned before building. Three occupied, one occupied by a contract clause nobody uses.** The cross-cutting finding: the party who would be verified usually controls both the evidence and the purchase — and the only adoption that ever worked was a port authority mandating it |
| [`docs/23-draft-survey.md`](docs/23-draft-survey.md) | **The one candidate that survives.** Judgement not measurement, an agreed 0.5% tolerance, buyer is not the constrained party, and adoption is unilateral — plus the single question that would kill it |
| [`outreach/draft-emails.md`](outreach/draft-emails.md) | Five drafts. Nothing sent. One is marked HOLD until Phase 0b actually runs |
| [`sources/`](sources/) | The recovered primary material itself |
| [`tools/fetch-missing-posts.sh`](tools/fetch-missing-posts.sh) | Retries the four blog posts still missing. Run it when the Internet Archive is healthy |
| [`tools/phase0/`](tools/phase0/) | The Phase 0 code. Regenerates every number in `docs/10` from public data |
| [`tools/phase0b/`](tools/phase0b/) | Mines Find Case Law for judgments with a named vessel, a US port and a disputed time. Scored candidates committed | Includes `tricon_run.py`, which reconstructs the [2020] EWHC 700 port call from public AIS.
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
