"""Convert a pyproject.toml file to a requirements.txt file."""

# Based on: https://pypi.org/project/toml-to-requirements/

import os
import re
import shlex
from collections.abc import Iterator
from pathlib import Path
from typing import Any, Optional

from packaging.requirements import Requirement


def _windows_safe(req_str: str) -> str:
    """Insert a space before bare `<` or `>` so Windows cmd.exe does not
    interpret them as shell redirection when the string is passed via `-r`
    to a `.BAT` subprocess."""
    return re.sub(r"(?<=[^ ])([<>])", r" \1", req_str)


def _poetry_version_to_pep440(version: str) -> str:
    """Convert a Poetry version constraint to PEP 440 syntax.

    - `^1.2.3` → `>=1.2.3`
    - `~1.2.3` → `~=1.2.3`  (`~=` passes through unchanged)
    - `*`      → `""` (no constraint)
    - `1.2.3` (bare version) → `==1.2.3`
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
    Normalize PEP 621 `project.dependencies` into a sorted unique list.

    Args:
        project_dependencies: Value from `project.dependencies`.

    Returns:
        Sorted dependency strings, or `None` when input is `None`.
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


def _requirements_includes(text: str) -> Iterator[str]:
    """Yield include paths after pip-style line and option preprocessing."""
    pending = ""
    for line in [*text.splitlines(), ""]:
        # Join before stripping comments, as pip does. Comment lines themselves
        # never continue onto the following line.
        if line.endswith("\\") and not line.lstrip().startswith("#"):
            pending += line[:-1]
            continue
        line, pending = pending + line, ""
        line = re.sub(r"(^|\s+)#.*$", "", line).strip()
        if not line.startswith("-"):
            continue
        line = re.sub(
            r"\$\{([A-Z0-9_]+)\}",
            lambda match: os.environ.get(match[1]) or match[0],
            line,
        )
        try:
            options = iter(shlex.split(line))
        except ValueError:
            # Leave malformed options for pip to report during installation.
            continue
        for option in options:
            if option in ("-r", "--requirement", "-c", "--constraint"):
                include = next(options, "")
            elif option.startswith(("--requirement=", "--constraint=")):
                include = option.partition("=")[2]
            elif option.startswith(("-r", "-c")):
                include = option[2:]
            else:
                continue
            if include:
                yield include


def read_requirements_file_text(path: Path) -> str:
    """
    Return the text of a `requirements.txt` file and of the files it includes.

    Files included with `-r`/`--requirement` or `-c`/`--constraint` are read
    too, relative to the file that includes them, so a change to any of them
    changes the result. Includes support quoted paths, line continuations and
    pip's `${NAME}` environment variables. URLs and missing files are skipped.

    Args:
        path: The path of the `requirements.txt` file.

    Returns:
        The concatenated text of the file and of the files it includes.
    """

    parts: list[str] = []
    visited: set[Path] = set()

    def read(file: Path) -> None:
        resolved = file.resolve()
        if resolved in visited or not file.is_file():
            return
        visited.add(resolved)
        text = file.read_text(encoding="utf-8", errors="replace")
        parts.append(text)
        for include in _requirements_includes(text):
            if re.match(r"^[a-z][a-z0-9+.-]*://", include, re.I):
                continue
            read(file.parent / include)

    read(Path(path))
    return "".join(parts)
