from dataclasses import dataclass
from typing import Any, List, Optional

from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint


@control("Path")
class Path(Shape):
    @dataclass
    class PathElement:
        pass

    @dataclass
    class MoveTo(PathElement):
        x: float
        y: float
        type: str = "moveto"

    @dataclass
    class LineTo(PathElement):
        x: float
        y: float
        type: str = "lineto"

    @dataclass
    class QuadraticTo(PathElement):
        cp1x: float
        cp1y: float
        x: float
        y: float
        w: float = 1
        type: str = "conicto"

    @dataclass
    class CubicTo(PathElement):
        cp1x: float
        cp1y: float
        cp2x: float
        cp2y: float
        x: float
        y: float
        type: str = "cubicto"

    @dataclass
    class SubPath(PathElement):
        elements: List["Path.PathElement"]
        x: float
        y: float
        type: str = "subpath"

    @dataclass
    class Arc(PathElement):
        x: float
        y: float
        width: float
        height: float
        start_angle: float
        sweep_angle: float
        type: str = "arc"

    @dataclass
    class ArcTo(PathElement):
        x: float
        y: float
        radius: float = 0
        rotation: float = 0
        large_arc: bool = False
        clockwise: bool = True
        type: str = "arcto"

    @dataclass
    class Oval(PathElement):
        x: float
        y: float
        width: float
        height: float
        type: str = "oval"

    @dataclass
    class Rect(PathElement):
        x: float
        y: float
        width: float
        height: float
        border_radius: OptionalBorderRadiusValue = None
        type: str = "rect"

    @dataclass
    class Close(PathElement):
        type: str = "close"

    elements: Optional[List[PathElement]] = None
    paint: Optional[Paint] = None
