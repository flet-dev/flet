from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import BaseControl, control
from flet.controls.control_event import ControlEventHandler, EventHandler
from flet.controls.core.autofill_group import AutofillHint
from flet.controls.core.text import TextSelection, TextSelectionChangeEvent
from flet.controls.material.form_field_control import FormFieldControl
from flet.controls.padding import PaddingValue
from flet.controls.text_style import StrutStyle
from flet.controls.types import (
    Brightness,
    ClipBehavior,
    ColorValue,
    MouseCursor,
    Number,
    TextAlign,
)

__all__ = [
    "InputFilter",
    "KeyboardType",
    "NumbersOnlyInputFilter",
    "TextCapitalization",
    "TextField",
    "TextOnlyInputFilter",
]


class KeyboardType(Enum):
    """
    The type of information for which to optimize the text input control.

    On Android, behavior may vary across device and keyboard provider.
    """

    NONE = "none"
    """
    Prevents the OS from showing the on-screen virtual keyboard.
    """

    TEXT = "text"
    """
    Optimized for textual information.

    Requests the default platform keyboard.
    """

    MULTILINE = "multiline"
    """
    Optimized for multiline textual information.

    Requests the default platform keyboard, but accepts newlines when the
    enter key is pressed. This is the input type used for all multiline text
    fields.
    """

    NUMBER = "number"
    """
    Optimized for unsigned numerical information without a decimal point.

    Requests a default keyboard with ready access to the number keys.
    """

    PHONE = "phone"
    """
    Optimized for telephone numbers.

    Requests a keyboard with ready access to the number keys, `"*"`, and `"#"`.
    """

    DATETIME = "datetime"
    """
    Optimized for date and time information.

    - On iOS, requests the default keyboard.
    - On Android, requests a keyboard with ready
        access to the number keys, `":"`, and `"-"`.
    """

    EMAIL = "email"
    """
    Optimized for email addresses.

    Requests a keyboard with ready access to the `"@"` and `"."` keys.
    """

    URL = "url"
    """
    Optimized for URLs.

    Requests a keyboard with ready access to the `"/"` and `"."` keys.
    """

    VISIBLE_PASSWORD = "visiblePassword"
    """
    Optimized for passwords that are visible to the user.

    Requests a keyboard with ready access to both letters and numbers.
    """

    NAME = "name"
    """
    Optimized for a person's name.

    - On iOS, requests the [UIKeyboardType.namePhonePad](https://developer.apple.com/documentation/uikit/uikeyboardtype/namephonepad)
        keyboard, a keyboard optimized for entering a person’s name or phone number.
        Does not support auto-capitalization.
    - On Android, requests a keyboard optimized for
        [TYPE_TEXT_VARIATION_PERSON_NAME](https://developer.android.com/reference/android/text/InputType#TYPE_TEXT_VARIATION_PERSON_NAME).
    """  # noqa: E501

    STREET_ADDRESS = "streetAddress"
    """
    Optimized for postal mailing addresses.

    - On iOS, requests the default keyboard.
    - On Android, requests a keyboard optimized for
        [TYPE_TEXT_VARIATION_POSTAL_ADDRESS](https://developer.android.com/reference/android/text/InputType#TYPE_TEXT_VARIATION_POSTAL_ADDRESS).
    """  # noqa: E501

    WEB_SEARCH = "webSearch"
    """
    Optimized for web searches.

    Requests a keyboard that includes keys useful for web searches as well as URLs.

    - On iOS, requests a default keyboard with ready access to the `"."` key.
        In contrast to [`URL`][(c).], a space bar is available.
    - On Android this is remapped to the [`URL`][(c).] keyboard type as it always
        shows a space bar.
    """

    TWITTER = "twitter"
    """
    Optimized for social media.

    Requests a keyboard that includes keys useful for handles and tags.

    - On iOS, requests a default keyboard with ready access to the `"@"` and `"#"` keys.
    - On Android this is remapped to the [`EMAIL`][(c).] keyboard type as it
        always shows the `"@"` key.
    """


class TextCapitalization(Enum):
    """
    Configures how the platform keyboard will select an uppercase or
    lowercase keyboard.

    Only supports text keyboards, other keyboard types will ignore this
    configuration. Capitalization is locale-aware.
    """

    CHARACTERS = "characters"
    """
    Uppercase keyboard for each character.

    Info:
        Corresponds to `InputType.TYPE_TEXT_FLAG_CAP_CHARACTERS` on Android, and
        `UITextAutocapitalizationTypeAllCharacters` on iOS.
    """

    WORDS = "words"
    """
    Uppercase keyboard for the first letter of each word.

    Info:
        Corresponds to `InputType.TYPE_TEXT_FLAG_CAP_WORDS` on Android, and
        `UITextAutocapitalizationTypeWords` on iOS.
    """

    SENTENCES = "sentences"
    """
    Uppercase keyboard for the first letter of each sentence.

    Info:
        Corresponds to `InputType.TYPE_TEXT_FLAG_CAP_SENTENCES` on Android, and
        `UITextAutocapitalizationTypeSentences` on iOS.
    """

    NONE = "none"
    """
    Lowercase keyboard.
    """


