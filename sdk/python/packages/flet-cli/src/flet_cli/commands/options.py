import argparse
from typing import Any


class Option:
    """A reusable option object which delegates all arguments
    to parser.add_argument().
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs

    def add_to_parser(self, parser: argparse._ActionsContainer) -> None:
        """
        Add this option definition to an argument parser or compatible container.

        Args:
            parser: Parser-like object exposing `add_argument()`.
        """

        parser.add_argument(*self.args, **self.kwargs)

    def add_to_group(self, group: argparse._ArgumentGroup) -> None:
        """
        Add this option definition to an argument group.

        Args:
            group: Argument group that receives the option.
        """

        group.add_argument(*self.args, **self.kwargs)


verbose_option = Option(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="Enable verbose output. "
    "Use -v for standard verbose logging and -vv for more detailed output",
)
