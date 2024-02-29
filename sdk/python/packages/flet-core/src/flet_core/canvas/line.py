from typing import Any, Optional

from flet_core.canvas.shape import Shape
from flet_core.control import OptionalNumber
from flet_core.painting import Paint


class Line(Shape):
    def __init__(
        self,
        x1: OptionalNumber = None,
        y1: OptionalNumber = None,
        x2: OptionalNumber = None,
        y2: OptionalNumber = None,
        paint: Optional[Paint] = None,
        #
        # Control
        #
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        Shape.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.paint = paint

    def _get_control_name(self):
        return "line"

    def before_update(self):
        super().before_update()
        self._set_attr_json("paint", self.__paint)

    # x1
    @property
    def x1(self) -> OptionalNumber:
        return self._get_attr("x1")

    @x1.setter
    def x1(self, value: OptionalNumber):
        self._set_attr("x1", value)

    # y1
    @property
    def y1(self) -> OptionalNumber:
        return self._get_attr("y1")

    @y1.setter
    def y1(self, value: OptionalNumber):
        self._set_attr("y1", value)

    # x2
    @property
    def x2(self) -> OptionalNumber:
        return self._get_attr("x2")

    @x2.setter
    def x2(self, value: OptionalNumber):
        self._set_attr("x2", value)

    # y2
    @property
    def y2(self) -> OptionalNumber:
        return self._get_attr("y2")

    @y2.setter
    def y2(self, value: OptionalNumber):
        self._set_attr("y2", value)

    # paint
    @property
    def paint(self) -> Optional[Paint]:
        return self.__paint

    @paint.setter
    def paint(self, value: Optional[Paint]):
        self.__paint = value
