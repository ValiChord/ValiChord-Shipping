# 12 — Phase 2: one page, no narration

**The report exists and reads as a survey document rather than a demo.**

Rendered artefact: [`../tools/phase2/example_output/report.html`](../tools/phase2/example_output/report.html)
· generator: [`../tools/phase2/render.py`](../tools/phase2/render.py). Built 25 August 2026.

The test set in [`09-demo-plan.md`](09-demo-plan.md) was: *a maritime professional
understands it without anyone explaining it.* That test cannot be marked passed from here —
only a maritime professional can pass it. What can be reported is what was built, what was
found wrong, and what remains unverified.

---

## What the page shows

A single scrolling page, no interaction required:

1. **Disclosure, before anything else.** Telemetry is real; the four parties are synthetic.
2. **Case particulars** in a ruled strip — vessel, IMO, port, date, fix count.
3. **The finding, in one sentence.** The carrier sealed a claim of arrival at 05:30. At that
   moment the public track puts her 17.35 nm out, 5.35 nm outside the 12 nm limit, making
   12.2 knots, broadcasting her own status as "under way using engine". She crossed the
   limit 30 minutes later.
4. **The chart** — distance from port against time, drawn from the real fixes, with the
   port limit as a line and the claim sitting visibly above it.
5. **Every claim against the track** — a row per party, with the verdict.
6. **Seals** — each commitment and its verification state.
7. **What this record does not decide.**

## Design decisions

**The palette is the Admiralty chart convention.** Chart-paper ground, admiralty blue-black
ink, a pale sea tint below the limit line. Magenta is the UKHO overprint for cautions and
warnings, so on this page it appears **exactly once**, on the contradiction. Green marks
what verified. The discipline is the point: if a second element turns magenta, the signal
is gone.

**Typography** — Source Serif 4 for headings, IBM Plex Sans for body, IBM Plex Mono for
timestamps, coordinates, hashes and every column of digits. The register aimed at is a
class-society or survey report, not a product page. Credibility is the design goal; anything
that looked like a startup landing page would undercut the content.

**The chart is distance-from-port against time** because that is the axis the dispute turns
on. Someone who knows ships can read it without a legend: the curve descends, the limit is
a dashed line, and the claim marker sits well above it.

---

## Two real bugs, caught by measuring rather than looking

Worth recording, because both were invisible in a screenshot and obvious in the numbers.

**The claim label rendered at x = −150 — entirely off-canvas.** The label was anchored
`end` at the marker, and the marker sat near the left edge, so 212 px of text ran off the
page. Fixed by making the anchor edge-aware: it flips side depending on where the marker
falls, so labels stay on canvas as the data changes.

**The whole arrival was crushed into the left 3% of the axis.** The full track spans 18
hours, of which roughly 17 are the vessel lying stopped after arrival. Plotting all of it
put the claim marker at x = 73 and the crossing at x = 97 on a 1000-wide chart — 24 pixels
apart, on a page whose entire purpose is showing the gap between them.

Fixed by charting the **approach window** — first fix through 45 minutes past the crossing.
The markers are now 311 px apart and the descent through the limit is the dominant shape on
the page.

Both were found by querying `getBBox()` on every text node and checking for overflow and
overlap, not by eye. The scaled screenshot looked fine. **A legibility phase needs a
measurable definition of legible**, or it just becomes a taste exercise.

## Verified before publishing

| Check | Result |
|---|---|
| Text nodes overflowing the viewBox | none |
| Overlapping text labels | none |
| Body horizontal scroll at 1200 px | none (1185 px content) |
| Light and dark themes | both render; every colour resolves through tokens |
| Fonts | all three families load; headings render in Source Serif 4 |
| Unclosed or mismatched tags | none |

Dark mode was checked properly rather than assumed: the tokens are redefined in all three
states — bare `:root`, `prefers-color-scheme: dark` guarded against an explicit light
choice, and `[data-theme="dark"]` — and no colour is declared only inside a theme block.

---

## What is still unverified

**The actual test.** Nobody who works a laytime desk has seen this. Everything above is a
statement about construction, not reception. The failure mode this phase exists to catch —
a technically correct artefact that no maritime professional can read — cannot be ruled out
from inside the project.

**The 30-minute discrepancy is modest.** Real NOR disputes often run to hours. The
discrepancy here was chosen to sit inside the real track, so it is honest, but it is not
dramatic. Worth noting that the measurement window on the crossing is 29 seconds, so the
signal is roughly sixty times the noise — a smaller discrepancy would still be detectable.

**One case, one vessel, one port.** The generator is parameterised but has been exercised
against a single arrival.

---

## Next

Phase 2 is the last phase that can be completed alone. [`docs/09`](09-demo-plan.md) puts
Phase 3 next — a real external witness, which is what turns *"nobody can backdate this"*
from illustrated into true, and where Holochain earns its place.

But the sequencing question is now open in a way it was not before. There is something to
show. The binding constraint has never been technical — it is whether anyone will pay, and
that question is unchanged since [`docs/04`](04-strategic-assessment.md).

**Showing this page to one person who works cargo claims or a laytime desk would be worth
more than Phase 3.**
