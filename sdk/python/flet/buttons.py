import dataclasses
from dataclasses import field
from typing import Dict, Optional, Union

from flet.border import BorderSide
from flet.types import BorderRadiusValue, PaddingValue

try:
    from typing import Literal
except:
    from typing_extensions import Literal

MaterialState = Literal[
    "hovered",
    "focused",
    "pressed",
    "dragged",
    "selected",
    "scrolledUnder",
    "disabled",
    "error",
    "",
]


@dataclasses.dataclass
class OutlinedBorder:
    pass


@dataclasses.dataclass
class StadiumBorder:
    type: str = field(default="stadium")


@dataclasses.dataclass
class RoundedRectangleBorder:
    type: str = field(default="roundedRectangle")
    radius: BorderRadiusValue = field(default=None)


@dataclasses.dataclass
class CircleBorder:
    type: str = field(default="circle")


@dataclasses.dataclass
class BeveledRectangleBorder:
    type: str = field(default="beveledRectangle")
    radius: BorderRadiusValue = field(default=None)


@dataclasses.dataclass
class CountinuosRectangleBorder:
    type: str = field(default="countinuosRectangle")
    radius: BorderRadiusValue = field(default=None)


@dataclasses.dataclass
class ButtonStyle:
    color: Union[None, str, Dict[MaterialState, str]] = field(default=None)
    bgcolor: Union[None, str, Dict[MaterialState, str]] = field(default=None)
    overlay_color: Union[None, str, Dict[MaterialState, str]] = field(default=None)
    shadow_color: Union[None, str, Dict[MaterialState, str]] = field(default=None)
    surface_tint_color: Union[None, str, Dict[MaterialState, str]] = field(default=None)
    elevation: Union[None, float, int, Dict[MaterialState, Union[float, int]]] = field(
        default=None
    )
    animation_duration: Optional[int] = field(default=None)
    padding: Union[PaddingValue, Dict[MaterialState, PaddingValue]] = field(
        default=None
    )
    side: Union[None, BorderSide, Dict[MaterialState, BorderSide]] = field(default=None)
    shape: Union[None, OutlinedBorder, Dict[MaterialState, OutlinedBorder]] = field(
        default=None
    )
