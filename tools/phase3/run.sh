#!/bin/bash
# Phase 3 end to end. Needs tools/phase1/run.sh to have produced case.json.
# Contacts live public services (drand, OpenTimestamps) -- needs network.
set -e
cd "$(dirname "$0")"
echo "=== witnessed commit / reveal / verify ===" && python phase3.py
echo && echo "=== negative control ===" && python negative_control.py
