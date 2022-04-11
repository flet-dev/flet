from typing import Optional

from beartype import beartype

from flet.control import Control
from flet.ref import Ref


class ProgressBar(Control):
    def __init__(
        self,
        id: str = None,
        ref: Ref = None,
        width: float = None,
        height: float = None,
        padding: float = None,
        margin: float = None,
        expand: int = None,
        opacity: float = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # Specific
        #
        value: float = None,
        label: str = None,
        description: str = None,
        bar_height: float = None,
        color: str = None,
        bgcolor: str = None,
    ):
        Control.__init__(
            self,
            id=id,
            ref=ref,
            width=width,
            height=height,
            padding=padding,
            margin=margin,
            expand=expand,
            opacity=opacity,
            visible=visible,
            disabled=disabled,
            data=data,
        )
        self.value = value
        self.label = label
        self.description = description
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
    def value(self, value: Optional[float]):
        self._set_attr("value", value)

    # label
    @property
    def label(self):
        return self._get_attr("label")

    @label.setter
    def label(self, value):
        self._set_attr("label", value)

    # description
    @property
    def description(self):
        return self._get_attr("description")

    @description.setter
    def description(self, value):
        self._set_attr("description", value)

    # bar_height
    @property
    def bar_height(self):
        return self._get_attr("barheight")

    @bar_height.setter
    @beartype
    def bar_height(self, value: float):
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
