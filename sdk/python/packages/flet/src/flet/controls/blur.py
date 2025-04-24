from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple, Union

from flet.controls.types import Number

__all__ = [
    "Blur",
    "BlurTileMode",
    "BlurValue",
    "OptionalBlurValue",
    "OptionalBlurTileMode",
]


class BlurTileMode(Enum):
    CLAMP = "clamp"
    DECAL = "decal"
    MIRROR = "mirror"
    REPEATED = "repeated"


@dataclass
class Blur:
    sigma_x: Number
    sigma_y: Number
    tile_mode: Optional[BlurTileMode] = None


BlurValue = Union[Number, Tuple[Number, Number], Blur]
OptionalBlurValue = Optional[BlurValue]
OptionalBlurTileMode = Optional[BlurTileMode]
