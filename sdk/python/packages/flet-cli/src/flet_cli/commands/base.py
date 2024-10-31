import argparse
from typing import Any, List, Optional

from flet_cli.commands.options import Option, verbose_option


class BaseCommand:
    """A CLI subcommand"""

    # The subcommand's name
    name: Optional[str] = None
    # The subcommand's help string, if not given, __doc__ will be used.
    description: Optional[str] = None
    # A list of pre-defined options which will be loaded on initializing
    # Rewrite this if you don't want the default ones
    arguments: List[Option] = [verbose_option]

    def __init__(self, parser: argparse.ArgumentParser) -> None:
        for arg in self.arguments:
            arg.add_to_parser(parser)
        self.add_arguments(parser)

    @classmethod
    def register_to(
        cls,
        subparsers: argparse._SubParsersAction,
        name: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """Register a subcommand to the subparsers,
        with an optional name of the subcommand.
        """
        help_text = cls.description or cls.__doc__
        name = name or cls.name or ""
        # Remove the existing subparser as it will raises an error on Python 3.11+
        subparsers._name_parser_map.pop(name, None)
        subactions = subparsers._get_subactions()
        subactions[:] = [action for action in subactions if action.dest != name]
        parser = subparsers.add_parser(
            name,
            description=help_text,
            help=help_text,
            # formatter_class=PdmFormatter,
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
