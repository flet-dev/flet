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
        parser.add_argument(*self.args, **self.kwargs)

    def add_to_group(self, group: argparse._ArgumentGroup) -> None:
        group.add_argument(*self.args, **self.kwargs)


verbose_option = Option(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="-v for detailed output and -vv for more detailed",
)
