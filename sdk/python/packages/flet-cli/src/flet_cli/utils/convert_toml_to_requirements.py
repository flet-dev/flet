"""Convert a pyproject.toml file to a requirements.txt file."""

# Based on: https://pypi.org/project/toml-to-requirements/

from __future__ import annotations

from typing import Any


def _convert_poetry_to_requirements(
    parsed_toml_file: dict[str, Any],
    *,
    optional_lists: list[str] | None,
) -> list[str]:
    project: dict | None = parsed_toml_file.get("tool", {}).get("poetry")

    if project is None:
        raise RuntimeError(
            "The project section is missing from the TOML file. Exiting..."
        )

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
        for dependency, version in project.get("dependencies", {}).items()
        if dependency != "python"
    }

    if optional_lists is not None:
        groups: dict[str, Any] = project.get("group", {})

        for optional_list_to_include in optional_lists:
            if optional_list_to_include not in groups:
                continue

            group: dict[str, Any] = groups[optional_list_to_include]

            optional_dependencies: set[str] = {
                format_dependency_version(dependency, version)
                for dependency, version in group.get("dependencies", {}).items()
            }

            dependencies.update(optional_dependencies)

    return sorted(dependencies)


def _convert_setuptools_to_requirements(
    parsed_toml_file: dict[str, Any],
    *,
    optional_lists: list[str] | None,
) -> list[str]:
    project: dict | None = parsed_toml_file.get("project")

    if project is None:
        raise RuntimeError(
            "The project section is missing from the TOML file. Exiting..."
        )

    dependencies = set(project.get("dependencies", []))

    if optional_lists is not None:
        optional_dependency_list: dict[str, Any] = project.get(
            "optional-dependencies", {}
        )
        optional_lists_to_include: set[str] = (
            set(optional_lists) if optional_lists is not None else set()
        )

        for optional_list, deps in optional_dependency_list.items():
            if optional_list in optional_lists_to_include:
                dependencies.update(deps)

    return sorted(dependencies)


def convert_toml_to_requirements(
    parsed_toml_file: dict[str, Any], *, optional_lists: list[str] | None
) -> list[str]:
    """Convert a pyproject.toml file to a requirements.txt file.

    Args:
        parsed_toml_file: Parsed contents of the pyproject.toml file.
        optional_lists: A list of optional dependency lists to include.
        poetry: Whether to use poetry instead of setuptools.

    Returns:
        The contents of the requirements.txt file.

    Raises:
        RuntimeError: If poetry is set to True since it is not yet supported.
    """
    if parsed_toml_file.get("tool", {}).get("poetry"):
        return _convert_poetry_to_requirements(
            parsed_toml_file, optional_lists=optional_lists
        )

    return _convert_setuptools_to_requirements(
        parsed_toml_file,
        optional_lists=optional_lists,
    )
