from enum import Enum
from typing import Any, List, Optional

from flet_core.canvas.shape import Shape
from flet_core.painting import Paint
from flet_core.types import OffsetValue


class PointMode(Enum):
    POINTS = "points"
    LINES = "lines"
    POLYGON = "polygon"


class Points(Shape):
    def __init__(
        self,
        points: Optional[List[OffsetValue]] = None,
        point_mode: Optional[PointMode] = None,
        paint: Optional[Paint] = None,
        # base
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        Shape.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

        self.points = points
        self.point_mode = point_mode
        self.paint = paint

    def _get_control_name(self):
        return "points"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("points", self.__points)
        self._set_attr_json("paint", self.__paint)

    # point_mode
    @property
    def point_mode(self) -> Optional[PointMode]:
        return self.__point_mode

    @point_mode.setter
    def point_mode(self, value: Optional[PointMode]):
        self.__point_mode = value
        self._set_attr("pointMode", value.value if value is not None else None)

    # points
    @property
    def points(self) -> Optional[List[OffsetValue]]:
        return self.__points

    @points.setter
    def points(self, value: Optional[List[OffsetValue]]):
        self.__points = value if value is not None else []

    # paint
    @property
    def paint(self) -> Optional[Paint]:
        return self.__paint

    @paint.setter
    def paint(self, value: Optional[Paint]):
        self.__paint = value
