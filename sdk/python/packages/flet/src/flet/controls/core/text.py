from dataclasses import dataclass
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import (
    ControlEventHandler,
    Event,
    EventControlType,
    EventHandler,
)
from flet.controls.core.text_span import TextSpan
from flet.controls.layout_control import LayoutControl
from flet.controls.text_style import TextOverflow, TextStyle, TextThemeStyle
from flet.controls.types import (
    ColorValue,
    FontWeight,
    Number,
    TextAlign,
)

__all__ = [
    "Text",
    "TextAffinity",
    "TextSelection",
    "TextSelectionChangeCause",
    "TextSelectionChangeEvent",
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

    base_offset: int
    """
    The offset at which the selection originates.
    """

    extent_offset: int
    """
    The offset at which the selection terminates.
    """

    affinity: "TextAffinity" = TextAffinity.DOWNSTREAM
    """
    If the text range is collapsed and has more than one visual location (e.g., occurs
    at a line break), which of the two locations to use when painting the caret.
    """

    directional: bool = False
    """
    Whether this selection has disambiguated its base and extent.
    """

    @property
    def start(self) -> int:
        """
        The index of the first character in the range.

        Note:
            This property is read-only.
        """
        if self.base_offset < self.extent_offset:
            return self.base_offset
        else:
            return self.extent_offset

    @property
    def end(self) -> int:
        """
        The next index after the characters in this range.

        Note:
            This property is read-only.
        """
        if self.base_offset < self.extent_offset:
            return self.extent_offset
        else:
            return self.base_offset

    @property
    def is_valid(self) -> bool:
        """
        Whether this range represents a valid position in the text.

        Note:
            This property is read-only.
        """
        return self.start >= 0 and self.end >= 0

    @property
    def is_collapsed(self) -> bool:
        """
        Whether this range is empty (but still potentially placed inside the text).

        Note:
            This property is read-only.
        """
        return self.start == self.end

    @property
    def is_normalized(self) -> bool:
        """
        Whether the start of this range precedes the end.

        Note:
            This property is read-only.
        """
        return self.start <= self.end

    def get_selected_text(self, source_text: str) -> str:
        """
        Returns the selected text from the given full text.

        Args:
            source_text: The full text to get the selection from.

        Raises:
            AssertionError: If the selection is not valid,
                i.e. [`is_valid`][(c).] is `False`.
        """
        assert self.is_valid
        return source_text[self.start : self.end]


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
    """An event emitted when the text selection changes."""

    selected_text: str
    """The selected text."""

    selection: TextSelection
    """The new text selection."""

    cause: Optional[TextSelectionChangeCause] = None
    """The cause of the selection change."""


@control("Text")
class Text(LayoutControl):
    """
    Display text.

    It consists of two sources combined to produce the final text:
    [`value`][(c).] and [`spans`][(c).].

    ```python
    ft.Text("Hello from Flet!", size=24, weight=ft.FontWeight.W_600)
    ```
    """

    value: str = ""
    """
    The text displayed.
    """

    spans: Optional[list[TextSpan]] = None
    """
    The list of [`TextSpan`][flet.]
    objects to build a rich text paragraph.
    """

    text_align: TextAlign = TextAlign.START
    """
    Text horizontal align.
    """

    font_family: Optional[str] = None
    """
    System or custom font family to render text with. See
    [`Fonts`](https://flet.dev/docs/controls/page#fonts) cookbook guide for
    instructions on how to import and use custom fonts in your application.
    """

    size: Optional[Number] = None
    """
    Text size in virtual pixels.

    Defaults to `14`.
    """

    weight: Optional[FontWeight] = None
    """
    Font weight.

    Defaults to `FontWeight.NORMAL`.
    """

    italic: bool = False
    """
    Whether to use italic typeface.
    """

    style: Optional[TextStyle] = None
    """
    The text's style.
    """

    theme_style: Optional[TextThemeStyle] = None
    """
    Pre-defined text style.
    """

    max_lines: Optional[int] = None
    """
    An optional maximum number of lines for the text to span, wrapping if necessary.

    If the text exceeds the given number of lines, it will be truncated according to
    `overflow`.

    If this is 1, text will not wrap. Otherwise, text will be wrapped at the edge of
    the box.
    """

    overflow: TextOverflow = TextOverflow.CLIP
    """
    Defines how the text overflows.
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

    Defaults to `False`.
    """

    color: Optional[ColorValue] = None
    """
    The text's foreground color.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The text's background color.
    """

    semantics_label: Optional[str] = None
    """
    An alternative semantics label for this text.

    If present, the semantics of this control will contain this value instead of the
    actual text. This will overwrite any of the `TextSpan.semantics_label`s.

    This is useful for replacing abbreviations or shorthands with the full text value:

    /// details | Example
        type: example
    ```python
    ft.Text("$$", semantics_label="Double dollars")
    ```
    ///
    """

    show_selection_cursor: bool = False
    """
    Whether to show cursor (blinking caret) when the text is selected.

    Note:
        Has effect only when [`selectable`][(c).] is `True`.
    """

    enable_interactive_selection: bool = True
    """
    Whether to enable user interface affordances for changing the text selection.

    For example, setting this to `True` will enable features such as long-pressing to
    select text and show the cut/copy/paste menu, and tapping to move the text caret.
    On the other hand, when this is `False`, the text selection cannot be adjusted by
    the user, text cannot be copied.

    Note:
        Has effect only when [`selectable`][(c).] is `True`.
    """

    selection_cursor_width: Number = 2.0
    """
    Defines how thick the cursor should be.

    The cursor will be drawn under the text.
    The cursor width will extend to the right of the boundary between characters for
    left-to-right text and to the left for right-to-left text. This corresponds
    to extending downstream relative to the selected position.
    Negative values may be used to reverse this behavior.

    Note:
        Has effect only when [`selectable`][(c).] is `True`.
    """

    selection_cursor_height: Optional[Number] = None
    """
    Defines how tall the cursor should be.
    """

    selection_cursor_color: Optional[ColorValue] = None
    """
    The color of the cursor.

    The cursor indicates the current text insertion point.
    """

    on_tap: Optional[ControlEventHandler["Text"]] = None
    """
    Called when the user taps on this selectable text.

    Note:
        Has effect only when [`selectable`][(c).] is `True`.
    """

    on_selection_change: Optional[EventHandler[TextSelectionChangeEvent["Text"]]] = None
    """
    Called when the user changes the selection of text (including the cursor location).

    Note:
        Has effect only when [`selectable`][(c).] is `True`.
    """
