from dataclasses import dataclass, field
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.border import BorderSide
from flet.controls.buttons import OutlinedBorder
from flet.controls.control import Control
from flet.controls.control_state import OptionalControlStateValue
from flet.controls.padding import PaddingValue
from flet.controls.types import ClipBehavior, ColorValue, MouseCursor, OptionalNumber

__all__ = ["MenuBar", "MenuStyle"]


@dataclass
class MenuStyle:
    alignment: Optional[Alignment] = None
    bgcolor: OptionalControlStateValue[ColorValue] = None
    shadow_color: OptionalControlStateValue[ColorValue] = None
    surface_tint_color: OptionalControlStateValue[ColorValue] = None
    elevation: OptionalControlStateValue[OptionalNumber] = None
    padding: OptionalControlStateValue[PaddingValue] = None
    side: OptionalControlStateValue[BorderSide] = None
    shape: OptionalControlStateValue[OutlinedBorder] = None
    mouse_cursor: OptionalControlStateValue[MouseCursor] = None


@control("MenuBar")
class MenuBar(Control):
    """
    A menu bar that manages cascading child menus.

    It could be placed anywhere but typically resides above the main body of the
    application and defines a menu system for invoking callbacks in response to user
    selection of a menu item.

    Online docs: https://flet.dev/docs/controls/menubar
    """

    controls: list[Control] = field(default_factory=list)
    """
    The list of menu items that are the top level children of the `MenuBar`.
    """

    clip_behavior: ClipBehavior = ClipBehavior.NONE
    """
    Whether to clip the content of this control or not.

    Value is of type [`ClipBehavior`](https://flet.dev/docs/reference/types/clipbehavior)
    and defaults to `ClipBehavior.NONE`.
    """

    style: Optional[MenuStyle] = None
    """
    Value is of type [`MenuStyle`](https://flet.dev/docs/reference/types/menustyle).
    """

    def before_update(self):
        super().before_update()
        assert any(
            c.visible for c in self.controls
        ), "MenuBar must have at minimum one visible control"
