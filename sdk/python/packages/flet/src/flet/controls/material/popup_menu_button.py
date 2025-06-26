from dataclasses import field
from enum import Enum
from typing import Optional

from flet.controls.animation import AnimationStyle
from flet.controls.base_control import control
from flet.controls.box import BoxConstraints
from flet.controls.buttons import ButtonStyle, OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.padding import OptionalPaddingValue, PaddingValue
from flet.controls.types import (
    ClipBehavior,
    IconValueOrControl,
    MouseCursor,
    Number,
    OptionalColorValue,
    OptionalNumber,
    StrOrControl,
)


class PopupMenuPosition(Enum):
    OVER = "over"
    UNDER = "under"


@control("PopupMenuItem")
class PopupMenuItem(Control):
    content: Optional[StrOrControl] = None
    """
    A `Control` representing custom content of this menu item.
    """

    icon: Optional[IconValueOrControl] = None
    """
    An icon to draw before the text label of this menu item.
    """

    checked: Optional[bool] = None
    """
    If set to `True` or `False` a menu item draws a checkmark.
    """

    height: Number = 48.0
    """
    The minimum height of this menu item.

    Defaults to `48`.
    """

    padding: OptionalPaddingValue = None
    """
    The padding of this menu item.

    Note that the `height` value of this menu item may influence the applied padding.
    For example, if a `height` greater than the height of the sum of the padding and a
    `content` is provided, then the padding's effect will not be visible.

    Padding value is an instance of [`Padding`](https://flet.dev/docs/reference/types/padding) 
    class.

    Defaults to `padding.symmetric(horizontal=12)`.
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    The cursor to be displayed when a mouse pointer enters or is hovering over this
    control.

    Value is of type [`MouseCursor`](https://flet.dev/docs/reference/types/mousecursor).
    """

    on_click: OptionalControlEventHandler["PopupMenuItem"] = None
    """
    Called when a user clicks on this menu item.
    """


@control("PopupMenuButton")
class PopupMenuButton(ConstrainedControl):
    """
    An icon button which displays a menu when clicked.

    Online docs: https://flet.dev/docs/controls/popupmenubutton
    """

    content: Optional[StrOrControl] = None
    """
    A `Control` that will be displayed instead of "more" icon.
    """

    items: list[PopupMenuItem] = field(default_factory=list)
    """
    A collection of `PopupMenuItem` controls to display in a dropdown menu.
    """

    icon: Optional[IconValueOrControl] = None
    """
    If provided, an icon to draw on the button.
    """

    bgcolor: OptionalColorValue = None
    """
    The menu's background [color](https://flet.dev/docs/reference/colors).
    """

    icon_color: OptionalColorValue = None
    """
    The `icon`'s [color](https://flet.dev/docs/reference/colors).
    """

    shadow_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) used to paint the shadow below
    the menu.
    """

    surface_tint_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) used as an overlay on color to
    indicate elevation.
    """

    icon_size: OptionalNumber = None
    """
    The `icon`'s size.
    """

    splash_radius: OptionalNumber = None
    """
    The splash radius.
    """

    elevation: OptionalNumber = None
    """
    The menu's elevation when opened.

    Defaults to `8`.
    """

    menu_position: Optional[PopupMenuPosition] = None
    """
    Defines position of the popup menu relative to the button.

    Value is of type
    [`PopupMenuPosition`](https://flet.dev/docs/reference/types/popupmenuposition) and
    defaults to `PopupMenuPosition.OVER`.
    """

    clip_behavior: ClipBehavior = ClipBehavior.NONE
    """
    The `content` will be clipped (or not) according to this option.

    Value is of type
    [`ClipBehavior`](https://flet.dev/docs/reference/types/clipbehavior) and defaults to
    `ClipBehavior.NONE`.
    """

    enable_feedback: Optional[bool] = None
    """
    Whether detected gestures should provide acoustic and/or haptic feedback.

    On Android, for example, setting this to `True` produce a click sound and a
    long-press will produce a short vibration.

    Defaults to `True`.
    """

    shape: Optional[OutlinedBorder] = None
    """
    The menu's shape.

    Value is of type [`OutlinedBorder`](https://flet.dev/docs/reference/types/outlinedborder) 
    and defaults to `CircleBorder(radius=10.0)`.
    """

    padding: PaddingValue = 8
    """
    Value is of type [`Padding`](https://flet.dev/docs/reference/types/padding) and
    defaults to `Padding.all(8.0)`.
    """

    menu_padding: OptionalPaddingValue = None
    """
    TBD
    """

    style: Optional[ButtonStyle] = None
    """
    TBD
    """

    popup_animation_style: Optional[AnimationStyle] = None
    """
    TBD
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    TBD
    """

    on_open: OptionalControlEventHandler["PopupMenuButton"] = None
    """
    Called when the popup menu is shown.
    """

    on_cancel: OptionalControlEventHandler["PopupMenuButton"] = None
    """
    Called when the user dismisses/cancels the popup menu without selecting an item.
    """

    on_select: OptionalControlEventHandler["PopupMenuButton"] = None
    """
    TBD
    """

    def __contains__(self, item):
        return item in self.items
