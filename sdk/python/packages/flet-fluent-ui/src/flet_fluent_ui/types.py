from enum import Enum

__all__ = [
    "ExpanderDirection",
    "InfoBarSeverity",
]


class InfoBarSeverity(Enum):
    """
    The severity of an :class:`~flet_fluent_ui.InfoBar`, which sets its color
    and icon.
    """

    INFO = "info"
    """An informational message with a neutral appearance."""

    WARNING = "warning"
    """A warning with a yellow appearance."""

    ERROR = "error"
    """An error with a red appearance."""

    SUCCESS = "success"
    """A success message with a green appearance."""


class ExpanderDirection(Enum):
    """
    The direction an :class:`~flet_fluent_ui.Expander` opens in.
    """

    DOWN = "down"
    """The content opens below the header."""

    UP = "up"
    """The content opens above the header."""
