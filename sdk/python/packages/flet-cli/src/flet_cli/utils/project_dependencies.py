"""Convert a pyproject.toml file to a requirements.txt file."""

# Based on: https://pypi.org/project/toml-to-requirements/

from typing import Any, Optional


def get_poetry_dependencies(
    poetry_dependencies: Optional[dict[str, Any]] = None,
) -> Optional[list[str]]:
    """
    Convert Poetry dependency declarations into pip-style requirement strings.

    Args:
        poetry_dependencies: Value from `tool.poetry.dependencies`.

    Returns:
        Sorted requirement strings or `None` when `poetry_dependencies` is `None`.
    """

    if poetry_dependencies is None:
        return None

    def format_dependency_version(dependency_name: str, dependency_value: Any):
        """
        Format a single Poetry dependency entry as a requirement specifier.

        Supports version constraints, git dependencies (including branch/rev/tag
        and subdirectory), path/url dependencies, and optional environment markers.

        Args:
            dependency_name: Dependency key in Poetry configuration.
            dependency_value: String or mapping that describes the dependency.

        Returns:
            A requirement string consumable by pip-style tooling.

        Raises:
            ValueError: If the dependency mapping uses an unsupported shape.
        """

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
                            raise ValueError(
                                "Unsupported dependency specification: "
                                f"{dependency_name} = {dependency_value}"
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
    """
    Normalize PEP 621 `project.dependencies` into a sorted unique list.

    Args:
        project_dependencies: Value from `project.dependencies`.

    Returns:
        Sorted dependency strings, or `None` when input is `None`.
    """

    if project_dependencies is None:
        return None

    dependencies = set(project_dependencies)

    return sorted(dependencies)
