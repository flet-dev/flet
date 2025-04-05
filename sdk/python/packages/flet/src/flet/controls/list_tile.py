from dataclasses import field
from enum import Enum
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.buttons import OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control, control
from flet.controls.padding import OptionalPaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    MouseCursor,
    Number,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
    UrlTarget,
    VisualDensity,
)

__all__ = ["ListTile", "ListTileTitleAlignment", "ListTileStyle"]


class ListTileTitleAlignment(Enum):
    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"
    THREE_LINE = "threeLine"
    TITLE_HEIGHT = "titleHeight"


class ListTileStyle(Enum):
    LIST = "list"
    DRAWER = "drawer"


@control("ListTile")
class ListTile(ConstrainedControl, AdaptiveControl):
    """
    A single fixed-height row that typically contains some text as well as a leading or trailing icon.

    Example:

    ```
    import flet as ft

    def main(page):
        page.title = "ListTile Example"
        page.add(
            ft.Card(
                content=ft.Container(
                    width=500,
                    content=ft.Column(
                        [
                            ft.ListTile(
                                title=ft.Text("One-line list tile"),
                            ),
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.SETTINGS),
                                title=ft.Text("One-line selected list tile"),
                                selected=True,
                            ),
                        ],
                        spacing=0,
                    ),
                    padding=ft.padding.symmetric(vertical=10),
                )
            )
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/listtile
    """

    title: Optional[Control] = None
    subtitle: Optional[Control] = None
    is_three_line: bool = False
    leading: Optional[Control] = None
    trailing: Optional[Control] = None
    content_padding: OptionalPaddingValue = None
    bgcolor: OptionalColorValue = None
    bgcolor_activated: Optional[str] = None
    hover_color: OptionalColorValue = None
    selected: bool = False
    dense: bool = False
    autofocus: bool = False
    toggle_inputs: bool = False
    selected_color: OptionalColorValue = None
    selected_tile_color: OptionalColorValue = None
    style: Optional[ListTileStyle] = None
    enable_feedback: bool = field(default=True)
    horizontal_spacing: Number = 16.0
    min_leading_width: Number = 40.0
    min_vertical_padding: Number = 4.0
    url: Optional[str] = None
    url_target: Optional[UrlTarget] = None
    title_alignment: Optional[ListTileTitleAlignment] = None
    icon_color: OptionalColorValue = None
    text_color: OptionalColorValue = None
    shape: Optional[OutlinedBorder] = None
    visual_density: Optional[VisualDensity] = None
    mouse_cursor: Optional[MouseCursor] = None
    title_text_style: Optional[TextStyle] = None
    subtitle_text_style: Optional[TextStyle] = None
    leading_and_trailing_text_style: Optional[TextStyle] = None
    min_height: OptionalNumber = None
    on_click: OptionalControlEventCallable = None
    on_long_press: OptionalControlEventCallable = None
