from dataclasses import field
from enum import Enum
from typing import Optional

from flet.controls.animation import AnimationStyle
from flet.controls.base_control import control
from flet.controls.box import BoxConstraints
from flet.controls.buttons import ButtonStyle, OutlinedBorder
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.layout_control import LayoutControl
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ClipBehavior,
    ColorValue,
    IconDataOrControl,
    MouseCursor,
    Number,
    StrOrControl,
)


class PopupMenuPosition(Enum):
    OVER = "over"
    UNDER = "under"


@control("PopupMenuItem")
class PopupMenuItem(Control):
    """
    A popup menu item.
    """

    content: Optional[StrOrControl] = None
    """
    A `Control` representing custom content of this menu item.
    """

    icon: Optional[IconDataOrControl] = None
    """
    An icon to draw before the text label of this menu item.
    """

    checked: Optional[bool] = None
    """
    Whether this menu item is checked.

    If set to `True`, a checkmark will be shown on the left of the
    [`content`][(c).].
    """

    height: Number = 48.0
    """
    The minimum height of this menu item.
    """

    padding: Optional[PaddingValue] = None
    """
    The padding of this menu item.

    Defaults to `Padding.symmetric(horizontal=12)`.

    Note:
        The [`height`][(c).] value of this menu item may
        influence the applied padding.

        For example, if a `height` greater than the height of the sum of the padding
        and a [`content`][(c).] is provided, then the padding's
        effect will not be visible.
    """

    label_text_style: Optional[TextStyle] = None
    """
    The text style of the label of this menu item."""

    mouse_cursor: Optional[MouseCursor] = None
    """
    The cursor to be displayed when a mouse pointer enters or
    is hovering over this item.
    """

    on_click: Optional[ControlEventHandler["PopupMenuItem"]] = None
    """
    Called when a user clicks on this menu item.
    """


@control("PopupMenuButton")
class PopupMenuButton(LayoutControl):
    """
    An icon button which displays a menu when clicked.

    ```python
    ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(content="Sm"),
            ft.PopupMenuItem(content="Med"),
            ft.PopupMenuItem(content="Lg"),
        ],
        menu_position=ft.PopupMenuPosition.UNDER,
    )
    ```

    """

    content: Optional[StrOrControl] = None
    """
    A `Control` that will be displayed instead of "more" icon.
    """

    items: list[PopupMenuItem] = field(default_factory=list)
    """
    A collection of `PopupMenuItem` controls to display in a dropdown menu.
    """

    icon: Optional[IconDataOrControl] = None
    """
    If provided, an icon to draw on the button.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The menu's background color.
    """

    icon_color: Optional[ColorValue] = None
    """
    The `icon`'s color.
    """

    shadow_color: Optional[ColorValue] = None
    """
    The color used to paint the shadow below
    the menu.
    """

    icon_size: Optional[Number] = None
    """
    The `icon`'s size.
    """

    splash_radius: Optional[Number] = None
    """
    The splash radius.
    """

    elevation: Optional[Number] = None
    """
    The menu's elevation when opened.

    Defaults to `8`.
    """

    menu_position: Optional[PopupMenuPosition] = None
    """
    Defines position of the popup menu relative to the button.

    Defaults to `PopupMenuPosition.OVER`.
    """

    clip_behavior: ClipBehavior = ClipBehavior.NONE
    """
    The `content` will be clipped (or not) according to this option.
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

    Defaults to `CircleBorder(radius=10.0)`.
    """

    padding: PaddingValue = 8
    """
    TBD
    """

    menu_padding: Optional[PaddingValue] = None
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

    on_open: Optional[ControlEventHandler["PopupMenuButton"]] = None
    """
    Called when the popup menu is shown.
    """

    on_cancel: Optional[ControlEventHandler["PopupMenuButton"]] = None
    """
    Called when the user dismisses/cancels the popup menu without selecting an item.
    """

    on_select: Optional[ControlEventHandler["PopupMenuButton"]] = None
    """
    TBD
    """

    def __contains__(self, item):
        return item in self.items
