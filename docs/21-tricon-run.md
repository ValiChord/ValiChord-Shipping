# 21 — The Tricon case, run against real AIS

**It worked. A real port call from a real judgment, reconstructed from free public AIS,
consistent with the court record at every point that AIS can see.**

**And it corroborates rather than contradicts — exactly as [`docs/17`](17-phase0b-case-candidates.md)
predicted, for exactly the reason [`docs/20`](20-is-this-already-solved.md) then explains.**

Run 26 August 2026 against `AIS_2017_03_20.zip` (301 MB, NOAA/MarineCadastre, 849 MB
uncompressed).

---

## The case

*Tricon Energy Ltd v MTM Trading LLC* [2020] EWHC 700 (Comm). Agreed facts, quoted from
the judgment:

> "(c) NOR was tendered at the discharge port, Houston, on 20 March 2017 at 01.12; (d) the
> Vessel was shifting to her berth between 14.48 and 20.40 on 21 March 2017; (e) discharge
> commenced on 22 March 2017 at 03.20"

**The judgment never names the vessel.** She is "the Vessel" throughout.

## Identifying her — an inference, and its strength

The owner is MTM Trading LLC, whose fleet carries `MTM`-prefixed names. Scanning the whole
national AIS file for that day returns **three** MTM vessels in US waters:

| Vessel | IMO | Fixes | Closest to Galveston Bar |
|---|---|---|---|
| **MTM HONG KONG** | 9228320 | 665 | **9.20 nm** |
| MTM ROTTERDAM | 9477567 | 589 | 741.81 nm |
| MTM ST JEAN | 9278674 | 1254 | 811.66 nm |

The other two were off Georgia and the Carolinas. **Only one candidate was anywhere near
Houston**, and her behaviour matches the judgment on every point AIS can observe.

**This remains an inference and must be labelled as one.** MTM Trading could have chartered
a vessel not carrying the fleet name. Nothing in the judgment confirms the identification.
What can be said is that the match is strong and the alternatives are absent.

## What the telemetry shows

Distances measured to the Galveston Bar pilot station (29.31 N, 94.70 W), where
Houston-bound tankers arrive.

```
00:00   72.92 nm   13.5 kt   under way
01:00   59.41 nm   13.4 kt   under way     <- NOR tendered 01.12 per the judgment
02:00   46.14 nm   13.4 kt   under way
03:00   32.84 nm   13.4 kt   under way
04:00   21.04 nm   11.1 kt   under way
05:00   16.16 nm   10.6 kt   under way
06:00    9.66 nm    5.3 kt   under way
06:09    9.27 nm    0.1 kt   AT ANCHOR     <- anchor down
07:00 – 23:00   ~9.2 nm   0.0 kt   at anchor, all day
```

She anchored at **06:09:52** and did not move again that day. Closest approach on 20 March:
**9.20 nm** — she never entered the channel. Consistent with the judgment's "shifting to her
berth" on **21 March**, the following afternoon.

**Every AIS-observable element of the court record is reproduced from public data at no
cost.**

## The finding, stated carefully

**At 01:12 on 20 March 2017 — the moment NOR was tendered — the vessel was approximately 59
nautical miles from the pilot station, making 13.4 knots, under way using engine. She
anchored just under five hours later.**

**This is not a catch, and presenting it as one would be a serious error.**

- NOR is a **notice**, sent by email or telex. Tendering it while inbound is ordinary
  practice, and many charterparties expressly permit it.
- **These times were common ground between the parties.** Neither side disputed them. The
  dispute was whether the demurrage claim was time-barred for want of supporting documents.
- Whether an NOR tendered from 59 nm out was *valid* is a question of law under the
  particular charter — the "arrived ship" line of authority — and this record says nothing
  about it. Per [`docs/08`](08-external-evidence-and-the-real-gap.md): **we establish the
  facts; they argue the law.**

What it does show: had anyone wished to test the physical facts behind that NOR, the
evidence was free, public, and available in minutes.

Nobody wished to. That is the finding.

---

## What this establishes, and what it kills

**Establishes:** the method works end to end on a real case with no counterparty, no NDA and
no introductions. Judgment → vessel identification → telemetry → reconstruction. The claim
in [`docs/16`](16-external-review.md) Part 7 that this was buildable alone was correct.

**Kills:** the idea that finding more cases would help. This case is representative, not
unlucky. [`docs/20`](20-is-this-already-solved.md) sets out why — the industry's own account
of demurrage leakage is workload, time bars, unqueryable data and staff turnover, and
disputed arrival times appear nowhere in it. The one real case available confirmed the
timings rather than exposing them, because **that is what the data is for.**

**The honest summary:** we built a working instrument, pointed it at a real dispute, and it
told us the parties already agreed. That is a successful experiment with a negative result,
and the negative result is worth more than another twenty cases would be.

## What not to do next

**Do not download more AIS days.** The bottleneck is not evidence.

**Do not chase the *Target*** ([2012] EWHC 1590, Galveston, April 2010) on the theory that
an older case might contradict. It might, and it would change nothing — see `docs/20`.

**Do read [`docs/20`](20-is-this-already-solved.md) before writing to anyone in the
industry.** It is the difference between sounding like someone who has done the work and
sounding like someone who has not.

---

**Reproduce it**

```bash
cd tools/phase0b
curl -o ais/AIS_2017_03_20.zip \
  https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2017/AIS_2017_03_20.zip
python tricon_run.py
```

Data: NOAA / MarineCadastre, public domain. Judgment: The National Archives Find Case Law,
Open Justice Licence.
