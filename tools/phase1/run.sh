#!/bin/bash
# Phase 1 end to end. Needs tools/phase0/fetch.sh to have run first.
set -e
cd "$(dirname "$0")"
python -m pip install --quiet --disable-pip-version-check cryptography
echo "=== building case from real AIS ==="   && python build_case.py
echo && echo "=== commit / reveal / verify ===" && python demo.py
echo && echo "=== negative control ==="        && python tamper_test.py
