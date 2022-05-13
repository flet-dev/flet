from typing import Union

from beartype import beartype

from flet.control import Control, OptionalNumber
from flet.ref import Ref


class VerticalDivider(Control):
    def __init__(
        self,
        ref: Ref = None,
        opacity: OptionalNumber = None,
        visible: bool = None,
        data: any = None,
        #
        # Specific
        #
        width: OptionalNumber = None,
        thickness: OptionalNumber = None,
        color: str = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            opacity=opacity,
            visible=visible,
            data=data,
        )

        self.width = width
        self.thickness = thickness
        self.color = color

    def _get_control_name(self):
        return "verticaldivider"

    # width
    @property
    def width(self):
        return self._get_attr("width")

    @width.setter
    @beartype
    def width(self, value: OptionalNumber):
        self._set_attr("width", value)

    # thickness
    @property
    def thickness(self):
        return self._get_attr("thickness")

    @thickness.setter
    @beartype
    def thickness(self, value: OptionalNumber):
        self._set_attr("thickness", value)

    # color
    @property
    def color(self):
        return self._get_attr("color")

    @color.setter
    def color(self, value):
        self._set_attr("color", value)
