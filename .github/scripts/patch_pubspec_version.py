# /// script
# dependencies = ["pyyaml"]
# ///

"""
Patches a Dart/Flutter `pubspec.yaml` file to:
    - Optionally set the `version:` field to a given value.
    - Pin selected dependencies in `dependencies:` and `dependency_overrides:`.

Dependencies patched:
    - flet

Usage:
    uv run patch_pubspec_version.py <pubspec> <version> [--dependencies-only] [--exact]

Arguments:
    pubspec                 Path to the pubspec.yaml file to patch.
    version                 Version string to set.
    --dependencies-only     Patch only dependencies without changing package `version:`.
    --exact                 Pin to exact version (no ^ caret). Use for apps/templates.
"""

import argparse
import sys
from pathlib import Path

import yaml


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Patch pubspec version and/or selected dependencies."
    )
    parser.add_argument("pubspec", help="Path to pubspec.yaml")
    parser.add_argument("version", help="Version string to apply")
    parser.add_argument(
        "--dependencies-only",
        action="store_true",
        help="Patch only dependencies without changing package version.",
    )
    parser.add_argument(
        "--exact",
        action="store_true",
        help="Pin to exact version (no ^ caret). Use for apps/templates.",
    )
    args = parser.parse_args()

    pubspec_path = Path(args.pubspec).resolve()
    version = args.version

    if not pubspec_path.exists():
        print(f"Error: File not found: {pubspec_path}")
        sys.exit(1)

    print(f"Patching {pubspec_path} with version {version}")

    with pubspec_path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # patch version
    if not args.dependencies_only:
        data["version"] = version

    # patch dependencies and dependency_overrides
    pin = version if args.exact else f"^{version}"
    for dep in ["flet"]:
        if dep in data.get("dependencies", {}):
            data["dependencies"][dep] = pin
        if dep in data.get("dependency_overrides", {}):
            data["dependency_overrides"][dep] = pin

    with pubspec_path.open("w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False)

    print(f"Successfully patched {pubspec_path} with version {version}")


if __name__ == "__main__":
    main()
