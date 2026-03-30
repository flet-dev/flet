"""Convert a pyproject.toml file to a requirements.txt file."""

# Based on: https://pypi.org/project/toml-to-requirements/

import re
from typing import Any, Optional

from packaging.requirements import Requirement


def _windows_safe(req_str: str) -> str:
    """Insert a space before bare ``<`` or ``>`` so Windows cmd.exe does not
    interpret them as shell redirection when the string is passed via ``-r``
    to a ``.BAT`` subprocess."""
    return re.sub(r"(?<=[^ ])([<>])", r" \1", req_str)


def _poetry_version_to_pep440(version: str) -> str:
    """Convert a Poetry version constraint to PEP 440 syntax.

    - ``^1.2.3`` → ``>=1.2.3``
    - ``~1.2.3`` → ``~=1.2.3``  (``~=`` passes through unchanged)
    - ``*``      → ``""`` (no constraint)
    - ``1.2.3`` (bare version) → ``==1.2.3``
    - Anything else is returned as-is (already PEP 440).
    """
    version = version.replace(" ", "")
    if not version or version == "*":
        return ""
    if version.startswith("^"):
        return f">={version[1:]}"
    if version.startswith("~") and not version.startswith("~="):
        return f"~={version[1:]}"
    # Bare version number → pin with ==
    if version[0].isdigit():
        return f"=={version}"
    return version


def _poetry_dep_to_pep508(name: str, value: Any) -> str:
    """Convert a single Poetry dependency entry to a PEP 508 requirement string."""
    suffix = ""

    if isinstance(value, dict):
        version = value.get("version")
        if version:
            specifier = _poetry_version_to_pep440(version)
            markers = value.get("markers")
            if markers is not None:
                suffix = f"; {markers}"
            if specifier:
                return f"{name}{specifier}{suffix}"
            return f"{name}{suffix}"

        git_url = value.get("git")
        if git_url:
            url = f"git+{git_url}" if not git_url.startswith("git@") else git_url
            rev = value.get("branch") or value.get("rev") or value.get("tag")
            if rev:
                url = f"{url}@{rev}"
            subdirectory = value.get("subdirectory")
            if subdirectory:
                url = f"{url}#subdirectory={subdirectory}"
            markers = value.get("markers")
            if markers is not None:
                suffix = f"; {markers}"
            return f"{name} @ {url}{suffix}"

        path = value.get("path")
        if path:
            return path

        url = value.get("url")
        if url:
            return url

        raise ValueError(f"Unsupported dependency specification: {name} = {value}")

    # String value
    specifier = _poetry_version_to_pep440(value)
    if specifier:
        return f"{name}{specifier}"
    return name


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

    dependencies: set[str] = {
        _windows_safe(_poetry_dep_to_pep508(dep, ver))
        for dep, ver in poetry_dependencies.items()
        if dep != "python"
    }

    return sorted(dependencies)


def get_project_dependencies(
    project_dependencies: Optional[list[str]] = None,
) -> Optional[list[str]]:
    """
    Normalize PEP 621 ``project.dependencies`` into a sorted unique list.

    Args:
        project_dependencies: Value from ``project.dependencies``.

    Returns:
        Sorted dependency strings, or ``None`` when input is ``None``.
    """
    if project_dependencies is None:
        return None

    dependencies: set[str] = set()
    for dep in project_dependencies:
        try:
            req = Requirement(dep)
            dependencies.add(_windows_safe(str(req)))
        except Exception:
            dependencies.add(_windows_safe(dep))

    return sorted(dependencies)
