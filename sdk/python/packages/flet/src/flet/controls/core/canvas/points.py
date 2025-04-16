from enum import Enum
from typing import Any, List, Optional

from flet.controls.base_control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint
from flet.controls.transform import OffsetValue


class PointMode(Enum):
    POINTS = "points"
    LINES = "lines"
    POLYGON = "polygon"


@control("Points")
class Points(Shape):
    points: Optional[List[OffsetValue]] = None
    point_mode: Optional[PointMode] = None
    paint: Optional[Paint] = None
