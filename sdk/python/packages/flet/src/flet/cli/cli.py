import argparse
import sys

import flet.cli.commands.build
import flet.cli.commands.create
import flet.cli.commands.pack
import flet.cli.commands.publish
import flet.cli.commands.run
import flet.version


# Source https://stackoverflow.com/a/26379693
def set_default_subparser(self, name, args=None, positional_args=0):
    """default subparser selection. Call after setup, just before parse_args()
    name: is the name of the subparser to call by default
    args: if set is the argument list handed to parse_args()

    , tested with 2.7, 3.2, 3.3, 3.4
    it works with 2.6 assuming argparse is installed
    """
    subparser_found = False
    existing_default = False  # check if default parser previously defined
    for arg in sys.argv[1:]:
        if arg in ["-h", "--help", "--version"]:  # global help if no subparser
            break
    else:
        for x in self._subparsers._actions:
            if not isinstance(x, argparse._SubParsersAction):
                continue
            for sp_name in x._name_parser_map.keys():
                if sp_name in sys.argv[1:]:
                    subparser_found = True
                if sp_name == name:  # check existance of default parser
                    existing_default = True
        if not subparser_found:
            # If the default subparser is not among the existing ones,
            # create a new parser.
            # As this is called just before 'parse_args', the default
            # parser created here will not pollute the help output.

            if not existing_default:
                for x in self._subparsers._actions:
                    if not isinstance(x, argparse._SubParsersAction):
                        continue
                    x.add_parser(name)
                    break  # this works OK, but should I check further?

            # insert default in last position before global positional
            # arguments, this implies no global options are specified after
            # first positional argument
            if args is None and len(sys.argv) > 1:
                sys.argv.insert(positional_args, name)
            elif args is not None:
                args.insert(positional_args, name)
            # print(sys.argv)


argparse.ArgumentParser.set_default_subparser = set_default_subparser


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version=flet.version.version)
    sp = parser.add_subparsers(dest="command")
    # sp.default = "run"

    flet.cli.commands.create.Command.register_to(sp, "create")
    flet.cli.commands.run.Command.register_to(sp, "run")
    flet.cli.commands.pack.Command.register_to(sp, "pack")
    flet.cli.commands.publish.Command.register_to(sp, "publish")
    flet.cli.commands.build.Command.register_to(sp, "build")
    parser.set_default_subparser("run", positional_args=1)

    # print usage if called without args
    if len(sys.argv) == 1:
        parser.print_help(sys.stdout)
        sys.exit(1)

    # parse args
    args = parser.parse_args()

    # execute command
    args.handler(args)


if __name__ == "__main__":
    main()
