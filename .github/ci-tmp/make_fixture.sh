#!/usr/bin/env bash
# TEMPORARY -- part of the issue #2269 Linux icon verification harness.
#
# Generate a throwaway Flet app that exercises the Linux icon and desktop
# entry code paths. Generated outside the repo checkout so it cannot be
# committed by accident, and kept minimal (no extension dependencies) so a
# failure points at the icon work rather than at an unrelated plugin.
#
# Usage: make_fixture.sh <leg> <app_dir> <repo_root>
#
# Legs:
#   default  no icon in assets -- the template's 1024x1024 default is used,
#            which the runner must downscale to fit within _NET_WM_ICON
#   themed   256x256 icon_linux.png -> installs into hicolor/256x256
#   large    512x512 icon_linux.png -> must install into hicolor/512x512
#   hostile  quotes, newline, tab and backslash in the description plus a
#            space in the artifact name -- exercises escaping and Exec quoting
set -euo pipefail

LEG="$1"
APP_DIR="$2"
REPO_ROOT="$3"

ARTIFACT="flet-icon-test"
DESCRIPTION="A plain description."
ICON_SIZE=""

case "$LEG" in
  default) ;;
  themed) ICON_SIZE=256 ;;
  large) ICON_SIZE=512 ;;
  hostile)
    ARTIFACT="flet icon test"
    # Apostrophe (breaks single-quoted YAML), double quote (breaks JSON and
    # HTML attributes), newline and tab (break a desktop entry) and a
    # backslash (a desktop entry escape character).
    DESCRIPTION="Bob's \"great\" tool
	with C:\\path"
    ICON_SIZE=256
    ;;
  *)
    echo "unknown leg: $LEG" >&2
    exit 2
    ;;
esac

mkdir -p "$APP_DIR/src/assets"
cd "$APP_DIR"

cat > src/main.py <<'PY'
import flet as ft


def main(page: ft.Page):
    page.add(ft.Text("flet icon test"))


ft.run(main)
PY

if [ -n "$ICON_SIZE" ]; then
  python3 "$REPO_ROOT/.github/ci-tmp/make_png.py" \
    "src/assets/icon_linux.png" "$ICON_SIZE" "$ICON_SIZE" 32 96 200
fi

# The description goes through a file so the shell never has to quote it.
printf '%s' "$DESCRIPTION" > .description.txt

python3 "$REPO_ROOT/.github/ci-tmp/write_pyproject.py" \
  "$ARTIFACT" .description.txt "$REPO_ROOT"

rm -f .description.txt
echo "--- pyproject.toml"
cat pyproject.toml
