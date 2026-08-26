"""Phase 0b step 2 -- fetch each candidate judgment and score it for testability.

A judgment is testable against free public AIS only if it names ALL of:
  * a vessel  (so we can find her in the AIS by name)
  * a US port (so NOAA/MarineCadastre covers the water)
  * a date in 2009-2025 (the free AIS window)
  * a disputed clock time (so there is a fact to check)
"""
import json, re, sys, time, urllib.request

UA = "valichord-shipping-phase0b (research; contact via github.com/ValiChord)"

US_PORTS = [
    "Houston", "Galveston", "New Orleans", "Corpus Christi", "Beaumont",
    "Port Arthur", "Baton Rouge", "Los Angeles", "Long Beach", "Baltimore",
    "Norfolk", "Savannah", "Charleston", "Mobile", "Tampa", "Texas City",
    "Lake Charles", "Paulsboro", "Philadelphia", "Seattle", "Tacoma",
    "Oakland", "Jacksonville", "Brownsville", "Pascagoula", "Convent",
    "Destrehan", "New York", "Freeport", "Portland", "Vancouver, Washington",
]
NOR_WORDS = ["notice of readiness", "laytime", "demurrage", "arrived ship",
             "tendered", "berth", "anchorage"]

TIME_RE = re.compile(r"\b([01]?\d|2[0-3])[.:]([0-5]\d)\s*(?:hrs|hours|am|pm)?\b", re.I)
YEAR_RE = re.compile(r"\b(20(?:0[9]|1\d|2[0-5]))\b")
VESSEL_RE = re.compile(r'(?:"|“)([A-Z][A-Z \-\.]{2,30})(?:"|”)'
                       r'|\bthe\s+(?:m\.?v\.?|mv|m/v|vessel)\s+([A-Z][A-Za-z\- ]{2,30})')


def text_of(url):
    req = urllib.request.Request(url + "/data.xml", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read(3_000_000).decode("utf-8", "replace")
    raw = re.sub(r"<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", raw)


def main():
    cases = json.load(open("candidates_index.json", encoding="utf-8"))
    hits, done = [], 0
    for c in cases:
        done += 1
        try:
            t = text_of(c["url"])
        except Exception as e:
            print(f"  [{done}/{len(cases)}] FAIL {c['ncn']}: {type(e).__name__}",
                  file=sys.stderr)
            continue

        ports = sorted({p for p in US_PORTS if re.search(rf"\b{re.escape(p)}\b", t)})
        if not ports:
            continue
        nor = sorted({w for w in NOR_WORDS if w in t.lower()})
        if "notice of readiness" not in nor and "laytime" not in nor:
            continue
        years = sorted(set(YEAR_RE.findall(t)))
        if not years:
            continue
        times = TIME_RE.findall(t)
        vessels = sorted({(a or b).strip() for a, b in VESSEL_RE.findall(t)
                          if len(((a or b) or "").strip()) > 3})[:8]

        score = (len(ports) > 0) + (len(times) >= 3) + ("notice of readiness" in nor) \
                + (len(vessels) > 0) + (len(years) > 0)
        hits.append({**c, "usPorts": ports, "years": years,
                     "clockTimes": len(times), "vesselCandidates": vessels,
                     "norTerms": nor, "score": score, "chars": len(t)})
        print(f"  [{done}/{len(cases)}] HIT {c['ncn']} score={score} "
              f"ports={ports[:3]} years={years[:4]}", file=sys.stderr)
        time.sleep(0.3)

    hits.sort(key=lambda h: (-h["score"], -h["clockTimes"]))
    with open("candidates_scored.json", "w", encoding="utf-8") as fh:
        json.dump(hits, fh, indent=2)
    print(f"\n{len(hits)} judgments mention a US port and laytime/NOR",
          file=sys.stderr)


if __name__ == "__main__":
    main()
