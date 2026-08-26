# 17 — Phase 0b: real disputes, from published judgments

**Ran 26 August 2026. The method works and produced named vessels at named US ports with
exact disputed times. Whether any of them can actually be checked against free AIS is
still open, and the honest answer today is "one, probably, with work."**

Proposed in [`docs/16`](16-external-review.md) Part 7. Code in
[`../tools/phase0b/`](../tools/phase0b/).

---

## Why this exists

[`docs/10`](10-phase0-findings.md)'s second test compared a crew-set AIS field against GPS
inside the same message, and [`docs/13`](13-phase3-findings.md) conceded the 0.372%
divergence it found was *"staleness at least as much as dishonesty."* It does not test the
thing that matters — whether a **carrier's own claimed times** diverge from telemetry —
because that needs carrier logs nobody has given us.

Published court judgments are a source of real disputed times that needs no counterparty.
Unlike LMAA arbitration awards, which are anonymised, English Commercial Court judgments
name the vessel, the port and the times.

## What was done

The National Archives' *Find Case Law* has an Atom API under the Open Justice Licence.
Four queries — `laytime`, `demurrage`, `"notice of readiness"`, `charterparty laytime` —
returned **290 unique judgments from 2010 onward**. Each was fetched and scored for the
four things a testable case needs: a named vessel, a US port, a date inside the free-AIS
window, and a disputed clock time.

**43 mention a US port and laytime or NOR.** That list is committed as
[`candidates_scored.json`](../tools/phase0b/candidates_scored.json).

---

## The finding that matters most: most hits are false positives

**"New York" is almost always an arbitration seat or a party address, not a port call.**
It accounts for the large majority of the 43 and should be discarded on sight.

**"Baltimore" was worse.** `[2019] EWHC 2522 (Comm)` scored well and mentions Baltimore
repeatedly — because the charter was on an amended **Baltimore Form C Berth Grain form**.
The voyage was Brazil to China. It has nothing to do with the United States.

This is worth recording because it is the difference between a day's work and a wasted
week, and because a keyword pipeline reports it as a hit either way. **Every candidate
must be read before it is believed.**

---

## The three that survived reading

### 1. *BP Oil International Ltd v Target Shipping Ltd* [2012] EWHC 1590 (Comm)

**The best candidate, because the vessel is named.**

| | |
|---|---|
| Vessel | the oil tanker **"Target"** |
| US ports | **Galveston** and **Houston** |
| Dates | discharged Galveston **13–14 April 2010**; Houston **21–23 April 2010** |
| Timezone | the judgment states its times are **GMT** — unusually convenient |

**Obstacle:** NOAA's daily-CSV AIS layout does not cover 2010.
`AIS_2010_04_13.zip` returns 404. Pre-2015 data exists in a different structure and would
need separate handling. **Verified by request, not assumed.**

### 2. *Tricon Energy Ltd v MTM Trading LLC* [2020] EWHC 700 (Comm)

**The best candidate on data availability.**

| | |
|---|---|
| Owner | **MTM Trading LLC** — a real fleet, publicly listed |
| US port | **Houston** (discharge) |
| Agreed facts | NOR tendered **20 March 2017 at 01.12**; shifting to berth **14.48–20.40 on 21 March**; discharge commenced **22 March at 03.20** |
| AIS | `AIS_2017_03_20.zip` — **available, 301 MB**. Verified by request |

**Two obstacles, both real.**

The judgment calls her only "the Vessel" and never names her. She would have to be
identified from AIS by matching MTM's public fleet against vessels in the Houston approach
on those dates — feasible, but it is an inference, and a wrong identification would
poison everything downstream.

More importantly: **the times were common ground.** The dispute was about whether the
demurrage claim was time-barred for missing documents, not about when anything happened.
So this case cannot demonstrate a contradiction. What it could demonstrate is weaker but
still worth having: that AIS independently reconstructs the agreed facts of a real
demurrage claim.

### 3. *Endesa-related coal case* [2011] EWHC 1165 (Comm)

Six named vessels with exact tendered-NOR times in a single judgment — *Co-op Phoenix*
12:30 on 14 June, *Alpha Glory* 13:30 on 15 June, *C Young* 20:30 on 7 July, *Royal
Breeze* 16:00 on 16 July, plus *Double Progress* and *Iron Manolis*.

**All in 2008 — before NOAA's AIS record begins.** Unusable, and recorded anyway because
it is the clearest illustration of the shape the method wants: multiple named vessels,
exact tendered times, one congested port, one judgment.

---

## What this establishes, and what it does not

**Establishes:** the source is real, machine-readable, free, and yields exactly the fields
required. Building the candidate list cost an afternoon and needed nobody's permission —
which was the whole argument for trying it.

**Does not establish:** that a single case can actually be run end to end. The three
survivors each fail on something different — no AIS for the year, no vessel name, or dates
before the record starts. **None has yet been checked against telemetry.**

**The gap this exposes.** The strongest demonstration needs a case where the times were
*disputed*, not agreed. Most reported judgments turn on questions of law — construction of
a clause, time bars — precisely because the facts were settled below. Cases that turn on
disputed facts tend to end in arbitration, which is anonymised. **That tension is
structural and was not anticipated in `docs/16` Part 7.** It may mean the method yields
corroboration rather than contradiction, which is a weaker but still saleable claim.

---

## Next actions, in order

1. **Widen the scan.** Four queries and 290 judgments is a first pass. Add `"arrived
   ship"`, `WIBON`, `"laytime commenced"`, and the US Gulf terminal names, and drop the
   2010 floor to catch older reported cases with later AIS-era facts.
2. **Run the Tricon case.** One 301 MB download and the existing Phase 0 code. Even
   corroboration of agreed facts is a result, and it is the only candidate that can run
   today.
3. **Check whether pre-2015 NOAA AIS is retrievable** in its actual format. If it is, the
   *Target* becomes the lead candidate, because she is named.
4. **Try US federal courts.** SDNY, E.D. Louisiana and S.D. Texas hear charterparty
   demurrage disputes, name vessels, and are not covered by this scan at all.

---

**Sources**

- [Find Case Law — The National Archives](https://caselaw.nationalarchives.gov.uk/), Atom
  API, [Open Justice Licence](https://caselaw.nationalarchives.gov.uk/open-justice-licence)
- [*BP Oil International Ltd v Target Shipping Ltd* [2012] EWHC 1590 (Comm)](https://caselaw.nationalarchives.gov.uk/ewhc/comm/2012/1590)
- [*Tricon Energy Ltd v MTM Trading LLC* [2020] EWHC 700 (Comm)](https://caselaw.nationalarchives.gov.uk/ewhc/comm/2020/700)
- [[2011] EWHC 1165 (Comm)](https://caselaw.nationalarchives.gov.uk/ewhc/comm/2011/1165)
- [[2019] EWHC 2522 (Comm)](https://caselaw.nationalarchives.gov.uk/ewhc/comm/2019/2522) — the Baltimore false positive
- [NOAA / MarineCadastre AIS](https://coast.noaa.gov/htdata/CMSP/AISDataHandler/)
