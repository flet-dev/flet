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
    """
    Defines the visual style/appearance of a menu.
    """

    alignment: Optional[Alignment] = None
    """
    Determines the desired alignment of the submenu when opened relative to
    the button that opens it.

    If there isn't sufficient space to open the menu with the given alignment,
    and there's space on the other side of the button, then the alignment is
    swapped to it's opposite (`1` becomes `-1`, etc.), and the menu will try to
    appear on the other side of the button. If there isn't enough space there
    either, then the menu will be pushed as far over as necessary to display
    as much of itself as possible, possibly overlapping the parent button.
    """

    bgcolor: Optional[ControlStateValue[ColorValue]] = None
    """
    The menu's background fill color.
    """

    shadow_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The shadow color of the menu

    The material's elevation shadow can be difficult to see for dark themes,
    so by default the menu classes add a semi-transparent overlay to indicate
    elevation.
    """

    elevation: Optional[ControlStateValue[Optional[Number]]] = None
    """
    The menu's elevation, i.e. the size of the shadow below the menu.
    """

    padding: Optional[ControlStateValue[PaddingValue]] = None
    """
    The padding between the menu's boundary and its child.
    """

    side: Optional[ControlStateValue[BorderSide]] = None
    """
    The color and weight of the menu's outline.

    This value is combined with [`shape`][(c).] to create a
    shape decorated with an outline.
    """

    shape: Optional[ControlStateValue[OutlinedBorder]] = None
    """
    The menu's shape.

    This shape is combined with [`side`][(c).] to create a
    shape decorated with an outline.
    """

    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    The cursor for a mouse pointer when it enters or is hovering over the menu.
    """

    fixed_size: Optional[ControlStateValue[Size]] = None
    """
    The menu's size.

    This size is still constrained by the style's [`min_size`][(c).] and
    [`max_size`][(c).]. Fixed size dimensions whose value is `float('inf')` are
    ignored.

    To specify menus with a fixed width and the default height use
    `Size.from_width(320)`. Similarly, to specify a fixed height and the default
    width use `Size.from_height(100)`.
    """

    max_size: Optional[ControlStateValue[Size]] = None
    """
    The maximum size of the menu itself.

    A [`Size.infinite`][flet.] or `None` value for this property
    means that the menu's maximum size is not constrained.

    This value must be greater than or equal to [`min_size`][(c).].
    """

    min_size: Optional[ControlStateValue[Size]] = None
    """
    The minimum size of the menu itself.

    This value must be less than or equal to [`max_size`][(c).].
    """

    visual_density: Optional[VisualDensity] = None
    """
    Defines how compact the menu's layout will be.
    """


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
