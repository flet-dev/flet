from enum import Enum
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.buttons import OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.padding import OptionalPaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    IconValueOrControl,
    MouseCursor,
    Number,
    OptionalColorValue,
    OptionalNumber,
    StrOrControl,
    UrlTarget,
    VisualDensity,
)

__all__ = ["ListTile", "ListTileTitleAlignment", "ListTileStyle"]


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

    Online docs: https://flet.dev/docs/controls/listtile
    """

    title: Optional[StrOrControl] = None
    """
    A `Control` to display as primary content of the list tile.

    Typically a [`Text`](https://flet.dev/docs/controls/text) control. This should not 
    wrap. To enforce the single line limit, use [`Text.max_lines`](https://flet.dev/docs/controls/text#max_lines).
    """

    subtitle: Optional[StrOrControl] = None
    """
    Additional content displayed below the title. Typically a 
    [`Text`](https://flet.dev/docs/controls/text) widget.

    If `is_three_line` is `False`, this should not wrap. If `is_three_line` is `True`, 
    this should be configured to take a maximum of two lines. For example, you can use 
    [`Text.max_lines`](https://flet.dev/docs/controls/text#max_lines) to enforce the 
    number of lines.
    """

    is_three_line: bool = False
    """
    Whether this list tile is intended to display three lines of text.

    If `True`, then subtitle must be non-null (since it is expected to give the second 
    and third lines of text).

    If `False`, the list tile is treated as having one line if the subtitle is null and 
    treated as having two lines if the subtitle is non-null.

    When using a Text control for title and subtitle, you can enforce line limits
    using [`Text.max_lines`](https://flet.dev/docs/controls/text#max_lines).
    """

    leading: Optional[IconValueOrControl] = None
    """
    A `Control` to display before the title.
    """

    trailing: Optional[IconValueOrControl] = None
    """
    A `Control` to display after the title. Typically an [`Icon`](https://flet.dev/docs/controls/icon) 
    control.
    """

    content_padding: OptionalPaddingValue = None
    """
    The tile's internal padding. Insets a ListTile's contents: its `leading`, `title`, 
    `subtitle`, and `trailing` controls.

    Value is of type [`Padding`](https://flet.dev/docs/reference/types/padding) and 
    defaults to `padding.symmetric(horizontal=16)`.
    """

    bgcolor: OptionalColorValue = None
    """
    The list tile's background [color](https://flet.dev/docs/reference/colors).
    """

    bgcolor_activated: Optional[str] = None
    """
    The list tile's splash [color](https://flet.dev/docs/reference/colors) after the 
    tile was tapped.
    """

    hover_color: OptionalColorValue = None
    """
    The tile's [color](https://flet.dev/docs/reference/colors) when hovered.
    """

    selected: bool = False
    """
    If this tile is also enabled then icons and text are rendered with the same color. 
    By default the selected color is the theme's primary color.
    """

    dense: bool = False
    """
    Whether this list tile is part of a vertically dense list. Dense list tiles default 
    to a smaller height.
    """

    autofocus: bool = False
    """
    `True` if the control will be selected as the initial focus. If there is more than 
    one control on a page with autofocus set, then the first one added to the page will 
    get focus.
    """

    toggle_inputs: bool = False
    """
    Whether clicking on a list tile should toggle the state of `Radio`, `Checkbox` or `
    Switch` inside the tile.

    Defaults to `False`.
    """

    selected_color: OptionalColorValue = None
    """
    Defines the [color](https://flet.dev/docs/reference/colors) used for icons and text 
    when `selected=True`.
    """

    selected_tile_color: OptionalColorValue = None
    """
    Defines the background [color](https://flet.dev/docs/reference/colors) of ListTile 
    when `selected=True`.
    """

    style: Optional[ListTileStyle] = None
    """
    Defines the font used for the title.

    Value is of type [`ListTileStyle`](https://flet.dev/docs/reference/types/listtilestyle) 
    and defaults to `ListTileStyle.LIST`.
    """

    enable_feedback: bool = True
    """
    Whether detected gestures should provide acoustic and/or haptic feedback. 
    On Android, for example, setting this to `True` produce a click sound and a 
    long-press will produce a short vibration. 

    Defaults to `True`.
    """

    horizontal_spacing: Number = 16.0
    """
    The horizontal gap between the `title` and the `leading`/`trailing` controls.

    Defaults to `16`.
    """

    min_leading_width: Number = 40.0
    """
    The minimum width allocated for the `leading` control.

    Defaults to `40`.
    """

    min_vertical_padding: Number = 4.0
    """
    The minimum padding on the top and bottom of the `title` and `subtitle` controls.

    Defaults to `4`.
    """

    url: Optional[str] = None
    """
    The URL to open when the list tile is clicked. If registered, `on_click` event is 
    fired after that.
    """

    url_target: Optional[UrlTarget] = None
    """
    Where to open URL in the web mode.

    Value is of type [`UrlTarget`](https://flet.dev/docs/reference/types/urltarget).
    """

    title_alignment: Optional[ListTileTitleAlignment] = None
    """
    Defines how `leading` and `trailing` are vertically aligned relative to the titles 
    (`title` and `subtitle`).

    Value is of type [`ListTileAlignment`](https://flet.dev/docs/reference/types/listtilealignment)
    and defaults to `ListTileAlignment.THREE_LINE` in Material 3 or 
    `ListTileAlignment.TITLE_HEIGHT` in Material 2.
    """

    icon_color: OptionalColorValue = None
    """
    Defines the default [color](https://flet.dev/docs/reference/colors) for the `Icon`s 
    present in `leading` and `trailing`.
    """

    text_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) used for text. Defines the color
    of `Text` controls found in `title`, `subtitle`, `leading`, and `trailing`.
    """

    shape: Optional[OutlinedBorder] = None
    """
    The tile's shape. The value is an instance of [`OutlinedBorder`](https://flet.dev/docs/reference/types/outlinedborder)
    class.
    """

    visual_density: Optional[VisualDensity] = None
    """
    Defines how compact the control's layout will be.

    Value is of type [`VisualDensity`](https://flet.dev/docs/reference/types/visualdensity).
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    The cursor to be displayed when a mouse pointer enters or is hovering over this 
    control. The value is [`MouseCursor`](https://flet.dev/docs/reference/types/mousecursor) 
    enum.
    """

    title_text_style: Optional[TextStyle] = None
    """
    The [`TextStyle`](https://flet.dev/docs/reference/types/textstyle) for the `title` 
    control.
    """

    subtitle_text_style: Optional[TextStyle] = None
    """
    The [`TextStyle`](https://flet.dev/docs/reference/types/textstyle) for the 
    `subtitle` control.
    """

    leading_and_trailing_text_style: Optional[TextStyle] = None
    """
    The [`TextStyle`](https://flet.dev/docs/reference/types/textstyle) for the 
    `leading` and `trailing` controls.
    """

    min_height: OptionalNumber = None
    """
    The minimum height allocated for this control.

    If `None` or not set, default tile heights are `56.0`, `72.0`, and `88.0` for one, 
    two, and three lines of text respectively.
    If [`dense`](https://flet.dev/docs/controls/listtile#dense) is `True`, these 
    defaults are changed to `48.0`, `64.0`, and `76.0`.

    Note that, a visual density value or a large title will also adjust the default 
    tile heights.
    """

    on_click: OptionalControlEventHandler["ListTile"] = None
    """
    Fires when a user clicks or taps the list tile.
    """

    on_long_press: OptionalControlEventHandler["ListTile"] = None
    """
    Fires when the user long-presses on this list tile.
    """
