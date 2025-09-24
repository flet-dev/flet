function patch_python_package_versions() {
    cd "$SDK_PYTHON_PATH" || exit 1
    sed -i -e "s/version = \"\"/version = \"$PYPI_VER\"/g" packages/flet/src/flet/version.py
    sed -i -e "s/version = \"\"/version = \"$PYPI_VER\"/g" packages/flet-cli/src/flet_cli/version.py
    sed -i -e "s/version = \"\"/version = \"$PYPI_VER\"/g" packages/flet-desktop/src/flet_desktop/version.py
    sed -i -e "s/version = \"\"/version = \"$PYPI_VER\"/g" packages/flet-web/src/flet_web/version.py

    uv run --no-dev || true
    uv version --package flet $PYPI_VER
    uv version --package flet-cli $PYPI_VER
    uv version --package flet-desktop $PYPI_VER
    uv version --package flet-web $PYPI_VER
}

function patch_flet_desktop_package_name() {
    uv run $ROOT/ci/patch_toml_package_name.py $SDK_PYTHON_PATH/packages/flet-desktop/pyproject.toml $1
}

function publish_to_pypi() {
    # If not a PR:
    if [[ ${GITHUB_EVENT_NAME:-} != "pull_request" ]]; then
        if [[ ${GITHUB_REF_NAME:-} == "main" || ${GITHUB_REF_TYPE:-} == "tag" ]]; then
            # On main branch or a tag -> upload to PyPI
            uvx twine upload "$@"
        else
            # Otherwise -> upload to Gemfury
            for wheel in "$@"; do
                curl -F package=@$wheel "https://${GEMFURY_TOKEN}@push.fury.io/flet/"
            done
        fi
    fi
}
