import json
import os
import re
import shutil
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

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

    Raises:
        ExampleNotFoundError: If the ID is empty or contains `.` or `..` parts.
    """
    parts = [p for p in example.replace("\\", "/").split("/") if p]
    if not parts or any(p in (".", "..") for p in parts):
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

    Raises:
        ExampleNotFoundError: If `ref` or the example doesn't exist, or the
            directory has no `pyproject.toml`.
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


def set_project_metadata(
    pyproject_path: Path, name: str, description: str | None
) -> None:
    """
    Set `[project].name`, and `[project].description` when given, in place.

    Edits the matching lines rather than re-serializing the TOML, so the
    example's formatting and comments are kept.
    """
    text = pyproject_path.read_text(encoding="utf-8")
    match = re.search(r"(?ms)^\[project\][ \t]*\n(.*?)(?=^\[|\Z)", text)
    if not match:
        return
    table = match.group(1)
    values = {"name": name}
    if description is not None:
        values["description"] = description
    for key, value in values.items():
        line = f"{key} = {json.dumps(value, ensure_ascii=False)}"
        table, count = re.subn(
            rf"(?m)^{key}[ \t]*=.*$", line.replace("\\", "\\\\"), table, count=1
        )
        if not count:
            table = f"{line}\n{table}"
    pyproject_path.write_text(
        text[: match.start(1)] + table + text[match.end(1) :], encoding="utf-8"
    )


def strip_tooling_only_tables(text: str) -> str:
    """
    Return pyproject.toml `text` without the tables that are irrelevant for the
    example, with blank lines collapsed.
    """
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
    stripped = re.sub(r"\n{3,}", "\n\n", "\n".join(kept)).strip("\n")
    return f"{stripped}\n"
