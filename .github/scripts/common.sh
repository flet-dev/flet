function patch_python_package_versions() {
    cd $SDK_PYTHON || exit 1

    # Update package versions in version.py files
    for pkg in flet flet-cli flet-desktop flet-web; do
      sed -i -e "s/version = \"\"/version = \"$PYPI_VER\"/g" packages/$pkg/src/${pkg//-/_}/version.py
    done

    uv sync --no-default-groups || true

    # Bump pyproject versions
    uv version --package flet $PYPI_VER
    uv version --package flet-cli $PYPI_VER
    uv version --package flet-desktop $PYPI_VER
    uv version --package flet-web $PYPI_VER
}
