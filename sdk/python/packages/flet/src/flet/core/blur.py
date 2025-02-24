from dataclasses import dataclass, field

from flet.core.enumerations import ExtendedEnum


class BlurTileMode(ExtendedEnum):
    CLAMP = "clamp"
    DECAL = "decal"
    MIRROR = "mirror"
    REPEATED = "repeated"


@dataclass
class Blur:
    sigma_x: float
    sigma_y: float
    tile_mode: BlurTileMode = field(default=BlurTileMode.CLAMP)
