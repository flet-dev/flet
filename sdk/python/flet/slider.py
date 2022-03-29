from typing import Optional, Union

from beartype import beartype

from flet.control import Control


class Slider(Control):
    def __init__(
        self,
        label=None,
        id=None,
        ref=None,
        value=None,
        min=None,
        max=None,
        step=None,
        show_value=None,
        value_format=None,
        vertical=None,
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
        self.min = min
        self.max = max
        self.step = step
        self.show_value = show_value
        self.value_format = value_format
        self.vertical = vertical
        self.focused = focused
        self.on_change = on_change
        self.on_focus = on_focus
        self.on_blur = on_blur

    def _get_control_name(self):
        return "slider"

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

    # show_value
    @property
    def show_value(self):
        return self._get_attr("showValue", data_type="bool", def_value=False)

    @show_value.setter
    @beartype
    def show_value(self, value: Optional[bool]):
        self._set_attr("showValue", value)

    # value_format
    @property
    def value_format(self):
        return self._get_attr("valueFormat")

    @value_format.setter
    def value_format(self, value):
        self._set_attr("valueFormat", value)

    # vertical
    @property
    def vertical(self):
        return self._get_attr("vertical", data_type="bool", def_value=False)

    @vertical.setter
    @beartype
    def vertical(self, value: Optional[bool]):
        self._set_attr("vertical", value)

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
