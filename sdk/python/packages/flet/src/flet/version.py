"""Provide the current Flet version."""

import os
import subprocess as sp
from pathlib import Path

from flet.utils.files import which
from flet.utils.platform_utils import is_mobile, is_windows

DEFAULT_VERSION = "0.1.0"

# will be replaced by CI
version = ""


def from_git():
    """Try to get the version from Git tags."""
    working = Path().absolute()
    try:
        version_file_path = Path(__file__).resolve()
        repo_root = find_repo_root(version_file_path.parent)

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


def find_repo_root(start_path: Path) -> Path | None:
    """Find the root directory of the Git repository containing the start path."""
    current_path = start_path.resolve()
    while current_path != current_path.parent:
        if (current_path / ".git").is_dir():
            return current_path
        current_path = current_path.parent
    return None


if not version and not is_mobile():
    # Only try to get the version from Git if the pre-set version is empty
    # This is more likely to happen in a development/source environment
    version = from_git() or DEFAULT_VERSION  # Fallback to a default if Git fails

# If 'version' is still empty after the above (e.g., in a built package
# where CI didn't replace it), it might be appropriate to have another
# default or a way to set it during the build process. However, the
# CI replacement is the standard way for packaged versions.
if not version:
    version = DEFAULT_VERSION  # Final fallback
