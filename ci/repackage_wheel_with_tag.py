import os
import sys
import tempfile
from pathlib import Path

import wheel.cli.pack
import wheel.cli.unpack


def repackage_wheel(wheel_path, new_tag):

    wheel_path = os.path.realpath(wheel_path)
    print(f"Re-packaging wheel {wheel_path} with {new_tag}")

    # Create temporary directory
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_path = Path(tmp_dir)

        # Unpack the wheel file
        wheel.cli.unpack.unpack(wheel_path, tmp_dir)

        # Print directory structure
        for root, dirs, files in os.walk(tmp_dir):
            for name in files:
                print(os.path.join(root, name))
            for name in dirs:
                print(os.path.join(root, name))

        # Get unpacked wheel directory
        wheel_dirs = list(tmp_dir_path.glob("flet_*"))
        if not wheel_dirs:
            raise FileNotFoundError("Unpacked wheel directory not found.")
        wheel_dir = wheel_dirs[0]
        print(f"wheel temp dir: {wheel_dir}")

        # Change into the unpacked wheel directory
        os.chdir(wheel_dir)

        # Process metadata files and replace the tag
        metadata_files = list(wheel_dir.glob("*.dist-info/WHEEL"))
        for metadata_file in metadata_files:
            with open(metadata_file, "r") as f:
                content = f.read()
            new_content = content.replace(
                "Tag: py3-none-any",
                "\n".join([f"Tag: {t}" for t in new_tag.split(",")]),
            )
            with open(metadata_file, "w") as f:
                f.write(new_content)
            print(new_content)

        # Repack the wheel
        wheel.cli.pack.pack(".", str(Path(wheel_path).parent), None)

    print(f"Successfully generated {wheel_path} with {new_tag} tag.")


if len(sys.argv) < 3:
    print("Specify path to wheel and a new tag")
    sys.exit(1)

repackage_wheel(sys.argv[1], sys.argv[2])
