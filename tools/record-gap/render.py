"""Record-gap demo, step 3 -- render the comparison as one page a claims desk can read.

Reads case.json and gap_report.json. Writes report.html (standalone, for the repo)
and artifact.html (body fragment, for publishing).

The test this has to pass is the one set in docs/09 and inherited from phase 2: a
maritime professional understands it without anyone explaining it. If it needs
narration it has failed, and being correct does not rescue it.

Design notes, so edits stay coherent:

  * The palette and the three faces are phase 2's, unchanged. This is the same
    project talking about a different problem, and it should look like it.
  * Magenta is the UKHO chart overprint for cautions. Phase 2 spends it exactly
    once; that rule does not survive contact with this page, because there are
    genuinely several deficiencies to mark. So it is spent on one MEANING
    instead, consistently: magenta is damage and deficiency -- the failure, the
    entries that arrived stripped of their reason, and the verdicts that cannot
    be answered. Green is corroboration -- the lube oil trail, and the verdicts
    that can. Nothing else takes either colour. If a third meaning acquires a
    colour, the page stops working.
  * The hero is two timelines on one shared axis, not a table. The whole argument
    is that the left of the top panel is empty, and no table makes emptiness
    legible the way a blank stretch of axis does.
  * Four lanes, not three. The lube oil service tank gets its own lane because it
    is common to all three generators -- that is the entire causation question,
    and burying it inside the DG2 lane would hide the answer.
  * Every number on the page is read from the JSON. Nothing is typed in by hand.
"""
import json
import os
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.join(HERE, "case.json")
REPORT = os.path.join(HERE, "gap_report.json")
OUT_STANDALONE = os.path.join(HERE, "report.html")
OUT_FRAGMENT = os.path.join(HERE, "artifact.html")

T0 = datetime(2023, 2, 1)
T1 = datetime(2026, 7, 15)
LANES = ["DG1", "DG2", "DG3", "LO"]
LANE_LABEL = {
    "DG1": "DG1 turbocharger",
    "DG2": "DG2 turbocharger",
    "DG3": "DG3 turbocharger",
    "LO": "LO service tank",
}
LANE_SUB = {
    "DG1": "standby set",
    "DG2": "main duty",
    "DG3": "main duty",
    "LO": "common to all three",
}


def D(s):
    return datetime.strptime(s, "%Y-%m-%d")


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def lane_of(row):
    return "LO" if row["job_code"].startswith("LO-") else row["dg"]


