#!/bin/bash
# Phase 0 data pull: four dates of US AIS, two port boxes.
#
# ~1.3 GB of transfer. Archives are deleted after extraction -- only the filtered
# port CSVs are kept (~50 MB each for Houston, ~18 MB for LA/LB).
#
# NOTE: downloads use curl, not Python urllib. urllib fails SSL verification on some
# Windows boxes ("Basic Constraints of CA cert not marked critical") where curl is fine.
set -e
cd "$(dirname "$0")"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124 Safari/537.36"
BASE="https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2023"

for d in 2023_01_15 2023_04_16 2023_07_16 2023_10_15; do
  if [ -s "lalb_$d.csv" ] && [ -s "houston_$d.csv" ]; then
    echo "=== $d (already extracted) ==="; continue
  fi
  echo "=== $d ==="
  curl -fsSL -m 900 -A "$UA" "$BASE/AIS_$d.zip" -o "AIS_$d.zip" \
       -w "  downloaded %{size_download} bytes\n" </dev/null
  python extract_box.py "AIS_$d.zip" "$d"
  rm -f "AIS_$d.zip"
done
echo "done -- now run: python aggregate.py && python divergence.py"
