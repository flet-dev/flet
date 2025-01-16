export root=$APPVEYOR_BUILD_FOLDER
export flet_sdk_root=$root/sdk/python
echo "flet_sdk_root: $flet_sdk_root"

python --version
pip install --upgrade setuptools wheel twine tomlkit
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"

function patch_python_package_versions() {
    PYPI_VER="${APPVEYOR_BUILD_VERSION/+/.dev}"
    sed -i -e "s/version = \"\"/version = \"$PYPI_VER\"/g" $flet_sdk_root/packages/flet/src/flet/version.py
    sed -i -e "s/version = \"\"/version = \"$PYPI_VER\"/g" $flet_sdk_root/packages/flet-cli/src/flet_cli/version.py
    sed -i -e "s/version = \"\"/version = \"$PYPI_VER\"/g" $flet_sdk_root/packages/flet-desktop/src/flet_desktop/version.py
    sed -i -e "s/version = \"\"/version = \"$PYPI_VER\"/g" $flet_sdk_root/packages/flet-web/src/flet_web/version.py
    python3 $root/ci/patch_toml_versions.py $flet_sdk_root/packages/flet/pyproject.toml $PYPI_VER
    python3 $root/ci/patch_toml_versions.py $flet_sdk_root/packages/flet-cli/pyproject.toml $PYPI_VER
    python3 $root/ci/patch_toml_versions.py $flet_sdk_root/packages/flet-desktop/pyproject.toml $PYPI_VER
    python3 $root/ci/patch_toml_versions.py $flet_sdk_root/packages/flet-web/pyproject.toml $PYPI_VER
}

function patch_flet_desktop_package_name() {
    python3 $root/ci/patch_toml_package_name.py $flet_sdk_root/packages/flet-desktop/pyproject.toml $1
}

function publish_to_pypi() {
    if [[ ("$APPVEYOR_REPO_BRANCH" == "main" || "$APPVEYOR_REPO_TAG_NAME" != "") && "$APPVEYOR_PULL_REQUEST_NUMBER" == "" ]]; then
        twine upload "$@"
    elif [[ "$APPVEYOR_PULL_REQUEST_NUMBER" == "" ]]; then
        for wheel in "$@"; do
            curl -F package=@$wheel https://$GEMFURY_TOKEN@push.fury.io/flet/
        done
    fi
}