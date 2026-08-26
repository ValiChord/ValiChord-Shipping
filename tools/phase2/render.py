"""Phase 2 — render the discrepancy record as one page a laytime desk can read.

Reads ../phase1/case.json and ../phase1/discrepancy_record.json, writes report.html.
Self-contained: no external assets except Google Fonts.

The test this has to pass (docs/09): a maritime professional understands it without
anyone explaining it. If it needs narration it has failed, and correctness does not
rescue it.

Design notes, so edits stay coherent:
  * The palette is the Admiralty chart convention. Magenta is the UKHO overprint for
    cautions and warnings -- so it appears EXACTLY ONCE on this page, on the
    contradiction. If a second thing turns magenta, the signal is gone.
  * The chart is distance-from-port against time, because that is the axis the
    dispute actually turns on. The port limit is drawn as a line, and the claim sits
    visibly above it.
  * Everything is generated from the real track. No hand-drawn paths.
"""
import json, math, os, sys
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.join(HERE, "..", "phase1", "case.json")
REC = os.path.join(HERE, "..", "phase1", "discrepancy_record.json")
OUT = os.path.join(HERE, "report.html")


def T(s):
    return datetime.strptime(s.replace("Z", ""), "%Y-%m-%dT%H:%M:%S")


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build_chart(track, port, claimed_iso, cross_after, cross_before, stop_before,
                w=1000, h=360):
    """Distance-from-port against time, over the APPROACH WINDOW only.

    The full track spans 18 hours, of which 17 are the vessel lying stopped. Plotting
    all of it crushes the entire arrival into the left 3% of the axis and puts the
    claim label off-canvas. The dispute is about the approach, so the chart is about
    the approach: first fix through 45 minutes past the crossing.
    """
    pad_l, pad_r, pad_t, pad_b = 64, 26, 46, 36
    t0 = T(track[0]["t"])
    t1 = T(cross_before) + timedelta(minutes=45)
    win = [p for p in track if t0 <= T(p["t"]) <= t1]
    span = (t1 - t0).total_seconds()
    dmax = max(p["dist_nm"] for p in win) * 1.10

    def x(t):
        return pad_l + (T(t) - t0).total_seconds() / span * (w - pad_l - pad_r)

    def y(d):
        return pad_t + (1 - d / dmax) * (h - pad_t - pad_b)

    pts = " ".join(f"{x(p['t']):.1f},{y(p['dist_nm']):.1f}" for p in win)
    limit_y = y(port["limit_nm"])

    grid = "".join(
        f'<line class="grid" x1="{pad_l}" y1="{y(d):.1f}" x2="{w-pad_r}" y2="{y(d):.1f}"/>'
        f'<text class="ax" x="{pad_l-10}" y="{y(d)+4:.1f}" text-anchor="end">{d}</text>'
        for d in range(0, int(dmax) + 1, 5))

    ticks = ""
    cur = t0.replace(minute=(t0.minute // 15) * 15, second=0) + timedelta(minutes=15)
    while cur <= t1:
        xs = x(cur.strftime("%Y-%m-%dT%H:%M:%S"))
        ticks += (f'<line class="tick" x1="{xs:.1f}" y1="{h-pad_b}" x2="{xs:.1f}" '
                  f'y2="{h-pad_b+5}"/><text class="ax" x="{xs:.1f}" y="{h-pad_b+19}" '
                  f'text-anchor="middle">{cur.strftime("%H:%M")}</text>')
        cur += timedelta(minutes=15)

    cl = T(claimed_iso)
    before = max((p for p in win if T(p["t"]) <= cl), key=lambda p: p["t"])
    cx, cy = x(claimed_iso.replace("Z", "")), y(before["dist_nm"])
    ax_ = x(cross_before)

    # keep labels on canvas: anchor away from whichever edge is closer
    lab_anchor, lab_dx = ("start", 12) if cx < w * 0.42 else ("end", -12)
    act_anchor, act_dx = ("start", 10) if ax_ < w * 0.72 else ("end", -10)

    return f'''<svg viewBox="0 0 {w} {h}" role="img"
  aria-label="Distance of the vessel from the port reference point during her approach.
  The carrier's claimed arrival time falls where she was still {before['dist_nm']:.1f}
  nautical miles out, well above the {port['limit_nm']:.0f} nautical mile port limit,
  making {before['sog']:.1f} knots.">
  <rect class="seaband" x="{pad_l}" y="{limit_y:.1f}" width="{w-pad_l-pad_r}"
        height="{h-pad_b-limit_y:.1f}"/>
  <text class="zonelab" x="{pad_l+10}" y="{limit_y+18:.1f}">INSIDE PORT LIMITS</text>
  {grid}{ticks}
  <line class="axis" x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{h-pad_b}"/>
  <line class="axis" x1="{pad_l}" y1="{h-pad_b}" x2="{w-pad_r}" y2="{h-pad_b}"/>
  <line class="limit" x1="{pad_l}" y1="{limit_y:.1f}" x2="{w-pad_r}" y2="{limit_y:.1f}"/>
  <text class="limitlab" x="{w-pad_r-8}" y="{limit_y-9:.1f}" text-anchor="end">PORT LIMIT {port['limit_nm']:.0f} nm</text>
  <line class="gapline" x1="{cx:.1f}" y1="{pad_t+14:.1f}" x2="{ax_:.1f}" y2="{pad_t+14:.1f}"/>
  <line class="gaptick" x1="{cx:.1f}" y1="{pad_t+9:.1f}" x2="{cx:.1f}" y2="{pad_t+19:.1f}"/>
  <line class="gaptick" x1="{ax_:.1f}" y1="{pad_t+9:.1f}" x2="{ax_:.1f}" y2="{pad_t+19:.1f}"/>
  <text class="gaplab" x="{(cx+ax_)/2:.1f}" y="{pad_t+4:.1f}" text-anchor="middle">{(T(cross_before)-cl).total_seconds()/60:.0f} min before she was inside</text>
  <polyline class="track" points="{pts}"/>
  <line class="actual" x1="{ax_:.1f}" y1="{limit_y:.1f}" x2="{ax_:.1f}" y2="{h-pad_b}"/>
  <circle class="actualdot" cx="{ax_:.1f}" cy="{limit_y:.1f}" r="4.5"/>
  <text class="actuallab" x="{ax_+act_dx:.1f}" y="{limit_y+34:.1f}" text-anchor="{act_anchor}">CROSSED {T(cross_before).strftime('%H:%M')}</text>
  <line class="claimline" x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx:.1f}" y2="{limit_y:.1f}"/>
  <circle class="claimdot" cx="{cx:.1f}" cy="{cy:.1f}" r="5.5"/>
  <text class="claimlab" x="{cx+lab_dx:.1f}" y="{cy-6:.1f}" text-anchor="{lab_anchor}">CARRIER CLAIMS ARRIVED {cl.strftime('%H:%M')}</text>
  <text class="claimsub" x="{cx+lab_dx:.1f}" y="{cy+11:.1f}" text-anchor="{lab_anchor}">still {before['dist_nm']:.2f} nm out &#183; {before['sog']:.1f} kt &#183; &#8220;under way using engine&#8221;</text>
  <text class="ylab" x="16" y="{pad_t+(h-pad_t-pad_b)/2:.1f}" transform="rotate(-90 16 {pad_t+(h-pad_t-pad_b)/2:.1f})" text-anchor="middle">NAUTICAL MILES FROM PORT</text>
</svg>'''


def main():
    case = json.load(open(CASE, encoding="utf-8"))
    rec = json.load(open(REC, encoding="utf-8"))
    track, port, vessel = case["track"], case["port"], case["vessel"]
    ev = case["derived_events"]
    carrier = next(f for f in rec["claimsVersusTelemetry"] if f["role"] == "CARRIER")
    claimed = carrier["claimedEventDateTime"]
    gap_min = (T(ev["port_limit_inbound"]["before"]) - T(claimed)).total_seconds() / 60
    b = carrier["telemetryBracket"]["lastFixAtOrBefore"]

    chart = build_chart(track, port, claimed,
                        ev["port_limit_inbound"]["after"], ev["port_limit_inbound"]["before"],
                        ev["stopped"]["before"])

    rows = ""
    for f in rec["claimsVersusTelemetry"]:
        bk = f["telemetryBracket"]["lastFixAtOrBefore"]
        bad = f["finding"] == "CONTRADICTED_BY_TELEMETRY"
        # Show WHAT was tested, not just the verdict. A reader who cannot see the
        # assertions has to take the verdict on trust, which is the opposite of the
        # point. Added 26 Aug 2026 -- see docs/16 Part 3.
        tested = "".join(
            f'<span class="pty">{"&#10007;" if not a["holds"] else "&#10003;"} '
            f'{esc(a["assertion"])} &#8212; {esc(a["measured"])}</span>'
            for a in f.get("assertionsTested", []))
        rows += f'''<tr class="{'flag' if bad else ''}">
      <td><span class="role">{esc(f['role'].replace('_',' '))}</span>
          <span class="pty">{esc(f['party'])}</span></td>
      <td class="num">{esc(f['claimedEventDateTime'])}</td>
      <td class="num">{bk['distanceFromPortNm']:.2f}</td>
      <td class="num">{bk['speedOverGroundKt']:.1f}</td>
      <td class="stat">{esc(bk['vesselBroadcastStatus'])}</td>
      <td><span class="verdict {'v-bad' if bad else 'v-ok'}">
        {'contradicted' if bad else 'consistent'}</span>{tested}</td></tr>'''

    seals = ""
    for i in rec["commitmentIntegrity"]:
        ok = i["commitment_matches_reveal"] and i["signature_valid"]
        seals += f'''<tr><td><span class="role">{esc(i['role'].replace('_',' '))}</span></td>
      <td class="hash">{esc(i['commitment_sha256'][:32])}&#8230;</td>
      <td><span class="verdict {'v-ok' if ok else 'v-bad'}">
        {'hash &amp; signature verified' if ok else 'FAILED'}</span></td></tr>'''

    nd = "".join(f"<li>{esc(u)}</li>" for u in rec["notDetermined"])

    html = f'''<title>Arrived Ship Check</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<style>
:root{{
  --paper:#FBFAF7; --ink:#12202B; --sea:#E6EDF1; --rule:#C3CFD6;
  --rule-soft:#E1E8EC; --caution:#B0177C; --verified:#2E6B5E; --muted:#5A6C76;
  --band:#F2F0EB;
}}
@media (prefers-color-scheme:dark){{
  :root:not([data-theme="light"]){{
    --paper:#0D1820; --ink:#E8EFF3; --sea:#16242E; --rule:#2E404C;
    --rule-soft:#1E2E38; --caution:#FF6BC0; --verified:#63BCA2; --muted:#8FA0AB;
    --band:#121F27;
  }}
}}
:root[data-theme="dark"]{{
  --paper:#0D1820; --ink:#E8EFF3; --sea:#16242E; --rule:#2E404C;
  --rule-soft:#1E2E38; --caution:#FF6BC0; --verified:#63BCA2; --muted:#8FA0AB;
  --band:#121F27;
}}
*{{box-sizing:border-box}}
body{{background:var(--paper);color:var(--ink);
  font-family:"IBM Plex Sans",system-ui,sans-serif;line-height:1.55;margin:0;
  -webkit-font-smoothing:antialiased}}
.wrap{{max-width:1080px;margin:0 auto;padding:44px 28px 80px;
  display:flex;flex-direction:column;gap:34px}}
.eyebrow{{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--muted)}}
h1{{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:clamp(30px,4vw,44px);
  line-height:1.12;margin:8px 0 0;text-wrap:balance;letter-spacing:-.01em}}
h2{{font-family:"Source Serif 4",Georgia,serif;font-weight:600;font-size:20px;margin:0;
  text-wrap:balance}}
p{{margin:0}}
.lede{{font-size:17px;color:var(--muted);max-width:62ch;margin-top:10px}}
.disclosure{{border:1px solid var(--rule);border-left:3px solid var(--muted);
  background:var(--band);padding:14px 18px;font-size:13.5px;color:var(--muted);
  display:flex;flex-direction:column;gap:5px}}
.disclosure b{{color:var(--ink);font-weight:600}}
.particulars{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
  gap:0;border-top:1.5px solid var(--ink);border-bottom:1px solid var(--rule)}}
.particulars div{{padding:12px 16px 13px;border-right:1px solid var(--rule-soft)}}
.particulars div:last-child{{border-right:none}}
.particulars dt{{font-family:"IBM Plex Mono",monospace;font-size:10.5px;
  letter-spacing:.13em;text-transform:uppercase;color:var(--muted);margin:0 0 3px}}
.particulars dd{{margin:0;font-size:15px;font-weight:500;
  font-variant-numeric:tabular-nums}}
.finding{{border:1px solid var(--caution);border-left:4px solid var(--caution);
  padding:18px 22px;display:flex;flex-direction:column;gap:8px}}
.finding .eyebrow{{color:var(--caution)}}
.finding p{{font-size:16.5px;max-width:66ch}}
figure{{margin:0;display:flex;flex-direction:column;gap:12px}}
.chartbox{{overflow-x:auto;border:1px solid var(--rule);background:var(--paper)}}
svg{{display:block;min-width:760px;width:100%;height:auto}}
.seaband{{fill:var(--sea)}}
.grid{{stroke:var(--rule-soft);stroke-width:1}}
.axis{{stroke:var(--rule);stroke-width:1}}
.tick{{stroke:var(--rule);stroke-width:1}}
.ax{{font-family:"IBM Plex Mono",monospace;font-size:10.5px;fill:var(--muted)}}
.ylab{{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.14em;
  fill:var(--muted)}}
.limit{{stroke:var(--ink);stroke-width:1.5;stroke-dasharray:7 4}}
.limitlab{{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.1em;
  fill:var(--ink)}}
.track{{fill:none;stroke:var(--ink);stroke-width:2;stroke-linejoin:round}}
.actual{{stroke:var(--verified);stroke-width:1.5}}
.actualdot{{fill:var(--verified)}}
.actuallab{{font-family:"IBM Plex Mono",monospace;font-size:11px;fill:var(--verified)}}
.claimline{{stroke:var(--caution);stroke-width:1.5;stroke-dasharray:3 3}}
.claimdot{{fill:var(--caution)}}
.claimlab{{font-family:"IBM Plex Mono",monospace;font-size:11.5px;letter-spacing:.06em;
  fill:var(--caution);font-weight:500}}
.claimsub{{font-family:"IBM Plex Mono",monospace;font-size:11px;fill:var(--caution)}}
.gaplab{{font-family:"IBM Plex Mono",monospace;font-size:11.5px;fill:var(--caution);
  font-weight:500;letter-spacing:.04em}}
.gapline{{stroke:var(--caution);stroke-width:1}}
.gaptick{{stroke:var(--caution);stroke-width:1}}
.zonelab{{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.14em;
  fill:var(--muted)}}
figcaption{{font-size:13px;color:var(--muted);max-width:70ch}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
thead th{{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.11em;
  text-transform:uppercase;color:var(--muted);text-align:left;font-weight:400;
  padding:0 12px 8px;border-bottom:1.5px solid var(--ink)}}
tbody td{{padding:12px;border-bottom:1px solid var(--rule-soft);vertical-align:top}}
tbody tr.flag{{background:color-mix(in srgb,var(--caution) 6%,transparent)}}
.role{{display:block;font-weight:600;font-size:13.5px}}
.pty{{display:block;font-size:12px;color:var(--muted)}}
.num,.hash{{font-family:"IBM Plex Mono",monospace;font-variant-numeric:tabular-nums;
  white-space:nowrap}}
.hash{{font-size:12px;color:var(--muted)}}
.stat{{font-size:12.5px;color:var(--muted)}}
.verdict{{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.08em;
  text-transform:uppercase;padding:3px 8px;border:1px solid currentColor;
  white-space:nowrap;display:inline-block}}
.v-ok{{color:var(--verified)}} .v-bad{{color:var(--caution)}}
.tablewrap{{overflow-x:auto}}
section{{display:flex;flex-direction:column;gap:14px}}
.nd{{border-top:1.5px solid var(--ink);padding-top:16px}}
.nd ul{{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:9px;
  font-size:14px;color:var(--muted);max-width:74ch}}
.nd li::marker{{color:var(--rule)}}
footer{{border-top:1px solid var(--rule);padding-top:16px;font-size:12.5px;
  color:var(--muted);display:flex;flex-direction:column;gap:5px}}
a{{color:inherit}}
@media (max-width:640px){{
  .wrap{{padding:28px 16px 60px;gap:26px}}
  .particulars div{{border-right:none;border-bottom:1px solid var(--rule-soft)}}
}}
</style>
<div class="wrap">
<header>
  <p class="eyebrow">Independent telemetry check &#183; protocol run {esc(rec['protocolRun']['id'])}</p>
  <h1>Was she an arrived ship?</h1>
  <p class="lede">A carrier's claimed arrival time, sealed before disclosure and then
  checked against the public record of where the vessel physically was.</p>
</header>

<div class="disclosure">
  <p><b>Telemetry is real.</b> {esc(vessel['name'])}&#8217;s complete track &#8212;
  {case['fix_count']} position fixes &#8212; is unmodified public AIS from
  NOAA&#8239;/&#8239;MarineCadastre.</p>
  <p><b>The four parties are synthetic.</b> No shipping line, port authority or terminal
  supplied operational records. The carrier&#8217;s claim is deliberately constructed to
  test the method. Nothing here says any real carrier misreported anything.</p>
  <p><b>Each claimed time was stated independently of the track.</b> The port
  authority&#8217;s and terminal operator&#8217;s times are fixed clock values with
  plausible reporting lags, not values copied from the telemetry &#8212; so their
  agreement below is a result, not an artefact of how the scenario was built. Every
  assertion tested is printed against its verdict.</p>
</div>

<dl class="particulars">
  <div><dt>Vessel</dt><dd>{esc(vessel['name'])}</dd></div>
  <div><dt>IMO</dt><dd>{esc(vessel['imo'].replace('IMO',''))}</dd></div>
  <div><dt>Port</dt><dd>{esc(port['unlocode'])}</dd></div>
  <div><dt>Date</dt><dd>15 Jan 2023</dd></div>
  <div><dt>Fixes</dt><dd>{case['fix_count']}</dd></div>
</dl>

<div class="finding">
  <p class="eyebrow">Finding</p>
  <p>The carrier sealed a claim that the vessel had arrived at
  <b>{T(claimed).strftime('%H:%M')}&#8239;UTC</b>. At that moment the public track puts her
  <b>{b['distanceFromPortNm']:.2f}&#8239;nm</b> from the port reference point &#8212;
  {b['distanceFromPortNm']-port['limit_nm']:.2f}&#8239;nm outside the
  {port['limit_nm']:.0f}&#8239;nm limit &#8212; making <b>{b['speedOverGroundKt']:.1f} knots</b>,
  broadcasting her own status as &#8220;{esc(b['vesselBroadcastStatus'])}&#8221;.
  She crossed the limit <b>{gap_min:.0f} minutes later</b>.</p>
</div>

<figure>
  <div class="chartbox">{chart}</div>
  <figcaption>Distance from the port reference point, plotted from all
  {case['fix_count']} real AIS fixes. Position, speed and the vessel&#8217;s own broadcast
  status contradict the claim independently, so the finding does not rest on where the
  limit is drawn. Timing uncertainty on the crossing is
  {ev['port_limit_inbound']['window_s']:.0f} seconds &#8212; the discrepancy is
  {gap_min*60/ev['port_limit_inbound']['window_s']:.0f} times larger than the
  measurement window.</figcaption>
</figure>

<section>
  <h2>Every claim against the track</h2>
  <div class="tablewrap"><table>
  <thead><tr><th>Party</th><th>Claimed time&#8239;(UTC)</th><th>Distance&#8239;nm</th>
    <th>Speed&#8239;kt</th><th>Vessel&#8217;s own status</th><th></th></tr></thead>
  <tbody>{rows}</tbody></table></div>
  <p class="lede" style="font-size:13.5px">Each claimed time is placed between the last fix
  before it and the first fix after. The vessel was between those two points and nowhere
  else &#8212; no interpolation, no smoothing.</p>
</section>

<section>
  <h2>Seals</h2>
  <div class="tablewrap"><table>
  <thead><tr><th>Party</th><th>SHA&#8209;256 commitment</th><th></th></tr></thead>
  <tbody>{seals}</tbody></table></div>
  <p class="lede" style="font-size:13.5px">Each party sealed a hash of its record, signed
  with an Ed25519 key, before any record was disclosed. Altering a record after sealing
  breaks the hash; recomputing the hash breaks the signature. Both were tested against
  three substitution attacks and refused all three.</p>
</section>

<section class="nd">
  <h2>What this record does not decide</h2>
  <ul>{nd}</ul>
</section>

<footer>
  <p>Telemetry: NOAA&#8239;/&#8239;MarineCadastre public AIS, 15 January 2023, unmodified.</p>
  <p>Demonstrator &#8212; ValiChord&#8209;Shipping, Phase&#8239;2. Method and limitations
  are documented in full alongside the code.</p>
</footer>
</div>'''

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"wrote {OUT}  ({os.path.getsize(OUT)/1024:.0f} KB)")
    print(f"claimed {T(claimed).strftime('%H:%M')}  actual crossing "
          f"{T(ev['port_limit_inbound']['before']).strftime('%H:%M')}  gap {gap_min:.0f} min")


if __name__ == "__main__":
    main()
