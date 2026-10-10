"""
Output formats of the Flutter-based CLI commands (`flet build`, `flet debug`,
`flet test`, ...).

* `rich` - interactive output: a live spinner shows the current step.
* `plain` - plain text lines, no color or animation (`--no-rich-output`).
* `github` - `plain` plus GitHub Actions workflow commands: every build step
  is a collapsible `::group::` and warnings/errors are `::warning::`/`::error::`
  annotations. See
  https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands
"""

import contextlib
import itertools
import os
from collections.abc import Generator, Mapping, Sequence
from typing import Any, Optional, Union

from rich.console import Console
from rich.errors import MarkupError
from rich.panel import Panel
from rich.style import Style
from rich.text import Text

LOG_FORMATS = ("rich", "plain", "github")
LOG_FORMAT_ENV_VAR = "FLET_CLI_LOG_FORMAT"
NO_RICH_OUTPUT_ENV_VAR = "FLET_CLI_NO_RICH_OUTPUT"

StyleType = Union[str, Style, None]


def escape_data(value: Any) -> str:
    """
    Escape the message part of a workflow command.

    Args:
        value: The message; converted to `str`.

    Returns:
        The message with `%`, `\\r` and `\\n` percent-encoded.
    """

    return str(value).replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def escape_property(value: Any) -> str:
    """
    Escape a property value (`title=`, `file=`, ...) of a workflow command.

    Args:
        value: The property value; converted to `str`.

    Returns:
        The value escaped like a message, with `:` and `,` also encoded.
    """

    return escape_data(value).replace(":", "%3A").replace(",", "%2C")


def workflow_command(command: str, message: Any = "", **properties: Any) -> str:
    """
    Format a GitHub Actions workflow command line.

    Args:
        command: The command name, such as `group` or `warning`.
        message: The command message.
        **properties: Command properties, in order; `None` values are omitted.

    Returns:
        A line like `::warning title=Icon,line=3::message`.
    """

    props = ",".join(
        f"{name}={escape_property(value)}"
        for name, value in properties.items()
        if value is not None
    )
    return f"::{command}{' ' + props if props else ''}::{escape_data(message)}"


def _truthy(value: Optional[str]) -> bool:
    # Same truthy values as `flet.utils.platform_utils.get_bool_env_var()`.
    return (value or "").lower() in ("true", "1", "yes")


def resolve_log_format(
    cli_value: Optional[str] = None,
    no_rich_output: bool = False,
    env: Optional[Mapping[str, str]] = None,
) -> str:
    """
    Resolve the output format from the CLI option and the environment.

    `--log-format` wins over `FLET_CLI_LOG_FORMAT`. `--no-rich-output` and
    `FLET_CLI_NO_RICH_OUTPUT` are aliases of `plain`: they turn the default
    `rich` format into `plain` and leave an explicit `plain` or `github`
    alone.

    Args:
        cli_value: The `--log-format` value, if given.
        no_rich_output: Whether `--no-rich-output` was given.
        env: Environment variables; defaults to an empty mapping.

    Returns:
        One of `LOG_FORMATS`.

    Raises:
        ValueError: When the selected format is not one of `LOG_FORMATS`.
    """

    env = env or {}
    log_format = (cli_value or env.get(LOG_FORMAT_ENV_VAR) or "rich").strip().lower()
    if log_format not in LOG_FORMATS:
        source = "--log-format" if cli_value else LOG_FORMAT_ENV_VAR
        raise ValueError(
            f"Invalid {source} value {log_format!r}; "
            f"expected one of: {', '.join(LOG_FORMATS)}."
        )
    if log_format == "rich" and (
        no_rich_output or _truthy(env.get(NO_RICH_OUTPUT_ENV_VAR))
    ):
        return "plain"
    return log_format


