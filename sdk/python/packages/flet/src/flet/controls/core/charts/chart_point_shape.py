from dataclasses import dataclass

from flet.controls.types import Number, OptionalColorValue, OptionalNumber


@dataclass(kw_only=True)
class ChartPointShape:
    type: str = ""


@dataclass
class ChartCirclePoint(ChartPointShape):
    color: OptionalColorValue = None
    radius: OptionalNumber = None
    stroke_color: OptionalColorValue = None
    stroke_width: Number = 0

    def __post_init__(self):
        self.type = "circle"


@dataclass
class ChartSquarePoint(ChartPointShape):
    color: OptionalColorValue = None
    size: Number = 4.0
    stroke_color: OptionalColorValue = None
    stroke_width: Number = 1.0

    def __post_init__(self):
        self.type = "square"


@dataclass
class ChartCrossPoint(ChartPointShape):
    color: OptionalColorValue = None
    size: Number = 8.0
    width: Number = 2.0

    def __post_init__(self):
        self.type = "cross"
