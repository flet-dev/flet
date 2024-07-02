import dataclasses
import time
from dataclasses import field
from enum import Enum
from typing import Any, Optional, Union, List

from flet_core.adaptive_control import AdaptiveControl
from flet_core.autofill_group import AutofillHint
from flet_core.control import Control, OptionalNumber
from flet_core.form_field_control import FormFieldControl, InputBorder
from flet_core.ref import Ref
from flet_core.text_style import TextStyle
from flet_core.types import (
    AnimationValue,
    BorderRadiusValue,
    OffsetValue,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    TextAlign,
    VerticalAlignment,
    OptionalEventCallable,
)
from flet_core.utils import deprecated

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class KeyboardType(Enum):
    NONE = "none"
    TEXT = "text"
    MULTILINE = "multiline"
    NUMBER = "number"
    PHONE = "phone"
    DATETIME = "datetime"
    EMAIL = "email"
    URL = "url"
    VISIBLE_PASSWORD = "visiblePassword"
    NAME = "name"
    STREET_ADDRESS = "streetAddress"


class TextCapitalization(Enum):
    CHARACTERS = "characters"
    WORDS = "words"
    SENTENCES = "sentences"


@dataclasses.dataclass
class InputFilter:
    regex_string: str
    allow: bool = field(default=True)
    replacement_string: str = field(default="")


class NumbersOnlyInputFilter(InputFilter):
    def __init__(self):
        super().__init__(regex_string=r"[0-9]")


class TextOnlyInputFilter(InputFilter):
    def __init__(self):
        super().__init__(regex_string=r"[a-zA-Z]")


