from dataclasses import dataclass
from typing import Optional

from flet.core.types import ColorValue, OptionalNumber


@dataclass
class ChartPointShape:
    pass


@dataclass
class ChartCirclePoint(ChartPointShape):
    color: Optional[ColorValue] = None
    radius: OptionalNumber = None
    stroke_color: Optional[ColorValue] = None
    stroke_width: OptionalNumber = None

    def __post_init__(self):
        self.type = "circle"


@dataclass
class ChartSquarePoint(ChartPointShape):
    color: Optional[ColorValue] = None
    size: OptionalNumber = None
    stroke_color: Optional[ColorValue] = None
    stroke_width: OptionalNumber = None

    def __post_init__(self):
        self.type = "square"


@dataclass
class ChartCrossPoint(ChartPointShape):
    color: Optional[ColorValue] = None
    size: OptionalNumber = None
    width: OptionalNumber = None

    def __post_init__(self):
        self.type = "cross"
