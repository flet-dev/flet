from dataclasses import dataclass
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import (
    Event,
    EventControlType,
    OptionalControlEventHandler,
    OptionalEventHandler,
)
from flet.controls.core.text_span import TextSpan
from flet.controls.text_style import TextOverflow, TextStyle, TextThemeStyle
from flet.controls.types import (
    FontWeight,
    OptionalColorValue,
    OptionalNumber,
    TextAlign,
)

__all__ = [
    "Text",
    "TextSelection",
    "TextSelectionChangeEvent",
    "TextSelectionChangeCause",
    "TextAffinity",
]


class TextAffinity(Enum):
    """
    Defines the permissions which can be checked and requested.
    """

    UPSTREAM = "upstream"
    """
    The position has affinity for the downstream side of the text position, i.e. in the 
    direction of the end of the string.
    """
    DOWNSTREAM = "downstream"
    """
    The position has affinity for the upstream side of the text position, i.e. in the 
    direction of the beginning of the string.
    """


@dataclass
class TextSelection:
    """
    A range of text that represents a selection.
    """

    start: Optional[int] = None
    """
    The index of the first character in the range.
    """

    end: Optional[int] = None
    """
    The next index after the characters in this range.
    """

    selection: Optional[str] = None
    """
    The text string that is selected.
    """

    base_offset: Optional[int] = None
    """
    The offset at which the selection originates.
    """

    extent_offset: Optional[int] = None
    """
    The offset at which the selection terminates.
    """

    affinity: Optional["TextAffinity"] = None
    """
    If the text range is collapsed and has more than one visual location (e.g., occurs
    at a line break), which of the two locations to use when painting the caret.

    Value is of type [`TextAffinity`](https://flet.dev/docs/reference/types/textaffinity).
    """

    directional: Optional[bool] = None
    """
    Whether this selection has disambiguated its base and extent.
    """

    collapsed: Optional[bool] = None
    """
    Whether this range is empty (but still potentially placed inside the text).
    """

    valid: Optional[bool] = None
    """
    Whether this range represents a valid position in the text.
    """

    normalized: Optional[bool] = None
    """
    Whether the start of this range precedes the end.
    """


class TextSelectionChangeCause(Enum):
    """
    Indicates what triggered the change in selected text.
    """

    UNKNOWN = "unknown"
    """
    The cause of the selection change is unknown or could not be determined.
    """

    TAP = "tap"
    """
    The user tapped on the text and that caused the selection (or the location of the
    cursor) to change.
    """

    DOUBLE_TAP = "doubleTap"
    """
    The user tapped twice in quick succession on the text and that caused the
    selection (or the location of the cursor) to change.
    """

    LONG_PRESS = "longPress"
    """
    The user long-pressed the text and that caused the selection (or the location of
    the cursor) to change.
    """

    FORCE_PRESS = "forcePress"
    """
    The user force-pressed the text and that caused the selection (or the location of
    the cursor) to change.
    """

    KEYBOARD = "keyboard"
    """
    The user used the keyboard to change the selection or the location of the cursor.

    Keyboard-triggered selection changes may be caused by the IME as well as by
    accessibility tools (e.g. TalkBack on Android).
    """

    TOOLBAR = "toolbar"
    """
    The user used the selection toolbar to change the selection or the location of
    the cursor.

    An example is when the user taps on select all in the tool bar.
    """

    DRAG = "drag"
    """
    The user used the mouse to change the selection by dragging over a piece of text.
    """

    SCRIBBLE = "scribble"
    """
    The user used iPadOS 14+ Scribble to change the selection.
    """


@dataclass
class TextSelectionChangeEvent(Event[EventControlType]):
    text: str
    cause: TextSelectionChangeCause
    selection: TextSelection


@control("Text")
class Text(ConstrainedControl):
    """
    Text is a control for displaying text.

    Online docs: https://flet.dev/docs/controls/text
    """

    value: Optional[str] = ""
    """
    The text displayed.
    """

    spans: Optional[list[TextSpan]] = None
    """
    The list of [`TextSpan`](https://flet.dev/docs/reference/types/textspan)
    objects to build a rich text paragraph.
    """

    text_align: Optional[TextAlign] = None
    """
    Text horizontal align.

    Value is of type [`TextAlign`](https://flet.dev/docs/reference/types/textalign)
    and defaults to `TextAlign.LEFT`.
    """

    font_family: Optional[str] = None
    """
    System or custom font family to render text with. See
    [`Fonts`](https://flet.dev/docs/controls/page#fonts) cookbook guide for
    instructions on how to import and use custom fonts in your application.
    """

    size: OptionalNumber = None
    """
    Text size in virtual pixels.

    Value is of type `OptionalNumber` and defaults to `14`.
    """

    weight: Optional[FontWeight] = None
    """
    Font weight.

    Value is of type [`FontWeight`](https://flet.dev/docs/reference/types/fontweight)
    and defaults to `FontWeight.NORMAL`.
    """

    italic: Optional[bool] = None
    """
    `True` to use italic typeface.

    Value is of type `bool` and defaults to `False`.
    """

    style: Optional[TextStyle] = None
    """
    The text's style.

    Value is of type [`TextStyle`](https://flet.dev/docs/reference/types/textstyle).
    """

    theme_style: Optional[TextThemeStyle] = None
    """
    Pre-defined text style.

    Value is of type [`TextThemeStyle`](https://flet.dev/docs/reference/types/textthemestyle).
    """

    max_lines: Optional[int] = None
    """
    An optional maximum number of lines for the text to span, wrapping if necessary.

    If the text exceeds the given number of lines, it will be truncated according to
    `overflow`.

    If this is 1, text will not wrap. Otherwise, text will be wrapped at the edge of
    the box.
    """

    overflow: Optional[TextOverflow] = None
    """
    Controls how text overflows.

    Value is of type [`TextOverflow`](https://flet.dev/docs/reference/types/textoverflow)
    and defaults to `TextOverflow.FADE`.
    """

    selectable: Optional[bool] = None
    """
    Whether the text should be selectable.

    Defaults to `False`.
    """

    no_wrap: Optional[bool] = None
    """
    If `False` (default) the text should break at soft line breaks.

    If `True`, the glyphs in the text will be positioned as if there was unlimited
    horizontal space.

    Value is of type `bool` and defaults to `False`.
    """

    color: OptionalColorValue = None
    """
    Text foreground [color](https://flet.dev/docs/reference/colors).
    """

    bgcolor: OptionalColorValue = None
    """
    Text background [color](https://flet.dev/docs/reference/colors).
    """

    semantics_label: Optional[str] = None
    """
    An alternative semantics label for this text.

    If present, the semantics of this control will contain this value instead of the
    actual text. This will overwrite any of the `TextSpan.semantics_label`s.

    This is useful for replacing abbreviations or shorthands with the full text value:

    Value is of type `str`.

    ```python
    ft.Text("$$", semantics_label="Double dollars")
    ```
    """

    show_selection_cursor: Optional[bool] = None
    """
    TBD
    """

    enable_interactive_selection: Optional[bool] = None
    """
    TBD
    """

    selection_cursor_width: OptionalNumber = None
    """
    TBD
    """

    selection_cursor_height: OptionalNumber = None
    """
    TBD
    """

    selection_cursor_color: OptionalColorValue = None
    """
    TBD
    """

    on_tap: OptionalControlEventHandler["Text"] = None
    """
    TBD
    """

    on_selection_change: OptionalEventHandler[TextSelectionChangeEvent["Text"]] = None
    """
    TBD
    """
