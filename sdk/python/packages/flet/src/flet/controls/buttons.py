from dataclasses import dataclass
from typing import Optional

from flet.controls.alignment import OptionalAlignment
from flet.controls.border import BorderSide, OptionalBorderSide
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.control_state import OptionalControlStateValue
from flet.controls.duration import OptionalDurationValue
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ColorValue,
    MouseCursor,
    Number,
    OptionalBool,
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
    "OptionalButtonStyle",
    "OptionalOutlinedBorder",
]


@dataclass
class OutlinedBorder:
    side: OptionalBorderSide = None
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
    eccentricity: Number = 0.0

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
    alignment: OptionalAlignment = None
    enable_feedback: OptionalBool = None
    text_style: OptionalControlStateValue[TextStyle] = None
    icon_size: OptionalControlStateValue[OptionalNumber] = None
    icon_color: OptionalControlStateValue[ColorValue] = None
    visual_density: Optional[VisualDensity] = None
    mouse_cursor: OptionalControlStateValue[MouseCursor] = None


# Typing
OptionalButtonStyle = Optional[ButtonStyle]
OptionalOutlinedBorder = Optional[OutlinedBorder]
