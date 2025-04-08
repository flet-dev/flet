from dataclasses import dataclass
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.border import BorderSide
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.duration import OptionalDurationValue
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ColorValue,
    ControlState,
    ControlStateValue,
    MouseCursor,
    OptionalNumber,
    VisualDensity,
)

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
    type: str = None


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
    color: ControlStateValue[ColorValue] = None
    bgcolor: ControlStateValue[ColorValue] = None
    overlay_color: ControlStateValue[ColorValue] = None
    shadow_color: ControlStateValue[ColorValue] = None
    surface_tint_color: ControlStateValue[ColorValue] = None
    elevation: ControlStateValue[OptionalNumber] = None
    animation_duration: OptionalDurationValue = None
    padding: ControlStateValue[PaddingValue] = None
    side: ControlStateValue[BorderSide] = None
    shape: ControlStateValue[OutlinedBorder] = None
    alignment: Optional[Alignment] = None
    enable_feedback: Optional[bool] = None
    text_style: ControlStateValue[TextStyle] = None
    icon_size: ControlStateValue[OptionalNumber] = None
    icon_color: ControlStateValue[ColorValue] = None
    visual_density: Optional[VisualDensity] = None
    mouse_cursor: ControlStateValue[MouseCursor] = None

    def __post_init__(self):
        if not isinstance(self.text_style, dict):
            self.text_style = {ControlState.DEFAULT: self.text_style}

        if not isinstance(self.padding, dict):
            self.padding = {ControlState.DEFAULT: self.padding}

        if not isinstance(self.side, dict):
            self.side = {ControlState.DEFAULT: self.side}

        if not isinstance(self.shape, dict):
            self.shape = {ControlState.DEFAULT: self.shape}
