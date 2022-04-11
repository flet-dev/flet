from typing import Optional

from beartype import beartype

from flet.control import Control, InputBorder, TextAlign
from flet.form_field import FormField
from flet.ref import Ref


class TextField(FormField):
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
        # TextField Specific
        #
        value: str = None,
        on_change=None,
        min_lines: int = None,
        max_lines: int = None,
        password: int = None,
        read_only=None,
        text_align: TextAlign = None,
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
        self.label = label
        self.value = value
        self.text_align = text_align
        self.min_lines = min_lines
        self.max_lines = max_lines
        self.read_only = read_only
        self.password = password
        self.on_change = on_change

    def _get_control_name(self):
        return "textfield"

    # value
    @property
    def value(self):
        return self._get_attr("value", def_value="")

    @value.setter
    def value(self, value):
        self._set_attr("value", value)

    # text_align
    @property
    def text_align(self):
        return self._get_attr("textAlign")

    @text_align.setter
    @beartype
    def text_align(self, value: TextAlign):
        self._set_attr("textAlign", value)

    # min_lines
    @property
    def min_lines(self):
        return self._get_attr("minLines")

    @min_lines.setter
    @beartype
    def min_lines(self, value: Optional[int]):
        self._set_attr("minLines", value)

    # max_lines
    @property
    def max_lines(self):
        return self._get_attr("maxLines")

    @max_lines.setter
    @beartype
    def max_lines(self, value: Optional[int]):
        self._set_attr("maxLines", value)

    # read_only
    @property
    def read_only(self):
        return self._get_attr("readOnly", data_type="bool", def_value=False)

    @read_only.setter
    @beartype
    def read_only(self, value: Optional[bool]):
        self._set_attr("readOnly", value)

    # password
    @property
    def password(self):
        return self._get_attr("password", data_type="bool", def_value=False)

    @password.setter
    @beartype
    def password(self, value: Optional[bool]):
        self._set_attr("password", value)

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
