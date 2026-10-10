"""
`--log-format {rich,plain,github}` of the Flutter-based commands.

`rich` and `plain` output must not change; `github` adds GitHub Actions
workflow commands: a `::group::` per build step and `::warning::`/`::error::`
annotations.
"""

import argparse
import io
from types import SimpleNamespace

import pytest
from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme

from flet_cli.commands import flutter_base
from flet_cli.commands.build import Command as BuildCommand
from flet_cli.commands.flutter_base import (
    BaseFlutterCommand,
    error_style,
    output,
    warning_style,
)
from flet_cli.utils.log_format import (
    CliOutput,
    detect_log_format,
    escape_data,
    escape_property,
    resolve_log_format,
    step_title,
    workflow_command,
)


def _console(terminal: bool) -> tuple[io.StringIO, Console]:
    """A console configured like the shared CLI console, recording to a buffer."""
    buffer = io.StringIO()
    return buffer, Console(
        file=buffer,
        log_path=False,
        log_time=False,
        theme=Theme({"log.message": "green bold"}),
        force_terminal=terminal,
        color_system="truecolor" if terminal else None,
        width=100,
    )


@pytest.fixture
def github(monkeypatch):
    """Switch the shared output to `github`, recording what it prints."""
    buffer, console = _console(terminal=False)
    monkeypatch.setattr(output, "console", console)
    monkeypatch.setattr(output, "format", "github")
    monkeypatch.setattr(output, "_group", None)
    monkeypatch.setattr(output, "_failed_group", None)
    return buffer


class _Live:
    """Stand-in for `rich.live.Live`: `cleanup()` only updates it."""

    def __init__(self):
        self.renderables = []

    def update(self, renderable, refresh=False):
        self.renderables.append(renderable)


def _command(**attrs) -> BaseFlutterCommand:
    cmd = BaseFlutterCommand.__new__(BaseFlutterCommand)
    cmd.live = _Live()
    cmd.no_rich_output = True
    cmd.skip_flutter_doctor = True
    cmd.current_platform = "Linux"
    cmd.statuses = []
    cmd.update_status = cmd.statuses.append
    for name, value in attrs.items():
        setattr(cmd, name, value)
    return cmd


class TestEscaping:
    def test_data(self):
        assert escape_data("100% done\r\nnext: a,b") == "100%25 done%0D%0Anext: a,b"

    def test_property(self):
        assert (
            escape_property("100% done\r\nnext: a,b")
            == "100%25 done%0D%0Anext%3A a%2Cb"
        )

    def test_percent_is_escaped_first(self):
        # A literal "%0A" must not turn into a newline when GitHub decodes it.
        assert escape_data("%0A") == "%250A"
        assert escape_property("%3A") == "%253A"

    def test_command_with_properties(self):
        assert (
            workflow_command(
                "warning",
                "line 1\nline 2",
                title="Icon: 512x512, not 1024",
                file="assets/icon.png",
                line=3,
            )
            == "::warning title=Icon%3A 512x512%2C not 1024,file=assets/icon.png,"
            "line=3::line 1%0Aline 2"
        )

    def test_command_omits_unset_properties(self):
        assert workflow_command("error", "boom", title=None, file=None) == (
            "::error::boom"
        )
        assert workflow_command("endgroup") == "::endgroup::"


class TestResolveLogFormat:
    def test_default_is_rich(self):
        assert resolve_log_format(None, False, {}) == "rich"

    @pytest.mark.parametrize("value", ["rich", "plain", "github", "GitHub"])
    def test_cli_value(self, value):
        assert resolve_log_format(value, False, {}) == value.lower()

    def test_env_value(self):
        assert resolve_log_format(None, False, {"FLET_CLI_LOG_FORMAT": "github"}) == (
            "github"
        )

    def test_cli_wins_over_env(self):
        env = {"FLET_CLI_LOG_FORMAT": "github"}
        assert resolve_log_format("plain", False, env) == "plain"

    @pytest.mark.parametrize(
        "no_rich, env",
        [(True, {}), (False, {"FLET_CLI_NO_RICH_OUTPUT": "1"})],
    )
    def test_no_rich_output_is_plain(self, no_rich, env):
        assert resolve_log_format(None, no_rich, env) == "plain"

    def test_no_rich_output_keeps_github(self):
        assert resolve_log_format("github", True, {}) == "github"

    def test_falsy_no_rich_output_env(self):
        assert resolve_log_format(None, False, {"FLET_CLI_NO_RICH_OUTPUT": "0"}) == (
            "rich"
        )

    def test_invalid_env_value(self):
        with pytest.raises(ValueError, match="FLET_CLI_LOG_FORMAT"):
            resolve_log_format(None, False, {"FLET_CLI_LOG_FORMAT": "json"})


