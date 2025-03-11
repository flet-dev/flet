from dataclasses import dataclass
from enum import Enum
from typing import Optional


class BlurTileMode(Enum):
    CLAMP = "clamp"
    DECAL = "decal"
    MIRROR = "mirror"
    REPEATED = "repeated"


@dataclass
class Blur:
    sigma_x: float
    sigma_y: float
    tile_mode: Optional[BlurTileMode] = None
