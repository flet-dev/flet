from typing import Optional, Union

from beartype import beartype

from flet.constrained_control import ConstrainedControl
from flet.control import Control, OptionalNumber
from flet.ref import Ref


class ProgressBar(ConstrainedControl):
    def __init__(
        self,
        ref: Ref = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        expand: Union[bool, int] = None,
        opacity: OptionalNumber = None,
        tooltip: str = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # Specific
        #
        value: OptionalNumber = None,
        bar_height: OptionalNumber = None,
        color: str = None,
        bgcolor: str = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            width=width,
            height=height,
            expand=expand,
            opacity=opacity,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )
        self.value = value
        self.bar_height = bar_height
        self.color = color
        self.bgcolor = bgcolor

    def _get_control_name(self):
        return "progressbar"

    # value
    @property
    def value(self):
        return self._get_attr("value")

    @value.setter
    @beartype
    def value(self, value: OptionalNumber):
        self._set_attr("value", value)

    # bar_height
    @property
    def bar_height(self):
        return self._get_attr("barheight")

    @bar_height.setter
    @beartype
    def bar_height(self, value: OptionalNumber):
        self._set_attr("barheight", value)

    # color
    @property
    def color(self):
        return self._get_attr("color")

    @color.setter
    def color(self, value):
        self._set_attr("color", value)

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgcolor", value)
