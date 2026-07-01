import argparse
import json
import sys

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
    parser: argparse.ArgumentParser, name: str, args: list = None, index: int = 0
):
    """
    Set a default subparser when no subparser is provided.
    This should be called after setting up the argument parser but before
    `parse_args()`.

    Args:
        name: The name of the default subparser to use.
        args: A list of arguments passed to `parse_args()`.
        index: Position in `sys.argv` where the default subparser should be
            inserted.
    """

    # exit if help or version flags are present
    if any(flag in sys.argv[1:] for flag in {"-h", "--help", "-V", "--version"}):
        return

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
    if any(arg in subparser_names for arg in sys.argv[1:]):
        return

    # if the default subparser doesn't exist, register it in the first subparser action
    if (name not in subparser_names) and subparser_actions:
        subparser_actions[0].add_parser(name)

    # insert the default subparser into the appropriate argument list
    if args is None:
        if len(sys.argv) > 1:
            sys.argv.insert(index, name)
    else:
        args.insert(index, name)


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

    # set "run" as the default subparser
    set_default_subparser(parser, name="run", index=1)

    return parser


def main():
    parser = get_parser()

    # print usage/help if called without arguments
    if len(sys.argv) == 1:
        parser.print_help(sys.stdout)
        sys.exit(1)

    # parse arguments
    args = parser.parse_args()

    # handle `flet --version [--json]` (no subcommand/handler is set)
    if getattr(args, "version", False):
        print(_render_version(args.json))
        sys.exit(0)

    # execute command
    args.handler(args)


if __name__ == "__main__":
    main()
