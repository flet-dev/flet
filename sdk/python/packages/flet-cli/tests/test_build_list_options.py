"""
Options of `flet build`, `flet debug` and `flet test` that take several values.
"""

import argparse

import pytest

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
