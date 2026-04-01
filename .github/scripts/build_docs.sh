#!/usr/bin/env bash
set -euo pipefail

# install uv
pip install uv

# generate coverage report and badges
cd sdk/python
for pkg in packages/*; do
  if [ -f "$pkg/pyproject.toml" ] && [ -d "$pkg/src" ]; then
    pkg_name=$(basename "$pkg")
    echo "====== $pkg ======"
    uv run --group docs-coverage docstr-coverage -C .docstr.yaml "$pkg/src" \
      --badge="../../website/static/docs/assets/badges/docs-coverage/${pkg_name}.svg"
    echo
  fi
done
cd -

# build website
cd website
yarn install
yarn build
cd -

# run verification checks
bash .github/scripts/check_docs.sh website/build
