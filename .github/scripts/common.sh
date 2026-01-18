function patch_python_package_versions() (
    set -euo pipefail
    cd "$SDK_PYTHON" || exit 1

    # Install dependencies
    uv sync --no-default-groups || true

    # Update package versions in version.py and pyproject.toml files
    for pkg in flet flet-cli flet-desktop flet-web; do
      sed -i -e "s/flet_version = \"\"/flet_version = \"$PYPI_VER\"/g" packages/$pkg/src/${pkg//-/_}/version.py
      uv version --package "$pkg" "$PYPI_VER"
      echo "Patched version for $pkg to $PYPI_VER"
    done

    # Get Flutter version from .fvmrc and set it in version.py
    FLUTTER_VERSION="$( uv run "$SCRIPTS/read_fvmrc.py" "${ROOT}/.fvmrc" )"
    sed -i -e "s/flutter_version = \"\"/flutter_version = \"$FLUTTER_VERSION\"/g" packages/flet/src/flet/version.py
    echo "Patched Flutter SDK version to $FLUTTER_VERSION"
)


repackage_wheel_with_tag() {
  uv run "$SCRIPTS/repackage_wheel_with_tag.py" "$@"
}

patch_toml_versions() {
  uv run "$SCRIPTS/patch_toml_versions.py" "$@"
}

patch_pubspec_version() {
  uv run "$SCRIPTS/patch_pubspec_version.py" "$@"
}
