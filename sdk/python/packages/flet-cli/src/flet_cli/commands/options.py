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


class PassThroughArgsAction(argparse.Action):
    """
    Collect the values of each occurrence of an option that passes arguments on
    to another program, as one list per occurrence.

    A value that starts with `-` is read as an option of its own unless it is
    attached with `=`, which leaves the occurrence without values and hands the
    value to whichever Flet option it names. An occurrence without values is
    therefore rejected, with a hint to attach the value or to pass it after
    `--`.
    """

    def __init__(self, option_strings, dest, example: str, **kwargs):
        """
        Args:
            option_strings: The option strings of the option.
            dest: The attribute that receives the collected values.
            example: A value that starts with `-`, shown in the hint.
            **kwargs: The other `add_argument()` arguments.
        """

        super().__init__(option_strings, dest, **kwargs)
        self.example = example

    def __call__(self, parser, namespace, values, option_string=None):
        if not values:
            raise argparse.ArgumentError(
                self,
                "expected at least one argument - attach one that starts with "
                f"`-` using `=`, e.g. `{self.option_strings[0]}={self.example}`, "
                "or pass it after `--`",
            )
        collected = getattr(namespace, self.dest, None) or []
        setattr(namespace, self.dest, [*collected, values])


verbose_option = Option(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="Enable verbose output. "
    "Use -v for standard verbose logging and -vv for more detailed output",
)
