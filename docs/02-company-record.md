# 02 — The company record

## Who they were

Holo Sail Technologies, Inc. — Omaha / Papillion, Nebraska (Sarpy County), with the founding
team based in West Caldwell, New Jersey. A related entity, Holo Sail Technologies LLC, is
registered in Wyoming. Publicly described as veteran-run.

The team roster as archived on 3 August 2020:

| Person | Role | Background as stated |
|---|---|---|
| Johnny Walker | Chief Executive Officer | Diesel mechanic, US Marine Corps Reserve motor transport, 1997. 20+ years across vessel operations, stevedoring, strategic planning, terminal safety and emergency response, route logistics, labour management, warehouse, breakbulk, containerisation, government regulations |
| Horence Hernando | Chief Operations Officer | SUNY Maritime College — marine business and commerce, minors in pre-law, humanities, maritime security. Deck licence programme. Sailed with Military Sealift Command, then marine terminal operations and stevedoring |
| Joey Glaser | Director of Technology Development | "10+ years of blockchain and cryptocurrency research"; specialises in "concept design, research, management" |
| Luke Glaser | Co-Director of Technology Development | Data engineer |
| Mason Stotts | Deputy Director of Technology Development | Joined as webmaster; IT, web and graphic design, business management |
| Ace Rodriguez | Director of Government Affairs | Nursing degrees; works for DaVita Inc.; UN representative for 5+ years |
| Archie Edward Williams III | Former Deputy Director of Operations (d. 2020) | International economics, game theory, psychology; graduate work in health sciences, international transportation, shipping management, logistics and supply chain, ship brokering and chartering; Merchant Mariner Credential; US Navy and Merchant Marines |

One further name appears in the February 2021 American Reporter article rather than on the
archived team page: **Dr. Jasmin Cowin**, described as Advisor to Executive Management,
Assistant Professor and Practicum Coordinator at Touro College Graduate School of Education, and
co-author of an SDG 4 corporate guidebook series at the SHERPA Institute. She is co-author of
that article. The archived `/advisors` page (December 2021) exists but did not capture its
contents, so the full advisory roster is unknown.

**The shape this describes matters more than any individual.** The maritime operations side was
deep and real — terminal operations, stevedoring, Military Sealift Command, merchant mariner
credentials. The engineering side was one data engineer, one webmaster promoted to deputy
director, and a director of technology whose stated qualification is a decade of *researching*
cryptocurrency. The company self-described as "divided into two specialties." The half that
knew shipping was strong. The half that had to build a distributed system on an
alpha-stage framework was not staffed for it.

*(Inference: this composition is the most economical explanation for the whole record —
credible operational analysis, no engineering artefacts, and two patent applications abandoned
through simple non-response, which is what happens when nobody in the building owns the
prosecution.)*

## The best technical thinking is on the website, not in the patent

This is the single most useful discovery in the corpus. The archived home page (3 August 2020)
contains concrete standards-interoperability work that appears **nowhere** in either patent
application:

> IPCSA is standardizing international shipping in conjunction with/using a PCS, IMO data
> reference model, WCO, and ISO - 28005
>
> Using the EDIFACT messages we can take the data from ISO - 28005 or something similar like
> the IALA's S-211, plugging that into our system bridging the gap

Decoded: the International Port Community Systems Association; Port Community Systems; the IMO
Compendium data model; the World Customs Organization data model; ISO 28005 (electronic port
clearance); UN/EDIFACT messaging; and IALA S-211 (port call message format).

That is a correct and specific answer to "how does this connect to what ports already run."
It is the question every logistics platform actually dies on, and Holo Sail had identified the
right standards to answer it. The patent — the document they spent money on and pointed
investors at — contains none of it, and instead spends its length restating what a blockchain
is.

The same page states the intended operational outcome plainly:

> Only drivers who have customs-cleared containers ready will be at the gate. Time windows and
> customs checks will be completely predetermined.

**Anyone picking this up should start from the archived website and the gCaptain editorial, not
the patent.** The pattern holds across the whole corpus: everything of value the company
produced is outside its patent applications. The standards work is on the home page. The
strategic analysis is in a trade journal. The patent has neither.

## Timeline

