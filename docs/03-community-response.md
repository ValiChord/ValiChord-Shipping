# 03 — How the Holochain community read the patent

Both source threads were recovered from the Internet Archive. **`forum.holochain.org` no longer
resolves**; the forum is gone. Full text is preserved in [`../sources/forum/`](../sources/forum/).

---

## The introduction — 27 March 2020

Thread: *Introducing Holo Sail Technologies, Inc*, posted by `luke.glaser`.

The thread is two posts long. The opening post is marketing copy with no architecture:

> "Holo Sail Technologies, Inc. strongly believes that the HoloChain platform has the answers to
> the failures of BlockChain. The adaptability of HoloChain makes it able to mitigate the
> potential negative effects of the thousands of actors and unpredictable factors which exist
> in the maritime industry."

The only reply, from `hubject` on 2 April 2020, notes that Holo Sail has been indexed in an
unrelated project directory. Four likes, one reply, no technical engagement in either direction.

**Holo Sail never posted a design, a DNA/hApp structure, a repository, or a technical question
to the community whose framework they were building on.** For a company claiming to be
mid-development on a Holochain application in 2020, this absence is itself a finding.

## The patent thread — July 2021

Thread: *Questions about Holo Sail Technologies Patent*, opened by `Brooks` on 20 July 2021,
cross-posted from Reddit user u/Goldenkat. Fifteen posts. This is the substantive record.

### The trigger

Holo Sail gave a promotional interview in which, per the opening post, they implied the patent
had already been granted and claimed vastly broader scope than the filing supports:

> "…I think we… would be missing a big part if we didn't mention that we have 16 other
> applications, industry applications on the patent… banking, fintech, law enforcement,
> emergency response… just to name a few… that are basically the same thing that we're doing to
> supply chain… basically plug and play… once we have all the nodes in for supply chain… once
> the supply chain is out of beta testing, we'll begin implement all the other 16 verticals
> that we have lined up."

`Brooks` checked and found no such content in the application:

> "In my read of the patent application, it doesn't specifically mention any of these other
> industries."

The only text supporting the claim is the standard boilerplate paragraph that appears in
essentially every US patent application, reserving unspecified additional embodiments.
`Brooks` also established that the patent was pending, not granted — correcting the interview —
and observed: "the patent is not written well in my opinion."

**This is directly verifiable against the filings, and it checks out.** Neither application
mentions banking, fintech, law enforcement, or emergency response. The "16 verticals" and the
"nodes in for supply chain… out of beta testing" both describe things that did not exist.

### The technical assessment

The most valuable post is **Bob Haugen** (`bhaugen`), of hREA / Valueflows — the same lineage
as the Sensorica and nondominium work. On 23 July 2021 he read the filing and concluded:

> "I re-read the patent document, and any system built on Holo-REA (aka hREA) could easily be
> able to do everything they mentioned. @pospi even did some experiments somewhat like that for
> BeefLedger."

And:

> "Everything they mentioned except the use of Holochain is being done by other systems now,
> including ones using blockchains, so their only differentiator I can see is Holochain."

This is the sharpest available summary of the invention's substance. Strip out the framework
choice and nothing remains that the logistics industry was not already doing.

Haugen's practical worry was ecosystem chilling:

> "Assuming they get the patent and defend it broadly, they could kill any other economic apps
> doing normal trade using Holochain. So, given that Holochain is prominently mentioned in
> their patent application, anybody wanting to create economic apps would be wise to avoid
> Holochain. Could have a depressing effect on the whole ecosystem."

He proposed the constructive resolution, which never came:

> "If Holo Sail were to pre-emptively give legally-reliable permission to any other Holochain
> apps, that could be a win-win. Otherwise I think they are bad for the ecosystem."

### The counter-reading

`stephenpurkiss` argued the concern was overstated, on two grounds. First, that the filing
claims the sum of many parts rather than Holochain itself. Second, that the Cryptographic
Autonomy License under which Holochain is released contains a patent-litigation termination
clause — quoted in the thread as CAL-1.0 § 5.3, under which initiating patent litigation against
the licensor or any recipient terminates all permissions granted to the litigant. His reading:

> "it looks like the patent coverage means if they did try to litigate they would lose use of
> it for themselves"

He immediately added that re-reading the clause left him "even more confused," and noted he is
not a lawyer.

He also identified the real cost, which was reputational rather than legal:

> "the issue here is more to do with the outside perception at this early stage of development
> and the impact it could/would have on adoption… if one large section doesn't go near it due
> to a perception then that hurts the community as a whole."

### The wider discussion

`jeremyboom8` proposed that the Holo Foundation establish an IP-stewardship function for
vulnerable early projects in the ecosystem, on the model of EFF-style defensive stewardship,
with a defence fund and an attorney referral list. Nothing came of it.

Several participants argued that intellectual property is illegitimate in principle. Haugen
supplied the grounding objection from lived experience — he had received a threat from an IP
claimant the previous day:

> "So it's a ludicrous system but it is unfortunately the one we are all living now…"

## What the thread got right, and what it missed

**Right:** the patent was pending not granted; it was poorly drafted; the "16 verticals" claim
was unsupported by the document; and Holochain was the only differentiator.

**Missed — understandably, since the information did not yet exist:** the entire concern was
moot. The office action had been mailed on 2 August 2021, nine days after Haugen's post. It was
never answered. Six months later the application was abandoned. The threat the community spent
July 2021 debating evaporated without anyone needing to do anything.

There is a reusable lesson in that. The community response was thoughtful, well-informed, and
aimed at a risk that dissolved on its own, while the actual signal — that this company had
published no code, engaged no developers, and posted twice on the forum in sixteen months — was
visible the whole time and went unremarked.

---

**Sources for this document**

- [Introducing Holo Sail Technologies, Inc](https://forum.holochain.org/t/introducing-holo-sail-technologies-inc/2620) — forum offline; archived 15 Jun 2025
- [Questions about Holo Sail Technologies Patent](https://forum.holochain.org/t/questions-about-holo-sail-technologies-patent-crosspost-from-reddit-user-u-goldenkat/6532) — forum offline; archived 20 Jun 2025
- Local copies: [`../sources/forum/`](../sources/forum/)
- [Cryptographic Autonomy License 1.0](https://opensource.org/licenses/CAL-1.0)
