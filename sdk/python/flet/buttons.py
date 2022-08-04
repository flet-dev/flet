import dataclasses
import math
from dataclasses import field
from typing import Dict, List, Union

from flet import alignment
from flet.alignment import Alignment
from flet.border import BorderSide
from flet.types import BorderRadiusValue, PaddingValue

try:
    from typing import Literal
except:
    from typing_extensions import Literal

OutlinedBorderType = Literal[
    None,
    "beveledRectangle",
    "circle",
    "countinuosRectangle",
    "roundedRectangle",
    "stadium",
]

# Material states
#   hovered
#   focused
#   pressed
#   dragged
#   selected
#   scrolledUnder
#   disabled
#   error


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
    color: Union[str, Dict[str, str]] = field(default=None)
    bgcolor: Union[str, Dict[str, str]] = field(default=None)
    overlay_color: Union[str, Dict[str, str]] = field(default=None)
    shadow_color: Union[str, Dict[str, str]] = field(default=None)
    surface_tint_color: Union[str, Dict[str, str]] = field(default=None)
    elevation: Union[float, int, Dict[str, Union[float, int]]] = field(default=None)
    animation_duration: int = field(default=None)
    padding: Union[PaddingValue, Dict[str, PaddingValue]] = field(default=None)
    side: Union[BorderSide, Dict[str, BorderSide]] = field(default=None)
    shape: Union[OutlinedBorder, Dict[str, OutlinedBorder]] = field(default=None)
