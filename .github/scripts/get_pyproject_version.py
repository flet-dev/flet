# /// script
# dependencies = ["tomlkit"]
# ///

"""
Reads a pyproject.toml file and prints the project's version (according to PEP 621).

Usage:
    uv run get_pyproject_version.py <pyproject.toml>

Exit codes:
    0  success
    1  usage error or file missing or version not found
"""

import sys
from pathlib import Path

import tomlkit


def get_version(toml_data) -> str:
    v = toml_data["project"]["version"]
    return v.strip()


def main() -> None:
    if len(sys.argv) != 2:
        print(
            "Usage: uv run get_pyproject_version.py <pyproject.toml>", file=sys.stderr
        )
        sys.exit(1)

    toml_path = Path(sys.argv[1]).resolve()
    if not toml_path.exists():
        print(f"Error: File not found: {toml_path}", file=sys.stderr)
        sys.exit(1)

    with toml_path.open(encoding="utf-8") as f:
        data = tomlkit.parse(f.read())

    version = get_version(data)

    # Print only the version, suitable for command substitution
    print(version)


if __name__ == "__main__":
    main()
