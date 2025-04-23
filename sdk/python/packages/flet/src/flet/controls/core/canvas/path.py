from dataclasses import dataclass, field
from typing import List, Optional

from flet.controls.base_control import control
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint


@control("Path")
class Path(Shape):
    @dataclass(kw_only=True)
    class PathElement:
        type: str = ""

    @dataclass
    class MoveTo(PathElement):
        x: float
        y: float

        def __post_init__(self):
            self.type = "moveto"

    @dataclass
    class LineTo(PathElement):
        x: float
        y: float

        def __post_init__(self):
            self.type = "lineto"

    @dataclass
    class QuadraticTo(PathElement):
        cp1x: float
        cp1y: float
        x: float
        y: float
        w: float = 1

        def __post_init__(self):
            self.type = "conicto"

    @dataclass
    class CubicTo(PathElement):
        cp1x: float
        cp1y: float
        cp2x: float
        cp2y: float
        x: float
        y: float

        def __post_init__(self):
            self.type = "cubicto"

    @dataclass
    class SubPath(PathElement):
        elements: List["Path.PathElement"]
        x: float
        y: float

        def __post_init__(self):
            self.type = "subpath"

    @dataclass
    class Arc(PathElement):
        x: float
        y: float
        width: float
        height: float
        start_angle: float
        sweep_angle: float

        def __post_init__(self):
            self.type = "arc"

    @dataclass
    class ArcTo(PathElement):
        x: float
        y: float
        radius: float = 0
        rotation: float = 0
        large_arc: bool = False
        clockwise: bool = True

        def __post_init__(self):
            self.type = "arcto"

    @dataclass
    class Oval(PathElement):
        x: float
        y: float
        width: float
        height: float

        def __post_init__(self):
            self.type = "oval"

    @dataclass
    class Rect(PathElement):
        x: float
        y: float
        width: float
        height: float
        border_radius: OptionalBorderRadiusValue = None

        def __post_init__(self):
            self.type = "rect"

    @dataclass
    class Close(PathElement):
        def __post_init__(self):
            self.type = "close"

    elements: List[PathElement] = field(default_factory=list)
    paint: Optional[Paint] = None
