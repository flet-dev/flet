from typing import Any, Optional

from flet_core.canvas.shape import Shape
from flet_core.painting import Paint
from flet_core.types import OffsetValue


class Line(Shape):
    def __init__(
        self,
        p1: OffsetValue = None,
        p2: OffsetValue = None,
        paint: Optional[Paint] = None,
        # base
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        Shape.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

        self.p1 = p1
        self.p2 = p2
        self.paint = paint

    def _get_control_name(self):
        return "line"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("p1", self.__p1)
        self._set_attr_json("p2", self.__p2)
        self._set_attr_json("paint", self.__paint)

    # p1
    @property
    def p1(self) -> OffsetValue:
        return self.__p1

    @p1.setter
    def p1(self, value: OffsetValue):
        self.__p1 = value

    # p2
    @property
    def p2(self) -> OffsetValue:
        return self.__p2

    @p2.setter
    def p2(self, value: OffsetValue):
        self.__p2 = value

    # paint
    @property
    def paint(self) -> Optional[Paint]:
        return self.__paint

    @paint.setter
    def paint(self, value: Optional[Paint]):
        self.__paint = value
