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
