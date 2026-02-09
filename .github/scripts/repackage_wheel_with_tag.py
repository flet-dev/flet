# /// script
# requires-python = ">3.10"
# dependencies = ["wheel"]
# ///

"""
Unpacks a wheel file, modifies its `.dist-info/WHEEL` metadata to set a new
tag, and repacks it in place.

The original wheel is not deleted, but a new wheel with the modified metadata
is written alongside it.

Typical use case: adjusting a wheel's supported tags (e.g. from "py3-none-any"
to platform-specific tags).

Steps:
    1. Unpack the given wheel into a temporary directory.
    2. Rewrite the `Tag:` lines in `*.dist-info/WHEEL`.
    3. Repack the wheel into the same directory as the original.

Usage:
    uv run repackage_wheel_with_tag.py <wheel_file> <new_tag>

Arguments:
    wheel_file   Path to the `.whl` file.
    new_tag      Comma-separated list of tags (e.g., "cp310-cp310-manylinux_x86_64,cp310-cp310-win_amd64").
"""

import sys
import tempfile
from pathlib import Path

import wheel._commands.pack
import wheel._commands.unpack


def repackage_wheel(wheel_path: str, new_tag: str) -> None:
    wheel_path = Path(wheel_path).resolve()
    print(f"Re-packaging wheel {wheel_path} with tag(s): {new_tag}")

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
        tmp_dir_path = Path(tmp_dir)

        # Unpack the wheel file
        wheel._commands.unpack.unpack(str(wheel_path), tmp_dir)

        # Find the unpacked wheel directory
        wheel_dirs = list(tmp_dir_path.glob("flet_*"))
        if not wheel_dirs:
            raise FileNotFoundError("Unpacked wheel directory not found.")
        wheel_dir = wheel_dirs[0].resolve()
        print(f"Wheel temp dir: {wheel_dir}")

        # Update WHEEL metadata file(s)
        for metadata_file in wheel_dir.glob("*.dist-info/WHEEL"):
            content = metadata_file.read_text(encoding="utf-8")
            new_content = content.replace(
                "Tag: py3-none-any",
                "\n".join([f"Tag: {t}" for t in new_tag.split(",")]),
            )
            metadata_file.write_text(new_content, encoding="utf-8")
            print(f"Updated tags in {metadata_file}:\n{new_content}")

        # Repack the wheel
        wheel._commands.pack.pack(str(wheel_dir), str(wheel_path.parent), None)

    print(f"Successfully generated wheel with new tag(s): {new_tag}")


def main() -> None:
    if not (len(sys.argv) >= 3):
        print("Usage: uv run repackage_wheel_with_tag.py <wheel_file> <new_tag>")
        sys.exit(1)

    wheel_file, new_tag = sys.argv[1], sys.argv[2]
    repackage_wheel(wheel_file, new_tag)


if __name__ == "__main__":
    main()
