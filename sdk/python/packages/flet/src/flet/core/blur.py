from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple, Union

from flet.core.types import Number

__all__ = ["Blur", "BlurTileMode", "BlurValue", "OptionalBlurValue"]


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
OptionalBlurValue = Union[Number, Tuple[Number, Number], Blur]
