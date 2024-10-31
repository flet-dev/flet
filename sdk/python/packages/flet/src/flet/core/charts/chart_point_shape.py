from dataclasses import dataclass, field
from typing import Optional

from flet.core.types import ColorValue


@dataclass
class ChartPointShape:
    pass


@dataclass
class ChartCirclePoint(ChartPointShape):
    type: str = field(default="circle")
    color: Optional[ColorValue] = None
    radius: Optional[float] = None
    stroke_color: Optional[ColorValue] = None
    stroke_width: Optional[float] = None


@dataclass
class ChartSquarePoint(ChartPointShape):
    type: str = field(default="square")
    color: Optional[ColorValue] = None
    size: Optional[float] = None
    stroke_color: Optional[ColorValue] = None
    stroke_width: Optional[float] = None


@dataclass
class ChartCrossPoint(ChartPointShape):
    type: str = field(default="cross")
    color: Optional[ColorValue] = None
    size: Optional[float] = None
    width: Optional[float] = None
