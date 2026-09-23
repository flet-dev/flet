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
from flet_cli.utils.cli import quote_for_shell


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


def test_directory_is_accepted(make_command, tmp_path):
    """A directory passes validation and goes on to provisioning."""
    cmd = make_command("build", "web", str(tmp_path))

    with pytest.raises(Provisioned):
        cmd.initialize_command()


def _suggestion(make_command, *argv):
    """Return the app path suggested for a command line naming a script file."""
    cmd = make_command(*argv)

    with pytest.raises(Exit) as exc_info:
        cmd.initialize_command()

    assert exc_info.value.code == 1
    assert "must be a directory, not a file" in exc_info.value.message
    return exc_info.value.message.rsplit("instead: ", 1)[1]


@pytest.mark.parametrize("command", [["build", "web"], ["debug", "web"]])
def test_script_file_suggests_its_directory(make_command, tmp_path, command):
    """A `main.py` path points the user at the directory containing it."""
    script = tmp_path / "main.py"
    script.write_text("")

    suggestion = _suggestion(make_command, *command, str(script))

    assert suggestion == quote_for_shell(str(tmp_path.resolve()))
    assert not (script / "build").exists()


def test_other_script_file_suggests_module_name(make_command, tmp_path):
    """A script other than `main.py` also needs `--module-name` to run."""
    script = tmp_path / "app.py"
    script.write_text("")

    suggestion = _suggestion(make_command, "build", "web", str(script))

    assert suggestion == f"{quote_for_shell(str(tmp_path.resolve()))} --module-name app"


def test_script_in_src_layout_suggests_project_root(make_command, tmp_path):
    """The project root is suggested when its `tool.flet.app.path` is `src`."""
    (tmp_path / "pyproject.toml").write_text('[tool.flet.app]\npath = "src"\n')
    (tmp_path / "src").mkdir()
    script = tmp_path / "src" / "main.py"
    script.write_text("")

    suggestion = _suggestion(make_command, "build", "web", str(script))

    assert suggestion == quote_for_shell(str(tmp_path.resolve()))


def test_relative_script_path_gets_relative_suggestion(
    make_command, tmp_path, monkeypatch
):
    """A relative path is answered relative to the working directory."""
    (tmp_path / "pyproject.toml").write_text('[tool.flet.app]\npath = "src"\n')
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("")
    monkeypatch.chdir(tmp_path)

    assert _suggestion(make_command, "build", "web", "src/main.py") == "."


def test_symlinked_script_suggests_its_target_directory(make_command, tmp_path):
    """A symlink to a script is answered with the directory of its target."""
    (tmp_path / "app").mkdir()
    (tmp_path / "app" / "main.py").write_text("")
    link = tmp_path / "other.py"
    try:
        link.symlink_to(tmp_path / "app" / "main.py")
    except OSError:
        pytest.skip("symlinks are not supported here")

    suggestion = _suggestion(make_command, "build", "web", str(link))

    assert suggestion == quote_for_shell(str((tmp_path / "app").resolve()))


def test_paths_are_escaped_for_rich_markup(make_command, tmp_path):
    """A directory named like a markup tag is shown, not swallowed by rich."""
    app_dir = tmp_path / "[beta]"
    app_dir.mkdir()
    (app_dir / "main.py").write_text("")
    cmd = make_command("build", "web", str(app_dir / "main.py"))

    with pytest.raises(Exit) as exc_info:
        cmd.initialize_command()

    console = Console(file=io.StringIO(), width=1000, record=True)
    console.print(exc_info.value.message)
    shown = console.export_text()
    assert str(app_dir.resolve() / "main.py") in shown
    assert f"instead: {quote_for_shell(str(app_dir.resolve()))}" in shown


def test_missing_path_fails_before_provisioning(make_command, tmp_path):
    """A mistyped path fails without provisioning or running `flutter doctor`."""
    cmd = make_command("build", "web", str(tmp_path / "does-not-exist"))

    with pytest.raises(Exit) as exc_info:
        cmd.initialize_command()

    assert exc_info.value.code == 1
    assert "does not exist or is not a directory" in exc_info.value.message
    assert cmd.skip_flutter_doctor