def detect_log_format(argv: Sequence[str], env: Mapping[str, str]) -> str:
    """
    Resolve the output format straight from the raw command line.

    The shared console is created at import time, before argparse runs, so the
    options that turn rich output off are looked up in `argv` here. Arguments
    after `--` are passed down to Flutter and are ignored. Never raises: an
    invalid value falls back to `rich` and is reported once argparse or
    `resolve_log_format()` sees it.

    Args:
        argv: The process arguments, usually `sys.argv`.
        env: Environment variables, usually `os.environ`.

    Returns:
        One of `LOG_FORMATS`.
    """

    cli_value = None
    no_rich_output = False
    for i, arg in enumerate(argv):
        if arg == "--":
            break
        if arg == "--no-rich-output":
            no_rich_output = True
        elif arg == "--log-format" and i + 1 < len(argv):
            cli_value = argv[i + 1]
        elif arg.startswith("--log-format="):
            cli_value = arg.split("=", 1)[1]
    try:
        return resolve_log_format(cli_value, no_rich_output, env)
    except ValueError:
        no_rich_output = no_rich_output or _truthy(env.get(NO_RICH_OUTPUT_ENV_VAR))
        return "plain" if no_rich_output else "rich"


def step_title(status: str) -> str:
    """
    Turn a rich status message into a plain step title.

    Args:
        status: A status message such as `[bold blue]Generating app icons...`.

    Returns:
        The text without markup and trailing ellipsis: `Generating app icons`.
    """

    title = plain_text(status).strip()
    for suffix in ("...", "…"):
        if title.endswith(suffix):
            title = title[: -len(suffix)].rstrip()
    return title


def annotation_path(path: Union[str, os.PathLike]) -> str:
    """
    Format a path for the `file=` property of an annotation.

    GitHub matches annotation files against the repository checkout, which is
    the working directory of a typical `flet build` step, so paths under the
    working directory are made relative to it.

    Args:
        path: The file path.

    Returns:
        The path relative to the working directory when it is inside it,
            otherwise the absolute path; always with `/` separators.
    """

    absolute = os.path.abspath(path)
    try:
        relative = os.path.relpath(absolute)
    except ValueError:  # another drive on Windows
        relative = None
    if relative is not None and not (
        relative == os.pardir or relative.startswith(os.pardir + os.sep)
    ):
        absolute = relative
    return absolute.replace(os.sep, "/")


class GithubLogConsole(Console):
    """
    Console for `github` output: `log()` writes plain lines.

    Rich's `log()` lays lines out in a table with a time column — repeated
    times are left blank, so continuation lines look indented — and wraps
    them at the console width (80 columns without a terminal). On GitHub
    Actions both are noise: the log viewer has its own timestamps and wraps
    long lines itself. So `log()` prints like `print(..., soft_wrap=True)`.
    """

    def log(  # type: ignore[override]
        self,
        *objects: Any,
        sep: str = " ",
        end: str = "\n",
        style: StyleType = None,
        justify: Any = None,
        emoji: Optional[bool] = None,
        markup: Optional[bool] = None,
        highlight: Optional[bool] = None,
        log_locals: bool = False,
        _stack_offset: int = 1,
    ) -> None:
        self.print(
            *objects,
            sep=sep,
            end=end,
            style=style,
            justify=justify,
            emoji=emoji,
            markup=markup,
            highlight=highlight,
            soft_wrap=True,
        )


def plain_text(message: Any, markup: bool = True) -> str:
    """
    Render a console message as plain text.

    Args:
        message: The message; rich markup is stripped when `markup` is true.
        markup: Whether `message` contains rich markup.

    Returns:
        The plain text of the message.
    """

    if isinstance(message, Text):
        return message.plain
    text = str(message)
    if not markup:
        return text
    try:
        return Text.from_markup(text).plain
    except MarkupError:
        return text


