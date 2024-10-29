from typing import Any, List, Optional

from flet.core.canvas.path import Path
from flet.core.canvas.shape import Shape
from flet.core.control import OptionalNumber
from flet.core.types import ColorEnums, ColorValue


class Shadow(Shape):
    def __init__(
        self,
        path: Optional[List[Path.PathElement]] = None,
        color: Optional[ColorValue] = None,
        elevation: OptionalNumber = None,
        transparent_occluder: Optional[bool] = None,
        #
        # Control
        #
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        Shape.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

        self.path = path
        self.color = color
        self.elevation = elevation
        self.transparent_occluder = transparent_occluder

    def _get_control_name(self):
        return "shadow"

    def before_update(self):
        super().before_update()
        self._set_attr_json("path", self.__path)

    # path
    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, value: Optional[List[Path.PathElement]]):
        self.__path = value if value is not None else []

    # color
    @property
    def color(self) -> Optional[ColorValue]:
        return self.__color

    @color.setter
    def color(self, value: Optional[ColorValue]):
        self.__color = value
        self._set_enum_attr("color", value, ColorEnums)

    # elevation
    @property
    def elevation(self) -> OptionalNumber:
        return self._get_attr("elevation")

    @elevation.setter
    def elevation(self, value: OptionalNumber):
        self._set_attr("elevation", value)

    # transparent_occluder
    @property
    def transparent_occluder(self) -> bool:
        return self._get_attr("transparentOccluder", data_type="bool", def_value=False)

    @transparent_occluder.setter
    def transparent_occluder(self, value: Optional[bool]):
        self._set_attr("transparentOccluder", value)
