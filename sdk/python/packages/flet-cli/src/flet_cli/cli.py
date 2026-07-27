import argparse
import json
import sys
from typing import Optional

import flet.version
import flet_cli.commands.build
import flet_cli.commands.clean
import flet_cli.commands.create
import flet_cli.commands.debug
import flet_cli.commands.devices
import flet_cli.commands.doctor
import flet_cli.commands.emulators
import flet_cli.commands.pack
import flet_cli.commands.publish
import flet_cli.commands.run
import flet_cli.commands.serve
import flet_cli.commands.test
from flet_cli.utils.linux_deps import linux_dependencies


def _version_info() -> dict:
    """Build the machine-readable `flet --version --json` document.

    Exposes Flet/Flutter versions and the Linux build dependencies. The
    supported Python/Pyodide set is no longer surfaced here — it now comes from
    python-build's manifest (see `flet_cli.utils.python_versions`).
    """
    return {
        "flet": flet.version.flet_version,
        "flutter": flet.version.flutter_version,
        "linux_dependencies": list(linux_dependencies),
    }


def _render_version(as_json: bool) -> str:
    """Render `flet --version` output as JSON or the human-readable text block."""
    if as_json:
        return json.dumps(_version_info(), indent=2)
    return f"Flet: {flet.version.flet_version}\nFlutter: {flet.version.flutter_version}"


# Source https://stackoverflow.com/a/26379693
def set_default_subparser(
    parser: argparse.ArgumentParser, name: str, args: list
) -> list:
    """
    Prepend a default subparser name when the command line doesn't name one.
    This should be called after setting up the argument parser but before
    `parse_args()`.

    Args:
        parser: The root argument parser.
        name: The name of the default subparser to use.
        args: The command-line arguments, without the program name.

    Returns:
        `args`, with the default subparser name prepended when applicable.
    """

    # exit if no arguments, or help or version flags are present
    if not args or any(flag in args for flag in {"-h", "--help", "-V", "--version"}):
        return args

    # all subparser actions
    subparser_actions = [
        action
        for action in parser._subparsers._actions
        if isinstance(action, argparse._SubParsersAction)
    ]

    # all subparser names
    subparser_names = [
        sp_name for action in subparser_actions for sp_name in action._name_parser_map
    ]

    # if an existing subparser is provided, skip setting a default
    if any(arg in subparser_names for arg in args):
        return args

    # if the default subparser doesn't exist, register it in the first subparser action
    if (name not in subparser_names) and subparser_actions:
        subparser_actions[0].add_parser(name)

    return [name, *args]


def get_parser() -> argparse.ArgumentParser:
    """Construct and return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # add version flags
    parser.add_argument(
        "--version",
        "-V",
        action="store_true",
        help="show version information and exit",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="with --version, output version information as JSON",
    )

    sp = parser.add_subparsers(dest="command")

    # register subcommands
    flet_cli.commands.create.Command.register_to(sp, "create")
    flet_cli.commands.run.Command.register_to(sp, "run")
    flet_cli.commands.build.Command.register_to(sp, "build")
    flet_cli.commands.clean.Command.register_to(sp, "clean")
    flet_cli.commands.debug.Command.register_to(sp, "debug")
    flet_cli.commands.test.Command.register_to(sp, "test")
    flet_cli.commands.pack.Command.register_to(sp, "pack")
    flet_cli.commands.publish.Command.register_to(sp, "publish")
    flet_cli.commands.serve.Command.register_to(sp, "serve")
    flet_cli.commands.emulators.Command.register_to(sp, "emulators")
    flet_cli.commands.devices.Command.register_to(sp, "devices")
    flet_cli.commands.doctor.Command.register_to(sp, "doctor")

    # Register MCP command only if flet-mcp is installed
    try:
        from importlib import import_module

        import_module("flet_mcp")
        mcp_cmd = import_module("flet_cli.commands.mcp")
        mcp_cmd.Command.register_to(sp, "mcp")
    except ImportError:
        pass

    return parser


def split_script_args(argv: list) -> tuple[list, Optional[list]]:
    """
    Split a command line at the first bare `--` separator.

    Everything after the separator is meant for the app script, not for Flet
    itself, so it must be removed before the parser (and `set_default_subparser`)
    sees it - otherwise `flet run app.py -- --web` would be read as Flet's own
    `--web` option, and `flet app.py -- build` would suppress the default `run`
    subcommand.

    Args:
        argv: Command-line arguments, without the program name.

    Returns:
        A `(argv, script_args)` tuple, where `script_args` is `None` when no
        `--` separator is present.
    """
    try:
        index = argv.index("--")
    except ValueError:
        return argv, None
    return argv[:index], argv[index + 1 :]


def parse_command_line(argv: list) -> argparse.Namespace:
    """
    Parse a Flet command line into the namespace passed to a command handler.

    Exits the process with a usage message when the command line is invalid.

    Args:
        argv: Command-line arguments, without the program name.

    Returns:
        The parsed arguments. For `flet run`, `script_args` holds the arguments
        to forward to the app script.
    """

    # pull off the arguments meant for the app script before the parser sees them
    argv, script_args = split_script_args(argv)

    parser = get_parser()

    # "run" is the default subcommand
    argv = set_default_subparser(parser, name="run", args=argv)

    args, unrecognized = parser.parse_known_args(argv)

    if unrecognized:
        message = f"unrecognized arguments: {' '.join(unrecognized)}"
        if getattr(args, "command", None) == "run":
            message += (
                "\nIf these are arguments for your app script, put them after "
                "a `--` separator, e.g. "
                f"`flet run {args.script} -- {' '.join(unrecognized)}`"
            )
        parser.error(message)

    # forward the arguments that followed `--` to the app script
    if script_args is not None:
        if getattr(args, "command", None) != "run":
            parser.error(
                "the `--` separator is only supported by `flet run`, to pass "
                "the arguments that follow it to your app script"
            )
        args.script_args = list(args.script_args) + script_args

    return args


def main():
    # print usage/help if called without arguments
    if len(sys.argv) == 1:
        get_parser().print_help(sys.stdout)
        sys.exit(1)

    args = parse_command_line(sys.argv[1:])

    # handle `flet --version [--json]` (no subcommand/handler is set)
    if getattr(args, "version", False):
        print(_render_version(args.json))
        sys.exit(0)

    # execute command
    args.handler(args)


if __name__ == "__main__":
    main()
