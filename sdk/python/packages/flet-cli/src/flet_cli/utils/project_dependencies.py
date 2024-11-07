"""Convert a pyproject.toml file to a requirements.txt file."""

# Based on: https://pypi.org/project/toml-to-requirements/

from __future__ import annotations

from typing import Any, Optional


def get_poetry_dependencies(
    poetry_dependencies: Optional[dict[str, Any]] = None,
) -> Optional[list[str]]:

    if poetry_dependencies is None:
        return None

    def format_dependency_version(dependency: str, version_value: Any):
        suffix = ""
        if isinstance(version_value, dict):
            version = version_value["version"]
            if version_value["markers"]:
                suffix = f";{version_value['markers']}"
        else:
            version = version_value

        sep = "=="
        if version.startswith("^"):
            sep = ">="
            version = version[1:]
        elif version.startswith("~"):
            sep = "~="
            version = version[1:]
            return f"{dependency}~={version[1:]}"
        elif "<" in version or ">" in version:
            sep = ""
            version = version.replace(" ", "")

        return f"{dependency}{sep}{version}{suffix}"

    dependencies: set[str] = {
        format_dependency_version(dependency, version)
        for dependency, version in poetry_dependencies.items()
        if dependency != "python"
    }

    return sorted(dependencies)


def get_project_dependencies(
    project_dependencies: Optional[dict[str, Any]] = None,
) -> Optional[list[str]]:

    if project_dependencies is None:
        return None

    dependencies = set(project_dependencies)

    return sorted(dependencies)
