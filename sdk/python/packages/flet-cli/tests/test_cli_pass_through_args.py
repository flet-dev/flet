"""
Arguments that Flet passes on to the program a command runs, given after a `--`
separator or with `--flutter-build-args` and `--pyinstaller-build-args`.
"""

import sys
import types

import pytest

import flet.utils.pip
import flet_cli.commands.pack as pack_command
import flet_cli.commands.test as test_command
from flet_cli.cli import parse_command_line

PASS_THROUGH_OPTIONS = [
    pytest.param(
        ["build", "apk"], "--flutter-build-args", "flutter_build_args", id="build"
    ),
    pytest.param(
        ["debug", "macos"], "--flutter-build-args", "flutter_build_args", id="debug"
    ),
    pytest.param(
        ["pack", "main.py"],
        "--pyinstaller-build-args",
        "pyinstaller_build_args",
        id="pack",
    ),
]
"""The commands that pass arguments to Flutter or PyInstaller, each with the
option that collects them and the attribute it sets."""


class TestSeparatedArgs:
    """
    The arguments after `--` are collected for Flutter or PyInstaller, after the
    values of `--flutter-build-args` or `--pyinstaller-build-args`.
    """

    @pytest.mark.parametrize(("command", "option", "dest"), PASS_THROUGH_OPTIONS)
    def test_are_collected(self, command, option, dest):
        """The arguments after `--` are collected as one list."""
        args = parse_command_line([*command, "--", "--first", "-s"])

        assert getattr(args, dest) == [["--first", "-s"]]

    @pytest.mark.parametrize(("command", "option", "dest"), PASS_THROUGH_OPTIONS)
    def test_follow_the_values_of_the_option(self, command, option, dest):
        """The arguments after `--` follow those given with the option."""
        args = parse_command_line([*command, f"{option}=--first", "--", "--second"])

        assert getattr(args, dest) == [["--first"], ["--second"]]

    @pytest.mark.parametrize(("command", "option", "dest"), PASS_THROUGH_OPTIONS)
    def test_empty_separator_adds_nothing(self, command, option, dest):
        """A `--` with nothing after it leaves `pyproject.toml` in effect."""
        assert getattr(parse_command_line([*command, "--"]), dest) is None

    def test_flet_options_before_the_separator_stay_with_flet(self):
        """An option before `--` is Flet's; the same one after it is Flutter's."""
        args = parse_command_line(["build", "apk", "-v", "--", "--verbose"])

        assert args.verbose == 1
        assert args.flutter_build_args == [["--verbose"]]


class TestPassThroughOptions:
    """
    `--flutter-build-args` and `--pyinstaller-build-args` need a value in every
    occurrence, and one that starts with `-` is attached with `=`.
    """

    @pytest.mark.parametrize(
        ("argv", "hint"),
        [
            pytest.param(
                ["build", "apk", "--flutter-build-args", "--verbose"],
                "--flutter-build-args=--obfuscate",
                id="flutter-flet-option",
            ),
            pytest.param(
                ["build", "apk", "--flutter-build-args", "--obfuscate"],
                "--flutter-build-args=--obfuscate",
                id="flutter-option",
            ),
            pytest.param(
                ["build", "apk", "--flutter-build-args"],
                "--flutter-build-args=--obfuscate",
                id="flutter-no-value",
            ),
            pytest.param(
                ["debug", "ios", "-d", "X", "--flutter-build-args", "--release"],
                "--flutter-build-args=--obfuscate",
                id="debug-flet-option",
            ),
            pytest.param(
                ["pack", "main.py", "--pyinstaller-build-args", "-y"],
                "--pyinstaller-build-args=--clean",
                id="pyinstaller-flet-option",
            ),
            pytest.param(
                ["pack", "main.py", "--pyinstaller-build-args", "--clean"],
                "--pyinstaller-build-args=--clean",
                id="pyinstaller-option",
            ),
            pytest.param(
                ["pack", "main.py", "--pyinstaller-build-args"],
                "--pyinstaller-build-args=--clean",
                id="pyinstaller-no-value",
            ),
        ],
    )
    def test_occurrence_without_values_is_rejected(self, argv, hint, capsys):
        """An occurrence without values fails with a hint to use `=` or `--`."""
        option = hint.split("=")[0]

        with pytest.raises(SystemExit):
            parse_command_line(argv)

        err = capsys.readouterr().err
        assert f"argument {option}: expected at least one argument" in err
        assert f"`{hint}`, or pass it after `--`" in err

    @pytest.mark.parametrize(("command", "option", "dest"), PASS_THROUGH_OPTIONS)
    def test_attached_values_are_collected(self, command, option, dest):
        """Values attached with `=` are collected, not read as Flet options."""
        args = parse_command_line(
            [*command, f"{option}=--verbose", f"{option}=--define=KEY=value"]
        )

        assert getattr(args, dest) == [["--verbose"], ["--define=KEY=value"]]
        assert args.verbose == 0

    @pytest.mark.parametrize(("command", "option", "dest"), PASS_THROUGH_OPTIONS)
    def test_is_unset_when_omitted(self, command, option, dest):
        """Without the option nothing is collected, so `pyproject.toml` is consulted."""
        assert getattr(parse_command_line(command), dest) is None


