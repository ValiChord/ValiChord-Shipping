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

**Different resources, different technology, same wall.** Holo Sail's core thesis was that
TradeLens's problem was blockchain's scalability, and that agent-centric architecture solved it.
That thesis is now falsified by events: TradeLens did not die of throughput. It died of
adoption.

Anyone reviving this needs an answer to the adoption problem specifically. Swapping the ledger
is answering a question nobody was asking.

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
better-resourced attempt subsequently failed for reasons the design does not address.

**Do keep the file open on one specific question:** whether cargo insurers or port authorities
would pay for verifiable, non-owned attestations of individual handover events. That question is
answerable with a handful of conversations rather than a build, it reuses existing attestation
work rather than starting a new product, and it targets the failure mode that actually killed
the incumbent instead of the one Holo Sail imagined.

If those conversations come back cold, this repository has done its job by costing a week
instead of a year.

---

**Sources for this document**

- [Maersk, IBM to shut down TradeLens — Supply Chain Dive, 30 Nov 2022](https://www.supplychaindive.com/news/Maersk-IBM-shut-down-TradeLens/637580/)
- [IBM, Maersk will shut down TradeLens — The Register, 30 Nov 2022](https://www.theregister.com/2022/11/30/ibm_and_maersk_tradelens_shutdown/)
- [TradeLens to be shut down due to lack of commercial viability — Shipping and Freight Resource](https://www.shippingandfreightresource.com/tradelens-to-be-shutdown-due-to-lack-of-commercial-viability/)
- [Port Community System — Port Economics, Management and Policy](https://porteconomicsmanagement.org/pemp/contents/part3/digital-transformation/port-community-system/)
- Holo Sail archived pages: [`../sources/website/`](../sources/website/)
