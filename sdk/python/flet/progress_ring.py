from beartype import beartype

from flet.control import Control

try:
    from typing import Literal
except:
    from typing_extensions import Literal


Position = Literal[None, "left", "top", "right", "bottom"]


class ProgressRing(Control):
    def __init__(
        self,
        label=None,
        id=None,
        ref=None,
        label_position: Position = None,
        size=None,
        width=None,
        height=None,
        padding=None,
        margin=None,
        visible=None,
        disabled=None,
    ):
        Control.__init__(
            self,
            id=id,
            ref=ref,
            width=width,
            height=height,
            padding=padding,
            margin=margin,
            visible=visible,
            disabled=disabled,
        )
        self.label = label
        self.size = size
        self.label_position = label_position

    def _get_control_name(self):
        return "progressring"

    # label
    @property
    def label(self):
        return self._get_attr("label")

    @label.setter
    def label(self, value):
        self._set_attr("label", value)

    # size
    @property
    def size(self):
        return self._get_attr("size")

    @size.setter
    def size(self, value):
        self._set_attr("size", value)

    # label_position
    @property
    def label_position(self):
        return self._get_attr("labelPosition")

    @label_position.setter
    @beartype
    def label_position(self, value: Position):
        self._set_attr("labelPosition", value)
