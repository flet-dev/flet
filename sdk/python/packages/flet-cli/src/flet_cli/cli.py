import argparse
import sys
from typing import Optional

import flet.version
import flet_cli.commands.build
import flet_cli.commands.create
import flet_cli.commands.doctor  # Adding the doctor command
import flet_cli.commands.pack
import flet_cli.commands.publish
import flet_cli.commands.run
import flet_cli.commands.serve
from flet.version import update_version


# Source https://stackoverflow.com/a/26379693
def set_default_subparser(
    parser: argparse.ArgumentParser,
    name: str,
    args: Optional[list[str]] = None,
    index: int = 0,
) -> list[str]:
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

    mutate_sys_argv = args is None
    current_args = list(sys.argv[1:] if mutate_sys_argv else args)

    # exit if help or version flags are present
    if any(flag in current_args for flag in {"-h", "--help", "-V", "--version"}):
        return current_args

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
    if any(arg in subparser_names for arg in current_args):
        return current_args

    # if the default subparser doesn't exist, register it in the first subparser action
    if (name not in subparser_names) and subparser_actions:
        subparser_actions[0].add_parser(name)

    # insert the default subparser into the appropriate argument list
    current_args.insert(index, name)

    if mutate_sys_argv:
        sys.argv = [sys.argv[0], *current_args]

    return current_args


def main():
    sys.exit(run())


def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=flet.version.version if flet.version.version else update_version(),
    )

    sp = parser.add_subparsers(dest="command")

    flet_cli.commands.create.Command.register_to(sp, "create")
    flet_cli.commands.run.Command.register_to(sp, "run")
    flet_cli.commands.build.Command.register_to(sp, "build")
    flet_cli.commands.pack.Command.register_to(sp, "pack")
    flet_cli.commands.publish.Command.register_to(sp, "publish")
    flet_cli.commands.serve.Command.register_to(sp, "serve")
    flet_cli.commands.doctor.Command.register_to(
        sp, "doctor"
    )  # Register the doctor command

    return parser


def run(args: Optional[list[str]] = None) -> int:
    parser = _create_parser()

    argv = list(args) if args is not None else list(sys.argv[1:])

    # set "run" as the default subparser
    argv = set_default_subparser(parser, name="run", args=argv, index=0)

    # print usage/help if called without arguments
    if not argv:
        parser.print_help(sys.stdout)
        return 1

    # parse arguments
    namespace = parser.parse_args(argv)

    # execute command
    namespace.handler(namespace)

    return 0


if __name__ == "__main__":
    main()
