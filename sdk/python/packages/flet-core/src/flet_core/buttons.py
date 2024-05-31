import dataclasses
from dataclasses import field
from typing import Dict, Optional, Union

from flet_core.border import BorderSide
from flet_core.types import BorderRadiusValue, ControlState, PaddingValue


@dataclasses.dataclass
class OutlinedBorder:
    pass


@dataclasses.dataclass
class StadiumBorder(OutlinedBorder):
    def __post_init__(self):
        self.type = "stadium"


@dataclasses.dataclass
class RoundedRectangleBorder(OutlinedBorder):
    radius: BorderRadiusValue = field(default=None)

    def __post_init__(self):
        self.type = "roundedRectangle"


@dataclasses.dataclass
class CircleBorder(OutlinedBorder):
    type: str = field(default="circle")


@dataclasses.dataclass
class BeveledRectangleBorder(OutlinedBorder):
    radius: BorderRadiusValue = field(default=None)

    def __post_init__(self):
        self.type = "beveledRectangle"


@dataclasses.dataclass
class ContinuousRectangleBorder(OutlinedBorder):
    radius: BorderRadiusValue = field(default=None)

    def __post_init__(self):
        self.type = "continuousRectangle"


@dataclasses.dataclass
class ButtonStyle:
    color: Union[None, str, Dict[Union[str, ControlState], str]] = field(default=None)
    bgcolor: Union[None, str, Dict[Union[str, ControlState], str]] = field(
        default=None
    )
    overlay_color: Union[None, str, Dict[Union[str, ControlState], str]] = field(
        default=None
    )
    shadow_color: Union[None, str, Dict[Union[str, ControlState], str]] = field(
        default=None
    )
    surface_tint_color: Union[None, str, Dict[Union[str, ControlState], str]] = field(
        default=None
    )
    elevation: Union[
        None, float, int, Dict[Union[str, ControlState], Union[float, int]]
    ] = field(default=None)
    animation_duration: Optional[int] = field(default=None)
    padding: Union[PaddingValue, Dict[Union[str, ControlState], PaddingValue]] = field(
        default=None
    )
    side: Union[None, BorderSide, Dict[Union[str, ControlState], BorderSide]] = field(
        default=None
    )
    shape: Union[
        None, OutlinedBorder, Dict[Union[str, ControlState], OutlinedBorder]
    ] = field(default=None)
