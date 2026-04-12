"""File watching support for long-running CrocoDocs development workflows.

CrocoDocs generates JSON/MDX artifacts that Docusaurus consumes at runtime.
When edits are made to the Python source files, examples, or sidebar config while the
docs dev server is already running, those generated artifacts must be refreshed
explicitly. This module owns that refresh loop.

The watcher intentionally uses only the Python standard library. That keeps the
developer workflow portable and avoids requiring every contributor to install
platform-specific tools like `fswatch` or `watchexec`.
"""

import os
import signal
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

from .config import CrocoDocsConfig
from .generate import run_generate
from .progress import ProgressReporter

# Directories that should never trigger documentation regeneration.
# They are either editor/build artifacts or trees CrocoDocs itself writes.
IGNORED_DIRECTORY_NAMES = {
    ".git",
    ".idea",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
}


@dataclass(frozen=True)
class WatchTarget:
    """A single filesystem target to watch.

    Attributes:
        path: Absolute path to the watched file or directory.
        suffixes: File suffixes that matter when `path` is a directory. A value
            of `None` means "watch every file beneath this directory".
        recursive: Whether directory traversal should recurse into subdirectories.
    """

    path: Path
    suffixes: Optional[frozenset[str]] = None
    recursive: bool = True


@dataclass(frozen=True)
class FileState:
    """A compact snapshot of a single watched file."""

    mtime_ns: int
    size: int


def build_watch_targets(config: CrocoDocsConfig) -> list[WatchTarget]:
    """Return the concrete files and directories that should trigger regeneration.

    The watch list mirrors CrocoDocs inputs:
    - hand-authored docs and sidebars
    - Python package sources used by Griffe
    - examples and copied asset roots
    """
    targets: list[WatchTarget] = [
        WatchTarget(config.docs_path, frozenset({".md", ".mdx"})),
        WatchTarget(config.sidebars_source, recursive=False),
        WatchTarget(config.examples_root, frozenset({".py", ".png", ".gif", ".svg"})),
    ]

    for package_root in sorted(config.packages.values(), key=str):
        targets.append(WatchTarget(package_root, frozenset({".py"})))

    for mapping in config.asset_mappings.values():
        suffixes = (
            frozenset(ext.lower() for ext in mapping.include_exts)
            if mapping.include_exts
            else None
        )
        targets.append(WatchTarget(mapping.source_path, suffixes))

    # Multiple config entries can collapse to the same directory (for example
    # examples_root and the examples asset mapping). Deduplicate to avoid repeated
    # scans while preserving a deterministic order for debug output.
    unique_targets: list[WatchTarget] = []
    seen: set[tuple[Path, Optional[frozenset[str]], bool]] = set()
    for target in targets:
        key = (target.path, target.suffixes, target.recursive)
        if key in seen:
            continue
        seen.add(key)
        unique_targets.append(target)
    return unique_targets


def iter_target_files(target: WatchTarget) -> Iterable[Path]:
    """Yield every relevant file covered by `target`.

    Missing paths are treated as empty so the watcher can handle paths that appear
    later without crashing.
    """
    path = target.path
    if not path.exists():
        return

    if path.is_file():
        if _matches_suffixes(path, target.suffixes):
            yield path
        return

    if target.recursive:
        yield from _walk_directory(path, target.suffixes)
    else:
        for child in sorted(path.glob("*")):
            if child.is_dir():
                continue
            if _should_skip_path(path, child):
                continue
            if _matches_suffixes(child, target.suffixes):
                yield child


def snapshot_targets(targets: Iterable[WatchTarget]) -> dict[Path, FileState]:
    """Build a filesystem snapshot for the provided watch targets."""
    snapshot: dict[Path, FileState] = {}
    for target in targets:
        for file_path in iter_target_files(target):
            try:
                stat_result = file_path.stat()
            except (FileNotFoundError, OSError):
                # The file may have been deleted or renamed between iteration
                # and stat — skip it for this snapshot cycle.
                continue
            snapshot[file_path] = FileState(
                mtime_ns=stat_result.st_mtime_ns,
                size=stat_result.st_size,
            )
    return snapshot


def detect_changes(
    previous: dict[Path, FileState], current: dict[Path, FileState]
) -> list[Path]:
    """Return watched files that were created, removed, or modified."""
    changed: set[Path] = set()

    previous_paths = set(previous)
    current_paths = set(current)

    changed.update(previous_paths - current_paths)
    changed.update(current_paths - previous_paths)

    for path in previous_paths & current_paths:
        if previous[path] != current[path]:
            changed.add(path)

    return sorted(changed)