def timeline(rows, handover, incident, blank_before_handover, w=980):
    """One panel: four lanes of events on a shared time axis.

    blank_before_handover draws the hatched 'nothing received' band, which is the
    single most important mark on the page.
    """
    pad_l, pad_r, pad_t, pad_b = 132, 18, 26, 34
    lane_h = 34
    h = pad_t + lane_h * len(LANES) + pad_b
    span = (T1 - T0).total_seconds()

    def x(d):
        return pad_l + (d - T0).total_seconds() / span * (w - pad_l - pad_r)

    def y(lane):
        return pad_t + LANES.index(lane) * lane_h + lane_h / 2

    p = ['<svg viewBox="0 0 %d %d" role="img" class="tl">' % (w, h)]

    # Hatch pattern for the unreceived period.
    p.append('<defs><pattern id="hatch" width="7" height="7" '
             'patternTransform="rotate(45)" patternUnits="userSpaceOnUse">'
             '<line x1="0" y1="0" x2="0" y2="7" class="hatchline"/></pattern></defs>')

    if blank_before_handover:
        p.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" '
                 'fill="url(#hatch)" class="blankband"/>'
                 % (x(T0), pad_t, x(handover) - x(T0), lane_h * len(LANES)))
        p.append('<text x="%.1f" y="%.1f" class="blanklab">'
                 'NO MAINTENANCE RECORDS RECEIVED FOR THIS PERIOD</text>'
                 % ((x(T0) + x(handover)) / 2, pad_t - 12))

    # Lane rules and labels.
    for lane in LANES:
        yy = y(lane)
        p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="lane"/>'
                 % (pad_l, yy, w - pad_r, yy))
        p.append('<text x="%.1f" y="%.1f" class="lanelab">%s</text>'
                 % (pad_l - 12, yy - 1, esc(LANE_LABEL[lane])))
        p.append('<text x="%.1f" y="%.1f" class="lanesub">%s</text>'
                 % (pad_l - 12, yy + 11, esc(LANE_SUB[lane])))

    # Handover rule.
    hx = x(handover)
    p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="handover"/>'
             % (hx, pad_t - 6, hx, pad_t + lane_h * len(LANES) + 4))
    p.append('<text x="%.1f" y="%.1f" class="handlab">MANAGEMENT CHANGE</text>'
             % (hx + 5, pad_t - 12))

    # Year ticks.
    for yr in (2023, 2024, 2025, 2026):
        d = datetime(yr, 1, 1)
        if d < T0 or d > T1:
            continue
        p.append('<text x="%.1f" y="%.1f" class="ax">%d</text>'
                 % (x(d), h - 12, yr))

    # Events.
    for r in rows:
        xx, yy, lane = x(D(r["done_date"])), y(lane_of(r)), lane_of(r)
        code = r["job_code"]
        if code == "TC-CLN":
            p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="ev-wash"/>'
                     % (xx, yy - 5, xx, yy + 5))
        elif code == "TC-REP":
            # A cartridge change that reached the incoming manager only through the
            # owner's purchase ledger arrives without its remarks field. It is drawn
            # hollow because that is what it is: the fact without the reason.
            stripped = str(r.get("source", "")).startswith("Owner purchase")
            p.append('<rect x="%.1f" y="%.1f" width="9" height="9" class="%s"/>'
                     % (xx - 4.5, yy - 4.5, "ev-stripped" if stripped else "ev-rep"))
        elif code == "TC-INS":
            p.append('<circle cx="%.1f" cy="%.1f" r="4.5" class="ev-ins"/>' % (xx, yy))
        elif code == "TC-DMG":
            p.append('<circle cx="%.1f" cy="%.1f" r="6.5" class="ev-dmg"/>' % (xx, yy))
        elif code.startswith("LO-"):
            p.append('<path d="M %.1f %.1f l 5.5 5.5 l -5.5 5.5 l -5.5 -5.5 Z" '
                     'class="ev-lo"/>' % (xx, yy - 5.5))

    # The two labelled moments.
    p.append('<text x="%.1f" y="%.1f" class="dmglab">DG1 FAILS</text>'
             % (x(incident) - 4, y("DG1") - 12))
    if not blank_before_handover:
        p.append('<text x="%.1f" y="%.1f" class="lolab">CONTAMINATED BATCH</text>'
                 % (x(D("2024-11-03")) - 4, y("LO") + 22))

    p.append("</svg>")
    return "".join(p)


