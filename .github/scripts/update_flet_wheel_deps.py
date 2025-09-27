# /// script
# dependencies = ["wheel"]
# ///

"""
This script scans a given directory for wheel files matching `flet-*.whl`,
unpacks them, modifies their `METADATA`, and repacks them in place.

Modifications applied:
    1. **Insert extra dependency**
        After any line starting with:
            Requires-Dist: flet-desktop==<version>
        insert:
            Requires-Dist: flet-desktop-light==<version>; platform_system == "Linux" and (extra == "all" or extra == "desktop")

    2. **Rewrite legacy markers**
        - Replace:
            platform_system != "desktop-light"
        with:
            (platform_system == 'Darwin' or platform_system == 'Windows') and 'embedded' not in platform_version

        - Replace:
            platform_system != "embedded"
        with:
            (platform_system == 'Darwin' or platform_system == 'Linux' or platform_system == 'Windows') and 'embedded' not in platform_version

Usage:
    uv run update_flet_wheel_deps.py <dist_dir>

Arguments:
    dist_dir    Path to a directory containing wheel files named like `flet-*.whl`.
"""

import os
import re
import sys
import tempfile
from pathlib import Path

import wheel.cli.pack
import wheel.cli.unpack


def find_wheel_files(directory: Path) -> list[Path]:
    """Return resolved paths to all wheel files matching `flet-*.whl` in `directory`."""
    wheels = sorted(directory.glob("flet-*.whl"))
    if not wheels:
        print(f"No files found matching the pattern flet-*.whl in {directory}")
        return []
    return [w.resolve() for w in wheels]


def extract_version_from_filename(wheel_file: Path) -> str | None:
    """
    Extract the version string from a wheel file name like flet-1.2.3-py3-none-any.whl.
    """
    match = re.search(r".*-([0-9]+[^-]+)-.*", wheel_file.name)
    return match.group(1) if match else None


def update_metadata(metadata_file: Path, version: str) -> None:
    """Patch the wheel's METADATA file in place with the required modifications."""
    lines = metadata_file.read_text(encoding="utf-8").splitlines(keepends=True)
    out: list[str] = []

    for line in lines:
        out.append(line)
        if line.startswith("Requires-Dist: flet-desktop=="):
            out.append(
                f'Requires-Dist: flet-desktop-light=={version}; platform_system == "Linux" and (extra == "all" or extra == "desktop")\n'
            )

    # Rewrite markers
    for i, line in enumerate(out):
        line = re.sub(
            r'platform_system\s*!=\s*"desktop-light"',
            "(platform_system == 'Darwin' or platform_system == 'Windows') and 'embedded' not in platform_version",
            line,
        )
        line = re.sub(
            r'platform_system\s*!=\s*"embedded"',
            "(platform_system == 'Darwin' or platform_system == 'Linux' or platform_system == 'Windows') and 'embedded' not in platform_version",
            line,
        )
        out[i] = line

    metadata_file.write_text("".join(out), encoding="utf-8")


def process_wheels(dist_dir: Path) -> None:
    """Find, patch, and repack all matching wheels in `dist_dir`."""
    wheel_files = find_wheel_files(dist_dir)
    if not wheel_files:
        return

    for wheel_file in wheel_files:
        print(f"Found file: {wheel_file}")
        version = extract_version_from_filename(wheel_file)
        if not version:
            print(f"Unable to extract version from {wheel_file.name}")
            continue
        print(f"Version: {version}")

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            wheel.cli.unpack.unpack(str(wheel_file), tmp_dir)
            unpacked_wheel_dir = next(Path(tmp_dir).glob("flet-*")).resolve()
            print(f"Wheel temp dir: {unpacked_wheel_dir}")

            for metadata_file in unpacked_wheel_dir.glob("*.dist-info/METADATA"):
                update_metadata(metadata_file, version)
                print(f"Updated METADATA: {metadata_file}")

            os.remove(wheel_file)
            wheel.cli.pack.pack(str(unpacked_wheel_dir), str(wheel_file.parent), None)

    print("Successfully updated flet-*.whl with platform-specific dependencies.")


def main() -> None:
    if not (len(sys.argv) >= 2):
        print("Usage: uv run update_flet_wheel_deps.py <dist_dir>")
        sys.exit(1)

    dist_dir = Path(sys.argv[1]).resolve()
    if not dist_dir.is_dir():
        print(f"Error: not a directory: {dist_dir}")
        sys.exit(1)

    process_wheels(dist_dir)


if __name__ == "__main__":
    main()
