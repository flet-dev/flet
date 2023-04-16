from typing import Any, List, Optional

from flet_core.control import Control, OptionalNumber
from flet_core.paint import Paint
from flet_core.types import OffsetValue


class DrawShape(Control):
    def __init__(
        self,
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        Control.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)


class DrawLine(DrawShape):
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
        DrawShape.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

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


class DrawCircle(DrawShape):
    def __init__(
        self,
        center: OffsetValue = None,
        radius: OptionalNumber = None,
        paint: Optional[Paint] = None,
        # base
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        DrawShape.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

        self.center = center
        self.radius = radius
        self.paint = paint

    def _get_control_name(self):
        return "circle"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("center", self.__center)
        self._set_attr_json("paint", self.__paint)

    # center
    @property
    def center(self) -> OffsetValue:
        return self.__center

    @center.setter
    def center(self, value: OffsetValue):
        self.__center = value

    # radius
    @property
    def radius(self) -> OptionalNumber:
        return self._get_attr("radius")

    @radius.setter
    def radius(self, value: OptionalNumber):
        self._set_attr("radius", value)

    # paint
    @property
    def paint(self) -> Optional[Paint]:
        return self.__paint

    @paint.setter
    def paint(self, value: Optional[Paint]):
        self.__paint = value
