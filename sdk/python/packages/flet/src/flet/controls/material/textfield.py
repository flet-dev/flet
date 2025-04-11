import asyncio
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Union

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.control import control
from flet.controls.core.autofill_group import AutofillHint
from flet.controls.material.form_field_control import FormFieldControl
from flet.controls.padding import PaddingValue
from flet.controls.text_style import StrutStyle
from flet.controls.types import (
    Brightness,
    ClipBehavior,
    MouseCursor,
    Number,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
    TextAlign,
)
from flet.utils import deprecated_warning

__all__ = [
    "TextField",
    "KeyboardType",
    "TextCapitalization",
    "InputFilter",
    "NumbersOnlyInputFilter",
    "TextOnlyInputFilter",
]


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


@dataclass
class InputFilter:
    regex_string: str
    allow: bool = True
    replacement_string: str = ""
    multiline: bool = False
    case_sensitive: bool = True
    unicode: bool = False
    dot_all: bool = False


class NumbersOnlyInputFilter(InputFilter):
    def __init__(self):
        super().__init__(regex_string=r"^[0-9]*$", allow=True, replacement_string="")


class TextOnlyInputFilter(InputFilter):
    def __init__(self):
        super().__init__(regex_string=r"^[a-zA-Z]*$", allow=True, replacement_string="")


@control("TextField")
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

    value: str = ""
    keyboard_type: KeyboardType = KeyboardType.TEXT
    multiline: bool = False
    min_lines: Optional[int] = None
    max_lines: Optional[int] = None
    max_length: Optional[int] = None
    password: bool = False
    can_reveal_password: bool = False
    read_only: bool = False
    shift_enter: bool = False
    text_align: Optional[TextAlign] = None
    autofocus: bool = False
    capitalization: Optional[TextCapitalization] = None
    autocorrect: bool = True
    enable_suggestions: bool = True
    smart_dashes_type: bool = True
    smart_quotes_type: bool = True
    show_cursor: bool = True
    cursor_color: OptionalColorValue = None
    cursor_error_color: OptionalColorValue = None
    cursor_width: Number = 2.0
    cursor_height: OptionalNumber = None
    cursor_radius: OptionalNumber = None
    selection_color: OptionalColorValue = None
    input_filter: Optional[InputFilter] = None
    obscuring_character: str = "•"
    enable_interactive_selection: bool = True
    enable_ime_personalized_learning: bool = True
    can_request_focus: bool = True
    ignore_pointers: bool = False
    enable_scribble: bool = True
    # todo(0.73.0): remove in favor of enable_stylus_handwriting

    enable_stylus_handwriting: bool = True
    animate_cursor_opacity: Optional[bool] = None
    always_call_on_tap: bool = False
    scroll_padding: PaddingValue = 20
    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    keyboard_brightness: Optional[Brightness] = None
    mouse_cursor: Optional[MouseCursor] = None
    strut_style: Optional[StrutStyle] = None
    autofill_hints: Optional[Union[AutofillHint, List[AutofillHint]]] = None
    on_change: OptionalControlEventCallable = None
    on_click: OptionalControlEventCallable = None
    on_submit: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None
    on_tap_outside: OptionalControlEventCallable = None

    def __setattr__(self, name, value):
        if name == "enable_scribble" and value is not True:
            deprecated_warning(
                name="enable_scribble",
                reason="Use enable_stylus_handwriting instead.",
                version="0.70.0",
                delete_version="0.73.0",
            )
        super().__setattr__(name, value)

    def before_update(self):
        super().before_update()
        assert (
            self.min_lines is None or self.min_lines > 0
        ), "min_lines must be greater than 0"
        assert (
            self.max_lines is None or self.max_lines > 0
        ), "min_lines must be greater than 0"
        assert (
            self.max_lines is None
            or self.min_lines is None
            or self.min_lines <= self.max_lines
        ), "min_lines can't be greater than max_lines"
        assert (
            self.max_length is None or self.max_length == -1 or self.max_length > 0
        ), "max_length must be either equal to -1 or greater than 0"
        if (
            (
                self.bgcolor is not None
                or self.fill_color is not None
                or self.hover_color is not None
                or self.focused_color is not None
            )
        ) and self.filled is None:
            self.filled = True  # required to display any of the above colors

    async def focus_async(self):
        await self._invoke_method_async("focus")

    def focus(self):
        asyncio.create_task(self.focus_async())
