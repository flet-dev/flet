"""`assets_dir` resolution in `flet.app`.

`assets_dir` defaults to `"assets"` whether or not the app has such a
directory, so the resolver must not hand a non-existent path downstream: the
desktop view ignores it silently while the web server logged
`assets_dir does not exist: ...`, so the same app warned only when run with
`--web`, about a directory the user never asked for.
"""

import os

import pytest

from flet.app import __get_assets_dir_path as get_assets_dir_path


@pytest.fixture(autouse=True)
def _no_env_override(monkeypatch):
    """`FLET_ASSETS_DIR` would otherwise leak in from the developer's shell."""
    monkeypatch.delenv("FLET_ASSETS_DIR", raising=False)


class TestMissingDirectoryIsDropped:
    """A path that does not exist resolves to None rather than being passed on.

    This is what stops `flet run --web` warning about the defaulted
    `assets/` directory of an app that simply has no assets.
    """

    def test_missing_absolute_path_is_dropped(self, tmp_path):
        assert get_assets_dir_path(str(tmp_path / "nope")) is None

    def test_missing_relative_path_is_dropped(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        assert get_assets_dir_path("assets", relative_to_cwd=True) is None

    def test_a_file_is_not_an_assets_dir(self, tmp_path):
        f = tmp_path / "assets"
        f.write_text("not a directory")
        assert get_assets_dir_path(str(f)) is None


class TestExistingDirectoryIsResolved:
    """The directory is still found and absolutised when it does exist."""

    def test_absolute_path_passes_through(self, tmp_path):
        (tmp_path / "assets").mkdir()
        resolved = get_assets_dir_path(str(tmp_path / "assets"))
        assert resolved is not None
        assert os.path.isdir(resolved)

    def test_relative_path_resolved_against_cwd(self, tmp_path, monkeypatch):
        (tmp_path / "assets").mkdir()
        monkeypatch.chdir(tmp_path)
        resolved = get_assets_dir_path("assets", relative_to_cwd=True)
        assert resolved is not None
        assert os.path.isabs(resolved)
        assert os.path.isdir(resolved)


class TestUnsetAndEnvOverride:
    """`None`/empty stay `None`; `FLET_ASSETS_DIR` still wins and is not dropped.

    A missing env value is deliberately left intact: unlike the default, it is
    always set on purpose, so downstream is the right place to complain about
    it.
    """

    def test_none_stays_none(self):
        assert get_assets_dir_path(None) is None

    def test_empty_string_stays_falsy(self):
        # Returned as-is rather than normalised to None; every caller guards
        # with a truthiness check, so this is harmless and left alone.
        assert not get_assets_dir_path("")

    def test_env_override_wins_over_a_real_directory(self, tmp_path, monkeypatch):
        (tmp_path / "assets").mkdir()
        (tmp_path / "other").mkdir()
        monkeypatch.setenv("FLET_ASSETS_DIR", str(tmp_path / "other"))
        assert get_assets_dir_path(str(tmp_path / "assets")) == str(tmp_path / "other")

    def test_missing_env_override_is_kept(self, tmp_path, monkeypatch):
        missing = str(tmp_path / "nope")
        monkeypatch.setenv("FLET_ASSETS_DIR", missing)
        assert get_assets_dir_path(None) == missing
