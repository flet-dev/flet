from typing import Any, Optional

from flet_core.canvas.shape import Shape
from flet_core.painting import Paint


class Fill(Shape):
    def __init__(
        self,
        paint: Optional[Paint] = None,
        # base
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        Shape.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

        self.paint = paint

    def _get_control_name(self):
        return "fill"

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
