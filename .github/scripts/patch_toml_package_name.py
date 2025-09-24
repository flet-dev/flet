# /// script
# dependencies = ["tomlkit"]
# ///

"""
This script patches the `[project].name` field in a
TOML file (typically `pyproject.toml`).

It is intended for cases where you want to change the package name
programmatically without touching any other fields or comments in the file.

The script:
    - Loads the specified TOML file using `tomlkit` (preserves formatting and comments).
    - Replaces the value of `project.name` with the new package name provided.
    - Writes the modified TOML back to the same file.

Usage:
    uv run patch_toml_package_name.py <toml_file> <new_package_name>

Arguments:
    toml_file         Path to the TOML file to patch (e.g., pyproject.toml).
    new_package_name  The new package name to set in `[project].name`.
"""

import pathlib
import sys

import tomlkit


def main() -> None:
    if not (len(sys.argv) >= 3):
        print("Usage: uv run patch_toml_package_name.py <toml_file> <new_package_name>")
        sys.exit(1)

    toml_file, package_name = sys.argv[1], sys.argv[2]
    toml_path = pathlib.Path(toml_file).resolve()

    if not toml_path.exists():
        print(f"Error: File not found: {toml_path}")
        sys.exit(1)

    print(f"Patching TOML file {toml_path} with new package name '{package_name}'")

    # read
    with toml_path.open("r", encoding="utf-8") as f:
        t = tomlkit.parse(f.read())

    # patch name safely
    if "project" not in t:
        print("Error: No [project] section in TOML file.")
        sys.exit(1)

    t["project"]["name"] = package_name

    # save
    with toml_path.open("w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(t))

    print(
        f"Successfully patched TOML file {toml_path} with new package name '{package_name}'"
    )


if __name__ == "__main__":
    main()
