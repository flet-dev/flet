import dataclasses
from typing import Any, List, Optional

from flet_core.alignment import Alignment
from flet_core.control import Control, OptionalNumber
from flet_core.painting import Paint, PointMode
from flet_core.text_span import TextSpan
from flet_core.text_style import TextStyle
from flet_core.types import (
    BlendMode,
    BlendModeString,
    BorderRadiusValue,
    FontWeight,
    FontWeightString,
    OffsetValue,
    RotateValue,
    TextAlign,
    TextAlignString,
)


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
    @dataclasses.dataclass
    class PathElement:
        pass

    @dataclasses.dataclass
    class Arc(PathElement):
        x: float
        y: float
        width: float
        height: float
        start_angle: float
        sweep_angle: float
        type: str = dataclasses.field(default="arc")

    @dataclasses.dataclass
    class ArcTo(PathElement):
        x: float
        y: float
        radius: float = dataclasses.field(default=0)
        rotation: float = dataclasses.field(default=0)
        large_arc: bool = dataclasses.field(default=False)
        clockwise: bool = dataclasses.field(default=True)
        type: str = dataclasses.field(default="arcto")

    @dataclasses.dataclass
    class MoveTo(PathElement):
        x: float
        y: float
        type: str = dataclasses.field(default="moveto")

    @dataclasses.dataclass
    class LineTo(PathElement):
        x: float
        y: float
        type: str = dataclasses.field(default="lineto")

    @dataclasses.dataclass
    class QuadraticTo(PathElement):
        cp1x: float
        cp1y: float
        x: float
        y: float
        w: float = dataclasses.field(default=1)
        type: str = dataclasses.field(default="conicto")

    @dataclasses.dataclass
    class CubicTo(PathElement):
        cp1x: float
        cp1y: float
        cp2x: float
        cp2y: float
        x: float
        y: float
        type: str = dataclasses.field(default="cubicto")

    @dataclasses.dataclass
    class Path(PathElement):
        elements: List["DrawPath.PathElement"]
        x: float
        y: float
        type: str = dataclasses.field(default="path")

    @dataclasses.dataclass
    class Close(PathElement):
        type: str = dataclasses.field(default="close")

    def __init__(
        self,
        elements: Optional[List[PathElement]] = None,
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

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("elements", self.__elements)
        self._set_attr_json("paint", self.__paint)

    # elements
    @property
    def elements(self):
        return self.__elements

    @elements.setter
    def elements(self, value: Optional[List[PathElement]]):
        self.__elements = value if value is not None else []

    # paint
    @property
    def paint(self) -> Optional[Paint]:
        return self.__paint

    @paint.setter
    def paint(self, value: Optional[Paint]):
        self.__paint = value


class DrawText(DrawShape):
    def __init__(
        self,
        text: Optional[str] = None,
        style: Optional[TextStyle] = None,
        spans: Optional[List[TextSpan]] = None,
        offset: OffsetValue = None,
        alignment: Optional[Alignment] = None,
        text_align: TextAlign = TextAlign.NONE,
        max_lines: Optional[int] = None,
        max_width: OptionalNumber = None,
        ellipsis: Optional[str] = None,
        rotate: OptionalNumber = None,
        # base
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        DrawShape.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

        self.text = text
        self.style = style
        self.spans = spans
        self.offset = offset
        self.alignment = alignment
        self.text_align = text_align
        self.max_lines = max_lines
        self.max_width = max_width
        self.ellipsis = ellipsis
        self.rotate = rotate

    def _get_control_name(self):
        return "text"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("style", self.__style)
        self._set_attr_json("spans", self.__spans)
        self._set_attr_json("offset", self.__offset)
        self._set_attr_json("alignment", self.__alignment)

    # text
    @property
    def text(self) -> Optional[str]:
        return self._get_attr("text")

    @text.setter
    def text(self, value: Optional[str]):
        self._set_attr("text", value)

    # style
    @property
    def style(self) -> Optional[TextStyle]:
        return self.__style

    @style.setter
    def style(self, value: Optional[TextStyle]):
        self.__style = value

    # spans
    @property
    def spans(self) -> Optional[List[TextSpan]]:
        return self.__spans

    @spans.setter
    def spans(self, value: Optional[List[TextSpan]]):
        self.__spans = value if value is not None else []

    # offset
    @property
    def offset(self) -> OffsetValue:
        return self.__offset

    @offset.setter
    def offset(self, value: OffsetValue):
        self.__offset = value

    # alignment
    @property
    def alignment(self) -> Optional[Alignment]:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value

    # text_align
    @property
    def text_align(self) -> TextAlign:
        return self.__text_align

    @text_align.setter
    def text_align(self, value: TextAlign):
        self.__text_align = value
        if isinstance(value, TextAlign):
            self._set_attr("textAlign", value.value)
        else:
            self.__set_text_align(value)

    def __set_text_align(self, value: TextAlignString):
        self._set_attr("textAlign", value)

    # max_lines
    @property
    def max_lines(self) -> Optional[int]:
        return self._get_attr("maxLines")

    @max_lines.setter
    def max_lines(self, value: Optional[int]):
        self._set_attr("maxLines", value)

    # max_width
    @property
    def max_width(self) -> OptionalNumber:
        return self._get_attr("maxWidth")

    @max_width.setter
    def max_width(self, value: OptionalNumber):
        self._set_attr("maxWidth", value)

    # ellipsis
    @property
    def ellipsis(self) -> Optional[str]:
        return self._get_attr("ellipsis")

    @ellipsis.setter
    def ellipsis(self, value: Optional[str]):
        self._set_attr("ellipsis", value)

    # rotate
    @property
    def rotate(self) -> OptionalNumber:
        return self._get_attr("rotate")

    @rotate.setter
    def rotate(self, value: OptionalNumber):
        self._set_attr("rotate", value)
