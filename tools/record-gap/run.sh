#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python build_case.py
python analyse.py
python render.py
