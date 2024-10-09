#!/bin/bash

wheel=${1:?}
new_tag=${2:?}

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