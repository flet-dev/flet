#!/usr/bin/env bash
set -euo pipefail

BUILD_DIR="${1:-website/build}"

python3 .github/scripts/check_docs.py "$BUILD_DIR"
