import dataclasses
from typing import Any, List, Optional

from flet_core.canvas.shape import Shape
from flet_core.painting import Paint
from flet_core.types import BorderRadiusValue


class Path(Shape):
    @dataclasses.dataclass
    class PathElement:
        pass

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
    class SubPath(PathElement):
        elements: List["Path.PathElement"]
        x: float
        y: float
        type: str = dataclasses.field(default="subpath")

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
    class Oval(PathElement):
        x: float
        y: float
        width: float
        height: float
        type: str = dataclasses.field(default="oval")

    @dataclasses.dataclass
    class Rect(PathElement):
        x: float
        y: float
        width: float
        height: float
        border_radius: BorderRadiusValue = dataclasses.field(default=None)
        type: str = dataclasses.field(default="rect")

    @dataclasses.dataclass
    class Close(PathElement):
        type: str = dataclasses.field(default="close")

    def __init__(
        self,
        elements: Optional[List[PathElement]] = None,
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

        self.elements = elements
        self.paint = paint

    def _get_control_name(self):
        return "path"

    def before_update(self):
        super().before_update()
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
