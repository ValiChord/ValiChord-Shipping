# 04 — Strategic assessment: is there anything here worth picking up?

**Short answer: not the thing Holo Sail was building. Possibly the thing they and TradeLens both
failed at, which is a different problem and closer to work we already have.**

---

## The wall both attempts hit

Holo Sail's own `/services` page (December 2021) lists who has to participate before the system
produces any value:

> Manufacturing · Trucking and Rail Companies · Ocean Shipping Lines · Terminal Operators ·
> Freight Forwarders · Freight or Marine Insurers · Retailers · Government Authorities ·
> Port Authorities · End-Customers · Distributors · Cargo-Insurers

Twelve counterparty classes. Most are commercial rivals. Several are regulators. The system
delivers nothing until a critical mass of them are all running nodes and publishing events.

This is a coordination problem wearing a technology problem's clothes, and it is the reason to
be cautious about the whole category.

### The TradeLens precedent

Holo Sail's patent names its competitor explicitly:

> "The competitors are searching in the wrong direction, for example, Maersk and IBM's
> Tradelens which is based on a blockchain platform."

On 29 November 2022, Maersk and IBM announced they were shutting TradeLens down. It went offline
by 31 March 2023. The stated reason was not technical failure:

> the platform was successfully developed, but "the need for full global industry collaboration
> has not been achieved," and it had not reached "the level of commercial viability necessary
> to continue operating"

So the record contains two attempts at this design:

| | Holo Sail | TradeLens |
|---|---|---|
| Resources | Four founders, no funding evident, no engineering team | The world's largest container line plus IBM |
| Ledger | Holochain (agent-centric) | Blockchain (Hyperledger Fabric) |
| Outcome | Two abandoned applications, no product | Built, launched, shut down |
| Cause of death | Never started building | Could not get the industry to join |

**Different resources, different technology, same wall.**

### The CEO predicted it, in print, twenty-two months early

This is the most surprising thing in the record, and it changes the assessment.

On 22 January 2021, Holo Sail's CEO published an editorial in **gCaptain** — a maritime trade
publication with a six-figure subscriber base — titled *Is Blockchain's Role in Supply Chain
Logistics Overhyped?* Full text at
[`../sources/website/2021-01-22-gcaptain-is-blockchains-role-overhyped.txt`](../sources/website/2021-01-22-gcaptain-is-blockchains-role-overhyped.txt).

It diagnoses TradeLens's actual cause of death before it happened, and not via the scalability
argument:

> "This implies long term challenges to the business model of the platforms, as the assumptions
> how the profits are generated challenges the conflict of interest arising out of the platform
> ownership. Tradelens provides an interesting illustration of this issue."

And the mechanism, precisely:

> "In addition to the conflict arising out of the carriers channelling transactions into their
> platform, computing is executed by a for-profit business (IBM) which is interested in
> maximizing profits from using its hardware to perform the computations… However, 'merchants'
> of logistics services are not inclined to pay any such fee themselves. It has to be passed in
> its entirety to the shippers who are yet to understand the nature of this additional charge
> and the need for it in the first place."

He also identifies the trust dynamic that makes the whole category hard:

> "our technology solutions are good for the tightly controlled silos of data and tightly
> controlled federations of data 'owners'. Any relaxation of those controls leads to breakdowns
> resulting in delayed freight, abandoned cargo, penalties, and losses."

— and the scope gap, that TradeLens and GSBN covered only containerised seafreight and would
have to "master the land-land moves" to be more than another fragment.

The article ends by turning the knife on his own industry, and implicitly on himself:

> "In the field of technology we often hear a comment about creating a solution looking for a
> problem which may not even exist."

**Correction to an earlier reading.** An initial pass over the patent alone supported the
conclusion that Holo Sail's thesis was "TradeLens has a scalability problem, agent-centric
architecture fixes it," and that events falsified this. That is accurate as a description of
*the patent*, which argues throughput and nothing else. It is not accurate about the company's
actual understanding. The CEO's published position was that ownership conflict and the fee
model were the binding constraints — which is what happened — with scalability as a secondary
technical argument. The diagnosis was right.

**What was missing was never the diagnosis.** It was the connection between the diagnosis and
anything built. The insight appears in a trade journal in January 2021. It appears nowhere in
the patent filed three months earlier, nowhere in the patent refiled a year later, and nowhere
in any product. The company's clearest thinking never reached its own work.

Anyone reviving this needs an answer to the adoption problem specifically. Swapping the ledger
is answering a question nobody was asking — a point Holo Sail's own CEO effectively made in
public and then did not act on.

---

## The case against picking this up

**The unbuilt part was never the interesting part.** Container telemetry is a solved commercial
category with many vendors. An agent-centric DHT is tractable engineering. Neither is where the
value or the difficulty sits.

**Holo Sail's real asset was relationships, and it is not recoverable.** Their `/collaborations`
page claims they had "already met and discussed working with various Port Authorities." Whatever
those conversations were worth, they belonged to two people with twenty years in terminal
operations and stevedoring. That cannot be reconstructed from an archive.