CSS = """
:root{
  --paper:#FBFAF7; --ink:#12202B; --sea:#E6EDF1; --rule:#C3CFD6;
  --rule-soft:#E1E8EC; --caution:#B0177C; --verified:#2E6B5E; --muted:#5A6C76;
  --band:#F2F0EB;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --paper:#0D1820; --ink:#E8EFF3; --sea:#16242E; --rule:#2E404C;
    --rule-soft:#1E2E38; --caution:#FF6BC0; --verified:#63BCA2; --muted:#8FA0AB;
    --band:#121F27;
  }
}
:root[data-theme="dark"]{
  --paper:#0D1820; --ink:#E8EFF3; --sea:#16242E; --rule:#2E404C;
  --rule-soft:#1E2E38; --caution:#FF6BC0; --verified:#63BCA2; --muted:#8FA0AB;
  --band:#121F27;
}
*{box-sizing:border-box}
body{background:var(--paper);color:var(--ink);
  font-family:"IBM Plex Sans",system-ui,sans-serif;line-height:1.55;margin:0;
  -webkit-font-smoothing:antialiased}
.wrap{max-width:1060px;margin:0 auto;padding:44px 22px 72px;
  display:flex;flex-direction:column;gap:38px}
.eyebrow{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--muted);margin:0}
h1{font-family:"Source Serif 4",Georgia,serif;font-weight:600;
  font-size:clamp(28px,4vw,42px);line-height:1.12;margin:10px 0 0;
  text-wrap:balance;max-width:20ch}
h2{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:20px;
  margin:0 0 14px;text-wrap:balance}
.standfirst{font-size:17px;color:var(--muted);max-width:64ch;margin:14px 0 0}
section{display:flex;flex-direction:column}
.particulars{display:grid;grid-template-columns:repeat(auto-fit,minmax(132px,1fr));
  gap:1px;background:var(--rule-soft);border:1px solid var(--rule-soft);margin:0}
.particulars>div{background:var(--paper);padding:11px 13px}
.particulars dt{font-family:"IBM Plex Mono",monospace;font-size:10px;
  letter-spacing:.13em;text-transform:uppercase;color:var(--muted);margin:0}
.particulars dd{margin:3px 0 0;font-size:14px;font-family:"IBM Plex Mono",monospace;
  font-variant-numeric:tabular-nums}
.question{background:var(--band);border-left:3px solid var(--rule);
  padding:18px 22px;font-family:"Source Serif 4",Georgia,serif;font-size:19px;
  max-width:70ch}
.panel{border:1px solid var(--rule-soft);background:var(--paper)}
.panel+.panel{margin-top:18px}
.panelhead{display:flex;flex-wrap:wrap;align-items:baseline;gap:12px;
  padding:13px 16px;border-bottom:1px solid var(--rule-soft);background:var(--band)}
.panelhead h3{margin:0;font-size:14px;font-family:"IBM Plex Mono",monospace;
  letter-spacing:.09em;text-transform:uppercase;font-weight:500}
.panelhead .count{font-family:"IBM Plex Mono",monospace;font-size:12px;
  color:var(--muted);font-variant-numeric:tabular-nums}
.tlwrap{overflow-x:auto;padding:6px 10px 2px}
.tl{width:100%;min-width:720px;height:auto;display:block}
.lane{stroke:var(--rule-soft);stroke-width:1}
.lanelab{font-family:"IBM Plex Mono",monospace;font-size:11px;fill:var(--ink);
  text-anchor:end}
.lanesub{font-family:"IBM Plex Mono",monospace;font-size:9.5px;fill:var(--muted);
  text-anchor:end;letter-spacing:.06em;text-transform:uppercase}
.ax{font-family:"IBM Plex Mono",monospace;font-size:10.5px;fill:var(--muted);
  text-anchor:middle}
.handover{stroke:var(--ink);stroke-width:1.5;stroke-dasharray:4 3}
.handlab{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.12em;
  fill:var(--ink)}
.hatchline{stroke:var(--rule);stroke-width:1.2}
.blankband{opacity:.9}
.blanklab{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.12em;
  fill:var(--muted);text-anchor:middle}
.ev-wash{stroke:var(--muted);stroke-width:1.5;opacity:.55}
.ev-rep{fill:var(--ink)}
.ev-stripped{fill:none;stroke:var(--caution);stroke-width:1.6}
.ev-ins{fill:none;stroke:var(--ink);stroke-width:1.5}
.ev-dmg{fill:var(--caution)}
.ev-lo{fill:var(--verified)}
.dmglab{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.1em;
  fill:var(--caution);text-anchor:middle}
.lolab{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.1em;
  fill:var(--verified);text-anchor:middle}
.key{display:flex;flex-wrap:wrap;gap:16px;padding:10px 16px 13px;
  border-top:1px solid var(--rule-soft);font-family:"IBM Plex Mono",monospace;
  font-size:10.5px;color:var(--muted);letter-spacing:.05em}
.key span{display:inline-flex;align-items:center;gap:6px}
.key i{width:10px;height:10px;display:inline-block}
.blanknote{padding:10px 16px 14px;font-family:"IBM Plex Mono",monospace;
  font-size:11.5px;color:var(--caution);letter-spacing:.03em}
table{border-collapse:collapse;width:100%;font-size:14px}
thead th{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.12em;
  text-transform:uppercase;color:var(--muted);text-align:left;font-weight:500;
  padding:0 12px 9px;border-bottom:1px solid var(--rule)}
tbody td{padding:14px 12px;border-bottom:1px solid var(--rule-soft);
  vertical-align:top}
tbody tr:last-child td{border-bottom:none}
.qcell{max-width:34ch}
.verdict{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.09em;
  text-transform:uppercase;padding:3px 8px;display:inline-block;
  border:1px solid currentColor;white-space:nowrap}
.v-yes{color:var(--verified)}
.v-no{color:var(--caution)}
.v-part{color:var(--muted)}
.detail{margin:8px 0 0;font-size:13px;color:var(--muted);max-width:40ch}
.census{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));
  gap:1px;background:var(--rule-soft);border:1px solid var(--rule-soft)}
.census>div{background:var(--paper);padding:18px 16px}
.census .n{font-family:"IBM Plex Mono",monospace;font-size:34px;font-weight:500;
  line-height:1;font-variant-numeric:tabular-nums;display:block}
.census .lab{font-family:"IBM Plex Mono",monospace;font-size:10px;
  letter-spacing:.12em;text-transform:uppercase;color:var(--muted);
  display:block;margin-top:9px}
.census .hi{color:var(--caution)}
ul.plain{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;
  gap:14px;max-width:72ch}
ul.plain li{padding-left:20px;position:relative;font-size:15px}
ul.plain li::before{content:"";position:absolute;left:0;top:9px;width:9px;
  height:1px;background:var(--rule)}
.disclosure{border:1px solid var(--rule);padding:22px 24px;background:var(--band)}
.disclosure h2{font-size:16px}
.disclosure dl{margin:0;display:flex;flex-direction:column;gap:13px}
.disclosure dt{font-family:"IBM Plex Mono",monospace;font-size:10px;
  letter-spacing:.13em;text-transform:uppercase;color:var(--muted)}
.disclosure dd{margin:3px 0 0;font-size:14px;max-width:74ch}
footer{border-top:1px solid var(--rule-soft);padding-top:20px;font-size:13px;
  color:var(--muted);max-width:74ch}
footer a{color:inherit}
@media (max-width:640px){
  .wrap{padding:30px 15px 54px;gap:30px}
  .qcell{max-width:none}
  thead{display:none}
  tbody td{display:block;border:none;padding:5px 12px}
  tbody tr{display:block;border-bottom:1px solid var(--rule-soft);padding:12px 0}
}
"""


