"""Convert a pyproject.toml file to a requirements.txt file."""

# Based on: https://pypi.org/project/toml-to-requirements/

from __future__ import annotations

from typing import Any, Optional


def get_poetry_dependencies(
    poetry_dependencies: Optional[dict[str, Any]] = None,
) -> Optional[list[str]]:

    if poetry_dependencies is None:
        return None

    def format_dependency_version(dependency_name: str, dependency_value: Any):
        sep = "@"
        value = ""
        suffix = ""

        if isinstance(dependency_value, dict):
            version = dependency_value.get("version")
            if version:
                sep = "=="
                value = version
            else:
                git_url = dependency_value.get("git")
                if git_url:
                    value = (
                        f"git+{git_url}" if not git_url.startswith("git@") else git_url
                    )
                    rev = (
                        dependency_value.get("branch")
                        or dependency_value.get("rev")
                        or dependency_value.get("tag")
                    )
                    if rev:
                        value = f"{value}@{rev}"
                    subdirectory = dependency_value.get("subdirectory")
                    if subdirectory:
                        value = f"{value}#subdirectory={subdirectory}"
                else:
                    path = dependency_value.get("path")
                    if path:
                        value = path
                        dependency_name = ""
                        sep = ""
                    else:
                        url = dependency_value.get("url")
                        if url:
                            value = url
                            dependency_name = ""
                            sep = ""
                        else:
                            raise Exception(
                                f"Unsupported dependency specification: {dependency_name} = {dependency_value}"
                            )

            # markers - common for all
            markers = dependency_value.get("markers")
            if markers is not None:
                suffix = f";{markers}"
        else:
            value = dependency_value
            sep = "=="

        if value.startswith("^"):
            sep = ">="
            value = value[1:]
        elif value.startswith("~"):
            sep = "~="
            value = value[1:]
            return f"{dependency_name}~={value[1:]}"
        elif "<" in value or ">" in value:
            sep = ""
            value = value.replace(" ", "")

        return f"{dependency_name}{sep}{value}{suffix}"

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
