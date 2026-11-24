import copy
import json
import os
import re
import shutil
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

EXAMPLES_REPO = "flet-dev/flet"
"""GitHub repository that hosts the Flet examples."""

EXAMPLES_REPO_PATH = "sdk/python/examples"
"""Path of the examples directory inside `EXAMPLES_REPO`."""

_SKIPPED_NAMES = {"__pycache__", "build", "dist"}

_TOOLING_ONLY_TABLES = ("tool.flet.gallery", "tool.flet.metadata")
_TOML_TABLE_HEADER_RE = re.compile(
    r"^\s*\[\[?\s*([A-Za-z0-9_-]+(?:\s*\.\s*[A-Za-z0-9_-]+)*)\s*\]\]?\s*(?:#.*)?$"
)


class ExampleNotFoundError(Exception):
    """Raised when an example ID does not name an example project."""


def normalize_example_id(example: str) -> str:
    """
    Return `example` as a `/`-separated path relative to the examples directory.

    Accepts backslashes and surrounding slashes, so IDs typed on Windows or copied
    with a trailing `/` work.

    Args:
        example: Example ID as given on the command line, e.g.
            `controls/material/button/basic`.

    Returns:
        The normalized example ID.

    Raises:
        ExampleNotFoundError: If the ID is empty, contains `.` or `..` parts, or
            names a drive, such as `C:/examples`.
    """
    parts = [p for p in example.replace("\\", "/").split("/") if p]
    if not parts or any(p in (".", "..") or ":" in p for p in parts):
        raise ExampleNotFoundError(f"Invalid example: {example!r}")
    return "/".join(parts)


def _is_skipped(name: str) -> bool:
    """Whether a file or directory name is local tooling output, not example source."""
    return name.startswith(".") or name in _SKIPPED_NAMES


def copy_local_example(example_dir: Path, dest: Path) -> None:
    """
    Copy the example project at `example_dir` into `dest`.

    Hidden entries and build output are left out, and so are subdirectories that
    are examples of their own (they contain a `pyproject.toml`).

    Args:
        example_dir: Directory of the example in the local examples checkout.
        dest: Directory to copy the example into; created when missing.

    Raises:
        ExampleNotFoundError: If `example_dir` has no `pyproject.toml`.
    """
    if not (example_dir / "pyproject.toml").is_file():
        raise ExampleNotFoundError(
            f"No example {example_dir.name!r} in {example_dir.parent}"
        )

    def ignore(directory: str, names: list[str]) -> set[str]:
        return {
            name
            for name in names
            if _is_skipped(name)
            or (
                (Path(directory) / name).is_dir()
                and (Path(directory) / name / "pyproject.toml").is_file()
            )
        }

    shutil.copytree(example_dir, dest, ignore=ignore, dirs_exist_ok=True)


def _is_safe_file_name(name: str) -> bool:
    """Whether `name` is a single file or directory name on every platform."""
    return name not in ("", ".", "..") and not any(c in name for c in "/\\:")


def _github_get(url: str) -> bytes:
    """Fetch `url`, authenticating with `$GITHUB_TOKEN` when it is set."""
    headers = {"User-Agent": "flet-cli"}
    if url.startswith("https://api.github.com/"):
        headers["Accept"] = "application/vnd.github+json"
        if token := os.environ.get("GITHUB_TOKEN"):
            headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers)) as resp:
        return resp.read()


def _list_github_dir(path: str, ref: str) -> list[dict]:
    """List a directory of `EXAMPLES_REPO` at `ref` with the GitHub contents API."""
    url = (
        f"https://api.github.com/repos/{EXAMPLES_REPO}/contents/"
        f"{urllib.parse.quote(path)}?ref={urllib.parse.quote(ref)}"
    )
    entries = json.loads(_github_get(url))
    if not isinstance(entries, list):
        # The contents API returns an object, not a list, for a file path.
        raise ExampleNotFoundError(f"{path} is a file, not an example directory")
    return entries


