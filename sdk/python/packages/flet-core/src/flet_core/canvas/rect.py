from typing import Any, Optional

from flet_core.canvas.shape import Shape
from flet_core.control import OptionalNumber
from flet_core.painting import Paint
from flet_core.types import BorderRadiusValue, OffsetValue


class Rect(Shape):
    def __init__(
        self,
        offset: OffsetValue = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        border_radius: Optional[BorderRadiusValue] = None,
        paint: Optional[Paint] = None,
        # base
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        Shape.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

        self.offset = offset
        self.width = width
        self.height = height
        self.border_radius = border_radius
        self.paint = paint

    def _get_control_name(self):
        return "rect"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("offset", self.__offset)
        self._set_attr_json("borderRadius", self.__border_radius)
        self._set_attr_json("paint", self.__paint)

    # offset
    @property
    def offset(self) -> OffsetValue:
        return self.__offset

    @offset.setter
    def offset(self, value: OffsetValue):
        self.__offset = value

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

    # border_radius
    @property
    def border_radius(self) -> BorderRadiusValue:
        return self.__border_radius

    @border_radius.setter
    def border_radius(self, value: BorderRadiusValue):
        self.__border_radius = value

    # paint
    @property
    def paint(self) -> Optional[Paint]:
        return self.__paint

    @paint.setter
    def paint(self, value: Optional[Paint]):
        self.__paint = value
