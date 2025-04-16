from dataclasses import dataclass
from typing import Optional

from flet.core.alignment import Alignment
from flet.core.border import BorderSide
from flet.core.text_style import TextStyle
from flet.core.types import (
    BorderRadiusValue,
    ColorValue,
    ControlState,
    ControlStateValue,
    MouseCursor,
    OptionalNumber,
    PaddingValue,
    VisualDensity,
)


@dataclass
class OutlinedBorder:
    pass


@dataclass
class StadiumBorder(OutlinedBorder):
    def __post_init__(self):
        self.type = "stadium"


@dataclass
class RoundedRectangleBorder(OutlinedBorder):
    radius: Optional[BorderRadiusValue] = None

    def __post_init__(self):
        self.type = "roundedRectangle"


@dataclass
class CircleBorder(OutlinedBorder):
    def __post_init__(self):
        self.type = "circle"


@dataclass
class BeveledRectangleBorder(OutlinedBorder):
    radius: Optional[BorderRadiusValue] = None

    def __post_init__(self):
        self.type = "beveledRectangle"


@dataclass
class ContinuousRectangleBorder(OutlinedBorder):
    radius: Optional[BorderRadiusValue] = None

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
    animation_duration: Optional[int] = None
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
