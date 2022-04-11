from typing import Optional

from beartype import beartype

from flet.control import Control
from flet.ref import Ref

try:
    from typing import Literal
except:
    from typing_extensions import Literal

LabelPosition = Literal[None, "left", "top", "right", "bottom"]


class ProgressRing(Control):
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
        label_position: LabelPosition = None,
        stroke_width: float = None,
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
        self.label_position = label_position
        self.stroke_width = stroke_width
        self.color = color
        self.bgcolor = bgcolor

    def _get_control_name(self):
        return "progressring"

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

    # label_position
    @property
    def label_position(self):
        return self._get_attr("labelPosition")

    @label_position.setter
    @beartype
    def label_position(self, value: LabelPosition):
        self._set_attr("label_position", value)

    # bar_height
    @property
    def stroke_width(self):
        return self._get_attr("strokeWidth")

    @stroke_width.setter
    @beartype
    def stroke_width(self, value: float):
        self._set_attr("strokeWidth", value)

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
