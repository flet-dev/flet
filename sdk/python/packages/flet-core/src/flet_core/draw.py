from typing import Any, List, Optional

from flet_core.control import Control, OptionalNumber
from flet_core.paint import Paint
from flet_core.types import BlendMode, BlendModeString, OffsetValue


class DrawShape(Control):
    def __init__(
        self,
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        Control.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)


class DrawArc(DrawShape):
    def __init__(
        self,
        start: OffsetValue = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        start_agnle: OptionalNumber = None,
        sweep_angle: OptionalNumber = None,
        use_center: Optional[bool] = None,
        paint: Optional[Paint] = None,
        # base
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        DrawShape.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

        self.start = start
        self.width = width
        self.height = height
        self.start_angle = start_agnle
        self.sweep_angle = sweep_angle
        self.use_center = use_center
        self.paint = paint

    def _get_control_name(self):
        return "arc"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("start", self.__start)
        self._set_attr_json("paint", self.__paint)

    # start
    @property
    def start(self) -> OffsetValue:
        return self.__start

    @start.setter
    def start(self, value: OffsetValue):
        self.__start = value

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
    def use_center(self) -> Optional[bool]:
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


class DrawColor(DrawShape):
    def __init__(
        self,
        color: Optional[str] = None,
        blend_mode: BlendMode = BlendMode.NONE,
        # base
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        DrawShape.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

        self.color = color
        self.blend_mode = blend_mode

    def _get_control_name(self):
        return "color"

    def _before_build_command(self):
        super()._before_build_command()

    # color
    @property
    def color(self) -> Optional[str]:
        return self._get_attr("color")

    @color.setter
    def color(self, value: Optional[str]):
        self._set_attr("color", value)

    # blend_mode
    @property
    def blend_mode(self) -> BlendMode:
        return self.__blend_mode

    @blend_mode.setter
    def blend_mode(self, value: BlendMode):
        self.__blend_mode = value
        if isinstance(value, BlendMode):
            self._set_attr("blendMode", value.value)
        else:
            self.__set_blend_mode(value)

    def __set_blend_mode(self, value: BlendModeString):
        self._set_attr("blendMode", value)


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


class DrawOval(DrawShape):
    def __init__(
        self,
        start: OffsetValue = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        paint: Optional[Paint] = None,
        # base
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        DrawShape.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

        self.start = start
        self.width = width
        self.height = height
        self.paint = paint

    def _get_control_name(self):
        return "oval"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("start", self.__start)
        self._set_attr_json("paint", self.__paint)

    # start
    @property
    def start(self) -> OffsetValue:
        return self.__start

    @start.setter
    def start(self, value: OffsetValue):
        self.__start = value

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


class DrawPaint(DrawShape):
    def __init__(
        self,
        paint: Optional[Paint] = None,
        # base
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        DrawShape.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

        self.paint = paint

    def _get_control_name(self):
        return "paint"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("paint", self.__paint)

    # paint
    @property
    def paint(self) -> Optional[Paint]:
        return self.__paint

    @paint.setter
    def paint(self, value: Optional[Paint]):
        self.__paint = value
