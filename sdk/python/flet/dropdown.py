from typing import Optional

from beartype import beartype

from flet.control import Control, InputBorder
from flet.form_field import FormField
from flet.ref import Ref

try:
    from typing import Literal
except:
    from typing_extensions import Literal


class Dropdown(FormField):
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
        # FormField specific
        #
        label: str = None,
        icon: str = None,
        border: InputBorder = None,
        filled: bool = None,
        hint_text: str = None,
        helper_text: str = None,
        counter_text: str = None,
        error_text: str = None,
        prefix_icon: str = None,
        prefix_text: str = None,
        suffix_icon: str = None,
        suffix_text: str = None,
        #
        # DropDown Specific
        #
        value: str = None,
        on_change=None,
        options=None,
    ):
        FormField.__init__(
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
            # FormField
            label=label,
            icon=icon,
            border=border,
            filled=filled,
            hint_text=hint_text,
            helper_text=helper_text,
            counter_text=counter_text,
            error_text=error_text,
            prefix_icon=prefix_icon,
            prefix_text=prefix_text,
            suffix_icon=suffix_icon,
            suffix_text=suffix_text,
        )

        self.value = value
        self.options = options
        self.on_change = on_change

    def _get_control_name(self):
        return "dropdown"

    # options
    @property
    def options(self):
        return self.__options

    @options.setter
    def options(self, value):
        self.__options = value

    # value
    @property
    def value(self):
        return self._get_attr("value")

    @value.setter
    def value(self, value):
        self._set_attr("value", value)

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)

    def _get_children(self):
        return self.__options


class Option(Control):
    def __init__(self, key=None, text=None, disabled=None, ref=None):
        Control.__init__(self, ref=ref, disabled=disabled)
        assert key != None or text != None, "key or text must be specified"
        self.key = key
        self.text = text
        self.disabled = disabled

    def _get_control_name(self):
        return "option"

    # key
    @property
    def key(self):
        return self._get_attr("key")

    @key.setter
    def key(self, value):
        self._set_attr("key", value)

    # text
    @property
    def text(self):
        return self._get_attr("text")

    @text.setter
    def text(self, value):
        self._set_attr("text", value)
