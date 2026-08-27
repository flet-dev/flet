import pytest

from flet_cli.cli import parse_command_line
from flet_cli.utils.cli import quote_for_shell


def _parse(*argv):
    """Parse a Flet command line given as separate arguments."""
    return parse_command_line(list(argv))


def test_no_script_args():
    """A plain `flet run app.py` passes nothing to the script."""
    args = _parse("run", "app.py")

    assert args.script == "app.py"
    assert args.script_args == []


def test_script_args_after_separator():
    """Arguments after `--` are forwarded to the script, options and all."""
    args = _parse("run", "app.py", "--", "--manual", "-x", "1")

    assert args.script == "app.py"
    assert args.script_args == ["--manual", "-x", "1"]


def test_flet_options_are_not_forwarded():
    """Flet's own options before `--` stay with Flet."""
    args = _parse("run", "-w", "app.py", "--", "--web")

    assert args.web is True
    assert args.script == "app.py"
    assert args.script_args == ["--web"]


def test_flet_options_between_script_and_separator():
    """Flet's options may follow the script path and precede `--`."""
    args = _parse("run", "app.py", "--web", "--port", "8080", "--", "--manual")

    assert args.web is True
    assert args.port == 8080
    assert args.script_args == ["--manual"]


def test_positional_script_args_need_no_separator():
    """Arguments that don't look like options are forwarded without `--`."""
    args = _parse("run", "app.py", "foo", "bar")

    assert args.script == "app.py"
    assert args.script_args == ["foo", "bar"]


def test_positional_and_separated_script_args_are_combined():
    """Arguments before and after `--` are forwarded in command-line order."""
    args = _parse("run", "app.py", "foo", "--", "--manual")

    assert args.script_args == ["foo", "--manual"]


def test_script_args_with_module():
    """`-m` module invocations forward script arguments too."""
    args = _parse("run", "-m", "my_app.main", "--", "--manual")

    assert args.module is True
    assert args.script == "my_app.main"
    assert args.script_args == ["--manual"]


def test_script_args_with_implicit_run_command():
    """The default `run` subcommand is applied even with a `--` separator."""
    args = _parse("app.py", "--", "--manual")

    assert args.command == "run"
    assert args.script == "app.py"
    assert args.script_args == ["--manual"]


def test_script_args_named_like_a_subcommand():
    """A script argument matching a subcommand name doesn't select it."""
    args = _parse("app.py", "--", "build", "test")

    assert args.command == "run"
    assert args.script == "app.py"
    assert args.script_args == ["build", "test"]


def test_unknown_flet_option_is_rejected(capsys):
    """A mistyped Flet option still errors instead of reaching the script."""
    with pytest.raises(SystemExit):
        _parse("run", "app.py", "--wev")

    err = capsys.readouterr().err
    assert "unrecognized arguments: --wev" in err
    # ...and the error suggests the `--` separator
    assert "flet run app.py -- --wev" in err


def test_suggested_separator_command_quotes_the_script(capsys):
    """
    The suggestion is meant to be pasted, so a script path needing quoting
    gets it - `flet run my app -- --wev` would run the wrong thing.
    """
    with pytest.raises(SystemExit):
        _parse("run", "my app.py", "--wev")

    expected = f"flet run {quote_for_shell('my app.py')} -- --wev"
    assert expected in capsys.readouterr().err


def test_suggested_separator_command_quotes_forwarded_args(capsys):
    """
    The forwarded arguments are quoted too, not just the script path. Only
    option-shaped tokens reach `unrecognized` - anything containing a space is
    read as a positional and collected into `script_args` instead - but those
    can still carry shell metacharacters.
    """
    with pytest.raises(SystemExit):
        _parse("run", "app.py", "--wev;rm")

    err = capsys.readouterr().err
    assert f"flet run app.py -- {quote_for_shell('--wev;rm')}" in err
    # The plain listing above it still shows the arguments verbatim.
    assert "unrecognized arguments: --wev;rm" in err


def test_separator_rejected_for_other_commands(capsys):
    """Only `flet run` accepts a `--` separator."""
    with pytest.raises(SystemExit):
        _parse("build", "apk", "--", "--manual")

    assert "only supported by `flet run`" in capsys.readouterr().err
