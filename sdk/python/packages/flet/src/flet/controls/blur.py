from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

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
    """
    Horizontal sigma.
    """

    sigma_y: Number
    """
    Vertical sigma.
    """

    tile_mode: Optional[BlurTileMode] = None
    """
    The tile mode for the blur.

    Value is of type [`BlurTileMode`](https://flet.dev/docs/reference/types/blurtilemode).
    """


BlurValue = Union[Number, tuple[Number, Number], Blur]
OptionalBlurValue = Optional[BlurValue]
OptionalBlurTileMode = Optional[BlurTileMode]