| Date | Event |
|---|---|
| 18 Oct 2019 | Provisional application 62/916,930 filed |
| 27 Mar 2020 | Luke Glaser introduces the company on the Holochain forum. Two posts in the thread; no architecture disclosed |
| 3 Aug 2020 | Website archived: shipping-first, standards-aware, names IPCSA / ISO 28005 / EDIFACT / S-211 |
| **29 Sep 2020** | **Blog post "The Path to a More Secure World" — pure cyber-security framing, no shipping content. Three weeks before the non-provisional is filed** |
| 19 Oct 2020 | Non-provisional 17/074,484 filed |
| **22 Jan 2021** | **CEO publishes an editorial in gCaptain: "Is Blockchain's Role in Supply Chain Logistics Overhyped?" The strongest document in the entire corpus — see [`04-strategic-assessment.md`](04-strategic-assessment.md)** |
| 10 Jun 2021 | Application published as US 2021/0174293 A1 |
| Sep 2021 | "Healing the Heroes of 9-11" documentary released, featuring the CEO |
| Jul 2021 | Promotional interview with Jonny Stang; community raises concerns on Reddit and the Holochain forum (see [`03-community-response.md`](03-community-response.md)) |
| 2 Aug 2021 | Non-final office action mailed |
| 7 Dec 2021 | Website archived: still no architecture; pitch now leads with "cloud-based vulnerabilities" and "superior cyber-security" |
| 4 Feb 2022 | Continuation-in-part filed — same specification |
| 11 Feb 2022 | **Parent abandoned** — failure to respond |
| 28 May 2022 | Trademark filed: "Haven by Holo Sail" — encrypted video conferencing |
| 2022 | Site restructured to `havens-den`, `holosailhaven`, `havencomms`, `havenconnect`, `havenfiles`, `havenops`, `havenvideopro`, `safehaven` |
| 13 Sep 2022 | Further trademark application filed |
| 19 Sep 2023 | Non-final office action mailed on the continuation-in-part |
| **4 Apr 2024** | **Continuation-in-part abandoned** — failure to respond |
| 10 Feb 2025 | CEO interview: company sells "HoloStacks," zero-trust decentralised encrypted infrastructure. Holochain not mentioned. Shipping not mentioned |
| By 2026 | `holosailtechnologies.com` has lapsed and been re-registered by an unrelated party, now serving Indonesian song-lyrics content |

## The pivot began earlier than it appears

The obvious reading — trademarks and site restructuring in 2022 — puts the pivot after the
first patent was abandoned. The archived blog corrects this.

"The Path to a More Secure World," dated 29 September 2020, is entirely about cyber-security
and contains no shipping content. It predates the non-provisional filing by three weeks. The
December 2021 `/services` page, more than a year later, still leads on security framing and
still contains no architecture.

**The drift away from shipping started before the patent that documents the shipping design was
even filed.** By the time the examiner's letter arrived in August 2021, the company's public
attention had been elsewhere for the better part of a year. That is a more coherent explanation
for two unanswered office actions than oversight.

The claim in the same post that the technology is "Cloud free and impenetrable to modern Cyber
and hacking attacks" is worth recording for calibration. Nothing is impenetrable, and the claim
indicates how the company's technical statements should be weighted generally.

## Why the pivot happened: they found a user

The archived `holosailhaven` page (May 2022) supplies the missing explanation, and it is not a
business-strategy story.

The page describes Haven as **"Holo Sail's first live product"** — "a private social network
designed for organizations and businesses," pitched as "FaceBook without the data harvesting."
Note the date. Roughly two and a half years after the provisional application, the first thing
the company shipped was a social network, not the shipping system.

The page carries a testimonial from the founder of **22ZERO**, a non-profit that treats PTSD in
veterans and first responders:

> "That video has been viewed around 34,000 times in two days with several thousand comments.
> We helped Cheri in the video Heal her PTS that's she's dealt with since childhood. As a result
> we are up to nearly 300 requests for help… Holo Sail Technologies developed a PTSD assessment
> tool through their platform that we can send directly to the client, they fill out the
> symptoms and they are scored, we get a copy the client gets a copy and we forward the case to
> the coaches. Normally I would have had to do assessments by phone. 15 minutes each. Multiply
> that by 300."

The connection is personal and publicly documented by the parties themselves. By 22ZERO's own
account, the CEO was a US Marine present in New York on 11 September 2001, was interviewed for
their documentary, and went through their programme. He then built them software.

**This is the clearest contrast in the record.** On one side, a shipping platform requiring
twelve classes of commercial counterparty to agree before it produced any value, with no
signed adopter after two and a half years. On the other, a single organisation with 300 people
waiting and a concrete task — score an assessment, route it to a coach — that software could
discharge that week.

They went where the users were. Given the two options as they actually stood, it is difficult
to call that the wrong decision.

