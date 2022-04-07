from typing import Optional, Union

from beartype import beartype

from flet.control import Control

try:
    from typing import Literal
except:
    from typing_extensions import Literal


Position = Literal[None, "left", "top", "right", "bottom"]


class SpinButton(Control):
    def __init__(
        self,
        label=None,
        id=None,
        ref=None,
        value=None,
        min=None,
        max=None,
        step=None,
        icon=None,
        label_position: Position = None,
        focused=None,
        data=None,
        on_change=None,
        on_focus=None,
        on_blur=None,
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
            data=data,
        )
        self.value = value
        self.label = label
        self.label_position = label_position
        self.min = min
        self.max = max
        self.step = step
        self.icon = icon
        self.focused = focused
        self.on_change = on_change
        self.on_focus = on_focus
        self.on_blur = on_blur

    def _get_control_name(self):
        return "spinbutton"

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)

    # value
    @property
    def value(self):
        return self._get_attr("value", data_type="float")

    @value.setter
    @beartype
    def value(self, value: Union[None, int, float]):
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
        return self._get_attr("labelposition")

    @label_position.setter
    @beartype
    def label_position(self, value: Position):
        self._set_attr("labelposition", value)

    # min
    @property
    def min(self):
        return self._get_attr("min")

    @min.setter
    @beartype
    def min(self, value: Union[None, int, float]):
        self._set_attr("min", value)

    # max
    @property
    def max(self):
        return self._get_attr("max")

    @max.setter
    @beartype
    def max(self, value: Union[None, int, float]):
        self._set_attr("max", value)

    # step
    @property
    def step(self):
        return self._get_attr("step")

    @step.setter
    @beartype
    def step(self, value: Union[None, int, float]):
        self._set_attr("step", value)

    # icon
    @property
    def icon(self):
        return self._get_attr("icon")

    @icon.setter
    def icon(self, value):
        self._set_attr("icon", value)

    # focused
    @property
    def focused(self):
        return self._get_attr("focused", data_type="bool", def_value=False)

    @focused.setter
    @beartype
    def focused(self, value: Optional[bool]):
        self._set_attr("focused", value)

    # on_focus
    @property
    def on_focus(self):
        return self._get_event_handler("focus")

    @on_focus.setter
    def on_focus(self, handler):
        self._add_event_handler("focus", handler)

    # on_blur
    @property
    def on_blur(self):
        return self._get_event_handler("blur")

    @on_blur.setter
    def on_blur(self, handler):
        self._add_event_handler("blur", handler)
