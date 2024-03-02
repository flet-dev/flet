from typing import Any, Optional

from flet_core.canvas.shape import Shape
from flet_core.types import BlendMode


class Color(Shape):
    def __init__(
        self,
        color: Optional[str] = None,
        blend_mode: BlendMode = BlendMode.NONE,
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
        self._set_attr(
            "blendMode", value.value if isinstance(value, BlendMode) else value
        )
