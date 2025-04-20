from dataclasses import field
from enum import Enum
from typing import List, Optional

from flet.controls.animation import AnimationStyle
from flet.controls.base_control import control
from flet.controls.box import BoxConstraints
from flet.controls.buttons import ButtonStyle, OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.padding import OptionalPaddingValue, PaddingValue
from flet.controls.types import (
    ClipBehavior,
    IconValue,
    IconValueOrControl,
    MouseCursor,
    Number,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
)


class PopupMenuPosition(Enum):
    OVER = "over"
    UNDER = "under"


@control("PopupMenuItem")
class PopupMenuItem(Control):
    text: Optional[str] = None
    icon: Optional[IconValue] = None
    checked: Optional[bool] = None
    content: Optional[Control] = None
    height: Number = 48.0
    padding: OptionalPaddingValue = None
    mouse_cursor: Optional[MouseCursor] = None
    on_click: OptionalControlEventCallable = None


@control("PopupMenuButton")
class PopupMenuButton(ConstrainedControl):
    """
    An icon button which displays a menu when clicked.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        def check_item_clicked(e):
            e.control.checked = not e.control.checked
            page.update()

        pb = ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(text="Item 1"),
                ft.PopupMenuItem(icon=ft.icons.POWER_INPUT, text="Check power"),
                ft.PopupMenuItem(
                    content=ft.Row(
                        [
                            ft.Icon(ft.icons.HOURGLASS_TOP_OUTLINED),
                            ft.Text("Item with a custom content"),
                        ]
                    ),
                    on_click=lambda _: print("Button with a custom content clicked!"),
                ),
                ft.PopupMenuItem(),  # divider
                ft.PopupMenuItem(
                    text="Checked item", checked=False, on_click=check_item_clicked
                ),
            ]
        )
        page.add(pb)

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/popupmenubutton
    """

    content: Optional[Control] = None
    items: List[PopupMenuItem] = field(default_factory=list)
    icon: Optional[IconValueOrControl] = None
    bgcolor: OptionalColorValue = None
    icon_color: OptionalColorValue = None
    shadow_color: OptionalColorValue = None
    surface_tint_color: OptionalColorValue = None
    icon_size: OptionalNumber = None
    splash_radius: OptionalNumber = None
    elevation: OptionalNumber = None
    menu_position: Optional[PopupMenuPosition] = None
    clip_behavior: ClipBehavior = ClipBehavior.NONE
    enable_feedback: Optional[bool] = None
    shape: Optional[OutlinedBorder] = None
    padding: PaddingValue = 8
    menu_padding: OptionalPaddingValue = None
    style: Optional[ButtonStyle] = None
    popup_animation_style: Optional[AnimationStyle] = None
    size_constraints: Optional[BoxConstraints] = None
    on_open: OptionalControlEventCallable = None
    on_cancel: OptionalControlEventCallable = None
    on_select: OptionalControlEventCallable = None

    def __contains__(self, item):
        return item in self.items
