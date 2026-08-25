# 05 — Source inventory

Status recorded as at **25 August 2026**. Anything marked *dead* or *lapsed* exists in this
repository only, or in the Internet Archive.

## Primary — patent

| Source | Status | Local copy |
|---|---|---|
| [US20210174293A1 — Google Patents](https://patents.google.com/patent/US20210174293A1/en) | Live | — |
| [US20220156679A1 — Google Patents](https://patents.google.com/patent/US20220156679A1/en) | Live | — |
| Original PDF supplied by Ceri | — | [`../sources/patent/US20210174293A1.pdf`](../sources/patent/US20210174293A1.pdf) |
| Extracted full text of parent (incl. claims) | — | [`../sources/patent/US20210174293A1-fulltext.txt`](../sources/patent/US20210174293A1-fulltext.txt) |
| Extracted description of continuation-in-part | — | [`../sources/patent/US20220156679A1-description.txt`](../sources/patent/US20220156679A1-description.txt) |
| [Holo Sail filings — uspto.report](https://uspto.report/company/Holo-Sail-Technologies) | Live | — |

Legal-event data was read from the Legal Events table on the Google Patents pages, which
reproduces USPTO status codes. Quoted verbatim in [`01-patent-record.md`](01-patent-record.md).

**Not obtained:** the file wrappers for either application — i.e. the actual text of the office
actions. These sit behind USPTO Patent Center authentication. Consequently, *why* the examiner
objected is inference in these notes, never assertion. Anyone with Patent Center access can
close this gap and should.

## Primary — Holochain forum (site offline)

`forum.holochain.org` **no longer resolves**. Recovered from the Internet Archive.

| Thread | Archived | Local copy |
|---|---|---|
| Introducing Holo Sail Technologies, Inc (27 Mar 2020) | 15 Jun 2025 | [`../sources/forum/2620-introducing-holo-sail-technologies.txt`](../sources/forum/2620-introducing-holo-sail-technologies.txt) |
| Questions about Holo Sail Technologies Patent (20 Jul 2021) | 20 Jun 2025 | [`../sources/forum/6532-questions-about-the-patent.txt`](../sources/forum/6532-questions-about-the-patent.txt) |

## Primary — company website (domain lapsed)

`holosailtechnologies.com` **lapsed and was re-registered by an unrelated party**. As at
August 2026 it serves Indonesian song-lyrics content with no connection to the company. Verified
by direct fetch. All originals below are from the Internet Archive.

| Page | Snapshot | Local copy |
|---|---|---|
| Home | 2020-08-03 | [`../sources/website/2020-08-03-home.txt`](../sources/website/2020-08-03-home.txt) |
| About Us | 2020-08-03 | [`../sources/website/2020-08-03-about-us.txt`](../sources/website/2020-08-03-about-us.txt) |
| Benefits | 2020-08-03 | [`../sources/website/2020-08-03-benefits.txt`](../sources/website/2020-08-03-benefits.txt) |
| Collaborations | 2020-08-03 | [`../sources/website/2020-08-03-collaborations.txt`](../sources/website/2020-08-03-collaborations.txt) |
| Post: "The Path to a More Secure World" | 2020-10-26 (post dated 2020-09-29) | [`../sources/website/2020-09-29-post-path-to-a-more-secure-world.txt`](../sources/website/2020-09-29-post-path-to-a-more-secure-world.txt) |
| Post: "Is Blockchain's Role… Overhyped?" — stub linking out to gCaptain | 2021-12-07 (post dated 13 Oct) | [`../sources/website/2021-10-13-post-is-blockchain-overhyped-stub.txt`](../sources/website/2021-10-13-post-is-blockchain-overhyped-stub.txt) |
| Advisors | 2021-12-07 | [`../sources/website/2021-12-07-advisors.txt`](../sources/website/2021-12-07-advisors.txt) |
| Services / "Why Holo Sail Tech?" | 2021-12-07 | [`../sources/website/2021-12-07-services.txt`](../sources/website/2021-12-07-services.txt) |
| HOLO SAIL HAVEN product page | 2022-05-24 | [`../sources/website/2022-05-24-holosail-haven.txt`](../sources/website/2022-05-24-holosail-haven.txt) |
| HoloSail Technologies LLC (WordPress) | Live at time of collection | [`../sources/website/holosailtechnologiesllc-wordpress.txt`](../sources/website/holosailtechnologiesllc-wordpress.txt) |

## Primary — trade press

| Source | Status | Local copy |
|---|---|---|
| [Is Blockchain's Role in Supply Chain Logistics Overhyped? — gCaptain, 22 Jan 2021](https://gcaptain.com/is-blockchains-role-in-supply-chain-logistics-overhyped/) | **Live** | [`../sources/website/2021-01-22-gcaptain-is-blockchains-role-overhyped.txt`](../sources/website/2021-01-22-gcaptain-is-blockchains-role-overhyped.txt) |

By the CEO, under the entity name "Holo Sail Holdings" — a third corporate variant alongside
Holo Sail Technologies Inc. and Holo Sail Technologies LLC. **The single most valuable document
in the corpus.** Found only because the archived blog post of 13 October 2021 is a stub that
links out to it. It diagnoses TradeLens's eventual cause of death twenty-two months early, and
names GSBN (Global Shipping Business Network) — the rival carrier consortium — which appears
nowhere else in the material collected here and is worth following up.

A full Wayback URL inventory for the domain — which is what evidences the 2022 pivot to the
"Haven" product line, and the 2026 lapse — is at
[`../sources/website/wayback-url-inventory.txt`](../sources/website/wayback-url-inventory.txt).

The `/advisors` page is included for completeness but recovered as an empty template; the Wix
site rendered its content via JavaScript and the archive did not capture it.

### Not recovered

The Internet Archive was intermittently unavailable during collection ("Internet Archive
services are temporarily offline"). These blog posts are known to exist from the URL inventory
but were not retrieved:

- `/post/holo-sail-is-headed-to-rotterdam` (snapshot 2020-08-03)
- `/post/what-is-a-port-community-system-pcs` (snapshot 2020-08-03)
- `/post/redefining-automation` (snapshot 2020-08-03)
- `/post/holosail-s-modernization-of-global-supply-chain` (snapshot 2020-08-03)

`what-is-a-port-community-system-pcs` is the one most likely to contain substance, given that
the home page's standards work is among the strongest technical content in the corpus. Worth a
retry when the Archive is stable.

A caution learned the hard way: several retrieval attempts returned an Internet Archive error
page **padded to 250–870 KB of whitespace**, which passes a naive file-size check. Confirm
recovered pages by their extracted text, not their byte count. Two files in this collection
initially looked like large successful captures and were error pages.

Also not recovered:

- The promotional interview with Jonny Stang (YouTube), referenced throughout the July 2021
  forum thread and the source of the "16 verticals" claim. Only the quotations preserved in
  that thread are held here.
- `holosailtechnology.medium.com` — a Medium account belonging to the CEO, returned 403 to
  automated retrieval. Contents unknown; may hold further writing of the gCaptain kind, which
  on the evidence is where this company's real thinking lives.
- The "Interview with The Crypto Truth" and the "Healing the Heroes of 9-11" documentary, both
  referenced on the archived blog.

## Secondary

| Source | Used for |
|---|---|
| [Maersk, IBM to shut down TradeLens — Supply Chain Dive](https://www.supplychaindive.com/news/Maersk-IBM-shut-down-TradeLens/637580/) | TradeLens shutdown and stated cause |
| [IBM, Maersk will shut down TradeLens — The Register](https://www.theregister.com/2022/11/30/ibm_and_maersk_tradelens_shutdown/) | Corroboration and dates |
| [HoloSail: Redefining Secure Communication — Stankevicius, 12 Feb 2025](https://stankevicius.co/tech/holosail-redefining-secure-communication-in-the-era-of-cyber-warfare/) | Current company position; confirms Holochain and shipping both absent |
| ["Haven by Holo Sail" trademark](https://uspto.report/TM/97428178/APP20220528094149/) | Pivot dating |
| [Holo Sail Technologies LLC — OpenCorporates](https://opencorporates.com/companies/us_wy/2019-000875993) | Corporate registration |
| [Cryptographic Autonomy License 1.0](https://opensource.org/licenses/CAL-1.0) | § 5.3 litigation-termination clause quoted in the forum thread |

## Negative findings

Recorded because absence of evidence was, in this case, informative. Each was searched for
specifically and not found:

- **No public code repository** under any spelling of Holo Sail / HoloSail, on GitHub or
  elsewhere.
- **No whitepaper, technical specification, or architecture document** anywhere in the corpus.
- **No hardware specification** for the "Designate" device beyond a list of measured quantities.
- **No Holochain DNA, hApp, or zome** published or referenced.
- **No further forum or developer-community engagement** by Holo Sail beyond the single
  two-post introduction thread of March 2020.

## Notes on method

Text was extracted from the PDF with `pdftotext -layout`, and from archived HTML by stripping
tags. The patent PDF is two-column, so extracted line order interleaves columns in places; the
original PDF is included for checking anything that reads oddly.

Personal contact details (a mobile number and an email address) appearing on the archived
`/collaborations` page have been redacted. No other alterations were made to source text.
