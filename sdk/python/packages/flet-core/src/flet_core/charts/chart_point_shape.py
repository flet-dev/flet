import dataclasses
from dataclasses import field
from typing import Optional


@dataclasses.dataclass
class ChartPointShape:
    pass


@dataclasses.dataclass
class ChartCirclePoint(ChartPointShape):
    type: str = field(default="circle")
    color: Optional[str] = field(default=None)
    radius: Optional[float] = field(default=None)
    stroke_color: Optional[str] = field(default=None)
    stroke_width: Optional[float] = field(default=None)


@dataclasses.dataclass
class ChartSquarePoint(ChartPointShape):
    type: str = field(default="square")
    color: Optional[str] = field(default=None)
    size: Optional[float] = field(default=None)
    stroke_color: Optional[str] = field(default=None)
    stroke_width: Optional[float] = field(default=None)


@dataclasses.dataclass
class ChartCrossPoint(ChartPointShape):
    type: str = field(default="cross")
    color: Optional[str] = field(default=None)
    size: Optional[float] = field(default=None)
    width: Optional[float] = field(default=None)
