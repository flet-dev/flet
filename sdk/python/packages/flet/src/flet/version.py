"""Provide the current Flet version."""

import json
import os
import subprocess as sp
from pathlib import Path
from typing import Optional

from flet.utils import is_mobile, is_windows, which

__all__ = [
    "FLUTTER_VERSION",
    "PYODIDE_VERSION",
    "find_repo_root",
    "from_git",
    "get_flutter_version",
    "version",
]

# set by CI
version = ""


# set by CI
FLUTTER_VERSION = ""
"""
The Flutter SDK version used when building the flet client or packaging
apps with [`flet build`](https://docs.flet.dev/cli/flet-build/).
"""

PYODIDE_VERSION = "0.27.7"
"""
The Pyodide version being used when packaging
with [`flet build web`](https://docs.flet.dev/cli/flet-build/).
"""


def _find_upwards(start_dir: Path, file_name: str) -> Optional[Path]:
    current_dir = start_dir.resolve()
    while current_dir != current_dir.parent:
        candidate = current_dir / file_name
        if candidate.is_file():
            return candidate
        current_dir = current_dir.parent
    return None


def _flutter_version_from_fvmrc(fvmrc_path: Path) -> Optional[str]:
    try:
        raw = fvmrc_path.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    if not raw:
        return None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return raw.strip().strip('"')
    if isinstance(data, dict):
        value = data.get("flutter")
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def get_flutter_version() -> str:
    """
    Return the required Flutter SDK version.

    In CI/release builds the value is stamped into `FLUTTER_VERSION`.
    In a local development checkout (where `FLUTTER_VERSION == ""`), it is
    resolved from the repository's `.fvmrc`.
    """

    if FLUTTER_VERSION:
        return FLUTTER_VERSION

    start_dirs = [Path.cwd(), Path(__file__).resolve().parent]
    for start_dir in start_dirs:
        fvmrc_path = _find_upwards(start_dir, ".fvmrc")
        if fvmrc_path:
            v = _flutter_version_from_fvmrc(fvmrc_path)
            if v:
                return v
    return ""


def from_git() -> Optional[str]:
    """Try to get the version from Git tags."""
    working = Path().absolute()
    try:
        repo_root = find_repo_root(Path(__file__).resolve().parent)

        if repo_root:
            os.chdir(repo_root)
            in_repo = (
                which("git.exe" if is_windows() else "git")
                and sp.run(
                    ["git", "status"],
                    capture_output=True,
                    text=True,
                ).returncode
                == 0
            )

            if in_repo:
                try:
                    git_p = sp.run(
                        ["git", "describe", "--abbrev=0"],
                        capture_output=True,
                        text=True,
                        check=True,  # Raise an exception for non-zero exit codes
                    )
                    tag = git_p.stdout.strip()
                    return tag[1:] if tag.startswith("v") else tag
                except sp.CalledProcessError as e:
                    print(f"Error getting Git version: {e}")
                except FileNotFoundError:
                    print("Git command not found.")
    finally:
        os.chdir(working)
    return None


def find_repo_root(start_path: Path) -> Optional[Path]:
    """Find the root directory of the Git repository containing the start path."""
    current_path = start_path.resolve()
    while current_path != current_path.parent:
        if (current_path / ".git").is_dir():
            return current_path
        current_path = current_path.parent
    return None


DEFAULT_FLET_VERSION = "0.1.0"

if not version and not is_mobile():
    # Only try to get the version from Git if the pre-set version is empty
    # This is more likely to happen in a development/source environment
    version = from_git() or DEFAULT_FLET_VERSION  # Fallback to default if Git fails

# If 'version' is still empty after the above (e.g., in a built package
# where CI didn't replace it), it might be appropriate to have another
# default or a way to set it during the build process. However, the
# CI replacement is the standard way for packaged versions.
if not version:
    version = DEFAULT_FLET_VERSION  # Final fallback
