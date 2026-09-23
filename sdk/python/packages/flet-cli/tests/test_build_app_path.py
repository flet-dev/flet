"""
Validation of the app path given to `flet build`, `flet debug` and `flet test`.

The path must be a directory. It is checked before the Flutter toolchain is
provisioned, so a mistyped path or a script file fails fast with a clear
message instead of crashing on `<file>/build` (#6840).
"""

import io

import pytest
from rich.console import Console

from flet_cli.cli import parse_command_line
from flet_cli.commands.flutter_base import BaseFlutterCommand


class Exit(Exception):
    """Captures `cleanup(1, message)` calls, which normally sys.exit."""

    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(f"cleanup({code}): {message}")


class Provisioned(Exception):
    """Raised by the stubbed toolchain provisioning, once the path is accepted."""


@pytest.fixture
def make_command(monkeypatch):
    """Build the command for a command line, with provisioning stubbed out."""

    def provision(self):
        raise Provisioned

    monkeypatch.setattr(BaseFlutterCommand, "initialize_command", provision)

    def make(*argv):
        options = parse_command_line(list(argv))
        cmd = options.handler.__self__
        cmd.options = options
        cmd.target_platform = "web"

        def cleanup(code, message=None, **kwargs):
            raise Exit(code, message)

        cmd.cleanup = cleanup
        return cmd

    return make


def _rejection_message(cmd):
    """Run `initialize_command()`, expecting a rejection, and return its message."""
    with pytest.raises(Exit) as exc_info:
        cmd.initialize_command()

    assert exc_info.value.code == 1
    assert cmd.skip_flutter_doctor
    return exc_info.value.message


class TestAcceptedPath:
    """A directory passes validation and goes on to provisioning."""

    def test_directory(self, make_command, tmp_path):
        cmd = make_command("build", "web", str(tmp_path))

        with pytest.raises(Provisioned):
            cmd.initialize_command()


class TestRejectedPath:
    """
    Anything but a directory is rejected before provisioning, and without
    running `flutter doctor`.
    """

    @pytest.mark.parametrize(
        "command",
        [["build", "web"], ["debug", "web"], ["test", "macos"]],
        ids=["build", "debug", "test"],
    )
    def test_script_file(self, make_command, tmp_path, command):
        script = tmp_path / "main.py"
        script.write_text("")

        message = _rejection_message(make_command(*command, str(script)))

        assert message == (
            f"Path to Flet app must be a directory, not a file: {script.resolve()}"
        )

    def test_missing_path(self, make_command, tmp_path):
        missing = tmp_path / "does-not-exist"

        message = _rejection_message(make_command("build", "web", str(missing)))

        assert message == (
            "Path to Flet app does not exist or is not a directory: "
            f"{missing.resolve()}"
        )

    def test_path_is_escaped_for_rich_markup(self, make_command, tmp_path):
        script = tmp_path / "[beta]" / "main.py"
        script.parent.mkdir()
        script.write_text("")

        message = _rejection_message(make_command("build", "web", str(script)))

        console = Console(file=io.StringIO(), width=1000, record=True)
        console.print(message)
        assert str(script.resolve()) in console.export_text()
