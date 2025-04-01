from dataclasses import field
from enum import Enum
from typing import List, Optional

from flet.core.animation import AnimationStyle
from flet.core.box import BoxConstraints
from flet.core.buttons import ButtonStyle, OutlinedBorder
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, OptionalNumber, control
from flet.core.types import (
    ClipBehavior,
    ColorValue,
    IconValue,
    MouseCursor,
    OptionalControlEventCallable,
    PaddingValue,
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
    height: OptionalNumber = None
    padding: Optional[PaddingValue] = None
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
    icon: Optional[IconValue] = None
    bgcolor: Optional[ColorValue] = None
    icon_color: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    icon_size: OptionalNumber = None
    splash_radius: OptionalNumber = None
    elevation: OptionalNumber = None
    menu_position: Optional[PopupMenuPosition] = None
    clip_behavior: Optional[ClipBehavior] = None
    enable_feedback: Optional[bool] = None
    shape: Optional[OutlinedBorder] = None
    padding: Optional[PaddingValue] = None
    menu_padding: Optional[PaddingValue] = None
    style: Optional[ButtonStyle] = None
    popup_animation_style: Optional[AnimationStyle] = None
    size_constraints: Optional[BoxConstraints] = None
    on_open: OptionalControlEventCallable = None
    on_cancel: OptionalControlEventCallable = None
    on_select: OptionalControlEventCallable = None

    def __contains__(self, item):
        return item in self.items