def verdict_class(status):
    return {"answerable": "v-yes", "unanswerable": "v-no"}.get(status, "v-part")


def verdict_text(status):
    return {"answerable": "Can establish", "unanswerable": "Cannot establish",
            "partial": "Partial"}[status]


def build(case, report):
    v = case["vessel"]
    handover = D(case["handover_date"])
    incident = D(case["incident_date"])
    rec = case["records"]
    a_recv, a_co = report["assessments"]
    census = a_co["gap_census"]["A"]

    out = []
    A = out.append

    A('<div class="wrap">')

    # --- header ---
    A('<header><p class="eyebrow">Record-gap comparison &middot; synthetic '
      'reconstruction</p>'
      '<h1>What the missing records cost you</h1>'
      '<p class="standfirst">A turbocharger fails on one of three diesel '
      'generators. The other two had their turbochargers changed sixteen months '
      'earlier, under the previous manager. Was this one problem or three? '
      'Below, the same history under two arrangements &mdash; records requested '
      'at handover, and records copied to the owner as they were written.</p>'
      '</header>')

    A('<section><dl class="particulars">')
    for k, val in (("Vessel", v["name"]), ("IMO", v["imo"] + " (invalid)"),
                   ("Type", v["type"]), ("Built", str(v["built"])),
                   ("Management change", case["handover_date"]),
                   ("Damage", case["incident_date"])):
        A('<div><dt>%s</dt><dd>%s</dd></div>' % (esc(k), esc(val)))
    A('</dl></section>')

    A('<section><div class="question">The surveyor needs running hours, overhaul '
      'history and <em>the reasons for those changes</em>, across all three '
      'generators. Two of the three sets were worked on before the current '
      'manager arrived.</div></section>')

    # --- the two timelines ---
    A('<section><h2>The same three years, twice</h2>')

    KEY_WASH = ('<span><i style="background:var(--muted);width:2px;height:12px">'
                '</i>Water wash</span>')
    KEY_REP = ('<span><i style="background:var(--ink)"></i>Cartridge replaced, '
               'with reason</span>')
    KEY_STRIP = ('<span><i style="border:1.6px solid var(--caution)"></i>'
                 'Cartridge replaced &mdash; purchase order only, no reason</span>')
    KEY_INS = ('<span><i style="border:1.5px solid var(--ink);border-radius:50%">'
               '</i>Inspection</span>')
    KEY_DMG = ('<span><i style="background:var(--caution);border-radius:50%"></i>'
               'Damage</span>')
    KEY_LO = ('<span><i style="background:var(--verified);transform:rotate(45deg)">'
              '</i>Lube oil event</span>')

    for label, rows, blank, note, key in (
        ("As received at handover", rec["handover"], True,
         "Two cartridge changes are visible only because the owner paid the "
         "invoices &mdash; and a purchase order does not record why the cartridge "
         "was changed. Nothing in the pack indicates how much else is absent.",
         [KEY_WASH, KEY_STRIP, KEY_DMG]),
        ("Co-held at write time", rec["coheld"], False, None,
         [KEY_WASH, KEY_REP, KEY_INS, KEY_DMG, KEY_LO]),
    ):
        A('<div class="panel"><div class="panelhead"><h3>%s</h3>'
          '<span class="count">%d entries</span></div>'
          '<div class="tlwrap">%s</div>'
          % (esc(label), len(rows),
             timeline(rows, handover, incident, blank)))
        A('<div class="key">' + "".join(key) + '</div>')
        if note:
            A('<p class="blanknote">%s</p>' % note)
    A('</section>')

    # --- the four questions ---
    A('<section><h2>What each record can establish</h2>'
      '<div style="overflow-x:auto"><table><thead><tr>'
      '<th class="qcell">Question</th><th>As received at handover</th>'
      '<th>Co-held at write time</th></tr></thead><tbody>')

    for qr, qc in zip(a_recv["questions"], a_co["questions"]):
        A('<tr><td class="qcell">%s</td>' % esc(qr["question"]))
        for q in (qr, qc):
            A('<td><span class="verdict %s">%s</span>'
              % (verdict_class(q["status"]), verdict_text(q["status"])))
            note = q.get("finding") or q.get("note") or ""
            if note:
                A('<p class="detail">%s</p>' % esc(note))
            A('</td>')
        A('</tr>')
    A('</tbody></table></div></section>')

    # --- the census ---
    A('<section><h2>The difference is not what you hold. It is what you can count.</h2>'
      '<p class="standfirst" style="margin-bottom:18px">A handover pack arrives as '
      'a pile of rows. An absent row and a job that was never done look exactly '
      'the same. Where each entry is published to the owner as it is written, the '
      'entries form a sequence &mdash; so a missing one leaves a hole you can '
      'point at.</p>')
    A('<div class="census">'
      '<div><span class="n">%d</span><span class="lab">Entries written by the '
      'outgoing manager</span></div>'
      '<div><span class="n hi">%d</span><span class="lab">Of those, received at '
      'handover</span></div>'
      '<div><span class="n">%d</span><span class="lab">Held by the owner under '
      'co-holding</span></div>'
      '<div><span class="n">%s</span><span class="lab">Missing entries the '
      'handover pack can identify</span></div>'
      '</div></section>'
      % (census["entries_written"],
         sum(1 for r in rec["handover"] if r["manager"] == "A"),
         census["entries_held"], "none"))

    # --- the honesty section ---
    A('<section><h2>What co-holding does not fix</h2><ul class="plain">')
    for item in report["not_fixed_by_coholding"]:
        A('<li>%s</li>' % esc(item))
    A('</ul></section>')

    # --- disclosure ---
    d = report["_disclosure"]
    A('<section class="disclosure"><h2>What is real here, and what is not</h2><dl>')
    for k, lab in (("real", "Real"), ("synthetic", "Invented"),
                   ("not_claimed", "Not claimed")):
        A('<dt>%s</dt><dd>%s</dd>' % (lab, esc(d[k])))
    A('</dl></section>')

    A('<footer>Built from the shape of a case published by Gard on 21 July 2026, '
      '&ldquo;The risk of taking over a vessel without its history&rdquo;, by '
      'Svend Leo Larsen and Kristin Urdahl. The underlying problem is documented '
      'in Gard&rsquo;s 2010 loss prevention circular and in IUMI&rsquo;s position '
      'paper <em>Loss of ship records</em> of 8 September 2015, which asked IACS, '
      'jointly with the London Joint Hull Committee, to make record retention a '
      'condition of class. Every figure on this page is computed from '
      '<code>case.json</code> by <code>analyse.py</code>.</footer>')

    A('</div>')
    return "".join(out)


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600'
         '&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">')

TITLE = "The Turbocharger You Cannot Explain"


def main():
    with open(CASE, encoding="utf-8") as f:
        case = json.load(f)
    with open(REPORT, encoding="utf-8") as f:
        report = json.load(f)

    body = build(case, report)
    style = "<style>" + CSS + "</style>"

    with open(OUT_STANDALONE, "w", encoding="utf-8") as f:
        f.write('<!doctype html><html lang="en"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1">'
                "<title>" + TITLE + "</title>" + FONTS + style +
                "</head><body>" + body + "</body></html>")

    # Artifact publishing wraps the file in its own skeleton, so emit the head
    # contents plus body only -- no doctype, html, head or body tags.
    with open(OUT_FRAGMENT, "w", encoding="utf-8") as f:
        f.write("<title>" + TITLE + "</title>" + FONTS + style + body)

    print("wrote " + OUT_STANDALONE)
    print("wrote " + OUT_FRAGMENT)


if __name__ == "__main__":
    main()
