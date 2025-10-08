function patch_python_package_versions() {
    cd "$SDK_PYTHON" || exit 1

    # Install dependencies
    uv sync --no-default-groups || true

    # Update package versions in version.py and pyproject.toml files
    for pkg in flet flet-cli flet-desktop flet-web; do
      sed -i -e "s/version = \"\"/version = \"$PYPI_VER\"/g" packages/$pkg/src/${pkg//-/_}/version.py
      uv version --package "$pkg" "$PYPI_VER"
      echo "Patched version for $pkg to $PYPI_VER"
    done
}


update_flet_wheel_deps() {
  uv run "$SCRIPTS/update_flet_wheel_deps.py" "$@"
}

repackage_wheel_with_tag() {
  uv run "$SCRIPTS/repackage_wheel_with_tag.py" "$@"
}

patch_toml_versions() {
  uv run "$SCRIPTS/patch_toml_versions.py" "$@"
}

patch_toml_package_name() {
  uv run "$SCRIPTS/patch_toml_package_name.py" "$@"
}

patch_pubspec_version() {
  uv run "$SCRIPTS/patch_pubspec_version.py" "$@"
}

get_pyproject_version() {
  uv run "$SCRIPTS/get_pyproject_version.py" "$@"
}

compute_build_versions() {
  local RUN_OFFSET="${RUN_OFFSET:-0}"
  : "${GITHUB_RUN_NUMBER:=0}"

  local VERSION PKG_VER BUILD_VER PYPI_VER

  _emit() {
    # $1..$4: VERSION PKG_VER BUILD_VER PYPI_VER
    export VERSION="$1" PKG_VER="$2" BUILD_VER="$3" PYPI_VER="$4"

    {
      echo "VERSION=$VERSION"
      echo "PKG_VER=$PKG_VER"
      echo "BUILD_VER=$BUILD_VER"
      echo "PYPI_VER=$PYPI_VER"
    } >> "$GITHUB_ENV"

    {
      echo "VERSION=$VERSION"
      echo "PKG_VER=$PKG_VER"
      echo "BUILD_VER=$BUILD_VER"
      echo "PYPI_VER=$PYPI_VER"
    } | tee -a "$GITHUB_OUTPUT"
  }

  _next_dev_from() {
    # $1: base version (e.g., 1.2.3) → outputs "PKG_VER BUILD_VER PYPI_VER"
    local base="$1"
    local major minor
    major="${base%%.*}"
    minor="${base#*.}"; minor="${minor%%.*}"
    minor=$((minor + 1))
    local pkg="${major}.${minor}.0"
    local build="${pkg}+$((GITHUB_RUN_NUMBER + RUN_OFFSET))"
    local pypi="${build/+/.dev}"
    printf '%s %s %s' "$pkg" "$build" "$pypi"
  }

  # ---------------- pyproject flow ----------------
  if [[ -n "${1-}" ]]; then
    local arg="$1" pyproject
    if [[ "$arg" == */* || "$arg" == *.toml ]]; then
      pyproject="$arg"
    else
      pyproject="${SDK_PYTHON}/packages/${arg}/pyproject.toml"
    fi

    VERSION="$(uv run "$SCRIPTS/get_pyproject_version.py" "$pyproject")"
    read -r PKG_VER BUILD_VER PYPI_VER < <(_next_dev_from "$VERSION")
    _emit "$VERSION" "$PKG_VER" "$BUILD_VER" "$PYPI_VER"
    return
  fi

  # ---------------- git/tag flow ----------------
  if [[ "${GITHUB_REF:-}" == refs/tags/* ]]; then
    VERSION="${GITHUB_REF#refs/tags/}"; VERSION="${VERSION#v}"
    PKG_VER="$VERSION"
    BUILD_VER="$PKG_VER"
    PYPI_VER="${BUILD_VER/+/.dev}"
    _emit "$VERSION" "$PKG_VER" "$BUILD_VER" "$PYPI_VER"
    return
  fi

  # Untagged: base = latest tag (or 0.0.0), then next-dev
  local cv
  cv="$(git describe --abbrev=0 2>/dev/null || echo "v0.0.0")"
  VERSION="${cv#v}"
  read -r PKG_VER BUILD_VER PYPI_VER < <(_next_dev_from "$VERSION")
  _emit "$VERSION" "$PKG_VER" "$BUILD_VER" "$PYPI_VER"
}
