"""
Arguments that `flet build` and `flet debug` pass to Flutter after a `--`
separator.
"""

import types

import pytest

from flet_cli.cli import parse_command_line

FLUTTER_ARGS = ["--obfuscate", "--split-debug-info=build/symbols"]


class TestSeparatedArgs:
    """The arguments after `--` follow the values of `--flutter-build-args`."""

    @pytest.mark.parametrize(
        "command", [["build", "apk"], ["debug", "macos"]], ids=["build", "debug"]
    )
    def test_are_collected(self, command):
        """The arguments after `--` are collected for Flutter."""
        args = parse_command_line([*command, "--", *FLUTTER_ARGS])

        assert args.flutter_build_args == [FLUTTER_ARGS]

    def test_follow_the_values_of_the_option(self):
        """The arguments after `--` follow those of `--flutter-build-args`."""
        args = parse_command_line(
            ["build", "apk", "--flutter-build-args=--no-pub", "--", *FLUTTER_ARGS]
        )

        assert args.flutter_build_args == [["--no-pub"], FLUTTER_ARGS]

    def test_flet_options_before_the_separator_stay_with_flet(self):
        """An option before `--` is Flet's; the same one after it is Flutter's."""
        args = parse_command_line(["build", "apk", "-v", "--", "--verbose"])

        assert args.verbose == 1
        assert args.flutter_build_args == [["--verbose"]]

    def test_empty_separator_adds_nothing(self):
        """A `--` with nothing after it leaves `pyproject.toml` in effect."""
        assert parse_command_line(["build", "apk", "--"]).flutter_build_args is None


class TestFlutterCommand:
    """The Flutter command that is run ends with the arguments after `--`."""

    @pytest.mark.parametrize(
        ("command", "flutter_command"),
        [
            (["build", "macos"], ["flutter", "build", "macos"]),
            (["debug", "macos"], ["flutter", "run", "-d", "macos"]),
        ],
        ids=["build", "debug"],
    )
    def test_ends_with_separated_args(
        self, command, flutter_command, tmp_path, monkeypatch
    ):
        """The Flutter command of `flet build` and `flet debug` ends with them."""
        options = parse_command_line([*command, "--", *FLUTTER_ARGS])
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
        assert runs[0][-len(FLUTTER_ARGS) :] == FLUTTER_ARGS
