"""Read the Python dependencies of a Flet app and pin its Flet packages."""

# Based on: https://pypi.org/project/toml-to-requirements/

import codecs
import os
import re
import shlex
from collections.abc import Iterator
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse
from urllib.request import url2pathname

from packaging.requirements import InvalidRequirement, Requirement
from packaging.specifiers import SpecifierSet
from packaging.utils import canonicalize_name

FLET_PACKAGES = frozenset(
    {
        "flet",
        "flet-ads",
        "flet-audio",
        "flet-audio-recorder",
        "flet-camera",
        "flet-charts",
        "flet-cli",
        "flet-code-editor",
        "flet-color-pickers",
        "flet-datatable2",
        "flet-desktop",
        "flet-flashlight",
        "flet-geolocator",
        "flet-local-auth",
        "flet-lottie",
        "flet-map",
        "flet-mcp",
        "flet-notifications",
        "flet-permission-handler",
        "flet-platform-assets",
        "flet-rive",
        "flet-secure-storage",
        "flet-shadcn-ui",
        "flet-spinkit",
        "flet-video",
        "flet-web",
        "flet-webview",
    }
)
"""The packages released with `flet`, at its version."""


class FletVersionConflictError(ValueError):
    """Raised when an app's requirements exclude the version of the Flet CLI."""


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


def pin_flet_dependencies(dependencies: list[str], flet_version: str) -> list[str]:
    """
    Pin `flet` and the packages released with it to the version of the Flet CLI.

    An app runs in a Flet client of the CLI's version, so its Python packages must
    have that version too. A range such as `flet>=1.0` would install the newest
    release instead. The extensions are pinned as well because each one requires
    its own version of `flet` exactly, and `micropip` can't step back to an older
    extension the way pip does.

    `flet==<flet_version>` is added when no requirement installs `flet` on every
    platform, unless an entry installs a path or URL, which may provide `flet`.

    Args:
        dependencies: The app's requirements. Pip options are kept as they are.
        flet_version: The version of the Flet CLI.

    Returns:
        The pinned requirements, or `dependencies` as they are when `flet` itself
        comes from a path or URL, such as the one `dev_packages` sets.

    Raises:
        FletVersionConflictError: If a requirement without an environment marker
            excludes `flet_version`.
    """
    requirements = [_parse_requirement(dep) for dep in dependencies]
    if any(
        _is_flet_location(dep)
        or (req is not None and canonicalize_name(req.name) == "flet" and req.url)
        for dep, req in zip(dependencies, requirements)
    ):
        return list(dependencies)

    pinned = []
    installs_flet = False
    may_install_flet = False
    for dep, req in zip(dependencies, requirements):
        if req is None:
            may_install_flet = may_install_flet or not dep.startswith("-")
        elif canonicalize_name(req.name) in FLET_PACKAGES and not req.url:
            if not req.specifier.contains(flet_version, prereleases=True):
                if req.marker is not None:
                    # It may not apply to the target, so pip decides.
                    pinned.append(dep)
                    continue
                raise FletVersionConflictError(
                    f"The app requires `{req}`, but this Flet CLI is version "
                    f"{flet_version}, and the app runs in a Flet client of that "
                    "version. Change the requirement, or use a Flet CLI version "
                    "that it allows."
                )
            req.specifier = SpecifierSet(f"=={flet_version}")
            dep = _windows_safe(str(req))
            installs_flet = installs_flet or (
                canonicalize_name(req.name) == "flet" and req.marker is None
            )
        pinned.append(dep)
    if not installs_flet and not may_install_flet:
        pinned.append(f"flet=={flet_version}")
    return pinned


def override_dependencies(dependencies: list[str], overrides: list[str]) -> list[str]:
    """
    Append `overrides` to `dependencies`, replacing requirements of the same packages.

    Args:
        dependencies: The requirements to override.
        overrides: The requirements that take precedence.

    Returns:
        The combined requirements.
    """
    names = {
        canonicalize_name(req.name)
        for req in map(_parse_requirement, overrides)
        if req is not None
    }
    kept = [
        dep
        for dep in dependencies
        if (req := _parse_requirement(dep)) is None
        or canonicalize_name(req.name) not in names
    ]
    return kept + overrides


def _parse_requirement(dep: str) -> Optional[Requirement]:
    """Parse a PEP 508 requirement, or return `None` for any other entry."""
    try:
        return Requirement(dep)
    except InvalidRequirement:
        return None


