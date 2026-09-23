"""
Options of `flet build`, `flet debug` and `flet test` that take several values.
"""

import argparse

import pytest

from flet_cli.cli import parse_command_line
from flet_cli.commands.build_base import BaseBuildCommand


def _list_options() -> list[argparse.Action]:
    """Return the options of the real build parser that take several values."""
    parser = argparse.ArgumentParser(add_help=False)
    BaseBuildCommand(parser)
    return [
        action
        for action in parser._actions
        if action.option_strings and action.nargs in ("+", "*")
    ]


class TestRepeatedListOption:
    """Repeating a list option keeps the values of every occurrence."""

    @pytest.mark.parametrize(
        "action", _list_options(), ids=lambda action: action.option_strings[0]
    )
    def test_keeps_every_value(self, action):
        """The values of both occurrences are kept, in order."""
        first, second = list(action.choices or ["first", "second"])[:2]
        option = action.option_strings[0]
        parser = argparse.ArgumentParser(add_help=False)
        BaseBuildCommand(parser)

        values = getattr(
            parser.parse_args([option, first, option, second]), action.dest
        )

        flattened = [
            value
            for item in values
            for value in (item if isinstance(item, list) else [item])
        ]
        assert flattened == [first, second]


class TestFlutterBuildArgs:
    """
    `--flutter-build-args` needs a value in every occurrence, and one that starts
    with `-` is attached with `=`.
    """

    @pytest.mark.parametrize(
        "argv",
        [
            ["build", "apk", "--flutter-build-args", "--verbose"],
            ["build", "apk", "--flutter-build-args", "--obfuscate"],
            ["build", "apk", "--flutter-build-args"],
            ["debug", "ios", "-d", "X", "--flutter-build-args", "--release"],
        ],
        ids=["flet-option", "flutter-option", "no-value", "debug-flet-option"],
    )
    def test_occurrence_without_values_is_rejected(self, argv, capsys):
        """An occurrence without values fails with a hint to attach it using `=`."""
        with pytest.raises(SystemExit):
            parse_command_line(argv)

        err = capsys.readouterr().err
        assert "argument --flutter-build-args: expected at least one argument" in err
        assert "`--flutter-build-args=--obfuscate`" in err

    def test_attached_values_are_collected(self):
        """Values attached with `=` are collected, not read as Flet options."""
        args = parse_command_line(
            [
                "build",
                "apk",
                "--flutter-build-args=--verbose",
                "--flutter-build-args=--dart-define=API_URL=https://example.com",
            ]
        )

        assert args.flutter_build_args == [
            ["--verbose"],
            ["--dart-define=API_URL=https://example.com"],
        ]
        assert args.verbose == 0

    def test_is_unset_when_omitted(self):
        """Without the option nothing is collected, so `pyproject.toml` is consulted."""
        assert parse_command_line(["build", "apk"]).flutter_build_args is None