class TextField(FormFieldControl, AdaptiveControl):
    """
    A text field lets the user enter text, either with hardware keyboard or with an onscreen keyboard.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        def button_clicked(e):
            t.value = f"Textboxes values are:  '{tb1.value}', '{tb2.value}', '{tb3.value}', '{tb4.value}', '{tb5.value}'."
            page.update()

        t = ft.Text()
        tb1 = ft.TextField(label="Standard")
        tb2 = ft.TextField(label="Disabled", disabled=True, value="First name")
        tb3 = ft.TextField(label="Read-only", read_only=True, value="Last name")
        tb4 = ft.TextField(label="With placeholder", hint_text="Please enter text here")
        tb5 = ft.TextField(label="With an icon", icon=ft.icons.EMOJI_EMOTIONS)
        b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
        page.add(tb1, tb2, tb3, tb4, tb5, b, t)

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/textfield
    """

    def __init__(
        self,
        value: Optional[str] = None,
        keyboard_type: Optional[KeyboardType] = None,
        multiline: Optional[bool] = None,
        min_lines: Optional[int] = None,
        max_lines: Optional[int] = None,
        max_length: Optional[int] = None,
        password: Optional[bool] = None,
        can_reveal_password: Optional[bool] = None,
        read_only: Optional[bool] = None,
        shift_enter: Optional[bool] = None,
        text_align: Optional[TextAlign] = None,
        autofocus: Optional[bool] = None,
        capitalization: Optional[TextCapitalization] = None,
        autocorrect: Optional[bool] = None,
        enable_suggestions: Optional[bool] = None,
        smart_dashes_type: Optional[bool] = None,
        smart_quotes_type: Optional[bool] = None,
        show_cursor: Optional[bool] = None,
        cursor_color: Optional[str] = None,
        cursor_width: OptionalNumber = None,
        cursor_height: OptionalNumber = None,
        cursor_radius: OptionalNumber = None,
        selection_color: Optional[str] = None,
        input_filter: Optional[InputFilter] = None,
        autofill_hints: Union[None, AutofillHint, List[AutofillHint]] = None,
        on_change: OptionalEventCallable = None,
        on_submit: OptionalEventCallable = None,
        on_focus: OptionalEventCallable = None,
        on_blur: OptionalEventCallable = None,
        #
        # FormField specific
        #
        text_size: OptionalNumber = None,
        text_style: Optional[TextStyle] = None,
        text_vertical_align: Union[VerticalAlignment, OptionalNumber] = None,
        label: Optional[str] = None,
        label_style: Optional[TextStyle] = None,
        icon: Optional[str] = None,
        border: Optional[InputBorder] = None,
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
        dense: Optional[bool] = None,
        filled: Optional[bool] = None,
        fill_color: Optional[str] = None,
        hover_color: Optional[str] = None,
        hint_text: Optional[str] = None,
        hint_style: Optional[TextStyle] = None,
        helper_text: Optional[str] = None,
        helper_style: Optional[TextStyle] = None,
        counter_text: Optional[str] = None,
        counter_style: Optional[TextStyle] = None,
        error_text: Optional[str] = None,
        error_style: Optional[TextStyle] = None,
        prefix: Optional[Control] = None,
        prefix_icon: Optional[str] = None,
        prefix_text: Optional[str] = None,
        prefix_style: Optional[TextStyle] = None,
        suffix: Optional[Control] = None,
        suffix_icon: Optional[str] = None,
        suffix_text: Optional[str] = None,
        suffix_style: Optional[TextStyle] = None,
        #
        # ConstrainedControl and AdaptiveControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        on_animation_end: OptionalEventCallable = None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        rtl: Optional[bool] = None,
        adaptive: Optional[bool] = None,
    ):
        FormFieldControl.__init__(
            self,
            ref=ref,
            key=key,
            width=width,
            height=height,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
            rtl=rtl,
            #
            # FormField
            #
            text_size=text_size,
            text_style=text_style,
            text_vertical_align=text_vertical_align,
            label=label,
            label_style=label_style,
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
            dense=dense,
            filled=filled,
            fill_color=fill_color,
            hover_color=hover_color,
            hint_text=hint_text,
            hint_style=hint_style,
            helper_text=helper_text,
            helper_style=helper_style,
            counter_text=counter_text,
            counter_style=counter_style,
            error_text=error_text,
            error_style=error_style,
            prefix=prefix,
            prefix_icon=prefix_icon,
            prefix_text=prefix_text,
            prefix_style=prefix_style,
            suffix=suffix,
            suffix_icon=suffix_icon,
            suffix_text=suffix_text,
            suffix_style=suffix_style,
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.value = value
        self.text_style = text_style
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
        self.autocorrect = autocorrect
        self.show_cursor = show_cursor
        self.enable_suggestions = enable_suggestions
        self.smart_dashes_type = smart_dashes_type
        self.smart_quotes_type = smart_quotes_type
        self.cursor_color = cursor_color
        self.cursor_height = cursor_height
        self.cursor_width = cursor_width
        self.cursor_radius = cursor_radius
        self.selection_color = selection_color
        self.input_filter = input_filter
        self.autofill_hints = autofill_hints
        self.on_change = on_change
        self.on_submit = on_submit
        self.on_focus = on_focus
        self.on_blur = on_blur

    def _get_control_name(self):
        return "textfield"

    def before_update(self):
        super().before_update()
        assert (
            self.max_lines is None
            or self.min_lines is None
            or self.min_lines <= self.max_lines
        ), "min_lines can't be greater than max_lines"
        self._set_attr_json("inputFilter", self.__input_filter)
        self._set_attr_json("autofillHints", self.__autofill_hints)
        if (
            (
                self.bgcolor is not None
                or self.fill_color is not None
                or self.hover_color is not None
                or self.focused_color is not None
            )
        ) and self.filled is None:
            self.filled = True  # required to display any of the above colors

    def focus(self):
        self._set_attr_json("focus", str(time.time()))
        self.update()

    @deprecated(
        reason="Use focus() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def focus_async(self):
        self.focus()

    # value
    @property
    def value(self) -> Optional[str]:
        return self._get_attr("value", def_value="")

    @value.setter
    def value(self, value: Optional[str]):
        self._set_attr("value", value)

    # keyboard_type
    @property
    def keyboard_type(self) -> Optional[KeyboardType]:
        return self.__keyboard_type

    @keyboard_type.setter
    def keyboard_type(self, value: Optional[KeyboardType]):
        self.__keyboard_type = value
        self._set_enum_attr("keyboardType", value, KeyboardType)

    # text_align
    @property
    def text_align(self) -> Optional[TextAlign]:
        return self.__text_align

    @text_align.setter
    def text_align(self, value: Optional[TextAlign]):
        self.__text_align = value
        self._set_enum_attr("textAlign", value, TextAlign)

    # multiline
    @property
    def multiline(self) -> Optional[bool]:
        return self._get_attr("multiline", data_type="bool", def_value=False)

    @multiline.setter
    def multiline(self, value: Optional[bool]):
        self._set_attr("multiline", value)

    # min_lines
    @property
    def min_lines(self) -> Optional[int]:
        return self._get_attr("minLines")

    @min_lines.setter
    def min_lines(self, value: Optional[int]):
        assert value is None or value > 0, "min_lines must be greater than 0"
        self._set_attr("minLines", value)

    # max_lines
    @property
    def max_lines(self) -> Optional[int]:
        return self._get_attr("maxLines")

    @max_lines.setter
    def max_lines(self, value: Optional[int]):
        assert value is None or value > 0, "max_lines must be greater than 0"
        self._set_attr("maxLines", value)

    # max_length
    @property
    def max_length(self) -> Optional[int]:
        return self._get_attr("maxLength")

    @max_length.setter
    def max_length(self, value: Optional[int]):
        assert (
            value is None or value == -1 or value > 0
        ), "max_length must be either equal to -1 or greater than 0"
        self._set_attr("maxLength", value)

    # read_only
    @property
    def read_only(self) -> Optional[bool]:
        return self._get_attr("readOnly", data_type="bool", def_value=False)

    @read_only.setter
    def read_only(self, value: Optional[bool]):
        self._set_attr("readOnly", value)

    # shift_enter
    @property
    def shift_enter(self) -> Optional[bool]:
        return self._get_attr("shiftEnter", data_type="bool", def_value=False)

    @shift_enter.setter
    def shift_enter(self, value: Optional[bool]):
        self._set_attr("shiftEnter", value)

    # password
    @property
    def password(self) -> Optional[bool]:
        return self._get_attr("password", data_type="bool", def_value=False)

    @password.setter
    def password(self, value: Optional[bool]):
        self._set_attr("password", value)

    # can_reveal_password
    @property
    def can_reveal_password(self) -> Optional[bool]:
        return self._get_attr("canRevealPassword", data_type="bool", def_value=False)

    @can_reveal_password.setter
    def can_reveal_password(self, value: Optional[bool]):
        self._set_attr("canRevealPassword", value)

    # autofocus
    @property
    def autofocus(self) -> Optional[bool]:
        return self._get_attr("autofocus", data_type="bool", def_value=False)

    @autofocus.setter
    def autofocus(self, value: Optional[bool]):
        self._set_attr("autofocus", value)

    # capitalization
    @property
    def capitalization(self) -> Optional[TextCapitalization]:
        return self.__capitalization

    @capitalization.setter
    def capitalization(self, value: Optional[TextCapitalization]):
        self.__capitalization = value
        self._set_enum_attr("capitalization", value, TextCapitalization)

    # autocorrect
    @property
    def autocorrect(self) -> Optional[bool]:
        return self._get_attr("autocorrect", data_type="bool", def_value=True)

    @autocorrect.setter
    def autocorrect(self, value: Optional[bool]):
        self._set_attr("autocorrect", value)

    # show_cursor
    @property
    def show_cursor(self) -> Optional[bool]:
        return self._get_attr("showCursor", data_type="bool", def_value=True)

    @show_cursor.setter
    def show_cursor(self, value: Optional[bool]):
        self._set_attr("showCursor", value)

    # enable_suggestions
    @property
    def enable_suggestions(self) -> Optional[bool]:
        return self._get_attr("enableSuggestions", data_type="bool", def_value=True)

    @enable_suggestions.setter
    def enable_suggestions(self, value: Optional[bool]):
        self._set_attr("enableSuggestions", value)

    # smart_dashes_type
    @property
    def smart_dashes_type(self) -> Optional[bool]:
        return self._get_attr("smartDashesType", data_type="bool", def_value=True)

    @smart_dashes_type.setter
    def smart_dashes_type(self, value: Optional[bool]):
        self._set_attr("smartDashesType", value)

    # smart_quotes_type
    @property
    def smart_quotes_type(self) -> Optional[bool]:
        return self._get_attr("smartQuotesType", data_type="bool", def_value=True)

    @smart_quotes_type.setter
    def smart_quotes_type(self, value: Optional[bool]):
        self._set_attr("smartQuotesType", value)

    # cursor_color
    @property
    def cursor_color(self):
        return self._get_attr("cursorColor")

    @cursor_color.setter
    def cursor_color(self, value):
        self._set_attr("cursorColor", value)

    # cursor_height
    @property
    def cursor_height(self) -> OptionalNumber:
        return self._get_attr("cursorHeight")

    @cursor_height.setter
    def cursor_height(self, value: OptionalNumber):
        self._set_attr("cursorHeight", value)

    # cursor_width
    @property
    def cursor_width(self) -> OptionalNumber:
        return self._get_attr("cursorWidth")

    @cursor_width.setter
    def cursor_width(self, value: OptionalNumber):
        self._set_attr("cursorWidth", value)

    # cursor_radius
    @property
    def cursor_radius(self) -> OptionalNumber:
        return self._get_attr("cursorRadius")

    @cursor_radius.setter
    def cursor_radius(self, value: OptionalNumber):
        self._set_attr("cursorRadius", value)

    # selection_color
    @property
    def selection_color(self) -> Optional[str]:
        return self._get_attr("selectionColor")

    @selection_color.setter
    def selection_color(self, value: Optional[str]):
        self._set_attr("selectionColor", value)

    # input_filter
    @property
    def input_filter(self) -> Optional[InputFilter]:
        return self.__input_filter

    @input_filter.setter
    def input_filter(self, value: Optional[InputFilter]):
        self.__input_filter = value

    # autofill_hints
    @property
    def autofill_hints(self) -> Union[None, AutofillHint, List[AutofillHint]]:
        return self.__autofill_hints

    @autofill_hints.setter
    def autofill_hints(self, value: Union[None, AutofillHint, List[AutofillHint]]):
        if value is not None:
            if isinstance(value, List):
                value = list(
                    map(
                        lambda x: x.value if isinstance(x, AutofillHint) else str(x),
                        value,
                    )
                )
            elif isinstance(value, AutofillHint):
                value = value.value
        self.__autofill_hints = value

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler: OptionalEventCallable):
        self._add_event_handler("change", handler)
        self._set_attr("onChange", True if handler is not None else None)

    # on_submit
    @property
    def on_submit(self) -> OptionalEventCallable:
        return self._get_event_handler("submit")

    @on_submit.setter
    def on_submit(self, handler: OptionalEventCallable):
        self._add_event_handler("submit", handler)

    # on_focus
    @property
    def on_focus(self) -> OptionalEventCallable:
        return self._get_event_handler("focus")

    @on_focus.setter
    def on_focus(self, handler: OptionalEventCallable):
        self._add_event_handler("focus", handler)

    # on_blur
    @property
    def on_blur(self) -> OptionalEventCallable:
        return self._get_event_handler("blur")

    @on_blur.setter
    def on_blur(self, handler: OptionalEventCallable):
        self._add_event_handler("blur", handler)