*(Inference, but a well-supported one: this reframes the abandoned patents. The applications
were not neglected through incompetence so much as deprioritised in favour of work that had
someone waiting for it. The office actions went unanswered because by then nobody wanted the
thing the patent covered.)*

## Evidence of traction

The archived blog displays view counts. "The Path to a More Secure World" shows **8 views**.
The adjacent posts show **13**, **13**, and **23**.

That is the measured public reach of the company's content operation. Combined with the absence
of any public code repository — searched for specifically, none found under any spelling — and
two applications abandoned without reply, the record does not support the picture of an active
development effort that ran out of runway. It supports a small team that produced positioning
material and never converted it into a product.

## Holochain disappeared from their messaging almost immediately

Tracking the word "Holochain" across their public output produces a sharper timeline than
tracking the product:

| Date | Document | How the technology is described |
|---|---|---|
| Mar 2020 | Holochain forum introduction | Holochain, named and central |
| Oct 2020 | Patent application filed | Holochain, named throughout; it is the entire claimed differentiator |
| **Jan 2021** | gCaptain editorial | "agent-centric strategy of distributed computing" — accurate, but **Holochain is not named** |
| **Feb 2021** | American Reporter article | "nodal neural network," "P2P Digital Ledger technology" — **Holochain is not named** |
| Feb 2025 | CEO interview | "HoloStacks," decentralised, "without using blockchain" — **Holochain is not named** |

Within four months of filing a patent whose sole differentiator was Holochain, the company had
stopped naming Holochain in public. The February 2021 replacement term, "nodal neural network,"
does not describe Holochain or anything else — a distributed hash table is not a neural network.
Whatever drove the substitution, it moved the public description away from a real technology
with a real specification toward a phrase with no referent.

*(Inference: this is consistent with either a deteriorating relationship with the Holochain
ecosystem, or with marketing written by people who did not understand the architecture. Nothing
in the recovered material distinguishes the two.)*

## Where they are now

The company exists and trades. A February 2025 interview with CEO John Walker describes
"HoloStacks," a "Zero-Trust, decentralized encrypted and scalable infrastructure solution," and
a suite covering "video meetings, file sharing, live streaming, logistics, and more."

**A correction to an earlier draft of these notes.** They have not dropped logistics entirely —
that overstated it. "Logistics" survives as one item in a product list, the company was still
posting supply-chain commentary on LinkedIn as late as September 2023, and the federal
contractor registration still describes "Port Community System" capabilities. What has gone is
specific and narrower: **the Holochain-based container shipping platform**. No public artefact
after 2021 describes it, both patents covering it are abandoned, and the framework it was built
on is no longer named.

**The design in the PDF is not being worked on by anybody.** That is the accurate claim.

## The federal contractor registration

Holo-Sail Technologies Incorporated is registered as a US federal contractor: UEI
`Z2JFPRMDQ5E3`, CAGE `8KN71`, established 2019, Subchapter S, West Caldwell NJ, active. **No
contract awards or obligated amounts are reported.**

The registration is miscoded. All three NAICS codes sit in subsector 813 — *Religious,
Grantmaking, Civic, Professional and Similar Organizations*:

- 813920 Professional Organizations (primary)
- 813312 Environment, Conservation and Wildlife Organizations
- 813410 Civic and Social Organizations

These are the codes for non-profit membership associations. The codes for what the company
actually described doing would be 541511 or 541512 (custom programming, computer systems design)
or 488510 (freight transportation arrangement). As registered, the company could not surface in
a federal opportunity search for its own line of work.

It is a small thing, and it is the same shape as everything else in this record: the analysis
was sound, the follow-through was not. Full detail in
[`../sources/website/2026-08-25-federal-contractor-registration.txt`](../sources/website/2026-08-25-federal-contractor-registration.txt).

---

**Sources for this document**

- Archived website pages, with snapshot timestamps: [`../sources/website/`](../sources/website/)
- [Holo Sail on the Holochain forum, 27 Mar 2020](https://forum.holochain.org/t/introducing-holo-sail-technologies-inc/2620) (forum now offline; archived copy in [`../sources/forum/`](../sources/forum/))
- ["Haven by Holo Sail" trademark](https://uspto.report/TM/97428178/APP20220528094149/)
- [HoloSail: Redefining Secure Communication — Stankevicius, 12 Feb 2025](https://stankevicius.co/tech/holosail-redefining-secure-communication-in-the-era-of-cyber-warfare/)
- [Holo Sail Technologies LLC — OpenCorporates](https://opencorporates.com/companies/us_wy/2019-000875993)
