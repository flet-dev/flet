from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from flet.core.constrained_control import ConstrainedControl
from flet.core.control import control
from flet.core.control_event import ControlEvent
from flet.core.text_span import TextSpan
from flet.core.text_style import TextOverflow, TextStyle, TextThemeStyle
from flet.core.types import (
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
    UPSTREAM = "upstream"
    DOWNSTREAM = "downstream"


@dataclass
class TextSelection:
    start: Optional[int] = None
    end: Optional[int] = None
    selection: Optional[str] = None
    base_offset: Optional[int] = None
    extent_offset: Optional[int] = None
    affinity: Optional[TextAffinity] = None
    directional: Optional[bool] = None
    collapsed: Optional[bool] = None
    valid: Optional[bool] = None
    normalized: Optional[bool] = None


class TextSelectionChangeCause(Enum):
    UNKNOWN = "unknown"
    TAP = "tap"
    DOUBLE_TAP = "doubleTap"
    LONG_PRESS = "longPress"
    FORCE_PRESS = "forcePress"
    KEYBOARD = "keyboard"
    TOOLBAR = "toolbar"
    DRAG = "drag"
    SCRIBBLE = "scribble"


@dataclass
class TextSelectionChangeEvent(ControlEvent):
    text: str
    cause: TextSelectionChangeCause
    selection: TextSelection


@control("Text")
class Text(ConstrainedControl):
    """
    Text is a control for displaying text.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "Text examples"

        page.add(
            ft.Text("Size 10", size=10),
            ft.Text("Size 30, Italic", size=20, color="pink600", italic=True),
            ft.Text("Limit long text to 2 lines and fading", style=ft.TextThemeStyle.HEADLINE_SMALL),
            ft.Text(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur quis nibh vitae purus consectetur facilisis sed vitae ipsum. Quisque faucibus sed nulla placerat sagittis. Phasellus condimentum risus vitae nulla vestibulum auctor. Curabitur scelerisque, nibh eget imperdiet consequat, odio ante tempus diam, sed volutpat nisl erat eget turpis. Sed viverra, diam sit amet blandit vulputate, mi tellus dapibus lorem, vitae vehicula diam mauris placerat diam. Morbi sit amet pretium turpis, et consequat ligula. Nulla velit sem, suscipit sit amet dictum non, tincidunt sed nulla. Aenean pellentesque odio porttitor sagittis aliquam. Nam varius at metus vitae vulputate. Praesent faucibus nibh lorem, eu pretium dolor dictum nec. Phasellus eget dui laoreet, viverra magna vitae, pellentesque diam.",
                max_lines=2,
            ),
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/text
    """

    value: str = ""
    spans: Optional[List[TextSpan]] = None
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
