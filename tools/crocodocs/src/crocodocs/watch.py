"""File watching support for long-running CrocoDocs development workflows.

CrocoDocs generates JSON/MDX artifacts that Docusaurus consumes at runtime.
When edits are made to the Python source files, examples, or sidebar config while the
docs dev server is already running, those generated artifacts must be refreshed
explicitly. This module owns that refresh loop.
"""

import signal
import subprocess
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

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
    """A single filesystem target to watch."""

    path: Path
    """Absolute path to the watched file or directory."""

    suffixes: Optional[frozenset[str]] = None
    """
    File suffixes that matter when `path` is a directory.
    A value of `None` means "watch every file beneath this directory".
    """

    recursive: bool = True
    """Whether directory traversal should recurse into subdirectories."""

    is_file: bool = False
    """Whether `path` should be treated as an individual file target."""


class WatchEventHandler(FileSystemEventHandler):
    """Collect relevant filesystem changes and expose them after a debounce window."""

    def __init__(self, targets: list[WatchTarget]) -> None:
        super().__init__()
        self._targets = targets
        self._lock = threading.Lock()
        self._pending_changes: set[Path] = set()
        self._last_change_at: Optional[float] = None

    def on_any_event(self, event) -> None:
        """Track create/modify/delete/move events for configured watch targets."""
        if event.is_directory or event.event_type not in {
            "created",
            "deleted",
            "modified",
            "moved",
        }:
            return

        changed_paths = {
            path
            for path in _event_paths(event)
            if _matches_any_target(path, self._targets)
        }
        if not changed_paths:
            return

        with self._lock:
            self._pending_changes.update(changed_paths)
            self._last_change_at = time.monotonic()

    def consume_ready_changes(self, debounce: float) -> list[Path]:
        """Return pending changes after the watcher has been quiet long enough."""
        with self._lock:
            if not self._pending_changes or self._last_change_at is None:
                return []

            if time.monotonic() - self._last_change_at < debounce:
                return []

            ready_changes = sorted(self._pending_changes)
            self._pending_changes.clear()
            self._last_change_at = None
            return ready_changes


def build_watch_targets(config: CrocoDocsConfig) -> list[WatchTarget]:
    """Return the concrete files and directories that should trigger regeneration.

    The watch list mirrors CrocoDocs inputs:
    - hand-authored docs and sidebars
    - Python package sources used by Griffe
    - examples and copied asset roots
    """
    targets: list[WatchTarget] = [
        WatchTarget(config.docs_path, frozenset({".md", ".mdx"})),
        WatchTarget(config.sidebars_source, recursive=False, is_file=True),
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
    seen: set[tuple[Path, Optional[frozenset[str]], bool, bool]] = set()
    for target in targets:
        key = (target.path, target.suffixes, target.recursive, target.is_file)
        if key in seen:
            continue
        seen.add(key)
        unique_targets.append(target)
    return unique_targets


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
    process running while a watchdog observer tracks changes and reruns `generate`
    after a short debounce window so multi-file edits only trigger one regeneration.
    """
    reporter = ProgressReporter("watch")
    targets = build_watch_targets(config)
    event_handler = WatchEventHandler(targets)
    observer = Observer()
    observer_started = False
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
        _schedule_targets(observer, event_handler, targets)
        observer.start()
        observer_started = True
        child = _start_child(command, command_cwd, reporter)

        while not stop_requested:
            if child is not None:
                child_returncode = child.poll()
                if child_returncode is not None:
                    reporter.info(
                        f"Child process exited with code {child_returncode}; stopping watcher."
                    )
                    return child_returncode

            ready_changes = event_handler.consume_ready_changes(debounce)
            if ready_changes:
                reporter.info(_format_change_message(ready_changes))
                _run_generate_cycle(config, reporter)

            time.sleep(interval)

        return 0
    finally:
        for sig, handler in original_handlers.items():
            signal.signal(sig, handler)
        if observer_started:
            observer.stop()
            observer.join(timeout=5)
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


def _schedule_targets(
    observer: Observer,
    event_handler: WatchEventHandler,
    targets: Iterable[WatchTarget],
) -> None:
    """Register the minimum set of observer roots needed for all watch targets."""
    scheduled_roots: dict[Path, bool] = {}
    for target in targets:
        root, recursive = _watch_root(target)
        scheduled_roots[root] = scheduled_roots.get(root, False) or recursive

    for root, recursive in sorted(scheduled_roots.items()):
        observer.schedule(event_handler, str(root), recursive=recursive)


def _watch_root(target: WatchTarget) -> tuple[Path, bool]:
    """Return the concrete observer root for a watch target."""
    root = target.path.parent if target.is_file else target.path
    recursive = False if target.is_file else target.recursive

    while not root.exists() and root != root.parent:
        root = root.parent
        recursive = True

    return root, recursive


def _event_paths(event) -> list[Path]:
    """Return the event source and destination paths, normalized to absolute paths."""
    paths = [Path(event.src_path).resolve()]
    dest_path = getattr(event, "dest_path", None)
    if dest_path:
        paths.append(Path(dest_path).resolve())
    return paths


def _matches_any_target(path: Path, targets: Iterable[WatchTarget]) -> bool:
    """Return True when a path belongs to at least one configured watch target."""
    return any(_matches_target(path, target) for target in targets)


def _matches_target(path: Path, target: WatchTarget) -> bool:
    """Return True when a path should trigger regeneration for a specific target."""
    if target.is_file:
        return path == target.path and _matches_suffixes(path, target.suffixes)

    try:
        relative_path = path.relative_to(target.path)
    except ValueError:
        return False

    if not relative_path.parts:
        return False

    if not target.recursive and len(relative_path.parts) != 1:
        return False

    if _should_skip_parts(relative_path.parts):
        return False

    return _matches_suffixes(path, target.suffixes)


def _should_skip_parts(parts: tuple[str, ...]) -> bool:
    """Return True for files inside ignored directories or hidden paths."""
    for part in parts:
        if part in IGNORED_DIRECTORY_NAMES:
            return True
        if part.startswith(".") and part not in {".env"}:
            return True
    return False


def _matches_suffixes(path: Path, suffixes: Optional[frozenset[str]]) -> bool:
    """Return True when a path should be included for a directory target."""
    if suffixes is None:
        return True
    return path.suffix.lower() in suffixes
