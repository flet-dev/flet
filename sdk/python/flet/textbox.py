from typing import Optional

from beartype import beartype

from flet.control import Control, TextAlign


class Textbox(Control):
    def __init__(
        self,
        label=None,
        id=None,
        ref=None,
        value=None,
        placeholder=None,
        error_message=None,
        description=None,
        icon=None,
        icon_color=None,
        prefix=None,
        suffix=None,
        multiline=None,
        rows=None,
        shift_enter=None,
        password=None,
        required=None,
        read_only=None,
        auto_adjust_height=None,
        resizable=None,
        underlined=None,
        borderless=None,
        focused=None,
        on_change=None,
        on_focus=None,
        on_blur=None,
        width=None,
        height=None,
        padding=None,
        margin=None,
        align: TextAlign = None,
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
        self.value = value
        self.placeholder = placeholder
        self.error_message = error_message
        self.description = description
        self.icon = icon
        self.icon_color = icon_color
        self.suffix = suffix
        self.prefix = prefix
        self.align = align
        self.multiline = multiline
        self.rows = rows
        self.shift_enter = shift_enter
        self.read_only = read_only
        self.auto_adjust_height = auto_adjust_height
        self.resizable = resizable
        self.underlined = underlined
        self.borderless = borderless
        self.password = password
        self.required = required
        self.focused = focused
        self.on_change = on_change
        self.on_focus = on_focus
        self.on_blur = on_blur

    def _get_control_name(self):
        return "textbox"

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
        return self._get_attr("value", def_value="")

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

    # error_message
    @property
    def error_message(self):
        return self._get_attr("errorMessage")

    @error_message.setter
    def error_message(self, value):
        self._set_attr("errorMessage", value)

    # description
    @property
    def description(self):
        return self._get_attr("description")

    @description.setter
    def description(self, value):
        self._set_attr("description", value)

    # icon
    @property
    def icon(self):
        return self._get_attr("icon")

    @icon.setter
    def icon(self, value):
        self._set_attr("icon", value)

    # icon_color
    @property
    def icon_color(self):
        return self._get_attr("iconColor")

    @icon_color.setter
    def icon_color(self, value):
        self._set_attr("iconColor", value)

    # prefix
    @property
    def prefix(self):
        return self._get_attr("prefix")

    @prefix.setter
    def prefix(self, value):
        self._set_attr("prefix", value)

    # suffix
    @property
    def suffix(self):
        return self._get_attr("suffix")

    @suffix.setter
    def suffix(self, value):
        self._set_attr("suffix", value)

    # align
    @property
    def align(self):
        return self._get_attr("align")

    @align.setter
    @beartype
    def align(self, value: TextAlign):
        self._set_attr("align", value)

    # multiline
    @property
    def multiline(self):
        return self._get_attr("multiline", data_type="bool", def_value=False)

    @multiline.setter
    @beartype
    def multiline(self, value: Optional[bool]):
        self._set_attr("multiline", value)

    # rows
    @property
    def rows(self):
        return self._get_attr("rows")

    @rows.setter
    @beartype
    def rows(self, value: Optional[int]):
        self._set_attr("rows", value)

    # shift_enter
    @property
    def shift_enter(self):
        return self._get_attr("shiftenter", data_type="bool", def_value=False)

    @shift_enter.setter
    @beartype
    def shift_enter(self, value: Optional[bool]):
        self._set_attr("shiftenter", value)

    # read_only
    @property
    def read_only(self):
        return self._get_attr("readOnly", data_type="bool", def_value=False)

    @read_only.setter
    @beartype
    def read_only(self, value: Optional[bool]):
        self._set_attr("readOnly", value)

    # auto_adjust_height
    @property
    def auto_adjust_height(self):
        return self._get_attr("autoadjustheight", data_type="bool", def_value=False)

    @auto_adjust_height.setter
    @beartype
    def auto_adjust_height(self, value: Optional[bool]):
        self._set_attr("autoadjustheight", value)

    # resizable
    @property
    def resizable(self):
        return self._get_attr("resizable", data_type="bool", def_value=True)

    @resizable.setter
    @beartype
    def resizable(self, value: Optional[bool]):
        self._set_attr("resizable", value)

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

    # password
    @property
    def password(self):
        return self._get_attr("password", data_type="bool", def_value=False)

    @password.setter
    @beartype
    def password(self, value: Optional[bool]):
        self._set_attr("password", value)

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
        if handler != None:
            self._set_attr("onchange", True)
        else:
            self._set_attr("onchange", None)

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
