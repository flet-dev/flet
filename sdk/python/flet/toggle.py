from typing import Optional

from beartype import beartype

from flet.control import Control


class Toggle(Control):
    def __init__(
        self,
        label=None,
        id=None,
        ref=None,
        value=None,
        value_field=None,
        inline=None,
        on_text=None,
        off_text=None,
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
        self.value_field = value_field
        self.label = label
        self.inline = inline
        self.on_text = on_text
        self.off_text = off_text
        self.focused = focused
        self.on_change = on_change
        self.on_focus = on_focus
        self.on_blur = on_blur

    def _get_control_name(self):
        return "toggle"

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
        return self._get_attr("value", data_type="bool", def_value=False)

    @value.setter
    @beartype
    def value(self, value: Optional[bool]):
        self._set_attr("value", value)

    # value_field
    @property
    def value_field(self):
        return self._get_attr("value")

    @value_field.setter
    def value_field(self, value):
        if value != None:
            self._set_attr("value", f"{{{value}}}")

    # label
    @property
    def label(self):
        return self._get_attr("label")

    @label.setter
    def label(self, value):
        self._set_attr("label", value)

    # inline
    @property
    def inline(self):
        return self._get_attr("inline", data_type="bool", def_value=False)

    @inline.setter
    @beartype
    def inline(self, value: Optional[bool]):
        self._set_attr("inline", value)

    # on_text
    @property
    def on_text(self):
        return self._get_attr("onText")

    @on_text.setter
    def on_text(self, value):
        self._set_attr("onText", value)

    # off_text
    @property
    def off_text(self):
        return self._get_attr("offText")

    @off_text.setter
    def off_text(self, value):
        self._set_attr("offText", value)

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
