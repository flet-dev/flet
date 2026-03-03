#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import re
import sys
import tomllib


PACKAGE_DIR = Path(__file__).resolve().parents[1] / "packages"
NAME_RE = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)(.*)$")


def iter_metadata_dependencies(data: dict) -> list[str]:
    project = data.get("project", {})
    deps = list(project.get("dependencies", []) or [])
    optional = project.get("optional-dependencies", {}) or {}
    for entries in optional.values():
        deps.extend(entries or [])
    return deps


def parse_name_and_spec(requirement: str) -> tuple[str, str] | None:
    requirement = requirement.split(";", 1)[0].strip()
    if not requirement:
        return None
    match = NAME_RE.match(requirement)
    if not match:
        return None
    name = match.group(1).lower()
    spec = match.group(2).strip().replace(" ", "")
    return name, spec


def main() -> int:
    errors: list[str] = []
    for pyproject in sorted(PACKAGE_DIR.glob("*/pyproject.toml")):
        data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
        project = data.get("project", {})
        project_name = str(project.get("name", "")).lower()
        version = str(project.get("version", "")).strip()
        if not project_name.startswith("flet"):
            continue
        expected = f"=={version}"

        for dep in iter_metadata_dependencies(data):
            parsed = parse_name_and_spec(dep)
            if not parsed:
                continue
            dep_name, dep_spec = parsed
            if not dep_name.startswith("flet"):
                continue
            if dep_name == project_name:
                continue
            if dep_spec != expected:
                errors.append(
                    f"{pyproject}: dependency '{dep}' must be pinned as "
                    f"'{dep_name} {expected}'"
                )

    if errors:
        print("Found non-pinned internal flet dependencies:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print("All internal flet dependencies are pinned to package versions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
