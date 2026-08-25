# Phase 2 — the legibility test

Findings: [`../../docs/12-phase2-findings.md`](../../docs/12-phase2-findings.md).
Plan: [`../../docs/09-demo-plan.md`](../../docs/09-demo-plan.md).

```bash
bash ../phase1/run.sh    # produces case.json + discrepancy_record.json
python render.py         # writes report.html
```

`report.html` is self-contained apart from Google Fonts. Open it directly.

## The test this has to pass

A maritime professional understands it **without anyone explaining it**. If it needs
narration it has failed, and correctness does not rescue it.

## Design decisions, so edits stay coherent

**The palette is the Admiralty chart convention.** Magenta is the UKHO overprint for
cautions and warnings — so on this page it appears **exactly once**, on the
contradiction. Green marks what verified. If a second thing turns magenta the signal is
gone.

**The chart is distance-from-port against time**, because that is the axis the dispute
turns on. The port limit is drawn as a line and the claim sits visibly above it.

**The chart covers the approach window only** — first fix through 45 minutes past the
crossing. The full track spans 18 hours of which 17 are the vessel lying stopped;
plotting all of it crushes the arrival into the left 3% of the axis and pushes the claim
label off-canvas. That was a real bug, caught by measuring label bounding boxes rather
than by looking.

**Labels are edge-aware.** Anchor flips depending on which side of the chart the marker
falls, so nothing renders off-canvas as the data changes.

**Everything is generated from the real track.** No hand-drawn paths, no smoothing, no
interpolation. Claimed times are bracketed between the fixes either side.

## Do not remove

The disclosure block stating that telemetry is real and the parties are synthetic. A page
that implied real carrier data it does not have would end a conversation with an insurer
permanently.

The "What this record does not decide" section. No adjudication, no monetary figure, no
confidence score — see [`../../docs/08-external-evidence-and-the-real-gap.md`](../../docs/08-external-evidence-and-the-real-gap.md).