class TestDetectLogFormat:
    @pytest.mark.parametrize(
        "argv, expected",
        [
            (["flet", "build", "apk"], "rich"),
            (["flet", "build", "apk", "--log-format", "github"], "github"),
            (["flet", "build", "apk", "--log-format=plain"], "plain"),
            (["flet", "build", "apk", "--no-rich-output"], "plain"),
            # Arguments after `--` belong to `flutter build`.
            (["flet", "build", "apk", "--", "--log-format", "github"], "rich"),
            # Invalid values are left for argparse to report.
            (["flet", "build", "apk", "--log-format", "json"], "rich"),
        ],
    )
    def test_argv(self, argv, expected):
        assert detect_log_format(argv, {}) == expected

    def test_env(self):
        assert detect_log_format(["flet"], {"FLET_CLI_LOG_FORMAT": "github"}) == (
            "github"
        )


class TestOption:
    def _parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(prog="flet build")
        BuildCommand(parser)
        return parser

    def test_listed_in_build_help(self):
        # Build agents detect support for the option from `flet build --help`.
        assert "--log-format {rich,plain,github}" in self._parser().format_help()

    @pytest.mark.parametrize(
        "args, expected",
        [
            ([], "rich"),
            (["--log-format", "github"], "github"),
            (["--log-format", "PLAIN"], "plain"),
            (["--no-rich-output"], "plain"),
        ],
    )
    def test_handle(self, monkeypatch, args, expected):
        monkeypatch.delenv("FLET_CLI_LOG_FORMAT", raising=False)
        monkeypatch.delenv("FLET_CLI_NO_RICH_OUTPUT", raising=False)
        monkeypatch.setattr(output, "format", output.format)
        options = self._parser().parse_args(["apk", *args])
        cmd = BuildCommand(argparse.ArgumentParser())
        BaseFlutterCommand.handle(cmd, options)
        assert cmd.log_format == expected
        assert output.format == expected
        assert cmd.no_rich_output == (expected != "rich")

    def test_invalid_choice(self, capsys):
        with pytest.raises(SystemExit):
            self._parser().parse_args(["apk", "--log-format", "json"])
        assert "invalid choice" in capsys.readouterr().err


class TestStepTitle:
    @pytest.mark.parametrize(
        "status, title",
        [
            ("[bold blue]Generating app icons...", "Generating app icons"),
            (
                "[bold blue]Building [cyan]Android App Bundle (.aab)[/cyan]...",
                "Building Android App Bundle (.aab)",
            ),
            ("Packaging Python app…", "Packaging Python app"),
            (
                "[bold blue]Notarizing [cyan]app.app[/cyan] (slow)...",
                "Notarizing app.app (slow)",
            ),
        ],
    )
    def test_strips_markup_and_ellipsis(self, status, title):
        assert step_title(status) == title


class TestRichAndPlainUnchanged:
    """`warn()` prints exactly what the `console.log` calls it replaced did."""

    MESSAGES = [
        'icon_background "#zz" is not a valid colour (expected #rrggbb); using white.',
        "Skipping rename of [cyan]app-release.apk[/cyan] because it exists.",
        "x" * 250,
    ]

    @pytest.mark.parametrize("terminal", [True, False], ids=["rich", "plain"])
    @pytest.mark.parametrize("message", MESSAGES)
    def test_warning(self, terminal, message):
        before, console = _console(terminal)
        console.log(f"Warning: {message}", style=warning_style)
        after, console = _console(terminal)
        CliOutput(console, "rich", warning_style=warning_style).warn(
            message, title="ignored", file="ignored.png", line=1
        )
        assert after.getvalue() == before.getvalue()

    @pytest.mark.parametrize("terminal", [True, False], ids=["rich", "plain"])
    def test_warning_without_markup(self, terminal):
        message = '.env not packaged; use `include = [".env"]` under [tool.flet.app]'
        before, console = _console(terminal)
        console.log(f"Warning: {message}", style=warning_style, markup=False)
        after, console = _console(terminal)
        CliOutput(console, "plain", warning_style=warning_style).warn(
            message, markup=False
        )
        assert after.getvalue() == before.getvalue()

    @pytest.mark.parametrize("terminal", [True, False], ids=["rich", "plain"])
    def test_warning_without_prefix(self, terminal):
        message = "Flutter SDK not found or invalid version installed."
        before, console = _console(terminal)
        console.log(message, style=warning_style)
        after, console = _console(terminal)
        CliOutput(console, "rich", warning_style=warning_style).warn(message, prefix="")
        assert after.getvalue() == before.getvalue()

    @pytest.mark.parametrize("terminal", [True, False], ids=["rich", "plain"])
    def test_warning_panel(self, terminal):
        message = "This build will generate an .xcarchive (Xcode Archive)."
        before, console = _console(terminal)
        console.print(Panel(message, style=warning_style))
        after, console = _console(terminal)
        CliOutput(console, "rich", warning_style=warning_style).warn(
            message, panel=True
        )
        assert after.getvalue() == before.getvalue()

    @pytest.mark.parametrize("terminal", [True, False], ids=["rich", "plain"])
    def test_error(self, terminal):
        message = "Gradle task bundleRelease failed"
        before, console = _console(terminal)
        console.log(message, style=error_style)
        after, console = _console(terminal)
        CliOutput(console, "rich", error_style=error_style).error(message)
        assert after.getvalue() == before.getvalue()

    @pytest.mark.parametrize("log_format", ["rich", "plain"])
    def test_step_updates_status(self, monkeypatch, log_format):
        buffer, console = _console(terminal=False)
        monkeypatch.setattr(output, "console", console)
        monkeypatch.setattr(output, "format", log_format)
        cmd = _command()
        with cmd.step("[bold blue]Generating app icons..."):
            pass
        assert cmd.statuses == ["[bold blue]Generating app icons..."]
        assert buffer.getvalue() == ""


