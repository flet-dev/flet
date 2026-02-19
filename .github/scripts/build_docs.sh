set -euo pipefail

# install uv
pip install uv

# generate coverage report and badges
for pkg in packages/*; do
if [ -f "$pkg/pyproject.toml" ] && [ -d "$pkg/src" ]; then
    pkg_name=$(basename "$pkg")
    echo "====== $pkg ======"
    uv run --no-dev --group docs-coverage docstr-coverage -C .docstr.yaml "$pkg/src" --badge="packages/flet/docs/assets/badges/docs-coverage/${pkg_name}.svg"
    echo
fi
done

# generate docs website
cd packages/flet
uv sync --group docs && uv run mkdocs build
cd -
