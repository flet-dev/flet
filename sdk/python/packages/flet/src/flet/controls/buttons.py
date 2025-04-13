from dataclasses import dataclass
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.border import BorderSide
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.control_state import ControlState, OptionalControlStateValue
from flet.controls.duration import OptionalDurationValue
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import ColorValue, MouseCursor, OptionalNumber, VisualDensity

__all__ = [
    "BeveledRectangleBorder",
    "ButtonStyle",
    "CircleBorder",
    "ContinuousRectangleBorder",
    "OutlinedBorder",
    "RoundedRectangleBorder",
    "StadiumBorder",
]


@dataclass
class OutlinedBorder:
    type: str = ""


@dataclass
class StadiumBorder(OutlinedBorder):
    def __post_init__(self):
        self.type = "stadium"


@dataclass
class RoundedRectangleBorder(OutlinedBorder):
    radius: OptionalBorderRadiusValue = None

    def __post_init__(self):
        self.type = "roundedRectangle"


@dataclass
class CircleBorder(OutlinedBorder):
    def __post_init__(self):
        self.type = "circle"


@dataclass
class BeveledRectangleBorder(OutlinedBorder):
    radius: OptionalBorderRadiusValue = None

    def __post_init__(self):
        self.type = "beveledRectangle"


@dataclass
class ContinuousRectangleBorder(OutlinedBorder):
    radius: OptionalBorderRadiusValue = None

    def __post_init__(self):
        self.type = "continuousRectangle"


@dataclass
class ButtonStyle:
    color: OptionalControlStateValue[ColorValue] = None
    bgcolor: OptionalControlStateValue[ColorValue] = None
    overlay_color: OptionalControlStateValue[ColorValue] = None
    shadow_color: OptionalControlStateValue[ColorValue] = None
    surface_tint_color: OptionalControlStateValue[ColorValue] = None
    elevation: OptionalControlStateValue[OptionalNumber] = None
    animation_duration: OptionalDurationValue = None
    padding: OptionalControlStateValue[PaddingValue] = None
    side: OptionalControlStateValue[BorderSide] = None
    shape: OptionalControlStateValue[OutlinedBorder] = None
    alignment: Optional[Alignment] = None
    enable_feedback: Optional[bool] = None
    text_style: OptionalControlStateValue[TextStyle] = None
    icon_size: OptionalControlStateValue[OptionalNumber] = None
    icon_color: OptionalControlStateValue[ColorValue] = None
    visual_density: Optional[VisualDensity] = None
    mouse_cursor: OptionalControlStateValue[MouseCursor] = None

    def __post_init__(self):
        if not isinstance(self.text_style, dict):
            self.text_style = {ControlState.DEFAULT: self.text_style}

        if not isinstance(self.padding, dict):
            self.padding = {ControlState.DEFAULT: self.padding}

        if not isinstance(self.side, dict):
            self.side = {ControlState.DEFAULT: self.side}

        if not isinstance(self.shape, dict):
            self.shape = {ControlState.DEFAULT: self.shape}
