from enum import Enum

__all__ = [
    "CalendarDisplayMode",
    "CalendarSelectionMode",
    "CloseButtonVisibilityMode",
    "ColorSpectrumShape",
    "CommandBarOverflowBehavior",
    "ExpanderDirection",
    "FlyoutPlacementMode",
    "InfoBarSeverity",
    "ListTileSelectionMode",
    "PaneDisplayMode",
    "PasswordRevealMode",
    "TabWidthBehavior",
    "TreeViewSelectionMode",
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


class TabWidthBehavior(Enum):
    """
    How wide the tabs of a :class:`~flet_fluent_ui.TabView` are.
    """

    EQUAL = "equal"
    """All tabs have the same width, which shrinks as tabs are added."""

    SIZE_TO_CONTENT = "sizeToContent"
    """Each tab is as wide as its label."""

    COMPACT = "compact"
    """
    The selected tab is as wide as its label, and the other tabs show only
    their icon.
    """


class CloseButtonVisibilityMode(Enum):
    """
    When the close buttons of the tabs of a :class:`~flet_fluent_ui.TabView`
    are shown.
    """

    ALWAYS = "always"
    """On every tab."""

    ON_HOVER = "onHover"
    """On the tab under the mouse pointer."""

    NEVER = "never"
    """
    Never: the selected tab can still be closed with Ctrl+W (Cmd+W on
    macOS).
    """


class TreeViewSelectionMode(Enum):
    """
    How the items of a :class:`~flet_fluent_ui.TreeView` can be selected.
    """

    NONE = "none"
    """Items can't be selected."""

    SINGLE = "single"
    """One item can be selected."""

    MULTIPLE = "multiple"
    """
    Items have checkboxes, and any number of them can be selected. Selecting
    an item selects its subitems.
    """


class PaneDisplayMode(Enum):
    """
    How the pane of a :class:`~flet_fluent_ui.NavigationView` is shown.
    """

    AUTO = "auto"
    """
    Depends on the width of the view: :attr:`EXPANDED` when it is wide,
    :attr:`COMPACT` when it is medium and :attr:`MINIMAL` when it is narrow.
    """

    EXPANDED = "expanded"
    """A pane on the left, with the icons and titles of the items."""

    COMPACT = "compact"
    """
    A narrow pane on the left with only icons, which the menu button opens
    over the content.
    """

    MINIMAL = "minimal"
    """
    No pane, only a menu button, which opens the pane over the content.
    """

    TOP = "top"
    """
    The items in a row above the content; the items that don't fit go into a
    "More" menu.
    """