**The sector is well served on tracking.** Terminal49, Port Optimizer, and others do container
visibility commercially today. Entering as a better tracker means competing on features against
funded incumbents with existing carrier integrations.

**Domain distance.** ValiChord's existing traction is in research reproducibility — validators,
attestations, pre-registration. Maritime logistics shares an architectural shape but no users,
no relationships, and no credibility. Starting a second front is expensive in exactly the way a
solo founder can least afford.

**The patent route is closed.** See [`01-patent-record.md`](01-patent-record.md). The 2019
priority date is prior art against us too.

## The case for a narrow version

**TradeLens's failure mode is specifically an ownership problem, and that is interesting.** A
platform owned by the largest carrier asks every competing carrier to publish its operational
data into a rival's system. The industry declined, and it was right to. This is not a general
proof that industry-wide platforms fail — it is evidence that *owned* ones do. A neutral,
non-owned, verifiable evidence layer is a materially different proposition, and it has not
actually been tried at scale in this sector.

**That argument now has independent support from inside the industry.** The gCaptain editorial
above reaches the same conclusion from twenty years of terminal operations experience rather
than from architectural preference, and it reached it in a trade publication read by the people
who would have to adopt such a thing. When the strongest argument for a direction is made
independently by someone with completely different priors, it is worth more than an internal
conviction. This is the single most encouraging item in the whole record.

**That is much closer to existing ValiChord work than "shipping software" sounds.** The
transferable asset is not container tracking. It is the attestation format and the question of
how an outside organisation connects to a verification layer without ceding control to whoever
runs it. Framed that way, maritime is a second instance of a problem already being worked, not a
new business.

**The standards homework is done and it is good.** Holo Sail identified IPCSA, Port Community
Systems, the IMO data reference model, WCO, ISO 28005, UN/EDIFACT, and IALA S-211 — see
[`02-company-record.md`](02-company-record.md). This is the correct answer to "how does this
touch what ports already run," it is in the archived website rather than the patent, and it is
free.

**The narrow shape, if there is one:** not a platform that twelve parties must join, but a
verifiable attestation about a single handover event that one party can publish and any other
party can check without joining anything. Value at n=1 rather than value at n=critical-mass.
Whether that has a buyer is unknown and untested — see below.

---

## What is genuinely unknown

Recorded honestly, because these are the questions that decide it and none of them are answered
by the material in this repository:

1. **Does any port authority, insurer, or freight forwarder currently pay for verifiable
   provenance of handover events?** Not "would it be useful" — does a budget line exist. Cargo
   insurers are the most plausible candidate, since disputed liability at handover is their
   direct cost.
2. **What did TradeLens's participants actually object to?** The public statements are corporate
   summaries. The specific objection matters enormously and is not in the record here.
3. **Did anything survive TradeLens?** Its participants and integrations went somewhere. That
   diaspora is worth tracing before assuming a green field.
4. **Is the neutrality argument something buyers respond to, or only something builders find
   compelling?** This is the load-bearing assumption of the "case for," and it is untested.

## Recommendation

**Do not pick up Holo Sail's project.** It was a platform play requiring industry-wide
consensus, attempted by a team without the engineering to build it, in a category where a far
better-resourced attempt subsequently failed for reasons the patented design does not address.

**Do keep the file open on one specific question:** whether cargo insurers or port authorities
would pay for verifiable, non-owned attestations of individual handover events. That question is
answerable with a handful of conversations rather than a build, it reuses existing attestation
work rather than starting a new product, and it targets the failure mode that actually killed
the incumbent rather than the one the patent imagined.

The gCaptain editorial raises the value of that question. Before finding it, the neutral-layer
argument rested on our own reasoning about why TradeLens died. It now also rests on a maritime
operations professional publishing the same diagnosis, in the industry's own press, two years
before the event confirmed it. That does not make the question answerable from a desk — it makes
it worth the phone calls.

**One caution against over-reading it.** Diagnosing a market failure correctly is not evidence
that a business exists in the gap. Holo Sail is itself the demonstration: they had the right
analysis in January 2021 and it produced nothing. The article's closing line — about "creating
a solution looking for a problem which may not even exist" — should be read as applying to any
revival of this idea, including ours. The test is a budget line, not an argument.

If those conversations come back cold, this repository has done its job by costing a week
instead of a year.

---

**Sources for this document**

- [Maersk, IBM to shut down TradeLens — Supply Chain Dive, 30 Nov 2022](https://www.supplychaindive.com/news/Maersk-IBM-shut-down-TradeLens/637580/)
- [IBM, Maersk will shut down TradeLens — The Register, 30 Nov 2022](https://www.theregister.com/2022/11/30/ibm_and_maersk_tradelens_shutdown/)
- [TradeLens to be shut down due to lack of commercial viability — Shipping and Freight Resource](https://www.shippingandfreightresource.com/tradelens-to-be-shutdown-due-to-lack-of-commercial-viability/)
- [Port Community System — Port Economics, Management and Policy](https://porteconomicsmanagement.org/pemp/contents/part3/digital-transformation/port-community-system/)
- Holo Sail archived pages: [`../sources/website/`](../sources/website/)
