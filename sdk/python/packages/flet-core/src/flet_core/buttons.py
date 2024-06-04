from dataclasses import dataclass, field
from typing import Dict, Optional, Union

from flet_core.border import BorderSide
from flet_core.types import BorderRadiusValue, MaterialState, PaddingValue


@dataclass
class OutlinedBorder:
    pass


@dataclass
class StadiumBorder(OutlinedBorder):
    type: str = field(default="stadium")


@dataclass
class RoundedRectangleBorder(OutlinedBorder):
    type: str = field(default="roundedRectangle")
    radius: BorderRadiusValue = field(default=None)


@dataclass
class CircleBorder(OutlinedBorder):
    type: str = field(default="circle")


@dataclass
class BeveledRectangleBorder(OutlinedBorder):
    type: str = field(default="beveledRectangle")
    radius: BorderRadiusValue = field(default=None)


@dataclass
class ContinuousRectangleBorder(OutlinedBorder):
    type: str = field(default="continuousRectangle")
    radius: BorderRadiusValue = field(default=None)


@dataclass
class ButtonStyle:
    color: Union[None, str, Dict[Union[str, MaterialState], str]] = field(default=None)
    bgcolor: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    overlay_color: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    shadow_color: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    surface_tint_color: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    elevation: Union[
        None, float, int, Dict[Union[str, MaterialState], Union[float, int]]
    ] = field(default=None)
    animation_duration: Optional[int] = field(default=None)
    padding: Union[PaddingValue, Dict[Union[str, MaterialState], PaddingValue]] = field(
        default=None
    )
    side: Union[None, BorderSide, Dict[Union[str, MaterialState], BorderSide]] = field(
        default=None
    )
    shape: Union[
        None, OutlinedBorder, Dict[Union[str, MaterialState], OutlinedBorder]
    ] = field(default=None)