def _is_flet_location(entry: str) -> bool:
    """Whether a path or URL names `flet`: a checkout, wheel, sdist or `#egg=flet`."""
    return bool(
        re.search(
            r"[#&]egg=flet(&|$)"
            r"|[/\\]flet[/\\]?(\[[^\]]*\])?\s*([#?&;]|$)"
            r"|(^|[/\\])flet-\d[^/\\]*\.(whl|tar\.gz|zip)(\[[^\]]*\])?\s*([#?;]|$)",
            entry,
            re.IGNORECASE,
        )
    )


def _requirements_lines(text: str) -> Iterator[str]:
    """Yield the lines of a requirements file, preprocessed the way pip does."""
    pending = ""
    for line in [*text.splitlines(), ""]:
        # Join before stripping comments, as pip does. Comment lines themselves
        # never continue onto the following line.
        if line.endswith("\\") and not line.lstrip().startswith("#"):
            pending += line[:-1]
            continue
        line, pending = pending + line, ""
        line = re.sub(r"(^|\s+)#.*$", "", line).strip()
        if line:
            yield re.sub(
                r"\$\{([A-Z0-9_]+)\}",
                lambda match: os.environ.get(match[1]) or match[0],
                line,
            )


def _requirements_options(line: str) -> Iterator[tuple[str, str]]:
    """Yield the `-r`, `-c` and `-e` options of a line, as (letter, value) pairs."""
    try:
        options = iter(shlex.split(line))
    except ValueError:
        # Leave malformed options for pip to report during installation.
        return
    for option in options:
        if option in ("-r", "--requirement", "-c", "--constraint", "-e", "--editable"):
            letter, value = option.lstrip("-")[0], next(options, "")
        elif option.startswith(("--requirement=", "--constraint=", "--editable=")):
            letter, value = option[2], option.partition("=")[2]
        elif option.startswith(("-r", "-c", "-e")):
            letter, value = option[1], option[2:]
        else:
            continue
        if value:
            yield letter, value


def _is_remote_url(value: str) -> bool:
    """Whether a value from a requirements file is a URL other than `file:`."""
    return re.match(
        r"^[a-z][a-z0-9+.-]*://", value, re.IGNORECASE
    ) is not None and not value.lower().startswith("file:")


def _requirements_files(path: Path) -> Iterator[tuple[str, bool]]:
    """
    Yield the text of a requirements file and of the files it includes.

    Includes are relative to the file that includes them. `file:` URLs are read;
    other URLs and missing files are skipped.

    Args:
        path: The path of the requirements file.

    Yields:
        The text of a file, and whether it was included as a constraints file.
    """
    visited: set[tuple[Path, bool]] = set()

    def read(file: Path, constraint: bool) -> Iterator[tuple[str, bool]]:
        key = (file.resolve(), constraint)
        if key in visited or not file.is_file():
            return
        visited.add(key)
        data = file.read_bytes()
        encoding = (
            "utf-16"
            if data.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE))
            else "utf-8-sig"
        )
        text = data.decode(encoding, errors="replace").replace("\r\n", "\n")
        yield text, constraint
        for line in _requirements_lines(text):
            if not line.startswith("-"):
                continue
            for letter, value in _requirements_options(line):
                if value.lower().startswith("file:"):
                    value = url2pathname(urlparse(value).path)
                if letter != "e" and not _is_remote_url(value):
                    yield from read(file.parent / value, letter == "c")

    yield from read(Path(path), False)


def read_requirements_file_text(path: Path) -> str:
    """
    Return the text of a `requirements.txt` file and of the files it includes.

    A change to any of the files changes the result.

    Args:
        path: The path of the `requirements.txt` file.

    Returns:
        The concatenated text of the file and of the files it includes.
    """
    return "".join(text for text, _ in _requirements_files(path))


def read_requirements(path: Path) -> list[str]:
    """
    Return the requirements of a `requirements.txt` file and of its `-r` includes.

    Args:
        path: The path of the `requirements.txt` file.

    Returns:
        The requirements without their options, the targets of `-e` options, and
        the URLs of `-r` includes, whose requirements can't be read here.
    """
    requirements = []
    for text, constraint in _requirements_files(path):
        if constraint:
            continue
        for line in _requirements_lines(text):
            if line.startswith("-"):
                requirements.extend(
                    value
                    for letter, value in _requirements_options(line)
                    if letter == "e" or (letter == "r" and _is_remote_url(value))
                )
            else:
                requirements.append(re.split(r"\s+-", line, maxsplit=1)[0])
    return requirements


def requirements_use_hashes(text: str) -> bool:
    """
    Whether the text of a requirements file uses hash-checking mode.

    Args:
        text: The text, as `read_requirements_file_text` returns it.

    Returns:
        `True` when a line has a `--hash` or `--require-hashes` option.
    """
    return any(
        re.search(r"(^|\s)--(hash|require-hashes)\b", line)
        for line in _requirements_lines(text)
    )
