from datetime import date, datetime
from typing import Optional

from beartype import beartype

from flet.control import Control


class DatePicker(Control):
    def __init__(
        self,
        label=None,
        id=None,
        ref=None,
        value=None,
        placeholder=None,
        required=None,
        allow_text_input=None,
        underlined=None,
        borderless=None,
        focused=None,
        on_change=None,
        on_focus=None,
        on_blur=None,
        width=None,
        visible=None,
        disabled=None,
    ):
        Control.__init__(
            self, id=id, ref=ref, width=width, visible=visible, disabled=disabled
        )
        self.label = label
        self.value = value
        self.placeholder = placeholder
        self.allow_text_input = allow_text_input
        self.underlined = underlined
        self.borderless = borderless
        self.required = required
        self.focused = focused
        self.on_change = on_change
        self.on_focus = on_focus
        self.on_blur = on_blur

    def _get_control_name(self):
        return "datepicker"

    def _set_attr(self, name, value, dirty=True):
        d = value
        if d == "":
            d = None
        elif name == "value" and d != None and not isinstance(d, date):
            d = datetime.fromisoformat(value.replace("Z", "+00:00"))
        self._set_attr_internal(name, d, dirty)

    # label
    @property
    def label(self):
        return self._get_attr("label")

    @label.setter
    def label(self, value):
        self._set_attr("label", value)

    # value
    @property
    def value(self):
        return self._get_attr("value")

    @value.setter
    def value(self, value):
        self._set_attr("value", value)

    # placeholder
    @property
    def placeholder(self):
        return self._get_attr("placeholder")

    @placeholder.setter
    def placeholder(self, value):
        self._set_attr("placeholder", value)

    # allow_text_input
    @property
    def allow_text_input(self):
        return self._get_attr("allowTextInput", data_type="bool", def_value=False)

    @allow_text_input.setter
    @beartype
    def allow_text_input(self, value: Optional[bool]):
        self._set_attr("allowTextInput", value)

    # underlined
    @property
    def underlined(self):
        return self._get_attr("underlined", data_type="bool", def_value=False)

    @underlined.setter
    @beartype
    def underlined(self, value: Optional[bool]):
        self._set_attr("underlined", value)

    # borderless
    @property
    def borderless(self):
        return self._get_attr("borderless", data_type="bool", def_value=False)

    @borderless.setter
    @beartype
    def borderless(self, value: Optional[bool]):
        self._set_attr("borderless", value)

    # required
    @property
    def required(self):
        return self._get_attr("required", data_type="bool", def_value=False)

    @required.setter
    @beartype
    def required(self, value: Optional[bool]):
        self._set_attr("required", value)

    # focused
    @property
    def focused(self):
        return self._get_attr("focused", data_type="bool", def_value=False)

    @focused.setter
    @beartype
    def focused(self, value: Optional[bool]):
        self._set_attr("focused", value)

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)

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
