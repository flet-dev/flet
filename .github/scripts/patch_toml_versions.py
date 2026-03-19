# /// script
# dependencies = ["tomlkit"]
# ///

"""Patch TOML package versions and pin internal flet dependencies.

This script updates:
    - `[project].version`
    - Internal flet dependencies in `[project].dependencies`
    - Internal flet dependencies in `[project].optional-dependencies`

Usage:
    uv run patch_toml_versions.py <toml_file> <version>
"""

import sys
from pathlib import Path
import re

import tomlkit


INTERNAL_DEPS = {
    "flet",
    "flet-cli",
    "flet-desktop",
    "flet-web",
}
REQ_RE = re.compile(
    r"^(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)(?P<spec>[^;]*)?(?P<marker>\s*;.*)?$"
)


def patch_dependency(req: str, version: str) -> str:
    """Pin a single requirement string if it references an internal flet package."""
    m = REQ_RE.match(req.strip())
    if not m:
        return req

    name = m.group("name")
    if name not in INTERNAL_DEPS:
        return req

    marker = m.group("marker") or ""
    if marker:
        return f"{name}=={version}{marker}"
    return f"{name}=={version}"


def patch_dependency_list(deps: list[str], version: str) -> None:
    """Patch dependencies list in-place."""
    for i, dep in enumerate(deps):
        deps[i] = patch_dependency(dep, version)


def main() -> None:
    if not (len(sys.argv) >= 3):
        print("Usage: uv run patch_toml_versions.py <toml_file> <version>")
        sys.exit(1)

    toml_path = Path(sys.argv[1]).resolve()
    version = sys.argv[2]

    if not toml_path.exists():
        print(f"Error: File not found: {toml_path}")
        sys.exit(1)

    print(f"Patching TOML file {toml_path} to version {version}")

    # read
    with toml_path.open(encoding="utf-8") as f:
        t = tomlkit.parse(f.read())

    # patch version
    t["project"]["version"] = version

    # patch dependencies
    deps: list[str] = t["project"].get("dependencies", [])
    patch_dependency_list(deps, version)

    # patch optional dependencies
    optional = t["project"].get("optional-dependencies", {})
    for _, opt_deps in optional.items():
        patch_dependency_list(opt_deps, version)

    # save
    with toml_path.open("w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(t))

    print(f"Successfully patched TOML file {toml_path} to version {version}")


if __name__ == "__main__":
    main()
