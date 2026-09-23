"""
Arguments that `flet pack` passes to PyInstaller, with `--pyinstaller-build-args`
or after a `--` separator.
"""

import sys
import types

import pytest

import flet.utils.pip
import flet_cli.commands.pack as pack_command
from flet_cli.cli import parse_command_line

PYINSTALLER_ARGS = ["--clean", "--log-level=WARN"]


class TestSeparatedArgs:
    """The arguments after `--` follow the values of `--pyinstaller-build-args`."""

    def test_are_collected(self):
        """The arguments after `--` are collected for PyInstaller."""
        args = parse_command_line(["pack", "main.py", "--", *PYINSTALLER_ARGS])

        assert args.pyinstaller_build_args == [PYINSTALLER_ARGS]

    def test_follow_the_values_of_the_option(self):
        """The arguments after `--` follow those of `--pyinstaller-build-args`."""
        args = parse_command_line(
            ["pack", "main.py", "--pyinstaller-build-args=--noupx", "--", "--clean"]
        )

        assert args.pyinstaller_build_args == [["--noupx"], ["--clean"]]

    def test_empty_separator_adds_nothing(self):
        """A `--` with nothing after it collects nothing."""
        args = parse_command_line(["pack", "main.py", "--"])

        assert args.pyinstaller_build_args is None


class TestPyInstallerBuildArgs:
    """
    `--pyinstaller-build-args` needs a value in every occurrence, and one that
    starts with `-` is attached with `=`.
    """

    @pytest.mark.parametrize(
        "argv",
        [
            ["pack", "main.py", "--pyinstaller-build-args", "--clean"],
            ["pack", "main.py", "--pyinstaller-build-args", "-y"],
            ["pack", "main.py", "--pyinstaller-build-args"],
        ],
        ids=["pyinstaller-option", "flet-option", "no-value"],
    )
    def test_occurrence_without_values_is_rejected(self, argv, capsys):
        """An occurrence without values fails with a hint to use `=` or `--`."""
        with pytest.raises(SystemExit):
            parse_command_line(argv)

        err = capsys.readouterr().err
        assert "argument --pyinstaller-build-args: expected at least one argument" in (
            err
        )
        assert "`--pyinstaller-build-args=--clean`, or pass it after `--`" in err


class TestPyInstallerCommand:
    """The PyInstaller command that is run ends with the arguments after `--`."""

    def test_ends_with_separated_args(self, tmp_path, monkeypatch):
        """The PyInstaller command ends with the arguments after `--`."""
        runs = []
        pyinstaller = types.ModuleType("PyInstaller")
        pyinstaller.__main__ = types.SimpleNamespace(run=runs.append)
        monkeypatch.setitem(sys.modules, "PyInstaller", pyinstaller)
        monkeypatch.setitem(sys.modules, "PyInstaller.__main__", pyinstaller.__main__)
        monkeypatch.setitem(
            sys.modules,
            "flet_cli.__pyinstaller.utils",
            types.SimpleNamespace(copy_flet_bin=lambda: None),
        )
        monkeypatch.setattr(
            flet.utils.pip, "ensure_flet_desktop_package_installed", lambda: None
        )
        monkeypatch.setattr(pack_command, "is_linux", lambda: False)
        monkeypatch.chdir(tmp_path)
        options = parse_command_line(["pack", "main.py", "--", *PYINSTALLER_ARGS])

        options.handler(options)

        assert runs[0][0] == "main.py"
        assert runs[0][-len(PYINSTALLER_ARGS) :] == PYINSTALLER_ARGS