class CliOutput:
    """
    Renders steps, warnings and errors in the selected log format.

    One instance is shared by the process, next to the shared rich console.
    In the `github` format it tracks the open `::group::`: GitHub Actions does
    not nest groups, so opening a group closes the previous one, and closing
    a group that was already closed that way is a no-op.
    """

    def __init__(
        self,
        console: Console,
        log_format: str = "rich",
        warning_style: StyleType = None,
        error_style: StyleType = None,
    ):
        self.console = console
        self.format = log_format
        self.warning_style = warning_style
        self.error_style = error_style
        self._group_ids = itertools.count(1)
        self._group: Optional[tuple[int, str]] = None
        self._failed_group: Optional[str] = None

    @property
    def github(self) -> bool:
        """Whether GitHub Actions workflow commands are emitted."""
        return self.format == "github"

    @property
    def group_title(self) -> Optional[str]:
        """Title of the open `github` group, or `None`."""
        return self._group[1] if self._group else None

    @property
    def error_title(self) -> Optional[str]:
        """
        Title for an error annotation: the open group, or else the group an
        exception has just left - a failure caught outside the step that
        raised it is still attributed to that step.
        """
        return self.group_title or self._failed_group

    def command(self, command: str, message: Any = "", **properties: Any) -> None:
        """
        Print a workflow command on a line of its own.

        Args:
            command: The command name.
            message: The command message.
            **properties: Command properties; `None` values are omitted.
        """

        self.console.print(
            workflow_command(command, message, **properties),
            markup=False,
            highlight=False,
            emoji=False,
            soft_wrap=True,
        )

    def start_group(self, title: str) -> int:
        """
        Open a `::group::`, closing the one that is still open.

        Args:
            title: The group title.

        Returns:
            A token to pass to `end_group()`.
        """

        if self._group:
            self.command("endgroup")
        self._failed_group = None
        group_id = next(self._group_ids)
        self._group = (group_id, title)
        self.command("group", title)
        return group_id

    def end_group(self, group_id: int) -> None:
        """
        Close the group opened with `group_id` if it is still the open one.

        Args:
            group_id: The token returned by `start_group()`.
        """

        if self._group and self._group[0] == group_id:
            self._group = None
            self.command("endgroup")

    @contextlib.contextmanager
    def group(self, title: str) -> Generator[None, None, None]:
        """
        Wrap a block in a `::group::`; it is closed even when the block raises.

        Args:
            title: The group title.
        """

        group_id = self.start_group(title)
        try:
            yield
        except Exception:
            self._failed_group = title
            raise
        finally:
            self.end_group(group_id)

    def warn(
        self,
        message: Any,
        title: Optional[str] = None,
        file: Optional[str] = None,
        line: Optional[int] = None,
        *,
        prefix: str = "Warning: ",
        markup: bool = True,
        style: StyleType = None,
        panel: bool = False,
    ) -> None:
        """
        Report a warning.

        `rich`/`plain`: logs `<prefix><message>` in the warning style (or
        prints it in a panel). `github`: emits a `::warning::` annotation.

        Args:
            message: The warning text.
            title: Annotation title (`github` only).
            file: File the annotation points to (`github` only).
            line: Line in `file` (`github` only).
            prefix: Text put before `message` in `rich`/`plain` output.
            markup: Whether `message` contains rich markup.
            style: Overrides the warning style in `rich` output.
            panel: Print the warning in a panel in `rich`/`plain` output.
        """

        if self.github:
            self.command(
                "warning",
                plain_text(message, markup),
                title=title,
                file=file,
                line=line,
            )
        elif panel:
            self.console.print(Panel(message, style=style or self.warning_style))
        else:
            self.console.log(
                f"{prefix}{message}",
                style=style or self.warning_style,
                markup=markup,
            )

    def error(
        self,
        message: Any,
        title: Optional[str] = None,
        file: Optional[str] = None,
        line: Optional[int] = None,
        *,
        prefix: str = "",
        markup: bool = True,
    ) -> None:
        """
        Report an error.

        `rich`/`plain`: logs `<prefix><message>` in the error style.
        `github`: emits an `::error::` annotation.

        Args:
            message: The error text.
            title: Annotation title (`github` only).
            file: File the annotation points to (`github` only).
            line: Line in `file` (`github` only).
            prefix: Text put before `message` in `rich`/`plain` output.
            markup: Whether `message` contains rich markup.
        """

        if self.github:
            self.command(
                "error",
                plain_text(message, markup),
                title=title,
                file=file,
                line=line,
            )
        else:
            self.console.log(
                f"{prefix}{message}", style=self.error_style, markup=markup
            )
