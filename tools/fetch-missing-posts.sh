#!/bin/bash
#
# Retry the four Holo Sail blog posts that could not be recovered on 25 Aug 2026.
#
# On that date the Internet Archive was returning 503 on every request, and
# archive.today was confirmed (by hand, in a browser) to hold nothing at all for
# holosailtechnologies.com. Run this again whenever the Archive is healthy.
#
# Usage:   bash tools/fetch-missing-posts.sh
# Output:  sources/website/<slug>.txt for anything it recovers
#
# IMPORTANT: this validates by extracted text length, NOT by file size. Internet
# Archive error pages arrive padded to 250-870 KB of whitespace and sail past a
# naive size check. Two files fooled the original collection that way.

set -u
cd "$(dirname "$0")/.." || exit 1
mkdir -p sources/website .tmp-fetch
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"

# timestamp|slug -- timestamps are the snapshots listed in the Wayback CDX
# inventory at sources/website/wayback-url-inventory.txt
TARGETS="
20200803141531|holosail-s-modernization-of-global-supply-chain
20200803142406|holo-sail-is-headed-to-rotterdam
20200803153932|what-is-a-port-community-system-pcs
20200803142746|redefining-automation
"

extract() {
  python - "$1" "$2" <<'PY'
import re,sys,html
raw=open(sys.argv[1],encoding='utf-8',errors='replace').read()
if 'Internet Archive services are temporarily offline' in raw: sys.exit(1)
if 'Wayback Machine has not archived' in raw: sys.exit(1)
s=re.sub(r'(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>',' ',raw)
s=re.sub(r'(?s)<!--.*?-->',' ',s)
s=re.sub(r'(?i)<(br|/p|/div|/li|/h[1-6]|/span)[^>]*>','\n',s)
s=re.sub(r'(?s)<[^>]+>',' ',s); s=html.unescape(s)
s=re.sub(r'[ \t]+',' ',s); s=re.sub(r'\n\s*\n+','\n',s).strip()
if len(re.sub(r'\s+',' ',s))<400: sys.exit(1)
open(sys.argv[2],'w',encoding='utf-8').write(s)
sys.exit(0)
PY
}

ROUNDS=${ROUNDS:-8}
for round in $(seq 1 "$ROUNDS"); do
  remaining=0
  echo "=== round $round of $ROUNDS ==="
  while IFS='|' read -r ts slug; do
    [ -z "${slug:-}" ] && continue
    final="sources/website/2020-08-03-post-${slug}.txt"
    [ -s "$final" ] && continue
    remaining=$((remaining+1))
    tmp=".tmp-fetch/$slug.html"
    code=$(curl -s -m 45 -A "$UA" -o "$tmp" -w "%{http_code}" \
      "https://web.archive.org/web/${ts}id_/https://www.holosailtechnologies.com/post/${slug}" </dev/null)
    if [ "$code" = "200" ] && extract "$tmp" "$final"; then
      echo "  RECOVERED  $slug"
    else
      rm -f "$final"; echo "  fail       $slug (http $code)"
    fi
    sleep 5
  done <<< "$TARGETS"
  [ "$remaining" = "0" ] && { echo "All four recovered."; break; }
  [ "$round" -lt "$ROUNDS" ] && { echo "--- backing off ---"; sleep 45; }
done

rm -rf .tmp-fetch
echo
echo "=== STATUS ==="
while IFS='|' read -r ts slug; do
  [ -z "${slug:-}" ] && continue
  f="sources/website/2020-08-03-post-${slug}.txt"
  if [ -s "$f" ]; then echo "  have    $f"; else echo "  MISSING $slug"; fi
done <<< "$TARGETS"
echo
echo "If any are still missing, the Internet Archive is the only known source."
echo "archive.today was checked by hand on 25 Aug 2026 and holds nothing for"
echo "this domain. See docs/05-source-inventory.md."
