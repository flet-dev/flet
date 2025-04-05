from dataclasses import dataclass

from flet.controls.types import OptionalColorValue, OptionalNumber


@dataclass
class ChartPointShape:
    pass


@dataclass
class ChartCirclePoint(ChartPointShape):
    color: OptionalColorValue = None
    radius: OptionalNumber = None
    stroke_color: OptionalColorValue = None
    stroke_width: OptionalNumber = None

    def __post_init__(self):
        self.type = "circle"


@dataclass
class ChartSquarePoint(ChartPointShape):
    color: OptionalColorValue = None
    size: OptionalNumber = None
    stroke_color: OptionalColorValue = None
    stroke_width: OptionalNumber = None

    def __post_init__(self):
        self.type = "square"


@dataclass
class ChartCrossPoint(ChartPointShape):
    color: OptionalColorValue = None
    size: OptionalNumber = None
    width: OptionalNumber = None

    def __post_init__(self):
        self.type = "cross"
