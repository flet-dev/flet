from typing import Optional

from beartype import beartype

from flet.control import Control, InputBorder
from flet.ref import Ref


class ConstrainedControl(Control):
    def __init__(
        self,
        ref: Ref = None,
        expand: int = None,
        opacity: float = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # ConstrainedControl specific
        #
        width: float = None,
        height: float = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            expand=expand,
            opacity=opacity,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.width = width
        self.height = height

    # width
    @property
    def width(self) -> float:
        return self._get_attr("width")

    @width.setter
    def width(self, value: float):
        self._set_attr("width", value)

    # height
    @property
    def height(self):
        return self._get_attr("height")

    @height.setter
    def height(self, value):
        self._set_attr("height", value)
