"""Tests for the `flet create` command."""

import os
import shlex
import subprocess
from pathlib import Path

import pytest

from flet_cli.cli import parse_command_line
from flet_cli.commands import create as create_cmd

# `flet create` falls back to downloading a template zip when the in-repo
# templates are not alongside the package; skip rather than hit the network.
_LOCAL_TEMPLATE = Path(create_cmd.__file__).resolve().parents[5] / "templates" / "app"

needs_local_template = pytest.mark.skipif(
    not _LOCAL_TEMPLATE.is_dir(),
    reason="needs the in-repo app template (otherwise `flet create` downloads one)",
)


def create_app(name, tmp_path, monkeypatch, capsys):
    """Run `flet create <name>` in `tmp_path` and return the printed lines."""
    monkeypatch.chdir(tmp_path)
    args = parse_command_line(["create", name])
    args.handler(args)
    out = capsys.readouterr().out
    return [line.strip() for line in out.splitlines() if line.strip()]


# ---------------------------------------------------------------------------
# next steps
# ---------------------------------------------------------------------------


@needs_local_template
class TestNextSteps:
    """
    `flet create` ends by printing the commands to run next, and those have to
    be commands that actually work.

    Two ways they have failed: `flet test <dir>` was printed even though
    `flet test` takes the platform as its first positional, so argparse
    rejected it; and a directory whose name needs shell quoting silently
    changed what the printed command meant (`cd my app`, `cd $demo`).
    """

    @staticmethod
    def _commands(lines):
        """The printed lines that are commands, not prose."""
        return [ln for ln in lines if ln.startswith(("cd ", "flet "))]

    def test_printed_flet_commands_parse(self, tmp_path, monkeypatch, capsys):
        """Every `flet ...` line printed as a next step is a valid command."""
        lines = create_app("sample", tmp_path, monkeypatch, capsys)
        flet_lines = [ln for ln in self._commands(lines) if ln.startswith("flet ")]

        assert flet_lines, f"no next-step commands printed: {lines}"
        for line in flet_lines:
            # Raises SystemExit(2) if argparse rejects it - which is the bug.
            parse_command_line(shlex.split(line)[1:])

    def test_next_steps_are_cd_then_bare_commands(self, tmp_path, monkeypatch, capsys):
        """
        The app directory is where `flet test` finds pytest, so the next steps
        cd into it rather than passing a path.
        """
        lines = create_app("sample", tmp_path, monkeypatch, capsys)

        assert self._commands(lines) == ["cd sample", "flet run", "flet test"]

    def test_creating_in_place_prints_no_cd(self, tmp_path, monkeypatch, capsys):
        """Creating into the current directory needs no `cd` line."""
        lines = create_app(".", tmp_path, monkeypatch, capsys)

        assert self._commands(lines) == ["flet run", "flet test"]

    @pytest.mark.parametrize("name", ["sample", "my app", "foo;bar", "$demo", "a&b"])
    def test_cd_line_reaches_the_new_directory(
        self, name, tmp_path, monkeypatch, capsys
    ):
        """
        The `cd` is meant to be pasted, so run it in a real shell and check
        where it lands.

        `shlex.split` is not enough here: it removes quotes but performs no
        expansion, so it reports `cd $demo` and `cd a&b` as correct when a
        shell would not. Only executing them distinguishes quoted from
        unquoted.
        """
        if os.name == "nt":
            pytest.skip("POSIX shell; `cmd.exe` quoting is covered by quote_for_shell")

        lines = create_app(name, tmp_path, monkeypatch, capsys)
        cd_line = next(ln for ln in self._commands(lines) if ln.startswith("cd "))

        landed = subprocess.run(
            ["/bin/sh", "-c", f"{cd_line} && pwd"],
            cwd=tmp_path,
            capture_output=True,
            text=True,
        )
        assert landed.stdout.strip() == os.path.realpath(tmp_path / name)