@dataclass
class InputFilter:
    """
    An input filter that uses a regular expression to allow or deny/block certain
    patterns in the input.
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
    """

    replacement_string: str = ""
    """
    A string used to replace banned/denied patterns.

    Defaults to an empty string.
    """

    multiline: bool = False
    """
    Whether this regular expression matches multiple lines.

    If the regexp does match multiple lines, the `"^"` and `"$"` characters match the
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
    Whether `"."` in this regular expression matches line terminators.

    When false, the `"."` character matches a single character, unless that character
    terminates a line. When true, then the `"."` character will match any single
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

    ```python
    ft.TextField(label="Name", hint_text="Jane Doe")
    ```
    """

    value: str = ""
    """
    Current value of the TextField.
    """

    selection: Optional[TextSelection] = None
    """
    Represents the current text selection or caret position in the field.

    When the user selects text, this property is updated to reflect the selected range.
    If no text is selected, it contains an empty range indicating the caret position.

    Setting this property visually updates the field's selection to match the given
    value, and hence leads to the [`on_selection_change`][(c).] event being triggered.
    To ensure the selection is visible and the event is fired, the text field must
    be focused. Call [`focus()`][(c).focus] on the field before setting this property.
    """

    keyboard_type: KeyboardType = KeyboardType.TEXT
    """
    The type of keyboard to use for editing the text.
    """

    multiline: bool = False
    """
    Whether this field can contain multiple lines of text.
    """

    min_lines: Optional[int] = None
    """
    The minimum number of lines to occupy when the content spans fewer lines.

    This affects the height of the field itself and does not limit the number of lines
    that can be entered into the field.

    Defaults to `1`.

    Raises:
        ValueError: If [`min_lines`][(c).] is not positive or exceeds
            [`max_lines`][(c).] when both are set.
    """

    max_lines: Optional[int] = None
    """
    The maximum number of lines to show at one time, wrapping if necessary.

    This affects the height of the field itself and does not limit the number of lines
    that can be entered into the field.

    If this is `1` (the default), the text will not wrap, but will scroll horizontally
    instead.

    Raises:
        ValueError: If [`max_lines`][(c).] is not positive or is less than
            [`min_lines`][(c).].
    """

    max_length: Optional[int] = None
    """
    Limits a maximum number of characters that can be entered into TextField.

    Raises:
        ValueError: If [`max_length`][(c).] is neither `-1` nor a positive integer.
    """

    password: bool = False
    """
    Whether to hide the text being edited.

    Defaults to `False`.
    """

    can_reveal_password: bool = False
    """
    Displays a toggle icon button that allows revealing the entered password. Is shown
    if both `password` and `can_reveal_password` are `True`.

    The icon is displayed in the same location as `suffix` and in case both
    `can_reveal_password`/`password` and `suffix` are provided, then the `suffix` is
    not shown.
    """

    read_only: bool = False
    """
    Whether the text can be changed.

    When this is set to `True`, the text cannot be modified by any shortcut or keyboard
    operation. The text is still selectable.

    Defaults to `False`.
    """

    shift_enter: bool = False
    """
    Changes the behavior of `Enter` button in `multiline` TextField to be chat-like,
    i.e. new line can be added with `Shift`+`Enter` and pressing just `Enter` fires
    `on_submit` event.
    """

    text_align: Optional[TextAlign] = None
    """
    How the text should be aligned horizontally.

    Defaults to `TextAlign.LEFT`.
    """

    autofocus: bool = False
    """
    True if the control will be selected as the initial focus. If there is more than
    one control on a page with autofocus set, then the first one added to the page will
    get focus.
    """

    capitalization: Optional[TextCapitalization] = None
    """
    Enables automatic on-the-fly capitalization of entered text.

    Defaults to `TextCapitalization.NONE`.
    """

    autocorrect: bool = True
    """
    Whether to enable autocorrection.

    Defaults to `True`.
    """

    enable_suggestions: bool = True
    """
    Whether to show input suggestions as the user types.

    This flag only affects Android. On iOS, suggestions are tied directly to
    `autocorrect`, so that suggestions are only shown when `autocorrect` is `True`.
    On Android autocorrection and suggestion are controlled separately.

    Defaults to `True`.
    """

    smart_dashes_type: bool = True
    """
    Whether to allow the platform to automatically format dashes.

    This flag only affects iOS versions 11 and above. As an example of what this does,
    two consecutive hyphen characters will be automatically replaced with one en dash,
    and three consecutive hyphens will become one em dash.

    Defaults to `True`.
    """

    smart_quotes_type: bool = True
    """
    Whether to allow the platform to automatically format quotes.

    This flag only affects iOS. As an example of what this does, a standard vertical
    double quote character will be automatically replaced by a left or right double
    quote depending on its position in a word.

    Defaults to `True`.
    """

    show_cursor: bool = True
    """
    Whether the field's cursor is to be shown.

    Defaults to `True`.
    """

    cursor_color: Optional[ColorValue] = None
    """
    The color of TextField cursor.
    """

    cursor_error_color: Optional[ColorValue] = None
    """
    TBD
    """

    cursor_width: Number = 2.0
    """
    Sets cursor width.
    """

    cursor_height: Optional[Number] = None
    """
    Sets cursor height.
    """

    cursor_radius: Optional[Number] = None
    """
    Sets cursor radius.
    """

    selection_color: Optional[ColorValue] = None
    """
    The color of TextField selection.
    """

    input_filter: Optional[InputFilter] = None
    """
    Provides as-you-type filtering/validation.

    Similar to the `on_change` callback, the input filters are not applied when the
    content of the field is changed programmatically.
    """

    obscuring_character: str = "•"
    """
    TBD
    """

    enable_interactive_selection: bool = True
    """
    TBD
    """

    enable_ime_personalized_learning: bool = True
    """
    TBD
    """

    can_request_focus: bool = True
    """
    TBD
    """

    ignore_pointers: bool = False
    """
    TBD
    """

    enable_stylus_handwriting: bool = True
    """
    TBD
    """

    animate_cursor_opacity: Optional[bool] = None
    """
    TBD
    """

    always_call_on_tap: bool = False
    """
    TBD
    """

    scroll_padding: PaddingValue = 20
    """
    TBD
    """

    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    """
    TBD
    """

    keyboard_brightness: Optional[Brightness] = None
    """
    TBD
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    TBD
    """

    strut_style: Optional[StrutStyle] = None
    """
    TBD
    """

    autofill_hints: Optional[Union[AutofillHint, list[AutofillHint]]] = None
    """
    Helps the autofill service identify the type of this text input.

    More information
    [here](https://api.flutter.dev/flutter/material/TextField/autofillHints.html).
    """

    on_change: Optional[ControlEventHandler["TextField"]] = None
    """
    Called when the typed input for the TextField has changed.
    """

    on_selection_change: Optional[
        EventHandler[TextSelectionChangeEvent["TextField"]]
    ] = None
    """
    Called when the text selection or caret position changes.

    This can be triggered either by user interaction (selecting text or moving
    the caret) or programmatically (through the [`selection`][(c).] property).
    """

    on_click: Optional[ControlEventHandler["TextField"]] = None
    """
    TBD
    """

    on_submit: Optional[ControlEventHandler["TextField"]] = None
    """
    Called when user presses ENTER while focus is on TextField.
    """

    on_focus: Optional[ControlEventHandler["TextField"]] = None
    """
    Called when the control has received focus.
    """

    on_blur: Optional[ControlEventHandler["TextField"]] = None
    """
    Called when the control has lost focus.
    """

    on_tap_outside: Optional[ControlEventHandler["TextField"]] = None
    """
    TBD
    """

    def _migrate_state(self, other: BaseControl):
        super()._migrate_state(other)
        if (
            isinstance(other, TextField)
            and self.value is None
            and self.value != other.value
        ):
            self.value = other.value

    def before_update(self):
        super().before_update()
        if self.min_lines is not None and self.min_lines <= 0:
            raise ValueError("min_lines must be greater than 0")
        if self.max_lines is not None and self.max_lines <= 0:
            raise ValueError("max_lines must be greater than 0")
        if (
            self.max_lines is not None
            and self.min_lines is not None
            and self.min_lines > self.max_lines
        ):
            raise ValueError("min_lines can't be greater than max_lines")
        if (
            self.max_length is not None
            and self.max_length != -1
            and self.max_length <= 0
        ):
            raise ValueError("max_length must be either equal to -1 or greater than 0")
        if (
            self.bgcolor is not None
            or self.fill_color is not None
            or self.hover_color is not None
            or self.focused_color is not None
        ) and self.filled is None:
            self.filled = True  # required to display any of the above colors
