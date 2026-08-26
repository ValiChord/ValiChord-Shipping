"""Phase 0b step 1 -- find published judgments that (a) turn on laytime/NOR timing and
(b) name a vessel at a US port inside the free-AIS window (2009-2025).

Source: The National Archives 'Find Case Law', Atom API, Open Justice Licence.
"""
import json, re, sys, time, urllib.request, urllib.parse
from xml.etree import ElementTree as ET

ATOM = "https://caselaw.nationalarchives.gov.uk/atom.xml"
NS = {"a": "http://www.w3.org/2005/Atom",
      "tna": "https://caselaw.nationalarchives.gov.uk"}
UA = "valichord-shipping-phase0b (research; contact via github.com/ValiChord)"

QUERIES = ["laytime", "demurrage", '"notice of readiness"', "charterparty laytime"]

# US ports with NOAA/MarineCadastre AIS coverage, plus common spellings
US_PORTS = [
    "Houston", "Galveston", "New Orleans", "Corpus Christi", "Beaumont",
    "Port Arthur", "Baton Rouge", "Los Angeles", "Long Beach", "Baltimore",
    "New York", "Norfolk", "Savannah", "Charleston", "Mobile", "Tampa",
    "Freeport, Texas", "Texas City", "Lake Charles", "Paulsboro", "Philadelphia",
    "Seattle", "Portland, Oregon", "Tacoma", "Oakland", "Jacksonville",
    "Brownsville", "Pascagoula", "Convent", "Destrehan", "Myrtle Grove",
]


def get(url, timeout=45):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def index(query, max_pages=15):
    out = {}
    for page in range(1, max_pages + 1):
        q = urllib.parse.urlencode({"query": query, "order": "-date",
                                    "per_page": 50, "page": page})
        try:
            root = ET.fromstring(get(f"{ATOM}?{q}"))
        except Exception as e:
            print(f"  page {page} failed: {e}", file=sys.stderr)
            break
        entries = root.findall("a:entry", NS)
        if not entries:
            break
        for e in entries:
            link = e.find("a:link[@rel='alternate']", NS).get("href")
            ncn = e.find("tna:identifier[@type='ukncn']", NS)
            out[link] = {
                "name": e.findtext("a:title", "", NS).strip(),
                "url": link,
                "ncn": ncn.get("slug") if ncn is not None else None,
                "published": e.findtext("a:published", "", NS)[:10],
            }
        time.sleep(0.4)
    return out


def main():
    cases = {}
    for q in QUERIES:
        print(f"indexing: {q}", file=sys.stderr)
        found = index(q)
        print(f"  {len(found)} judgments", file=sys.stderr)
        cases.update(found)

    # keep only what could overlap free US AIS (2009-2025 events; judgment later)
    cases = {k: v for k, v in cases.items()
             if v["published"] and v["published"][:4] >= "2010"}
    print(f"\n{len(cases)} unique judgments from 2010 onward", file=sys.stderr)

    with open("candidates_index.json", "w", encoding="utf-8") as fh:
        json.dump(list(cases.values()), fh, indent=2)
    print("wrote candidates_index.json", file=sys.stderr)


if __name__ == "__main__":
    main()
