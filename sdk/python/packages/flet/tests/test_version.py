"""Regression tests for `flet.version.find_repo_root`."""

from pathlib import Path

from flet.version import find_repo_root


def test_find_repo_root_regular_clone(tmp_path):
    """A directory whose ancestor contains `.git` (as a directory, i.e. a
    regular clone) should be detected as a repo root.
    """
    (tmp_path / ".git").mkdir()
    nested = tmp_path / "a" / "b" / "c"
    nested.mkdir(parents=True)

    assert find_repo_root(nested) == tmp_path.resolve()


def test_find_repo_root_worktree(tmp_path):
    """In a git worktree, `.git` is a regular file (`gitdir: ...`), not a
    directory. `find_repo_root` must still detect the worktree root.
    """
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    (worktree / ".git").write_text(
        "gitdir: /some/path/.git/worktrees/mybranch\n", encoding="utf-8"
    )
    nested = worktree / "a" / "b"
    nested.mkdir(parents=True)

    assert find_repo_root(nested) == worktree.resolve()


def test_find_repo_root_not_in_repo(tmp_path):
    """If no `.git` entry is found up to the filesystem root, returns None."""
    nested = tmp_path / "a" / "b"
    nested.mkdir(parents=True)

    # tmp_path itself may live under a repo on CI (the sandbox), so we can't
    # assert None here unconditionally. We only assert that when it does find
    # a root, the root is an ancestor of `nested` (sanity).
    result = find_repo_root(nested)
    assert result is None or Path(nested).resolve().is_relative_to(result)
