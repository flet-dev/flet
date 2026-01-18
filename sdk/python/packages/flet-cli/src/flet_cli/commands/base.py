import argparse
from typing import Any, Optional

from flet_cli.commands.options import Option, verbose_option


class CustomArgumentDefaultsHelpFormatter(argparse.HelpFormatter):
    """
    An argparse help formatter that appends default values to help text
    selectively.

    Defaults are added only when they are informative and not already
    present in the help string. Noisy or redundant defaults (such as
    None, empty lists, booleans for flag arguments, or suppressed values)
    are omitted.
    """

    def _get_help_string(self, action: argparse.Action) -> str:
        help_text = action.help or ""
        default = action.default

        # skip appending a default
        if (
            default is None
            or default == []
            or isinstance(default, bool)  # store_true / store_false flags
            or default is argparse.SUPPRESS
            or any(token in help_text for token in ("%(default)", "(default:"))
        ):
            return help_text

        # only add defaults for optionals or for nargs implying optional values
        defaulting_nargs = (argparse.OPTIONAL, argparse.ZERO_OR_MORE)
        if action.option_strings or action.nargs in defaulting_nargs:
            help_text += " (default: %(default)s)"

        return help_text


class BaseCommand:
    """A CLI subcommand"""

    # The subcommand's name
    name: Optional[str] = None
    # The subcommand's help string, if not given, __doc__ will be used.
    description: Optional[str] = None
    # A list of pre-defined options which will be loaded on initializing
    # Rewrite this if you don't want the default ones
    arguments: list[Option] = [verbose_option]

    def __init__(self, parser: argparse.ArgumentParser) -> None:
        for arg in self.arguments:
            arg.add_to_parser(parser)
        self.add_arguments(parser)

    @classmethod
    def register_to(
        cls,
        subparsers: argparse._SubParsersAction,
        name: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Register a subcommand to the subparsers,
        with an optional name of the subcommand.
        """
        help_text = cls.description or cls.__doc__
        name = name or cls.name or ""

        # Remove the existing subparser as it will raise an error on Python 3.11+
        subparsers._name_parser_map.pop(name, None)
        subactions = subparsers._get_subactions()
        subactions[:] = [action for action in subactions if action.dest != name]
        parser = subparsers.add_parser(
            name,
            description=help_text,
            help=help_text,
            formatter_class=CustomArgumentDefaultsHelpFormatter,
            **kwargs,
        )
        command = cls(parser)
        parser.set_defaults(handler=command.handle)

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Manipulate the argument parser to add more arguments"""
        pass

    def handle(self, options: argparse.Namespace) -> None:
        """The command handler function.
        :param options: the parsed Namespace object
        """
        raise NotImplementedError
