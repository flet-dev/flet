from enum import Enum

__all__ = [
    "CalendarDisplayMode",
    "CalendarSelectionMode",
    "ColorSpectrumShape",
    "ExpanderDirection",
    "InfoBarSeverity",
    "ListTileSelectionMode",
    "PasswordRevealMode",
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


class PasswordRevealMode(Enum):
    """
    Whether and how a :class:`~flet_fluent_ui.PasswordBox` lets the user see
    the password.
    """

    PEEK = "peek"
    """
    A reveal button shows the password while it is pressed. The button is
    hidden again after the box loses focus, until the box is cleared.
    """

    PEEK_ALWAYS = "peekAlways"
    """
    A reveal button shows the password while it is pressed, and stays
    available whenever the box has focus and is not empty.
    """

    HIDDEN = "hidden"
    """There is no reveal button: the password is always hidden."""

    VISIBLE = "visible"
    """There is no reveal button: the password is always shown."""


class ListTileSelectionMode(Enum):
    """
    How a :class:`~flet_fluent_ui.ListTile` can be selected.
    """

    NONE = "none"
    """The tile can't be selected."""

    SINGLE = "single"
    """
    The tile can be selected, and clicking a selected tile does not deselect
    it, like one option among several.
    """

    MULTIPLE = "multiple"
    """
    The tile shows a checkbox, and clicking toggles its selection, like one of
    several checked items.
    """


class CalendarSelectionMode(Enum):
    """
    How many dates the user can select in a
    :class:`~flet_fluent_ui.CalendarView`.
    """

    NONE = "none"
    """Dates can't be selected: the calendar only shows them."""

    SINGLE = "single"
    """One date can be selected."""

    RANGE = "range"
    """
    A range of dates can be selected: the first click picks the start, the
    second the end.
    """

    MULTIPLE = "multiple"
    """Any number of dates can be selected, not necessarily adjacent."""


class CalendarDisplayMode(Enum):
    """
    What a :class:`~flet_fluent_ui.CalendarView` shows: the days of a month,
    the months of a year or the years of a decade.
    """

    MONTH = "month"
    """The days of a month."""

    YEAR = "year"
    """The months of a year."""

    DECADE = "decade"
    """The years of a decade."""


class ColorSpectrumShape(Enum):
    """
    The shape of the color spectrum of a
    :class:`~flet_fluent_ui.ColorPicker`.
    """

    RING = "ring"
    """A ring of hues around the saturation and brightness area."""

    BOX = "box"
    """A square, with hue across and saturation down."""
