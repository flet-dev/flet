from dataclasses import dataclass, field
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.border import BorderSide
from flet.controls.buttons import OutlinedBorder
from flet.controls.control import Control
from flet.controls.control_state import ControlStateValue
from flet.controls.geometry import Size
from flet.controls.padding import PaddingValue
from flet.controls.types import (
    ClipBehavior,
    ColorValue,
    MouseCursor,
    Number,
    VisualDensity,
)

__all__ = ["MenuBar", "MenuStyle"]


@dataclass
class MenuStyle:
    alignment: Optional[Alignment] = None
    bgcolor: Optional[ControlStateValue[ColorValue]] = None
    shadow_color: Optional[ControlStateValue[ColorValue]] = None
    elevation: Optional[ControlStateValue[Optional[Number]]] = None
    padding: Optional[ControlStateValue[PaddingValue]] = None
    side: Optional[ControlStateValue[BorderSide]] = None
    shape: Optional[ControlStateValue[OutlinedBorder]] = None
    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    fixed_size: Optional[ControlStateValue[Size]] = None
    max_size: Optional[ControlStateValue[Size]] = None
    min_size: Optional[ControlStateValue[Size]] = None
    visual_density: Optional[VisualDensity] = None


@control("MenuBar")
class MenuBar(Control):
    """
    A menu bar that manages cascading child menus.

    It could be placed anywhere but typically resides above the main body of the
    application and defines a menu system for invoking callbacks in response to user
    selection of a menu item.

    ```python
    ft.MenuBar(
        controls=[
            ft.SubmenuButton(
                content=ft.Text("Submenu"),
                controls=[
                    ft.MenuItemButton(content=ft.Text("Item 1")),
                    ft.MenuItemButton(content=ft.Text("Item 2")),
                    ft.MenuItemButton(content=ft.Text("Item 3")),
                ],
            ),
        ],
    )
    ```

    """

    controls: list[Control] = field(default_factory=list)
    """
    A list of top-level menu controls to display in this menu bar.

    Raises:
        ValueError: If none of the controls are visible.
    """

    clip_behavior: ClipBehavior = ClipBehavior.NONE
    """
    Whether to clip the content of this control or not.
    """

    style: Optional[MenuStyle] = None
    """
    The menu bar style.
    """

    def before_update(self):
        super().before_update()
        if not any(c.visible for c in self.controls):
            raise ValueError("MenuBar must have at minimum one visible control")
