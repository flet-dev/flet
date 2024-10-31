from typing import Any, Optional

from flet.core.canvas.shape import Shape
from flet.core.types import BlendMode, ColorEnums, ColorValue


class Color(Shape):
    def __init__(
        self,
        color: Optional[ColorValue] = None,
        blend_mode: Optional[BlendMode] = None,
        #
        # Control
        #
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        Shape.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

        self.color = color
        self.blend_mode = blend_mode

    def _get_control_name(self):
        return "color"

    def before_update(self):
        super().before_update()

    # color
    @property
    def color(self) -> Optional[ColorValue]:
        return self.__color

    @color.setter
    def color(self, value: Optional[ColorValue]):
        self.__color = value
        self._set_enum_attr("color", value, ColorEnums)

    # blend_mode
    @property
    def blend_mode(self) -> Optional[BlendMode]:
        return self.__blend_mode

    @blend_mode.setter
    def blend_mode(self, value: Optional[BlendMode]):
        self.__blend_mode = value
        self._set_attr(
            "blendMode", value.value if isinstance(value, BlendMode) else value
        )
