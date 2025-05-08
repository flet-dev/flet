from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Union

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
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
    """
    `InputFilter` class.
    """

    regex_string: str
    """
    A regular expression pattern for the filter.

    It is recommended to use raw strings (prefix your string with `r`) for the pattern,
    ex: `r"pattern"`.
    """

    allow: bool = True
    """
    A boolean value indicating whether to allow or deny/block the matched patterns.

    Value is of type `bool` and defaults to `True`.
    """

    replacement_string: str = ""
    """
    A string used to replace banned/denied patterns.

    Defaults to an empty string.
    """

    multiline: bool = False
    """
    Whether this regular expression matches multiple lines.

    If the regexp does match multiple lines, the "^" and "$" characters match the
    beginning and end of lines. If not, the characters match the beginning and end of
    the input.
    """

    case_sensitive: bool = True
    """
    Whether this regular expression is case sensitive.

    If the regular expression is not case sensitive, it will match an input letter with
    a pattern letter even if the two letters are different case versions of the same
    letter.
    """

    unicode: bool = False
    """
    Whether this regular expression uses Unicode mode.
    """

    dot_all: bool = False
    """
    Whether "." in this regular expression matches line terminators.

    When false, the "." character matches a single character, unless that character
    terminates a line. When true, then the "." character will match any single
    character including line terminators.

    This feature is distinct from `multiline`. They affect the behavior of different
    pattern characters, so they can be used together or separately.
    """


class NumbersOnlyInputFilter(InputFilter):
    """
    Allows only numbers.
    """

    def __init__(self):
        super().__init__(regex_string=r"^[0-9]*$", allow=True, replacement_string="")


class TextOnlyInputFilter(InputFilter):
    """
    Allows only text.
    """

    def __init__(self):
        super().__init__(regex_string=r"^[a-zA-Z]*$", allow=True, replacement_string="")


@control("TextField")
class TextField(FormFieldControl, AdaptiveControl):
    """
    A text field lets the user enter text, either with hardware keyboard or with an
    onscreen keyboard.

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
