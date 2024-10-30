import os
import re
import sys
import tempfile
from pathlib import Path

import wheel.cli.pack
import wheel.cli.unpack


# Get all wheel file paths
def find_wheel_files(directory):
    wheel_files = list(Path(directory).glob("flet-*.whl"))
    if not wheel_files:
        print("No files found matching the pattern flet-*.whl")
        return []
    return [str(wheel_file.resolve()) for wheel_file in wheel_files]


# Extract version from the wheel file name
def extract_version(wheel_file):
    match = re.search(r".*-([0-9]+[^-]+)-.*", wheel_file)
    if match:
        return match.group(1)
    return None


# Process the METADATA file
def update_metadata(metadata_file, version):
    with open(metadata_file, "r") as file:
        lines = file.readlines()

        i = 0
        while i < len(lines):
            # insert Requires-Dist: flet-desktop-light ...
            if lines[i].startswith("Requires-Dist: flet-desktop "):
                lines.insert(
                    i + 1,
                    f'Requires-Dist: flet-desktop-light (=={version}) ; platform_system == "Linux" and (extra == "all" or extra == "desktop")\n',
                )
            lines[i] = re.sub(
                r'platform_system != "desktop-light"',
                "(platform_system == 'Darwin' or platform_system == 'Windows') and 'embedded' not in platform_version",
                lines[i],
            )
            lines[i] = re.sub(
                r'platform_system != "embedded"',
                "(platform_system == 'Darwin' or platform_system == 'Linux' or platform_system == 'Windows') and 'embedded' not in platform_version",
                lines[i],
            )
            i += 1

    with open(metadata_file, "w") as file:
        file.writelines(lines)


# Main logic
def process_wheels(directory):
    # Find all wheel files
    wheel_files = find_wheel_files(directory)
    if not wheel_files:
        return

    for wheel_file in wheel_files:
        print(f"Found file: {wheel_file}")

        # Extract version from the wheel file name
        version = extract_version(wheel_file)
        if not version:
            print(f"Unable to extract version from wheel file: {wheel_file}")
            continue

        print(f"Version: {version}")

        # Create a temporary directory
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Unpack the wheel file
            wheel.cli.unpack.unpack(wheel_file, tmp_dir)

            # Get the unpacked wheel directory
            unpacked_wheel_dir = next(Path(tmp_dir).glob("flet-*")).resolve()
            print(f"Wheel temp dir: {unpacked_wheel_dir}")

            # Process the METADATA file
            metadata_files = list(unpacked_wheel_dir.glob("*.dist-info/METADATA"))
            for metadata_file in metadata_files:
                update_metadata(metadata_file, version)
                print(f"Updated METADATA file: {metadata_file}")

            # Remove the old wheel file
            os.remove(wheel_file)

            # Repack the wheel
            wheel.cli.pack.pack(unpacked_wheel_dir, os.path.dirname(wheel_file), None)

    print("Successfully updated flet-*.whl with platform-specific dependencies.")


if len(sys.argv) < 2:
    print("Specify path to dist")
    sys.exit(1)

process_wheels(sys.argv[1])
