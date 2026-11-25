from enum import Enum

__all__ = [
    "CalendarDisplayMode",
    "CalendarSelectionMode",
    "ColorSpectrumShape",
    "CommandBarOverflowBehavior",
    "ExpanderDirection",
    "FlyoutPlacementMode",
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


class FlyoutPlacementMode(Enum):
    """
    Where a flyout opens relative to the control it is attached to, as for
    :class:`~flet_fluent_ui.Flyout`, :class:`~flet_fluent_ui.TeachingTip` and
    :class:`~flet_fluent_ui.DropDownButton`.

    If there is no room on the preferred side, the flyout opens on the other
    side.
    """

    AUTO = "auto"
    """Below the control if there is room for it, otherwise above it."""

    BOTTOM_CENTER = "bottomCenter"
    """Below the control, centered."""

    BOTTOM_LEFT = "bottomLeft"
    """Below the control, lined up with its left edge."""

    BOTTOM_RIGHT = "bottomRight"
    """Below the control, lined up with its right edge."""

    TOP_CENTER = "topCenter"
    """Above the control, centered."""

    TOP_LEFT = "topLeft"
    """Above the control, lined up with its left edge."""

    TOP_RIGHT = "topRight"
    """Above the control, lined up with its right edge."""

    LEFT_TOP = "leftTop"
    """To the left of the control, lined up with its top edge."""

    LEFT_CENTER = "leftCenter"
    """To the left of the control, centered."""

    LEFT_BOTTOM = "leftBottom"
    """To the left of the control, lined up with its bottom edge."""

    RIGHT_TOP = "rightTop"
    """To the right of the control, lined up with its top edge."""

    RIGHT_CENTER = "rightCenter"
    """To the right of the control, centered."""

    RIGHT_BOTTOM = "rightBottom"
    """To the right of the control, lined up with its bottom edge."""


class CommandBarOverflowBehavior(Enum):
    """
    What a :class:`~flet_fluent_ui.CommandBar` does when its primary items
    don't fit in its width.
    """

    DYNAMIC_OVERFLOW = "dynamicOverflow"
    """
    The items that don't fit move into the "More" menu, from the last one.
    """

    WRAP = "wrap"
    """The items wrap onto more lines."""

    SCROLLING = "scrolling"
    """The items scroll horizontally."""

    CLIP = "clip"
    """The items that don't fit are cut off."""

    NO_WRAP = "noWrap"
    """
    The items stay on one line, and the bar is as wide as they need, even if
    that is wider than the space it has.
    """
