# /// script
# dependencies = ["tomlkit"]
# ///

"""
Patchs a TOML file (e.g. pyproject.toml) to:
    - Set `[project].version` to a given value.
    - Update selected dependencies in `[project].dependencies` to the same version.

Dependencies patched:
    - flet-cli
    - flet-desktop
    - flet-web
    - flet

Usage:
    uv run patch_toml_versions.py <toml_file> <version>
"""

import sys
from pathlib import Path

import tomlkit


def patch_dependency(deps: list[str], dep_name: str, version: str) -> None:
    """Pin a dependency in-place to the given version if it matches dep_name."""
    for i, dep in enumerate(deps):
        if dep == dep_name:
            deps[i] = f"{dep_name}=={version}"
        elif dep.startswith(f"{dep_name};"):
            deps[i] = dep.replace(f"{dep_name};", f"{dep_name}=={version};")


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
    deps: list[str] = t["project"]["dependencies"]
    for name in ["flet-cli", "flet-desktop", "flet-web", "flet"]:
        patch_dependency(deps, name, version)

    # save
    with toml_path.open("w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(t))

    print(f"Successfully patched TOML file {toml_path} to version {version}")


if __name__ == "__main__":
    main()