class TestPytestArgs:
    """`flet test` passes the arguments after `--` to pytest."""

    def test_are_collected(self):
        """The arguments after `--` are collected for pytest."""
        args = parse_command_line(["test", "macos", "--", "-x", "--maxfail=1"])

        assert args.pytest_args == ["-x", "--maxfail=1"]

    def test_are_empty_without_a_separator(self):
        """Without a `--` separator, no arguments are collected for pytest."""
        assert parse_command_line(["test", "macos"]).pytest_args == []

    def test_reach_pytest(self, monkeypatch, tmp_path):
        """The collected arguments are passed to pytest after the `-k` expression."""
        options = parse_command_line(
            ["test", "macos", str(tmp_path), "-k", "smoke", "--", "-x"]
        )
        cmd = options.handler.__self__
        pytest_args = []
        monkeypatch.setattr(test_command, "_provision_steps", lambda cmd: tmp_path)
        monkeypatch.setattr(
            cmd, "_run_pytest", lambda flutter_dir: pytest_args.extend(cmd.pytest_args)
        )

        with pytest.raises(SystemExit):
            options.handler(options)

        assert pytest_args == ["-k", "smoke", "-x"]


class TestProgramCommand:
    """The command of the program that is run ends with the arguments after `--`."""

    @pytest.mark.parametrize(
        ("command", "flutter_command"),
        [
            (["build", "macos"], ["flutter", "build", "macos"]),
            (["debug", "macos"], ["flutter", "run", "-d", "macos"]),
        ],
        ids=["build", "debug"],
    )
    def test_flutter_command(self, command, flutter_command, tmp_path, monkeypatch):
        """The Flutter command of `flet build` and `flet debug` ends with them."""
        flutter_args = ["--obfuscate", "--split-debug-info=build/symbols"]
        options = parse_command_line([*command, "--", *flutter_args])
        cmd = options.handler.__self__
        cmd.options = options
        cmd.verbose = 0
        cmd.flutter_exe = "flutter"
        cmd.build_dir = cmd.flutter_dir = tmp_path
        cmd.template_data = {"options": {"target_arch": None}, "split_per_abi": False}
        cmd.get_pyproject = lambda setting=None: None
        cmd.target_platform = cmd.debug_platform = cmd.device_id = "macos"
        cmd.package_platform = cmd.platforms["macos"]["package_platform"]
        cmd.config_platform = cmd.platforms["macos"]["config_platform"]
        runs = []
        monkeypatch.setattr(cmd, "_serious_python_build_env", lambda: {})
        monkeypatch.setattr(
            cmd,
            "run",
            lambda args, **kwargs: (
                runs.append(args)
                or types.SimpleNamespace(returncode=0, stdout="", stderr="")
            ),
        )

        cmd._run_flutter_command()

        assert runs[0][: len(flutter_command)] == flutter_command
        assert runs[0][-len(flutter_args) :] == flutter_args

    def test_pyinstaller_command(self, tmp_path, monkeypatch):
        """The PyInstaller command of `flet pack` ends with them."""
        pyinstaller_args = ["--clean", "--log-level=WARN"]
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
        options = parse_command_line(["pack", "main.py", "--", *pyinstaller_args])

        options.handler(options)

        assert runs[0][0] == "main.py"
        assert runs[0][-len(pyinstaller_args) :] == pyinstaller_args
