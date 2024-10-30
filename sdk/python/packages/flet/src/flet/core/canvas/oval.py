from typing import Any, Optional

from flet.core.canvas.shape import Shape
from flet.core.control import OptionalNumber
from flet.core.painting import Paint


class Oval(Shape):
    def __init__(
        self,
        x: OptionalNumber = None,
        y: OptionalNumber = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        paint: Optional[Paint] = None,
        # base
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        Shape.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.paint = paint

    def _get_control_name(self):
        return "oval"

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

    # width
    @property
    def width(self) -> OptionalNumber:
        return self._get_attr("width")

    @width.setter
    def width(self, value: OptionalNumber):
        self._set_attr("width", value)

    # height
    @property
    def height(self) -> OptionalNumber:
        return self._get_attr("height")

    @height.setter
    def height(self, value: OptionalNumber):
        self._set_attr("height", value)

    # paint
    @property
    def paint(self) -> Optional[Paint]:
        return self.__paint

    @paint.setter
    def paint(self, value: Optional[Paint]):
        self.__paint = value
