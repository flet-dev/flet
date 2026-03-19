"""Provide the current Flet version."""

import json
import subprocess as sp
from pathlib import Path
from typing import Optional

from flet.utils import is_mobile, is_windows, which

__all__ = [
    "find_repo_root",
    "flet_version",
    "flutter_version",
    "from_git",
    "pyodide_version",
]

# set by CI
flet_version = ""
"""
The Flet version in use.

This value is set explicitly in CI for released packages. When running from
source and no version is provided, it is derived from the nearest Git tag
when available.
"""

# set by CI
flutter_version = ""
"""
The Flutter SDK version used when building the flet client or packaging
apps with [`flet build`](https://docs.flet.dev/cli/flet-build/).

This value is set explicitly in CI for released packages. When running from
source and no version is provided, it is resolved from the repository's
`.fvmrc` file when available.
"""

PYODIDE_VERSION = "0.27.7"
"""
The Pyodide version being used when packaging
with [`flet build web`](https://docs.flet.dev/cli/flet-build/).
"""


def from_git() -> Optional[str]:
    """Try to get the version from Git tags."""
    repo_root = find_repo_root(Path(__file__).resolve().parent)
    if not repo_root:
        return None

    git_cmd = "git.exe" if is_windows() else "git"
    if not which(git_cmd):
        return None

    try:
        result = sp.run(
            [git_cmd, "describe", "--tags", "--abbrev=0"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
        tag = result.stdout.strip()
        return tag[1:] if tag.startswith("v") else tag

    except sp.CalledProcessError as e:
        # Git is present but no tags / not a valid repo state
        print(f"Error getting Git version: {e}")
    except OSError as e:
        print(f"Error running Git: {e}")

    return None


def find_repo_root(start_path: Path) -> Optional[Path]:
    """Find the root directory of the Git repository containing the start path."""
    current_path = start_path.resolve()
    while current_path != current_path.parent:
        if (current_path / ".git").is_dir():
            return current_path
        current_path = current_path.parent
    return None


def get_flet_version() -> str:
    """Return the Flet version, falling back to Git or a default if needed."""

    # If the version is already set (e.g., replaced by CI), use it
    if flet_version:
        return flet_version

    # Only try to get the version from Git if the pre-set version is empty.
    # This is more likely to happen in a development/source environment.
    if not is_mobile():
        git_version = from_git()
        if git_version:
            return git_version  # Use Git version if available

    # If 'flet_version' is still empty after the above (e.g., in a built package
    # where CI didn't replace it), fall back to the default version.
    # CI replacement is the standard way for packaged versions.
    return "0.1.0"


def get_flutter_version() -> str:
    """
    Return the Flutter SDK version.

    Uses `flutter_version` when set (CI/release builds); otherwise resolves it
    from `.fvmrc` in a local development checkout.
    """

    # If the version is already set (e.g., replaced by CI), use it
    if flutter_version:
        return flutter_version

    if not is_mobile():
        repo_root = find_repo_root(Path(__file__).resolve().parent)
        if repo_root:
            fvmrc_path = repo_root / ".fvmrc"
            try:
                v = json.loads(fvmrc_path.read_text(encoding="utf-8"))[
                    "flutter"
                ].strip()
                if not v:
                    raise ValueError("Empty or missing 'flutter' value")
                return v
            except Exception as e:
                print(f"Error parsing {fvmrc_path!r}: {e}")

    # If 'flutter_version' is still empty after the above (e.g., in a built package
    # where CI didn't replace it), fall back to the below default.
    # CI replacement is the standard way for packaged versions.
    return "0"


flutter_version = get_flutter_version()
pyodide_version = PYODIDE_VERSION
flet_version = get_flet_version()
__version__ = flet_version
