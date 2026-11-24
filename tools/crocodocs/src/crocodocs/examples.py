"""Example data for the docs: example sources, metadata and project files."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib

from .config import CrocoDocsConfig

_EXAMPLE_TEXT_FILE_SUFFIXES = {".toml", ".txt", ".md", ".json", ".yaml", ".yml"}
_EXAMPLE_TEXT_FILE_MAX_BYTES = 64 * 1024


def _should_skip_example_path(root: Path, path: Path) -> bool:
    """Return True if path is inside a hidden directory or a build/dist/cache directory."""
    relative_parts = path.relative_to(root).parts
    return any(
        part.startswith(".") or part in {"__pycache__", "build", "dist"}
        for part in relative_parts
    )


def _generate_code_examples(examples_root: Path, output_path: Path) -> int:
    """Write a JSON file mapping relative example paths to their source text.

    Skips hidden directories and build/dist artifacts. Returns the count of entries written.
    """
    mapping: dict[str, str] = {}
    if not examples_root.exists():
        output_path.write_text("{}", encoding="utf-8")
        return 0

    for source_path in sorted(examples_root.rglob("*.py")):
        if _should_skip_example_path(examples_root, source_path):
            continue
        relative = source_path.relative_to(examples_root).as_posix()
        content = source_path.read_text(encoding="utf-8")
        mapping[relative] = content

    output_path.write_text(
        json.dumps(mapping, indent=2, sort_keys=True), encoding="utf-8"
    )
    return len(mapping)


def _read_pyproject(pyproject_path: Path) -> dict[str, Any]:
    try:
        return tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _example_web_supported(pyproject_path: Path) -> bool:
    """Return True when the example at pyproject_path supports the web platform.

    Web is supported when [tool.flet.gallery].platforms is absent, empty, or
    contains "web".
    """
    data = _read_pyproject(pyproject_path)
    flet = data.get("tool", {}).get("flet", {})
    platforms = flet.get("gallery", {}).get("platforms")
    if not platforms:
        return True
    return "web" in platforms


def _list_example_files(examples_root: Path) -> list[str]:
    """Return the files under examples_root as sorted paths relative to it.

    Asks git for tracked and untracked-but-not-ignored files, so local build output,
    virtual environments and app storage left in example directories are not listed.
    Falls back to walking the directory when git is unavailable. Hidden directories
    and build/dist artifacts are always skipped.
    """
    if not examples_root.exists():
        return []
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            cwd=examples_root,
            capture_output=True,
            check=True,
        )
        candidates = [p for p in result.stdout.decode("utf-8").split("\0") if p]
    except (OSError, subprocess.CalledProcessError):
        candidates = [
            p.relative_to(examples_root).as_posix()
            for p in examples_root.rglob("*")
            if p.is_file()
        ]
    return sorted(
        relative
        for relative in candidates
        if (examples_root / relative).is_file()
        and not _should_skip_example_path(examples_root, examples_root / relative)
    )


def _group_files_by_example(files: list[str]) -> dict[str, list[str]]:
    """Map each example directory to the files it owns, relative to that directory.

    An example directory is one containing a pyproject.toml. A file belongs to its
    nearest enclosing example directory, so a nested example's files are not also
    listed under the outer example.
    """
    example_dirs = {
        f.rpartition("/")[0] for f in files if f.endswith("/pyproject.toml")
    }
    grouped: dict[str, list[str]] = {d: [] for d in example_dirs}
    for relative in files:
        parent = relative.rpartition("/")[0]
        while parent and parent not in example_dirs:
            parent = parent.rpartition("/")[0]
        if parent:
            grouped[parent].append(relative[len(parent) + 1 :])
    return grouped


def _is_bundled_text_file(path: Path) -> bool:
    """Whether example-files.json carries the contents of the example file at path."""
    return (
        path.suffix in _EXAMPLE_TEXT_FILE_SUFFIXES
        and path.stat().st_size <= _EXAMPLE_TEXT_FILE_MAX_BYTES
    )


def _strip_example_pyprojects(
    repo_root: Path, pyproject_paths: list[Path]
) -> dict[Path, str]:
    """Return the given example pyproject.toml files as `flet create --example` writes them.

    The stripping lives in flet-cli, so it runs in the SDK's environment through
    scripts/example_pyprojects.py, the same way the CLI partials are rendered.
    """
    if not pyproject_paths:
        return {}
    script = Path(__file__).parent / "scripts" / "example_pyprojects.py"
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
    result = subprocess.run(
        [
            "uv",
            "--directory",
            str(repo_root / "sdk/python"),
            "run",
            "python",
            str(script),
        ],
        input=json.dumps([str(path) for path in pyproject_paths]),
        check=True,
        capture_output=True,
        text=True,
        cwd=repo_root,
        env=env,
    )
    # Skip anything printed before the JSON, e.g. flet-cli's Git version warning.
    stdout = result.stdout[max(result.stdout.find("{"), 0) :]
    return {Path(path): text for path, text in json.loads(stdout).items()}


def _generate_example_file_sources(
    examples_root: Path, files: list[str], output_path: Path, repo_root: Path
) -> int:
    """Write a JSON file mapping non-Python example text files to their contents.

    Covers files such as pyproject.toml that the docs show next to an example's
    Python source; pyproject.toml is shown as `flet create --example` writes it,
    without its docs tables. Python files are already in code-examples.json and
    binary or large files are left out. The docs load this file on demand,
    so it does not grow every page's bundle.
    """
    paths: list[Path] = []
    for example_dir, example_files in _group_files_by_example(files).items():
        for name in example_files:
            path = examples_root / example_dir / name
            if _is_bundled_text_file(path):
                paths.append(path)

    pyprojects = _strip_example_pyprojects(
        repo_root, [path for path in paths if path.name == "pyproject.toml"]
    )
    mapping: dict[str, str] = {}
    for path in paths:
        if path in pyprojects:
            content = pyprojects[path]
        else:
            try:
                content = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
        mapping[path.relative_to(examples_root).as_posix()] = content

    output_path.write_text(
        json.dumps(mapping, indent=2, sort_keys=True), encoding="utf-8"
    )
    return len(mapping)


def _generate_examples_metadata(
    examples_root: Path, files: list[str], output_path: Path
) -> int:
    """Write a JSON file mapping example directory paths to their metadata.

    Walks every directory under examples_root that contains a pyproject.toml and emits
    a per-directory metadata entry. The directory key is its path relative to
    examples_root (e.g. "controls/material/button/basic"), matching the parent of
    the keys used in code-examples.json. Each entry lists the files of the example
    that the docs can show, relative to its directory: those whose contents are
    bundled in code-examples.json or example-files.json.
    """
    mapping: dict[str, dict[str, Any]] = {}
    for relative, example_files in sorted(_group_files_by_example(files).items()):
        pyproject_path = examples_root / relative / "pyproject.toml"
        data = _read_pyproject(pyproject_path)
        meta: dict[str, Any] = {"webSupported": _example_web_supported(pyproject_path)}
        flet_metadata = data.get("tool", {}).get("flet", {}).get("metadata", {})
        if title := flet_metadata.get("title"):
            meta["title"] = title
        if docs_intro := flet_metadata.get("docs_intro"):
            meta["docs_intro"] = docs_intro
        meta["viewableFiles"] = [
            name
            for name in example_files
            if name.endswith(".py")
            or _is_bundled_text_file(examples_root / relative / name)
        ]
        mapping[relative] = meta

    output_path.write_text(
        json.dumps(mapping, indent=2, sort_keys=True), encoding="utf-8"
    )
    return len(mapping)


def write_example_data(config: CrocoDocsConfig) -> tuple[int, int, int]:
    """Write the example data the docs read: code-examples.json,
    examples-metadata.json and example-files.json.

    Returns the number of entries written to each file, in that order.
    """
    output_dir = config.partials_output_dir
    code_example_entries = _generate_code_examples(
        config.examples_root, output_dir / "code-examples.json"
    )
    example_files = _list_example_files(config.examples_root)
    examples_metadata_entries = _generate_examples_metadata(
        config.examples_root, example_files, output_dir / "examples-metadata.json"
    )
    example_file_entries = _generate_example_file_sources(
        config.examples_root,
        example_files,
        output_dir / "example-files.json",
        repo_root=config.project_root.parent.parent,
    )
    return code_example_entries, examples_metadata_entries, example_file_entries
