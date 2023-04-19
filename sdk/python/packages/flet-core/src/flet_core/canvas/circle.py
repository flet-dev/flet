from typing import Any, Optional

from flet_core.canvas.shape import Shape
from flet_core.control import OptionalNumber
from flet_core.painting import Paint
from flet_core.types import OffsetValue


class Circle(Shape):
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
        Shape.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

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
