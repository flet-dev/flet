from dataclasses import dataclass, field
from enum import Enum
from typing import Union, Tuple

from flet.core.types import Number

__all__ = ["Blur", "BlurTileMode", "BlurValue"]


class BlurTileMode(Enum):
    CLAMP = "clamp"
    DECAL = "decal"
    MIRROR = "mirror"
    REPEATED = "repeated"


@dataclass
class Blur:
    sigma_x: Number
    sigma_y: Number
    tile_mode: BlurTileMode = field(default=BlurTileMode.CLAMP)


BlurValue = Union[Number, Tuple[Number, Number], Blur]
