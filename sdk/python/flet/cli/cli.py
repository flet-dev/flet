import argparse
import sys
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
        if arg in ["-h", "--help"]:  # global help if no subparser
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
            if args is None:
                sys.argv.insert(len(sys.argv) - positional_args, name)
            else:
                args.insert(len(args) - positional_args, name)


argparse.ArgumentParser.set_default_subparser = set_default_subparser


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version=flet.version.version)
    sp = parser.add_subparsers(dest="command")
    # sp.default = "run"

    run_parser = sp.add_parser("run")
    run_parser.add_argument("script", type=str, help="path to a Python script")
    run_parser.add_argument(
        "-p",
        "--port",
        dest="port",
        type=int,
        default=None,
        help="custom TCP port to run Flet app on",
    )
    run_parser.add_argument(
        "-d",
        "--directory",
        dest="directory",
        action="store_true",
        default=False,
        help="watch script directory",
    )
    run_parser.add_argument(
        "-r",
        "--recursive",
        dest="recursive",
        action="store_true",
        default=False,
        help="watch script directory and all sub-directories recursively",
    )
    run_parser.add_argument(
        "-n",
        "--hidden",
        dest="hidden",
        action="store_true",
        default=False,
        help="application window is hidden on startup",
    )
    run_parser.add_argument(
        "-w",
        "--web",
        dest="web",
        action="store_true",
        default=False,
        help="open app in a web browser",
    )

    build_parser = sp.add_parser("build")
    build_parser.add_argument("script", type=str, help="path to a Python script")
    build_parser.add_argument(
        "-F",
        "--onefile",
        dest="onefile",
        action="store_true",
        default=False,
        help="create a one-file bundled executable",
    )

    parser.set_default_subparser("run")
    args = parser.parse_args()
    print(args)

    print(args)

    # script_path = args.script
    # port = args.port


if __name__ == "__main__":
    main()
