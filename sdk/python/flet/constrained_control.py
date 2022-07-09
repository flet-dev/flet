from typing import Union

from beartype import beartype

from flet.control import Control, OptionalNumber
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
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
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
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

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

    # left
    @property
    def left(self) -> OptionalNumber:
        return self._get_attr("left")

    @left.setter
    @beartype
    def left(self, value: OptionalNumber):
        self._set_attr("left", value)

    # top
    @property
    def top(self) -> OptionalNumber:
        return self._get_attr("top")

    @top.setter
    @beartype
    def top(self, value: OptionalNumber):
        self._set_attr("top", value)

    # right
    @property
    def right(self) -> OptionalNumber:
        return self._get_attr("right")

    @right.setter
    @beartype
    def right(self, value: OptionalNumber):
        self._set_attr("right", value)

    # bottom
    @property
    def bottom(self) -> OptionalNumber:
        return self._get_attr("bottom")

    @bottom.setter
    @beartype
    def bottom(self, value: OptionalNumber):
        self._set_attr("bottom", value)
