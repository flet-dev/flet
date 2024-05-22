#!/bin/bash

# find wheel
wheel=$(realpath $(find $1 -maxdepth 1 -name "flet-*.whl"))

# Check if a file was found
if [ -z "$wheel" ]; then
  echo "No file found matching the pattern flet-*.whl"
else
  echo "Found file: $wheel"
fi

version=$(echo "$wheel" | sed -E 's/.*-([0-9.]+).*/\1/')
echo "$version"

# Define temporary directory and file
tmp_dir=$(mktemp -d)

# Unpack the wheel file
python -m wheel unpack --dest $tmp_dir $wheel

# get unpacked wheel dir
wheel_dir=$(realpath $(find $tmp_dir -maxdepth 1 -name "flet-*"))
echo "wheel temp dir: $wheel_dir"

pushd $wheel_dir

# process metadata
for metadata_file in *.dist-info/METADATA; do
    # Replace the condition in METADATA
    sed -i "/^Requires-Dist: flet-desktop /a Requires-Dist: flet-desktop-light (==$version) ; platform_system == 'Linux'" "$metadata_file"
    sed -i "s/platform_system != \"desktop-light\"/(platform_system == 'Darwin' or platform_system == 'Windows') and 'embedded' not in platform_version/g" "$metadata_file"
    sed -i "s/platform_system != \"embedded\"/(platform_system == 'Darwin' or platform_system == 'Linux' or platform_system == 'Windows') and 'embedded' not in platform_version/g" "$metadata_file"
    cat $metadata_file
done

# Repack the wheel
rm $wheel
python -m wheel pack --dest-dir $(dirname $wheel) .

# Cleanup temporary directory
popd
rm -rf "$tmp_dir"

echo "Successfully updated flet-*.whl with platform-specific dependencies."