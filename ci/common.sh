export root=$APPVEYOR_BUILD_FOLDER
export flet_sdk_root=$root/sdk/python
echo "flet_sdk_root: $flet_sdk_root"

python --version
pip install --upgrade setuptools wheel twine poetry tomlkit virtualenv

function patch_python_package_versions() {
    PYPI_VER="${APPVEYOR_BUILD_VERSION/+/.dev}"
    sed -i -e "s/version = \"\"/version = \"$PYPI_VER\"/g" $flet_sdk_root/packages/flet-core/src/flet_core/version.py
    python3 $root/ci/patch_toml_versions.py $flet_sdk_root/packages/flet/pyproject.toml $PYPI_VER
    python3 $root/ci/patch_toml_versions.py $flet_sdk_root/packages/flet-cli/pyproject.toml $PYPI_VER
    python3 $root/ci/patch_toml_versions.py $flet_sdk_root/packages/flet-core/pyproject.toml $PYPI_VER
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

function repackage_wheel_with_tag() {
    wheel=$1
    new_tag=$2

    echo "Re-packaging wheel $wheel_path with $new_tag"

    # Define temporary directory and file
    tmp_dir=$(mktemp -d)

    # Unpack the wheel file
    python -m wheel unpack --dest $tmp_dir $wheel

    # get unpacked wheel dir
    wheel_dir=$(realpath $(find $tmp_dir -maxdepth 1 -name "flet-*"))
    echo "wheel temp dir: $wheel_dir"

    pushd $wheel_dir

    # process metadata
    for metadata_file in *.dist-info/WHEEL; do
        # Replace tag in WHEEL
        sed -i "s/Tag: py3-none-any/Tag: $new_tag/g" "$metadata_file"
        cat $metadata_file
    done

    # Repack the wheel
    python -m wheel pack --dest-dir $(dirname $wheel) .

    # Cleanup temporary directory
    popd
    rm -rf "$tmp_dir"

    echo "Successfully generated $wheel with $new_tag tag."
}