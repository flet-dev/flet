from typing import Any, Optional

from flet.core.canvas.shape import Shape
from flet.core.control import OptionalNumber
from flet.core.painting import Paint


class Circle(Shape):
    def __init__(
        self,
        x: OptionalNumber = None,
        y: OptionalNumber = None,
        radius: OptionalNumber = None,
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

        self.x = x
        self.y = y
        self.radius = radius
        self.paint = paint

    def _get_control_name(self):
        return "circle"

    def before_update(self):
        super().before_update()
        self._set_attr_json("paint", self.__paint)

    # x
    @property
    def x(self) -> OptionalNumber:
        return self._get_attr("x")

    @x.setter
    def x(self, value: OptionalNumber):
        self._set_attr("x", value)

    # y
    @property
    def y(self) -> OptionalNumber:
        return self._get_attr("y")

    @y.setter
    def y(self, value: OptionalNumber):
        self._set_attr("y", value)

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
