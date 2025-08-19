from enum import Enum
from typing import Optional, Union

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.buttons import OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import ControlEventHandler
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ColorValue,
    IconDataOrControl,
    MouseCursor,
    Number,
    StrOrControl,
    Url,
    VisualDensity,
)

__all__ = ["ListTile", "ListTileStyle", "ListTileTitleAlignment"]


class ListTileTitleAlignment(Enum):
    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"
    THREE_LINE = "threeLine"
    TITLE_HEIGHT = "titleHeight"


class ListTileStyle(Enum):
    LIST = "list"
    DRAWER = "drawer"


@control("ListTile")
class ListTile(ConstrainedControl, AdaptiveControl):
    """
    A single fixed-height row that typically contains some text as well as a leading or
    trailing icon.
    """

    title: Optional[StrOrControl] = None
    """
    A control to display as primary content of the list tile.

    Typically a [`Text`][flet.Text] control. This should not
    wrap. To enforce the single line limit, use [`Text.max_lines`][flet.Text.max_lines].
    """

    subtitle: Optional[StrOrControl] = None
    """
    Additional content displayed below the title.

    If [`is_three_line`][flet.ListTile.is_three_line] is `False`, this should not wrap.
    If `is_three_line` is `True`, this should be configured to take a maximum of two
    lines.
    For example, you can use [`Text.max_lines`][flet.Text.max_lines] to enforce the
    number of lines.

    Typically a [`Text`][flet.Text] control.
    """

    is_three_line: bool = False
    """
    Whether this list tile is intended to display three lines of text.

    If `True`, then subtitle must be non-null (since it is expected to give the second
    and third lines of text).

    If `False`, the list tile is treated as having one line if the subtitle is null and
    treated as having two lines if the subtitle is non-null.

    When using a Text control for title and subtitle, you can enforce line limits
    using [`Text.max_lines`][flet.Text.max_lines].
    """

    leading: Optional[IconDataOrControl] = None
    """
    A control to display before the [`title`][flet.ListTile.title].
    """

    trailing: Optional[IconDataOrControl] = None
    """
    A control to display after the [`title`][flet.ListTile.title].

    Typically an [`Icon`][flet.Icon] control.
    """

    content_padding: Optional[PaddingValue] = None
    """
    The tile's internal padding. It insets the contents of this tile.
    : its `leading`, `title`,
    `subtitle`, and `trailing` controls.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The list tile's background color.
    """

    bgcolor_activated: Optional[str] = None
    """
    The list tile's splash color after the
    being was tapped.
    """

    hover_color: Optional[ColorValue] = None
    """
    The tile's color when hovered.
    """

    selected: bool = False
    """
    If this tile is also enabled then icons and text are rendered with the same color.
    By default the selected color is the theme's primary color.
    """

    dense: bool = False
    """
    Whether this list tile is part of a vertically dense list.

    Dense list tiles default to a smaller height.
    """

    autofocus: bool = False
    """
    `True` if the control will be selected as the initial focus. If there is more than
    one control on a page with autofocus set, then the first one added to the page will
    get focus.
    """

    toggle_inputs: bool = False
    """
    Whether clicking on a list tile should toggle the state of [`Radio`][flet.Radio],
    [`Checkbox`][flet.Checkbox] or [`Switch`][flet.Switch] inside this tile.
    """

    selected_color: Optional[ColorValue] = None
    """
    Defines the color used for icons and text
    when `selected=True`.
    """

    selected_tile_color: Optional[ColorValue] = None
    """
    Defines the background color of ListTile
    when `selected=True`.
    """

    style: Optional[ListTileStyle] = None
    """
    Defines the font used for the title.

    Defaults to `ListTileStyle.LIST`.
    """

    enable_feedback: bool = True
    """
    Whether detected gestures should provide acoustic and/or haptic feedback.
    On Android, for example, setting this to `True` produce a click sound and a
    long-press will produce a short vibration.
    """

    horizontal_spacing: Number = 16.0
    """
    The horizontal gap between the `title` and the
    [`leading`][flet.ListTile.leading] and [`trailing`][flet.ListTile.trailing]
    controls.
    """

    min_leading_width: Number = 40.0
    """
    The minimum width allocated for the `leading` control.
    """

    min_vertical_padding: Number = 4.0
    """
    The minimum padding on the top and bottom of the `title` and `subtitle` controls.
    """

    url: Optional[Union[str, Url]] = None
    """
    The URL to open when this button is clicked.

    Additionally, if [`on_click`][flet.ListTile.on_click] event callback is provided,
    it is fired after that.
    """

    title_alignment: Optional[ListTileTitleAlignment] = None
    """
    Defines how `leading` and `trailing` are vertically aligned relative to the titles
    (`title` and `subtitle`).

    Defaults to `ListTileTitleAlignment.THREE_LINE` in Material 3 or
    `ListTileTitleAlignment.TITLE_HEIGHT` in Material 2.
    """

    icon_color: Optional[ColorValue] = None
    """
    Defines the default color for the icons
    present in [`leading`][flet.ListTile.leading] and
    [`trailing`][flet.ListTile.trailing].
    """

    text_color: Optional[ColorValue] = None
    """
    The color used for
    texts in [`title`][flet.ListTile.title], [`subtitle`][flet.ListTile.subtitle],
    [`leading`][flet.ListTile.leading], and [`trailing`][flet.ListTile.trailing].
    """

    shape: Optional[OutlinedBorder] = None
    """
    The tile's shape.
    """

    visual_density: Optional[VisualDensity] = None
    """
    Defines how compact the control's layout will be.
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    The cursor to be displayed when a mouse pointer enters or is hovering over this
    control. The value is [`MouseCursor`][flet.MouseCursor]
    enum.
    """

    title_text_style: Optional[TextStyle] = None
    """
    The [`TextStyle`][flet.TextStyle] for the [`title`][flet.ListTile.title]
    control.
    """

    subtitle_text_style: Optional[TextStyle] = None
    """
    The [`TextStyle`][flet.TextStyle] for the
    `subtitle` control.
    """

    leading_and_trailing_text_style: Optional[TextStyle] = None
    """
    The [`TextStyle`][flet.TextStyle] for the
    `leading` and `trailing` controls.
    """

    min_height: Optional[Number] = None
    """
    The minimum height allocated for this control.

    If `None` or not set, default tile heights are `56.0`, `72.0`, and `88.0` for one,
    two, and three lines of text respectively.
    If [`dense`][flet.ListTile.dense] is `True`, these
    defaults are changed to `48.0`, `64.0`, and `76.0`.

    Note that, a visual density value or a large title will also adjust the default
    tile heights.
    """

    on_click: Optional[ControlEventHandler["ListTile"]] = None
    """
    Called when a user clicks or taps the list tile.
    """

    on_long_press: Optional[ControlEventHandler["ListTile"]] = None
    """
    Called when the user long-presses on this list tile.
    """
