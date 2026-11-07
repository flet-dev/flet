#!/usr/bin/env bash
# Let `flet build` / `flet test` bundle a Python minor whose runtimes are not
# released yet, from the GitHub Actions runs that built them. Temporary: used
# for Python 3.15 until python-build, dart-bridge, serious-python and the
# pypi.flet.dev wheels are released; delete it (and its workflow steps) then.
#
# What it wires, for the app in $APP_DIR:
#   * flet-cli's Python versions table: FLET_PYTHON_BUILD_MANIFEST points at
#     python-build's manifest from $PYTHON_BUILD_REF.
#   * serious_python: the app's pubspec overrides point at a clone of
#     $SERIOUS_PYTHON_REF, whose version tables know the new minor.
#   * runtimes + dart_bridge: serious-python's seed_unreleased_runtimes.sh copies
#     them from $PYTHON_BUILD_RUN_ID / $DART_BRIDGE_RUN_ID into place.
#   * mobile wheels (android, ios): PIP_FIND_LINKS at the msgpack wheels built by
#     the mobile-forge runs in $MOBILE_FORGE_RUN_IDS (pypi.flet.dev has no cp3XX
#     yet).
#
# Usage: wire_unreleased_python.sh <macos|ios|windows|linux|linux-arm64|android>
# Env:   APP_DIR, SERIOUS_PYTHON_VERSION (the minor), PYTHON_BUILD_REF,
#        SERIOUS_PYTHON_REF, PYTHON_BUILD_RUN_ID, DART_BRIDGE_RUN_ID,
#        MOBILE_FORGE_RUN_IDS (space-separated), GH_TOKEN, RUNNER_TEMP, GITHUB_ENV.
set -euo pipefail

platform="${1:?platform}"
tmp="${RUNNER_TEMP:?}/unreleased-python"
mkdir -p "$tmp"

export_env() {
    echo "$1=$2"
    echo "$1=$2" >> "${GITHUB_ENV:?}"
}

# 1. flet-cli's supported-versions table.
curl -fsSL -o "$tmp/manifest.json" \
    "https://raw.githubusercontent.com/flet-dev/python-build/${PYTHON_BUILD_REF:?}/manifest.json"
export_env FLET_PYTHON_BUILD_MANIFEST "$tmp/manifest.json"

# 2. serious_python from the branch, for the Flutter build and the packaging CLI.
sp="$tmp/serious-python"
if [ ! -d "$sp" ]; then
    git clone -q --depth 1 -b "${SERIOUS_PYTHON_REF:?}" \
        https://github.com/flet-dev/serious-python.git "$sp"
fi
sp_src="$sp/src"
if command -v cygpath >/dev/null 2>&1; then
    sp_src="$(cygpath -m "$sp_src")" # C:/... so TOML and pub accept it
fi
{
    echo
    echo "# Added by wire_unreleased_python.sh (CI only)."
    for pkg in serious_python serious_python_android serious_python_darwin \
        serious_python_linux serious_python_windows serious_python_platform_interface; do
        echo "$pkg = { path = \"$sp_src/$pkg\" }"
    done
} >> "${APP_DIR:?}/pyproject.toml"
# The appended lines must land in [tool.flet.flutter.pubspec.dependency_overrides],
# so that table has to be the file's last one.
last_table=$(grep -E '^\[' "$APP_DIR/pyproject.toml" | tail -n1)
if [ "$last_table" != "[tool.flet.flutter.pubspec.dependency_overrides]" ]; then
    echo "::error::$APP_DIR/pyproject.toml must end with [tool.flet.flutter.pubspec.dependency_overrides] (ends with $last_table)"
    exit 1
fi

# 3. Runtimes and dart_bridge binaries.
case "$platform" in
    macos) sp_platform=Darwin ;;
    ios) sp_platform=iOS ;;
    windows) sp_platform=Windows ;;
    linux | linux-arm64) sp_platform=Linux ;;
    android) sp_platform=Android ;;
    *) echo "::error::unknown platform $platform"; exit 1 ;;
esac
bash "$sp/.github/scripts/seed_unreleased_runtimes.sh" "$sp_platform"

# 4. Mobile wheels that pypi.flet.dev doesn't have yet.
if [ "$platform" = android ] || [ "$platform" = ios ]; then
    wheels="$tmp/wheels"
    mkdir -p "$wheels"
    for run in ${MOBILE_FORGE_RUN_IDS:?}; do
        gh run download "$run" --repo flet-dev/mobile-forge \
            --pattern 'wheels-msgpack*' --dir "$tmp/wheel-artifacts/$run"
    done
    find "$tmp/wheel-artifacts" -name "msgpack-*-cp${SERIOUS_PYTHON_VERSION//./}-*.whl" \
        -exec cp {} "$wheels/" \;
    ls "$wheels"
    if [ -z "$(ls "$wheels")" ]; then
        echo "::error::no cp${SERIOUS_PYTHON_VERSION//./} msgpack wheels in mobile-forge runs $MOBILE_FORGE_RUN_IDS"
        exit 1
    fi
    export_env PIP_FIND_LINKS "$wheels"
fi
