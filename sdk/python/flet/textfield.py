from typing import Any, Optional, Union

from beartype import beartype

from flet.control import Control, InputBorder, OptionalNumber, TextAlign
from flet.focus import FocusData
from flet.form_field_control import FormFieldControl
from flet.ref import Ref
from flet.types import BorderRadiusValue, PaddingValue

try:
    from typing import Literal
except:
    from typing_extensions import Literal

TextInputType = Literal[
    None,
    "text",
    "multiline",
    "number",
    "phone",
    "datetime",
    "email",
    "url",
    "visiblePassword",
    "name",
    "streetAddress",
    "none",
]

TextCapitalization = Literal[None, "none", "characters", "words", "sentences"]


class TextField(FormFieldControl):
    def __init__(
        self,
        ref: Optional[Ref] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        opacity: OptionalNumber = None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # FormField specific
        #
        text_size: OptionalNumber = None,
        label: Optional[str] = None,
        icon: Optional[str] = None,
        border: InputBorder = None,
        color: Optional[str] = None,
        bgcolor: Optional[str] = None,
        border_radius: BorderRadiusValue = None,
        border_width: OptionalNumber = None,
        border_color: Optional[str] = None,
        focused_color: Optional[str] = None,
        focused_bgcolor: Optional[str] = None,
        focused_border_width: OptionalNumber = None,
        focused_border_color: Optional[str] = None,
        content_padding: PaddingValue = None,
        filled: Optional[bool] = None,
        hint_text: Optional[str] = None,
        helper_text: Optional[str] = None,
        counter_text: Optional[str] = None,
        error_text: Optional[str] = None,
        prefix: Optional[Control] = None,
        prefix_icon: Optional[str] = None,
        prefix_text: Optional[str] = None,
        suffix: Optional[Control] = None,
        suffix_icon: Optional[str] = None,
        suffix_text: Optional[str] = None,
        #
        # TextField Specific
        #
        value: Optional[str] = None,
        keyboard_type: TextInputType = None,
        multiline: Optional[bool] = None,
        min_lines: Optional[int] = None,
        max_lines: Optional[int] = None,
        max_length: Optional[int] = None,
        password: Optional[bool] = None,
        can_reveal_password: Optional[bool] = None,
        read_only: Optional[bool] = None,
        shift_enter: Optional[bool] = None,
        text_align: TextAlign = None,
        autofocus: Optional[bool] = None,
        capitalization: TextCapitalization = None,
        cursor_color: Optional[str] = None,
        selection_color: Optional[str] = None,
        on_change=None,
        on_submit=None,
        on_focus=None,
        on_blur=None,
    ):
        FormFieldControl.__init__(
            self,
            ref=ref,
            width=width,
            height=height,
            expand=expand,
            opacity=opacity,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
            #
            # FormField
            #
            text_size=text_size,
            label=label,
            icon=icon,
            border=border,
            color=color,
            bgcolor=bgcolor,
            border_radius=border_radius,
            border_width=border_width,
            border_color=border_color,
            focused_color=focused_color,
            focused_bgcolor=focused_bgcolor,
            focused_border_width=focused_border_width,
            focused_border_color=focused_border_color,
            content_padding=content_padding,
            filled=filled,
            hint_text=hint_text,
            helper_text=helper_text,
            counter_text=counter_text,
            error_text=error_text,
            prefix=prefix,
            prefix_icon=prefix_icon,
            prefix_text=prefix_text,
            suffix=suffix,
            suffix_icon=suffix_icon,
            suffix_text=suffix_text,
        )
        self.value = value
        self.keyboard_type = keyboard_type
        self.text_align = text_align
        self.multiline = multiline
        self.min_lines = min_lines
        self.max_lines = max_lines
        self.max_length = max_length
        self.read_only = read_only
        self.shift_enter = shift_enter
        self.password = password
        self.can_reveal_password = can_reveal_password
        self.autofocus = autofocus
        self.capitalization = capitalization
        self.cursor_color = cursor_color
        self.selection_color = selection_color
        self.on_change = on_change
        self.on_submit = on_submit
        self.on_focus = on_focus
        self.on_blur = on_blur

    def _get_control_name(self):
        return "textfield"

    def focus(self):
        self._set_attr_json("focus", FocusData())
        self.update()

    # value
    @property
    def value(self):
        return self._get_attr("value", def_value="")

    @value.setter
    def value(self, value):
        self._set_attr("value", value)

    # keyboard_type
    @property
    def keyboard_type(self) -> TextInputType:
        return self._get_attr("keyboardType")

    @keyboard_type.setter
    @beartype
    def keyboard_type(self, value: TextInputType):
        self._set_attr("keyboardType", value)

    # text_align
    @property
    def text_align(self) -> TextAlign:
        return self._get_attr("textAlign")

    @text_align.setter
    @beartype
    def text_align(self, value: TextAlign):
        self._set_attr("textAlign", value)

    # multiline
    @property
    def multiline(self) -> Optional[bool]:
        return self._get_attr("multiline", data_type="bool", def_value=False)

    @multiline.setter
    @beartype
    def multiline(self, value: Optional[bool]):
        self._set_attr("multiline", value)

    # min_lines
    @property
    def min_lines(self) -> Optional[int]:
        return self._get_attr("minLines")

    @min_lines.setter
    @beartype
    def min_lines(self, value: Optional[int]):
        self._set_attr("minLines", value)

    # max_lines
    @property
    def max_lines(self) -> Optional[int]:
        return self._get_attr("maxLines")

    @max_lines.setter
    @beartype
    def max_lines(self, value: Optional[int]):
        self._set_attr("maxLines", value)

    # max_length
    @property
    def max_length(self) -> Optional[int]:
        return self._get_attr("maxLength")

    @max_length.setter
    @beartype
    def max_length(self, value: Optional[int]):
        self._set_attr("maxLength", value)

    # read_only
    @property
    def read_only(self) -> Optional[bool]:
        return self._get_attr("readOnly", data_type="bool", def_value=False)

    @read_only.setter
    @beartype
    def read_only(self, value: Optional[bool]):
        self._set_attr("readOnly", value)

    # shift_enter
    @property
    def shift_enter(self) -> Optional[bool]:
        return self._get_attr("shiftEnter", data_type="bool", def_value=False)

    @shift_enter.setter
    @beartype
    def shift_enter(self, value: Optional[bool]):
        self._set_attr("shiftEnter", value)

    # password
    @property
    def password(self) -> Optional[bool]:
        return self._get_attr("password", data_type="bool", def_value=False)

    @password.setter
    @beartype
    def password(self, value: Optional[bool]):
        self._set_attr("password", value)

    # can_reveal_password
    @property
    def can_reveal_password(self) -> Optional[bool]:
        return self._get_attr("canRevealPassword", data_type="bool", def_value=False)

    @can_reveal_password.setter
    @beartype
    def can_reveal_password(self, value: Optional[bool]):
        self._set_attr("canRevealPassword", value)

    # autofocus
    @property
    def autofocus(self) -> Optional[bool]:
        return self._get_attr("autofocus", data_type="bool", def_value=False)

    @autofocus.setter
    @beartype
    def autofocus(self, value: Optional[bool]):
        self._set_attr("autofocus", value)

    # capitalization
    @property
    def capitalization(self) -> TextCapitalization:
        return self._get_attr("capitalization")

    @capitalization.setter
    @beartype
    def capitalization(self, value: TextCapitalization):
        self._set_attr("capitalization", value)

    # cursor_color
    @property
    def cursor_color(self):
        return self._get_attr("cursorColor")

    @cursor_color.setter
    def cursor_color(self, value):
        self._set_attr("cursorColor", value)

    # selection_color
    @property
    def selection_color(self):
        return self._get_attr("selectionColor")

    @selection_color.setter
    def selection_color(self, value):
        self._set_attr("selectionColor", value)

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

    # on_submit
    @property
    def on_submit(self):
        return self._get_event_handler("submit")

    @on_submit.setter
    def on_submit(self, handler):
        self._add_event_handler("submit", handler)

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
