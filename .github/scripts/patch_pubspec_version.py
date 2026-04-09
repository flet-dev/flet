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
    # Pin to a version:
    uv run patch_pubspec_version.py <pubspec> <version> [--dependencies-only] [--exact]

    # Pin to a git commit:
    uv run patch_pubspec_version.py <pubspec> --dependencies-only \
        --git-ref <sha> --git-url <url> --git-path <path>

Arguments:
    pubspec                 Path to the pubspec.yaml file to patch.
    version                 Version string to set (not required with --git-ref).
    --dependencies-only     Patch only dependencies without changing package `version:`.
    --exact                 Pin to exact version (no ^ caret). Use for apps/templates.
    --git-ref               Pin flet dependency to a git commit SHA.
    --git-url               Git repository URL (used with --git-ref).
    --git-path              Path within the git repo (used with --git-ref).
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
    parser.add_argument("version", nargs="?", default=None, help="Version string to apply")
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
    parser.add_argument(
        "--git-ref",
        help="Pin flet dependency to a git commit SHA.",
    )
    parser.add_argument(
        "--git-url",
        help="Git repository URL (used with --git-ref).",
    )
    parser.add_argument(
        "--git-path",
        help="Path within the git repo (used with --git-ref).",
    )
    args = parser.parse_args()

    if not args.git_ref and not args.version:
        parser.error("either version or --git-ref is required")

    pubspec_path = Path(args.pubspec).resolve()

    if not pubspec_path.exists():
        print(f"Error: File not found: {pubspec_path}")
        sys.exit(1)

    with pubspec_path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if args.git_ref:
        # Pin flet to a git commit
        def make_git_dep():
            d = {"git": {"url": args.git_url, "ref": args.git_ref}}
            if args.git_path:
                d["git"]["path"] = args.git_path
            return d

        print(f"Patching {pubspec_path} with git ref {args.git_ref[:12]}")

        for dep in ["flet"]:
            if dep in data.get("dependencies", {}):
                data["dependencies"][dep] = make_git_dep()
            if dep in data.get("dependency_overrides", {}):
                data["dependency_overrides"][dep] = make_git_dep()
    else:
        version = args.version
        print(f"Patching {pubspec_path} with version {version}")

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

    print(f"Successfully patched {pubspec_path}")


if __name__ == "__main__":
    main()
