from typing import Optional

from beartype import beartype

from flet.control import Control


class Progress(Control):
    def __init__(
        self,
        label=None,
        id=None,
        ref=None,
        description=None,
        value=None,
        bar_height=None,
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
        self.value = value
        self.description = description
        self.label = label
        self.bar_height = bar_height

    def _get_control_name(self):
        return "progress"

    # value
    @property
    def value(self):
        return self._get_attr("value")

    @value.setter
    @beartype
    def value(self, value: Optional[int]):
        self._set_attr("value", value)

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
    def bar_height(self, value):
        self._set_attr("barheight", value)

    # label
    @property
    def label(self):
        return self._get_attr("label")

    @label.setter
    def label(self, value):
        self._set_attr("label", value)
