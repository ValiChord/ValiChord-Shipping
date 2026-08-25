# Recovered primary sources

Collected 25 August 2026. Provenance for every file is below. Status of each origin — live,
offline, or lapsed — is in [`../docs/05-source-inventory.md`](../docs/05-source-inventory.md).

These are third-party materials, reproduced for research, commentary, and preservation. They
remain the property of their authors. The Apache 2.0 licence on this repository covers our own
notes, not this directory's contents.

## `patent/`

| File | Origin |
|---|---|
| `US20210174293A1.pdf` | The published application as supplied. Two-column layout; the authoritative copy for anything that reads oddly in the extracted text |
| `US20210174293A1-fulltext.txt` | Text extracted from the above with `pdftotext -layout`. Includes the abstract, full description, and the single claim. Column interleaving is visible in places |
| `US20220156679A1-description.txt` | Description of the continuation-in-part, extracted from the Google Patents page. Used for the word-count comparison in `docs/01` |

## `forum/`

Both recovered from the Internet Archive. **`forum.holochain.org` no longer resolves.**

| File | Origin |
|---|---|
| `2620-introducing-holo-sail-technologies.txt` | Thread of 27 Mar 2020. Archived 15 Jun 2025 |
| `6532-questions-about-the-patent.txt` | Thread of 20 Jul 2021. Archived 20 Jun 2025 |

## `website/`

Recovered from the Internet Archive. **`holosailtechnologies.com` has lapsed** and now serves
unrelated content under new ownership.

| File | Origin |
|---|---|
| `2020-08-03-home.txt` | Home page. Contains the IPCSA / ISO 28005 / EDIFACT / IALA S-211 standards work — the strongest technical content in the corpus |
| `2020-08-03-about-us.txt` | Team roster and biographies |
| `2020-08-03-benefits.txt` | Operational claims, port efficiency, IMO 2020 sulphur cap |
| `2020-08-03-collaborations.txt` | Port authority and shipping association engagement claims. **Redacted:** one mobile number, one email address |
| `2020-09-29-post-path-to-a-more-secure-world.txt` | Blog post. Evidences the early drift to cyber-security framing, and carries the post view counts |
| `2021-01-22-gcaptain-is-blockchains-role-overhyped.txt` | **Not from the archive — retrieved live from gCaptain.** Editorial by the CEO, 22 Jan 2021. The single most valuable document in the corpus. Carries its own provenance header |
| `2021-02-04-american-reporter-sdg8.txt` | **Not from the archive — retrieved live.** Co-authored think-piece on automation, jobs and UN SDG 8. Matters mainly for what it omits: Holochain is never named, three months after the patent built on it was filed. Republished verbatim on the CEO's Medium account and on an advisor's blog |
| `2026-08-25-federal-contractor-registration.txt` | US federal contractor record. Active, no contract awards, and three NAICS codes that all describe non-profit membership associations |
| `2021-10-13-post-is-blockchain-overhyped-stub.txt` | Blog stub whose only content is a link out to the gCaptain article. How that article was found. Also carries post view counts |
| `2022-05-24-holosail-haven.txt` | The "HOLO SAIL HAVEN" product page. Describes Haven as "Holo Sail's first live product" and carries the 22ZERO testimonial that explains the pivot. **Redacted:** one email address |
| `2021-12-07-advisors.txt` | Recovered as an empty template — the Wix site rendered content via JavaScript and the archive did not capture it. Retained for completeness |
| `2021-12-07-services.txt` | Contains the twelve-counterparty market list quoted in `docs/04` |
| `holosailtechnologiesllc-wordpress.txt` | Separate WordPress site, live at time of collection |
| `wayback-url-inventory.txt` | Full Wayback CDX listing for the domain. Evidences the 2022 pivot to the "Haven" product line and the later lapse |

## Reading the URL inventory

`wayback-url-inventory.txt` is `timestamp url` pairs, one per line. Three eras are visible:

- **2020–2021** — `/about-us`, `/benefits`, `/collaborations`, `/blog`, `/advisors`: the shipping company
- **2022** — `/havens-den`, `/holosailhaven`, `/havencomms`, `/havenvideopro`, `/safehaven`,
  `/capabilities`: the pivot to encrypted communications
- **2026** — Indonesian-language music and song-lyrics pages: the domain in unrelated hands

Filter the third era out with a command like:

```bash
grep -viE 'musik|lagu|makna|/author/|/category/|/tag/' sources/website/wayback-url-inventory.txt
```

## Extraction method

PDF via `pdftotext -layout`. HTML by removing `script`, `style`, `noscript` and `svg` elements,
converting block-level closing tags to newlines, stripping remaining tags, unescaping HTML
entities, and collapsing whitespace. No other alterations beyond the redaction noted above.
