"""`--assets` resolution in `flet run`.

`--assets` defaults to `"assets"` whether or not the app has such a directory,
and the resolved path is exported to the app process as `FLET_ASSETS_DIR`.
Because an explicitly set environment variable is treated as deliberate, a
defaulted path that does not exist made the app warn

    assets_dir does not exist: /path/to/app/assets

on every `flet run --web` for an app with no assets - about a directory the
user never chose. Dropping a non-existent directory here is what keeps that
variable unset, so the warning is left for paths that really were configured.
"""

from pathlib import Path

from flet_cli.commands.run import resolve_assets_dir


class TestMissingDirectoryIsDropped:
    """Nothing is exported when the resolved directory is not there."""

    def test_defaulted_assets_dir_of_an_app_without_one(self, tmp_path):
        assert resolve_assets_dir(tmp_path, "assets") is None

    def test_missing_absolute_path(self, tmp_path):
        assert resolve_assets_dir(tmp_path, str(tmp_path / "nope")) is None

    def test_a_file_is_not_an_assets_dir(self, tmp_path):
        (tmp_path / "assets").write_text("not a directory")
        assert resolve_assets_dir(tmp_path, "assets") is None


class TestExistingDirectoryIsResolved:
    """A real directory is still found, and always returned absolute."""

    def test_relative_resolved_against_the_script_dir(self, tmp_path):
        (tmp_path / "assets").mkdir()
        resolved = resolve_assets_dir(tmp_path, "assets")
        assert resolved == str(tmp_path / "assets")
        assert Path(resolved).is_absolute()

    def test_custom_relative_name(self, tmp_path):
        (tmp_path / "media").mkdir()
        assert resolve_assets_dir(tmp_path, "media") == str(tmp_path / "media")

    def test_absolute_path_outside_the_script_dir(self, tmp_path):
        outside = tmp_path / "shared"
        outside.mkdir()
        app = tmp_path / "app"
        app.mkdir()
        assert resolve_assets_dir(app, str(outside)) == str(outside)


class TestOnlyADeliberateValueWarns:
    """The default is quiet when missing; anything else the user typed is not."""

    def test_default_is_silent(self, tmp_path, capsys):
        assert resolve_assets_dir(tmp_path, "assets") is None
        assert capsys.readouterr().out == ""

    def test_explicit_value_warns(self, tmp_path, capsys):
        assert resolve_assets_dir(tmp_path, "typo") is None
        out = capsys.readouterr().out
        assert "assets_dir does not exist" in out
        assert "typo" in out

    def test_explicit_value_that_exists_does_not_warn(self, tmp_path, capsys):
        (tmp_path / "media").mkdir()
        assert resolve_assets_dir(tmp_path, "media") is not None
        assert capsys.readouterr().out == ""


class TestUnset:
    """`None` and empty stay `None` without touching the filesystem."""

    def test_none(self, tmp_path):
        assert resolve_assets_dir(tmp_path, None) is None

    def test_empty_string(self, tmp_path):
        assert resolve_assets_dir(tmp_path, "") is None
