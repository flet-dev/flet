import argparse
import sys

import flet.version
from flet.version import update_version

import flet_cli.commands.build
import flet_cli.commands.create
import flet_cli.commands.pack
import flet_cli.commands.publish
import flet_cli.commands.run
import flet_cli.commands.doctor # Adding the doctor command


# Source https://stackoverflow.com/a/26379693
def set_default_subparser(
    parser: argparse.ArgumentParser, name: str, args: list = None, index: int = 0
):
    """
    Set a default subparser when no subparser is provided.
    This should be called after setting up the argument parser but before `parse_args()`.

    Parameters:
    - name (str): The name of the default subparser to use.
    - args (list, optional): A list of arguments passed to `parse_args()`. Defaults to None.
    - index (int): Position in `sys.argv` where the default subparser should be inserted. Defaults to 0.
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
        sp_name
        for action in subparser_actions
        for sp_name in action._name_parser_map.keys()
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


def main():
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
    flet_cli.commands.doctor.Command.register_to(sp, "doctor") # Register the doctor command

    # set "run" as the default subparser
    set_default_subparser(parser, name="run", index=1)

    # print usage/help if called without arguments
    if len(sys.argv) == 1:
        parser.print_help(sys.stdout)
        sys.exit(1)

    # parse arguments
    args = parser.parse_args()

    # execute command
    args.handler(args)


if __name__ == "__main__":
    main()