class TestGithub:
    def test_warning(self, github):
        _command().warn(
            "icon source is 512x256, not square.\nSupply a square image.",
            title="App icon",
            file="assets/icon.png",
            line=1,
        )
        assert github.getvalue() == (
            "::warning title=App icon,file=assets/icon.png,line=1::"
            "icon source is 512x256, not square.%0ASupply a square image.\n"
        )

    def test_warning_strips_markup(self, github):
        _command().warn("Skipping [cyan]app.apk[/cyan]", prefix="")
        assert github.getvalue() == "::warning::Skipping app.apk\n"

    def test_warning_keeps_brackets_without_markup(self, github):
        _command().warn("see [tool.flet.app]", markup=False)
        assert github.getvalue() == "::warning::see [tool.flet.app]\n"

    def test_long_warning_is_one_line(self, github):
        _command().warn("x" * 500)
        assert github.getvalue() == f"::warning::{'x' * 500}\n"

    def test_panel_warning_is_an_annotation(self, github):
        _command().warn("Unsigned build.", title="iOS signing", panel=True)
        assert github.getvalue() == "::warning title=iOS signing::Unsigned build.\n"

    def test_error(self, github):
        _command().error("Failed: a, b", title="flutter build", file="main.py")
        assert github.getvalue() == (
            "::error title=flutter build,file=main.py::Failed: a, b\n"
        )

    def test_step_is_a_group(self, github):
        cmd = _command()
        with cmd.step("[bold blue]Generating app icons..."):
            output.console.print("Generated app icons OK")
        assert cmd.statuses == []
        assert github.getvalue() == (
            "::group::Generating app icons\nGenerated app icons OK\n::endgroup::\n"
        )

    def test_group_closed_on_exception(self, github):
        cmd = _command()
        with pytest.raises(RuntimeError), cmd.step("Packaging Python app..."):
            raise RuntimeError("boom")
        assert github.getvalue() == "::group::Packaging Python app\n::endgroup::\n"
        assert output.group_title is None

    def test_nested_steps_do_not_nest_groups(self, github):
        # GitHub Actions does not nest groups: the inner step closes the outer
        # group, and the outer step's exit then closes nothing.
        cmd = _command()
        with cmd.step("Signing [cyan]app.app[/cyan]..."):
            output.console.print("Signed")
            with cmd.step("Notarizing [cyan]app.app[/cyan]..."):
                output.console.print("Notarized")
        assert github.getvalue() == (
            "::group::Signing app.app\nSigned\n::endgroup::\n"
            "::group::Notarizing app.app\nNotarized\n::endgroup::\n"
        )

    def test_cleanup_failure_inside_step(self, github):
        cmd = _command()
        with (
            pytest.raises(SystemExit) as exit_info,
            cmd.step("[bold blue]Building [cyan]Android App Bundle[/cyan]..."),
        ):
            cmd.cleanup(1, "Gradle task bundleRelease failed\nwith exit code 1")
        assert exit_info.value.code == 1
        assert github.getvalue() == (
            "::group::Building Android App Bundle\n"
            "::error title=Building Android App Bundle::"
            "Gradle task bundleRelease failed%0Awith exit code 1\n"
            "::endgroup::\n"
        )
        # The error panel is still rendered, as in `plain`.
        assert isinstance(cmd.live.renderables[-1], Panel)

    def test_cleanup_failure_after_step_raised(self, github):
        # An exception caught outside the step that raised it is still
        # attributed to that step.
        cmd = _command()
        with pytest.raises(SystemExit):
            try:
                with cmd.step("Notarizing app.app..."):
                    raise ValueError("notarization rejected")
            except ValueError as e:
                cmd.cleanup(1, str(e))
        assert github.getvalue() == (
            "::group::Notarizing app.app\n::endgroup::\n"
            "::error title=Notarizing app.app::notarization rejected\n"
        )

    def test_cleanup_failure_outside_step(self, github):
        with pytest.raises(SystemExit):
            _command().cleanup(1, "Path to Flet app must be a directory")
        assert github.getvalue() == "::error::Path to Flet app must be a directory\n"

    def test_cleanup_default_message(self, github):
        with pytest.raises(SystemExit):
            _command().cleanup(2)
        assert github.getvalue() == (
            "::error::Error building Flet app - see the log of failed command above.\n"
        )

    def test_cleanup_strips_markup(self, github):
        with pytest.raises(SystemExit):
            _command().cleanup(1, "Build output not found in [cyan]build/x[/cyan]")
        assert github.getvalue() == "::error::Build output not found in build/x\n"

    def test_cleanup_success_prints_no_commands(self, github):
        with pytest.raises(SystemExit) as exit_info:
            _command().cleanup(0, "Successfully built your app!")
        assert exit_info.value.code == 0
        assert github.getvalue() == ""

    def test_flutter_doctor_is_a_group(self, github):
        cmd = _command(skip_flutter_doctor=False)
        cmd.run_flutter_doctor = lambda: output.console.print("Doctor summary")
        with pytest.raises(SystemExit), cmd.step("Building app..."):
            cmd.cleanup(1, "Build failed")
        assert github.getvalue() == (
            "::group::Building app\n"
            "::error title=Building app::Build failed\n"
            "::endgroup::\n"
            "::group::Running Flutter doctor\nDoctor summary\n::endgroup::\n"
        )

    def test_build_snapshot(self, github):
        """A typical build: one group per step, annotations where they occur."""
        cmd = _command(emojis={"checkmark": "OK"})
        log = output.console.print
        with cmd.step("[bold blue]Creating app shell from template..."):
            log("Created app shell OK")
        with cmd.step("[bold blue]Packaging Python app..."):
            cmd.warn(
                ".env not packaged. Package it with `--include .env`.",
                title="App package",
                markup=False,
            )
            log("Packaged Python app OK")
        with cmd.step("[bold blue]Generating app icons..."):
            cmd.warn(
                "icon source is 512x256, not square.",
                title="App icon",
                file="assets/icon.png",
            )
            log("Generated app icons OK")
        with (
            pytest.raises(SystemExit),
            cmd.step("[bold blue]Building [cyan]Android App Bundle[/cyan]..."),
        ):
            log("Running Gradle task 'bundleRelease'...")
            cmd.cleanup(1)
        assert github.getvalue().splitlines() == [
            "::group::Creating app shell from template",
            "Created app shell OK",
            "::endgroup::",
            "::group::Packaging Python app",
            "::warning title=App package::"
            ".env not packaged. Package it with `--include .env`.",
            "Packaged Python app OK",
            "::endgroup::",
            "::group::Generating app icons",
            "::warning title=App icon,file=assets/icon.png::"
            "icon source is 512x256, not square.",
            "Generated app icons OK",
            "::endgroup::",
            "::group::Building Android App Bundle",
            "Running Gradle task 'bundleRelease'...",
            "::error title=Building Android App Bundle::"
            "Error building Flet app - see the log of failed command above.",
            "::endgroup::",
        ]


def test_find_platform_image_warning_in_github(github, tmp_path):
    """`find_platform_image` warns through the shared output, no command needed."""
    from flet_cli.commands.build_base import BaseBuildCommand

    assets = tmp_path / "assets"
    assets.mkdir()
    (assets / "icon.svg").write_bytes(b"<svg/>")
    fake_self = SimpleNamespace(target_platform="web", verbose=0)
    hash = SimpleNamespace(update=lambda *_: None)
    assert BaseBuildCommand.find_platform_image(fake_self, assets, "icon", hash) is None
    line = github.getvalue()
    assert line.startswith("::warning title=Image,file=")
    assert line.rstrip("\n").endswith(
        '::"icon.svg" is a vector (SVG) image and cannot be used for "icon". '
        'Provide a raster "icon.png" to customize it — using the default for now.'
    )


def test_module_console_matches_detected_format():
    # The shared console is plain whenever the detected format is not `rich`.
    assert flutter_base.no_rich_output == (flutter_base.log_format != "rich")
