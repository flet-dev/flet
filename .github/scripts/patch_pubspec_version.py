# /// script
# dependencies = ["pyyaml"]
# ///

"""
Patches a Dart/Flutter `pubspec.yaml` file to:
    - Set the `version:` field to a given value.
    - Pin selected dependencies in the `dependencies:` section to the same version.

Dependencies patched:
    - flet

Usage:
    uv run patch_pubspec_version.py <pubspec> <version>

Arguments:
    pubspec         Path to the pubspec.yaml file to patch.
    version         Version string to set.
"""

import sys
from pathlib import Path

import yaml


def main() -> None:
    if not (len(sys.argv) >= 3):
        print("Usage: uv run patch_pubspec_version.py <pubspec.yaml> <version>")
        sys.exit(1)

    pubspec_path = Path(sys.argv[1]).resolve()
    version = sys.argv[2]

    if not pubspec_path.exists():
        print(f"Error: File not found: {pubspec_path}")
        sys.exit(1)

    print(f"Patching {pubspec_path} with version {version}")

    with pubspec_path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # patch version
    data["version"] = version

    # patch dependencies
    for dep in ["flet"]:
        if dep in data.get("dependencies", {}):
            data["dependencies"][dep] = f"^{version}"

    with pubspec_path.open("w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False)

    print(f"Successfully patched {pubspec_path} with version {version}")


if __name__ == "__main__":
    main()
