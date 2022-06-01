from typing import Optional, Union

from beartype import beartype

from flet.control import Control, InputBorder, OptionalNumber
from flet.ref import Ref


class ConstrainedControl(Control):
    def __init__(
        self,
        ref: Ref = None,
        expand: Union[bool, int] = None,
        opacity: OptionalNumber = None,
        tooltip: str = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # ConstrainedControl specific
        #
        width: OptionalNumber = None,
        height: OptionalNumber = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            expand=expand,
            opacity=opacity,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.width = width
        self.height = height

    # width
    @property
    def width(self) -> OptionalNumber:
        return self._get_attr("width")

    @width.setter
    @beartype
    def width(self, value: OptionalNumber):
        self._set_attr("width", value)

    # height
    @property
    def height(self) -> OptionalNumber:
        return self._get_attr("height")

    @height.setter
    @beartype
    def height(self, value: OptionalNumber):
        self._set_attr("height", value)
