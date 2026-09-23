"""
Arguments that `flet test` passes to pytest.
"""

import pytest

import flet_cli.commands.test as test_command
from flet_cli.cli import parse_command_line


class TestSeparatedArgs:
    """The arguments after `--` are passed to pytest, after the `-k` expression."""

    def test_are_collected(self):
        args = parse_command_line(["test", "macos", "--", "-x", "--maxfail=1"])

        assert args.pytest_args == ["-x", "--maxfail=1"]

    def test_are_empty_without_a_separator(self):
        assert parse_command_line(["test", "macos"]).pytest_args == []

    def test_reach_pytest(self, monkeypatch, tmp_path):
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

    def test_are_rejected_by_other_commands(self, capsys):
        with pytest.raises(SystemExit):
            parse_command_line(["clean", "--", "-x"])

        assert "`--` separator is only supported by" in capsys.readouterr().err
