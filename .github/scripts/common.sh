patch_python_package_versions() {
    cd "$SDK_PYTHON" || exit 1

    # Install dependencies
    uv sync --no-default-groups || true

    # Get package names from arguments
    local packages=("$@")

    # If no packages are provided, update versions for all known packages
    if [ ${#packages[@]} -eq 0 ]; then
        packages=(flet flet-cli flet-desktop flet-web)
    fi

    for pkg in "${packages[@]}"; do
        # Update version in version.py file
        sed -i -e "s/version = \"\"/version = \"$PYPI_VER\"/g" "packages/$pkg/src/${pkg//-/_}/version.py"
        # Update version in pyproject.toml file
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