def run_watch(
    config: CrocoDocsConfig,
    *,
    interval: float,
    debounce: float,
    command: Optional[list[str]] = None,
    command_cwd: Optional[Path] = None,
) -> int:
    """Regenerate CrocoDocs outputs on input changes and optionally run a child process.

    The child process is usually the Docusaurus dev server. The watcher keeps that
    process running while polling inputs for changes and reruns `generate` after a
    short debounce window so multi-file edits only trigger one regeneration.
    """
    reporter = ProgressReporter("watch")
    targets = build_watch_targets(config)
    child: Optional[subprocess.Popen[str]] = None

    stop_requested = False

    def request_stop(signum: int, _frame: object) -> None:
        nonlocal stop_requested
        stop_requested = True
        reporter.info(f"Received signal {signum}; stopping watcher.")

    original_handlers = {
        sig: signal.getsignal(sig) for sig in (signal.SIGINT, signal.SIGTERM)
    }
    for sig in original_handlers:
        signal.signal(sig, request_stop)

    try:
        _run_generate_cycle(config, reporter)
        child = _start_child(command, command_cwd, reporter)
        previous_snapshot = snapshot_targets(targets)
        pending_changes: list[Path] = []
        last_change_at: Optional[float] = None

        while not stop_requested:
            if child is not None:
                child_returncode = child.poll()
                if child_returncode is not None:
                    reporter.info(
                        f"Child process exited with code {child_returncode}; stopping watcher."
                    )
                    return child_returncode

            time.sleep(interval)

            current_snapshot = snapshot_targets(targets)
            changed_paths = detect_changes(previous_snapshot, current_snapshot)
            previous_snapshot = current_snapshot

            if changed_paths:
                pending_changes = changed_paths
                last_change_at = time.monotonic()
                reporter.info(_format_change_message(changed_paths))
                continue

            if pending_changes and last_change_at is not None:
                quiet_for = time.monotonic() - last_change_at
                if quiet_for >= debounce:
                    _run_generate_cycle(config, reporter)
                    pending_changes = []
                    last_change_at = None

        return 0
    finally:
        for sig, handler in original_handlers.items():
            signal.signal(sig, handler)
        _stop_child(child, reporter)


def _run_generate_cycle(config: CrocoDocsConfig, reporter: ProgressReporter) -> None:
    """Run a single CrocoDocs generation cycle and keep watching on failure."""
    reporter.stage("Regenerating CrocoDocs artifacts")
    try:
        run_generate(
            config,
            docs_path=config.docs_path,
            manifest_output=config.manifest_output,
            api_output=config.api_output,
            base_url=config.base_url,
        )
    except Exception as exc:  # noqa: BLE001
        # A failed regeneration should not kill the dev server or the watcher.
        # Contributors often fix docs errors incrementally and expect the next save to
        # retry automatically.
        reporter.info(f"Generation failed: {exc}")


def _start_child(
    command: Optional[list[str]],
    command_cwd: Optional[Path],
    reporter: ProgressReporter,
) -> Optional[subprocess.Popen[str]]:
    """Spawn the optional child process that should run alongside the watcher."""
    if not command:
        return None

    reporter.info(
        "Starting child process: "
        + " ".join(command)
        + (f" (cwd={command_cwd})" if command_cwd else "")
    )
    return subprocess.Popen(command, cwd=command_cwd, text=True)  # noqa: S603


def _stop_child(
    child: Optional[subprocess.Popen[str]], reporter: ProgressReporter
) -> None:
    """Terminate the child process gracefully, then force kill if needed."""
    if child is None or child.poll() is not None:
        return

    reporter.info("Stopping child process.")
    child.terminate()
    try:
        child.wait(timeout=10)
    except subprocess.TimeoutExpired:
        reporter.info("Child did not exit in time; killing it.")
        child.kill()
        child.wait()


def _format_change_message(changed_paths: list[Path]) -> str:
    """Render a compact log line for detected file changes."""
    preview = ", ".join(path.name for path in changed_paths[:4])
    if len(changed_paths) > 4:
        preview += f", +{len(changed_paths) - 4} more"
    return f"Detected changes in {len(changed_paths)} file(s): {preview}"


def _walk_directory(root: Path, suffixes: Optional[frozenset[str]]) -> Iterable[Path]:
    """Walk root recursively, pruning ignored/hidden directories in-place.

    Unlike `Path.rglob`, `os.walk` lets us remove entries from *dirs* so the
    OS never descends into heavy trees like `node_modules` or `.venv`.
    """
    for dirpath, dirs, filenames in os.walk(root):
        # Prune in-place so os.walk skips these subtrees entirely.
        dirs[:] = sorted(
            d
            for d in dirs
            if d not in IGNORED_DIRECTORY_NAMES
            and not (d.startswith(".") and d not in {".env"})
        )

        for filename in sorted(filenames):
            if filename.startswith(".") and filename not in {".env"}:
                continue
            file_path = Path(dirpath) / filename
            if _matches_suffixes(file_path, suffixes):
                yield file_path


def _matches_suffixes(path: Path, suffixes: Optional[frozenset[str]]) -> bool:
    """Return True when a path should be included for a directory target."""
    if suffixes is None:
        return True
    return path.suffix.lower() in suffixes


def _should_skip_path(root: Path, path: Path) -> bool:
    """Return True for files inside ignored directories or hidden files."""
    try:
        relative_parts = path.relative_to(root).parts
    except ValueError:
        relative_parts = path.parts

    for part in relative_parts:
        if part in IGNORED_DIRECTORY_NAMES:
            return True
        if part.startswith(".") and part not in {".env"}:
            return True
    return False
