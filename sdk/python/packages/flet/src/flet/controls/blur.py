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
    """
    Edge sampling mode used when applying blur beyond source bounds.
    """

    CLAMP = "clamp"
    """
    Extends edge pixels outward.
    """

    DECAL = "decal"
    """
    Treats samples outside bounds as transparent.
    """

    MIRROR = "mirror"
    """
    Repeats the image by mirroring at each edge.
    """

    REPEATED = "repeated"
    """
    Repeats the image pattern without mirroring.
    """


@dataclass
class Blur:
    """
    Gaussian blur configuration.
    """

    sigma_x: Number
    """
    Horizontal Gaussian sigma.

    Larger values produce stronger blur along the X axis.
    """

    sigma_y: Number
    """
    Vertical Gaussian sigma.

    Larger values produce stronger blur along the Y axis.
    """

    tile_mode: Optional[BlurTileMode] = None
    """
    How sampling outside source bounds is handled during blur.
    """


BlurValue = Union[Number, tuple[Number, Number], Blur]
"""Type alias for blur configuration values.

Represents blur as either:
- a single sigma value applied to both axes,
- a `(sigma_x, sigma_y)` tuple,
- or an explicit [`Blur`][flet.] object.
"""
