from typing import Any, List, Optional

from flet_core.control import Control, OptionalNumber
from flet_core.paint import Paint, PointMode
from flet_core.types import BlendMode, BlendModeString, BorderRadiusValue, OffsetValue


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
        offset: OffsetValue = None,
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

        self.offset = offset
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
        self._set_attr_json("offset", self.__offset)
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
        offset: OffsetValue = None,
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

        self.offset = offset
        self.width = width
        self.height = height
        self.paint = paint

    def _get_control_name(self):
        return "oval"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("offset", self.__offset)
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


class DrawPoints(DrawShape):
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
        DrawShape.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

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
        self._set_attr("pointMode", value.value)

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


class DrawRect(DrawShape):
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
        DrawShape.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

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


class DrawPath(DrawShape):
    def __init__(
        self,
        elements: Optional[List[DrawShape]] = None,
        paint: Optional[Paint] = None,
        # base
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        DrawShape.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

        self.elements = elements
        self.paint = paint

    def _get_control_name(self):
        return "path"

    def _get_children(self):
        return self.__elements

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("paint", self.__paint)

    # elements
    @property
    def elements(self):
        return self.__elements

    @elements.setter
    def elements(self, value: Optional[List[DrawShape]]):
        self.__elements = value if value is not None else []

    # paint
    @property
    def paint(self) -> Optional[Paint]:
        return self.__paint

    @paint.setter
    def paint(self, value: Optional[Paint]):
        self.__paint = value

    class MoveTo(DrawShape):
        def __init__(
            self,
            x: OptionalNumber = None,
            y: OptionalNumber = None,
            # base
            ref=None,
            visible: Optional[bool] = None,
            disabled: Optional[bool] = None,
            data: Any = None,
        ):
            DrawShape.__init__(
                self, ref=ref, visible=visible, disabled=disabled, data=data
            )

            self.x = x
            self.y = y

        def _get_control_name(self):
            return "moveto"

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

    class LineTo(DrawShape):
        def __init__(
            self,
            x: OptionalNumber = None,
            y: OptionalNumber = None,
            # base
            ref=None,
            visible: Optional[bool] = None,
            disabled: Optional[bool] = None,
            data: Any = None,
        ):
            DrawShape.__init__(
                self, ref=ref, visible=visible, disabled=disabled, data=data
            )

            self.x = x
            self.y = y

        def _get_control_name(self):
            return "lineto"

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

    class ConicTo(DrawShape):
        def __init__(
            self,
            x1: OptionalNumber = None,
            y1: OptionalNumber = None,
            x2: OptionalNumber = None,
            y2: OptionalNumber = None,
            w: OptionalNumber = 1,
            # base
            ref=None,
            visible: Optional[bool] = None,
            disabled: Optional[bool] = None,
            data: Any = None,
        ):
            DrawShape.__init__(
                self, ref=ref, visible=visible, disabled=disabled, data=data
            )

            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2
            self.w = w

        def _get_control_name(self):
            return "conicto"

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

        # w
        @property
        def w(self) -> OptionalNumber:
            return self._get_attr("w", data_type="float", def_value=1)

        @w.setter
        def w(self, value: OptionalNumber):
            self._set_attr("w", value)

    class CubicTo(DrawShape):
        def __init__(
            self,
            x1: OptionalNumber = None,
            y1: OptionalNumber = None,
            x2: OptionalNumber = None,
            y2: OptionalNumber = None,
            x3: OptionalNumber = None,
            y3: OptionalNumber = None,
            # base
            ref=None,
            visible: Optional[bool] = None,
            disabled: Optional[bool] = None,
            data: Any = None,
        ):
            DrawShape.__init__(
                self, ref=ref, visible=visible, disabled=disabled, data=data
            )

            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2
            self.x3 = x3
            self.y3 = y3

        def _get_control_name(self):
            return "cubicto"

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

        # x3
        @property
        def x3(self) -> OptionalNumber:
            return self._get_attr("x3")

        @x3.setter
        def x3(self, value: OptionalNumber):
            self._set_attr("x3", value)

        # y3
        @property
        def y3(self) -> OptionalNumber:
            return self._get_attr("y3")

        @y3.setter
        def y3(self, value: OptionalNumber):
            self._set_attr("y3", value)

    class BezierTo(DrawShape):
        def __init__(
            self,
            x1: OptionalNumber = None,
            y1: OptionalNumber = None,
            x2: OptionalNumber = None,
            y2: OptionalNumber = None,
            # base
            ref=None,
            visible: Optional[bool] = None,
            disabled: Optional[bool] = None,
            data: Any = None,
        ):
            DrawShape.__init__(
                self, ref=ref, visible=visible, disabled=disabled, data=data
            )

            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2

        def _get_control_name(self):
            return "bezierto"

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

    class Close(DrawShape):
        def __init__(
            self,
            # base
            ref=None,
            visible: Optional[bool] = None,
            disabled: Optional[bool] = None,
            data: Any = None,
        ):
            DrawShape.__init__(
                self, ref=ref, visible=visible, disabled=disabled, data=data
            )

        def _get_control_name(self):
            return "close"