def download_example(example: str, ref: str, dest: Path) -> None:
    """
    Download the example `example` of `EXAMPLES_REPO` at git `ref` into `dest`.

    Uses one GitHub API request per directory of the example; the files themselves
    come from `raw.githubusercontent.com`, which is not rate-limited the same way.
    Hidden entries, build output and nested examples are left out.

    Args:
        example: Normalized example ID, relative to `EXAMPLES_REPO_PATH`.
        ref: Git branch, tag or commit to download the example from.
        dest: Directory to download the example into; created when missing.

    Raises:
        ExampleNotFoundError: If `ref` or the example doesn't exist, or the
            directory has no `pyproject.toml`.
        ValueError: If an entry's name isn't a plain file name, so writing it
            could land outside `dest`.
    """
    root = f"{EXAMPLES_REPO_PATH}/{example}"
    try:
        entries = _list_github_dir(root, ref)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise ExampleNotFoundError(
                f"No example {example!r} at {EXAMPLES_REPO}@{ref}"
            ) from e
        raise
    if not any(e["type"] == "file" and e["name"] == "pyproject.toml" for e in entries):
        raise ExampleNotFoundError(f"{example!r} is not an example project")

    pending = [("", entries)]
    while pending:
        relative, entries = pending.pop()
        for entry in entries:
            name = entry["name"]
            if not _is_safe_file_name(name):
                raise ValueError(f"Unsafe file name in example: {name!r}")
            if _is_skipped(name):
                continue
            target = f"{relative}/{name}" if relative else name
            if entry["type"] == "dir":
                children = _list_github_dir(f"{root}/{target}", ref)
                if any(c["name"] == "pyproject.toml" for c in children):
                    continue
                pending.append((target, children))
            elif entry["type"] == "file" and entry.get("download_url"):
                path = dest / target
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(_github_get(entry["download_url"]))


def _parse_toml(text: str) -> dict | None:
    """Parse `text` as TOML, or return None when it isn't valid."""
    try:
        return tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None


def _prune_empty_tables(data: dict) -> dict:
    """Return `data` without tables that are empty once their empty tables go."""
    pruned = {}
    for key, value in data.items():
        if isinstance(value, dict):
            value = _prune_empty_tables(value)
            if not value:
                continue
        pruned[key] = value
    return pruned


def set_project_metadata(text: str, name: str, description: str | None) -> str | None:
    """
    Set `[project].name`, and `[project].description` when given, in a
    pyproject.toml.

    Edits the matching lines rather than re-serializing the TOML, so the
    example's formatting and comments are kept.

    Args:
        text: Contents of the pyproject.toml.
        name: Project name to set.
        description: Project description to set, or None to keep the current one.

    Returns:
        The edited contents, or None when the edit can't be made safely, for
        example when the TOML is invalid or a value spans several lines.
    """
    original = _parse_toml(text)
    match = re.search(r"(?ms)^\[project\][ \t]*(?:#[^\n]*)?\n(.*?)(?=^\[|\Z)", text)
    if original is None or not match:
        return None
    table = match.group(1)
    values = {"name": name}
    if description is not None:
        values["description"] = description
    for key, value in values.items():
        line = f"{key} = {json.dumps(value, ensure_ascii=False)}"
        table, count = re.subn(
            rf"(?m)^[ \t]*{key}[ \t]*=.*$", line.replace("\\", "\\\\"), table, count=1
        )
        if not count:
            table = f"{line}\n{table}"
    edited = text[: match.start(1)] + table + text[match.end(1) :]

    expected = copy.deepcopy(original)
    expected.setdefault("project", {}).update(values)
    return edited if _parse_toml(edited) == expected else None


def strip_tooling_only_tables(text: str) -> str:
    """
    Remove the tables that are irrelevant for the example from a pyproject.toml,
    with any of their sub-tables, and collapses the blank lines left behind.

    Args:
        text: Contents of the pyproject.toml.

    Returns:
        The contents without those tables, or `text` unchanged when it isn't
            valid TOML or when the line-based removal would change anything else,
            for example a table header inside a multiline string.
    """
    original = _parse_toml(text)
    if original is None:
        return text
    kept: list[str] = []
    skipping = False
    for line in text.splitlines():
        if header := _TOML_TABLE_HEADER_RE.match(line):
            name = re.sub(r"\s+", "", header.group(1))
            skipping = any(
                name == table or name.startswith(f"{table}.")
                for table in _TOOLING_ONLY_TABLES
            )
        if not skipping:
            kept.append(line)
    stripped = re.sub(r"\n{3,}", "\n\n", "\n".join(kept)).strip("\n") + "\n"

    expected = copy.deepcopy(original)
    for table in _TOOLING_ONLY_TABLES:
        *parents, last = table.split(".")
        parent = expected
        for key in parents:
            parent = parent.get(key, {})
        parent.pop(last, None)
    parsed = _parse_toml(stripped)
    if parsed is None or _prune_empty_tables(parsed) != _prune_empty_tables(expected):
        return text
    return stripped
