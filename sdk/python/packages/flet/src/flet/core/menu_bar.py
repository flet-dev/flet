from dataclasses import dataclass, field
from typing import List, Optional

from flet.core.alignment import Alignment
from flet.core.border import BorderSide
from flet.core.buttons import OutlinedBorder
from flet.core.control import Control, control
from flet.core.types import (
    ClipBehavior,
    ColorValue,
    ControlState,
    ControlStateValue,
    MouseCursor,
    OptionalNumber,
    PaddingValue,
)

__all__ = ["MenuBar", "MenuStyle"]


@dataclass
class MenuStyle:
    alignment: Optional[Alignment] = None
    bgcolor: ControlStateValue[ColorValue] = None
    shadow_color: ControlStateValue[ColorValue] = None
    surface_tint_color: ControlStateValue[ColorValue] = None
    elevation: ControlStateValue[OptionalNumber] = None
    padding: ControlStateValue[PaddingValue] = None
    side: ControlStateValue[BorderSide] = None
    shape: ControlStateValue[OutlinedBorder] = None
    mouse_cursor: ControlStateValue[MouseCursor] = None

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
