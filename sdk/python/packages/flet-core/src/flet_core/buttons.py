from dataclasses import dataclass, field
from typing import Dict, Optional, Union

from flet_core.alignment import Alignment
from flet_core.border import BorderSide
from flet_core.text_style import TextStyle
from flet_core.types import (
    BorderRadiusValue,
    ControlState,
    PaddingValue,
    Number,
    VisualDensity,
    MouseCursor,
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
    radius: BorderRadiusValue = None

    def __post_init__(self):
        self.type = "roundedRectangle"


@dataclass
class CircleBorder(OutlinedBorder):
    type: str = field(default="circle")


@dataclass
class BeveledRectangleBorder(OutlinedBorder):
    radius: BorderRadiusValue = None

    def __post_init__(self):
        self.type = "beveledRectangle"


@dataclass
class ContinuousRectangleBorder(OutlinedBorder):
    radius: BorderRadiusValue = None

    def __post_init__(self):
        self.type = "continuousRectangle"


@dataclass
class ButtonStyle:
    color: Union[None, str, Dict[Union[str, ControlState], str]] = None
    bgcolor: Union[None, str, Dict[Union[str, ControlState], str]] = None
    overlay_color: Union[None, str, Dict[Union[str, ControlState], str]] = None
    shadow_color: Union[None, str, Dict[Union[str, ControlState], str]] = None
    surface_tint_color: Union[None, str, Dict[Union[str, ControlState], str]] = None
    elevation: Union[
        None, float, int, Dict[Union[str, ControlState], Union[float, int]]
    ] = None
    animation_duration: Optional[int] = None
    padding: Union[PaddingValue, Dict[Union[str, ControlState], PaddingValue]] = None
    side: Union[None, BorderSide, Dict[Union[str, ControlState], BorderSide]] = None
    shape: Union[
        None, OutlinedBorder, Dict[Union[str, ControlState], OutlinedBorder]
    ] = None
    alignment: Optional[Alignment] = None
    enable_feedback: Optional[bool] = None
    text_style: Union[None, TextStyle, Dict[Union[str, ControlState], TextStyle]] = None
    icon_size: Union[None, Number, Dict[Union[str, ControlState], Number]] = None
    icon_color: Union[None, str, Dict[Union[str, ControlState], str]] = None
    visual_density: Optional[VisualDensity] = None
    mouse_cursor: Union[
        None, MouseCursor, Dict[Union[str, ControlState], MouseCursor]
    ] = None
