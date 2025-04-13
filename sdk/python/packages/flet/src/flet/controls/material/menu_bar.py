from dataclasses import dataclass, field
from typing import List, Optional

from flet.controls.alignment import Alignment
from flet.controls.border import BorderSide
from flet.controls.buttons import OutlinedBorder
from flet.controls.control import Control, control
from flet.controls.control_state import ControlState, OptionalControlStateValue
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

    def __post_init__(self):
        if not isinstance(self.padding, dict):
            self.padding = {ControlState.DEFAULT: self.padding}

        if not isinstance(self.side, dict):
            self.side = {ControlState.DEFAULT: self.side}

        if not isinstance(self.shape, dict):
            self.shape = {ControlState.DEFAULT: self.shape}

        if not isinstance(self.mouse_cursor, dict):
            self.mouse_cursor = {ControlState.DEFAULT: self.mouse_cursor}


@control("MenuBar")
class MenuBar(Control):
    """
    A menu bar that manages cascading child menus.

    It could be placed anywhere but typically resides above the main body of the application
    and defines a menu system for invoking callbacks in response to user selection of a menu item.

    -----

    Online docs: https://flet.dev/docs/controls/menubar
    """

    controls: List[Control] = field(default_factory=list)
    clip_behavior: Optional[ClipBehavior] = None
    style: Optional[MenuStyle] = None

    def before_update(self):
        super().before_update()
        assert any(
            c.visible for c in self.controls
        ), "MenuBar must have at minimum one visible control"
