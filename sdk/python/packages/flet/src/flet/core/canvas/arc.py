from typing import Any, Optional

from flet.core.canvas.shape import Shape
from flet.core.control import OptionalNumber
from flet.core.painting import Paint


class Arc(Shape):
    def __init__(
        self,
        x: OptionalNumber = None,
        y: OptionalNumber = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        start_angle: OptionalNumber = None,
        sweep_angle: OptionalNumber = None,
        use_center: Optional[bool] = None,
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
        self.width = width
        self.height = height
        self.start_angle = start_angle
        self.sweep_angle = sweep_angle
        self.use_center = use_center
        self.paint = paint

    def _get_control_name(self):
        return "arc"

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

    # start_angle
    @property
    def start_angle(self) -> OptionalNumber:
        return self._get_attr("startAngle")

    @start_angle.setter
    def start_angle(self, value: OptionalNumber):
        self._set_attr("startAngle", value)

    # sweep_angle
    @property
    def sweep_angle(self) -> OptionalNumber:
        return self._get_attr("sweepAngle")

    @sweep_angle.setter
    def sweep_angle(self, value: OptionalNumber):
        self._set_attr("sweepAngle", value)

    # use_center
    @property
    def use_center(self) -> bool:
        return self._get_attr("useCenter", data_type="bool", def_value=False)

    @use_center.setter
    def use_center(self, value: Optional[bool]):
        self._set_attr("useCenter", value)

    # paint
    @property
    def paint(self) -> Optional[Paint]:
        return self.__paint

    @paint.setter
    def paint(self, value: Optional[Paint]):
        self.__paint = value
