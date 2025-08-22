export root=$GITHUB_WORKSPACE
export flet_sdk_root=$root/sdk/python
echo "flet_sdk_root: $flet_sdk_root"

# export PATH=$HOME/.local/bin:$PATH

function patch_python_package_versions() {
    sed -i -e "s/version = \"\"/version = \"$PYPI_VER\"/g" $flet_sdk_root/packages/flet/src/flet/version.py
    sed -i -e "s/version = \"\"/version = \"$PYPI_VER\"/g" $flet_sdk_root/packages/flet-cli/src/flet_cli/version.py
    sed -i -e "s/version = \"\"/version = \"$PYPI_VER\"/g" $flet_sdk_root/packages/flet-desktop/src/flet_desktop/version.py
    sed -i -e "s/version = \"\"/version = \"$PYPI_VER\"/g" $flet_sdk_root/packages/flet-web/src/flet_web/version.py

    uv run --directory $flet_sdk_root --no-dev
    uv version --package flet $PYPI_VER
    uv version --package flet-cli $PYPI_VER
    uv version --package flet-desktop $PYPI_VER
    uv version --package flet-web $PYPI_VER
}

function patch_flet_desktop_package_name() {
    uv run $root/ci/patch_toml_package_name.py $flet_sdk_root/packages/flet-desktop/pyproject.toml $1
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
