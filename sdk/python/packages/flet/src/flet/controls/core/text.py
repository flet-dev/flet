from dataclasses import dataclass
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import ControlEvent
from flet.controls.core.text_span import TextSpan
from flet.controls.text_style import TextOverflow, TextStyle, TextThemeStyle
from flet.controls.types import (
    FontWeight,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalEventCallable,
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
    TBD
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
class TextSelectionChangeEvent(ControlEvent):
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
    spans: Optional[list[TextSpan]] = None
    text_align: Optional[TextAlign] = None
    font_family: Optional[str] = None
    size: OptionalNumber = None
    weight: Optional[FontWeight] = None
    italic: Optional[bool] = None
    style: Optional[TextStyle] = None
    theme_style: Optional[TextThemeStyle] = None
    max_lines: Optional[int] = None
    overflow: Optional[TextOverflow] = None
    selectable: Optional[bool] = None
    no_wrap: Optional[bool] = None
    color: OptionalColorValue = None
    bgcolor: OptionalColorValue = None
    semantics_label: Optional[str] = None
    show_selection_cursor: Optional[bool] = None
    enable_interactive_selection: Optional[bool] = None
    selection_cursor_width: OptionalNumber = None
    selection_cursor_height: OptionalNumber = None
    selection_cursor_color: OptionalColorValue = None
    on_tap: OptionalControlEventCallable = None
    on_selection_change: OptionalEventCallable[TextSelectionChangeEvent] = None
