from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from flet.controls.types import Number

__all__ = [
    "Blur",
    "BlurTileMode",
    "BlurValue",
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
    """


BlurValue = Union[Number, tuple[Number, Number], Blur]
"""Type alias for blur configuration values.

Represents blur as either:
- a single sigma value applied to both axes,
- a `(sigma_x, sigma_y)` tuple,
- or an explicit [`Blur`][flet.] object.
"""
