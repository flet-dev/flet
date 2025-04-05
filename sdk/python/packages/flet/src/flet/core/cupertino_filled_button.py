from typing import Any, Optional

from flet.core.alignment import Alignment
from flet.core.border_radius import OptionalBorderRadiusValue
from flet.core.colors import Colors
from flet.core.control import Control
from flet.core.cupertino_button import CupertinoButton
from flet.core.padding import OptionalPaddingValue
from flet.core.ref import Ref
from flet.core.types import (
    IconValue,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
    UrlTarget,
)

__all__ = ["CupertinoFilledButton"]


class CupertinoFilledButton(CupertinoButton):
    """
    An iOS-style button filled with default background color.

    Example:
    ```
    import flet as ft


    def main(page: ft.Page):
        page.add(
            ft.CupertinoFilledButton(text="OK"),
        )

    ft.app(target=main)
    ```
    -----

    Online docs: https://flet.dev/docs/controls/cupertinofilledbutton
    """

    text: Optional[str] = None
    icon: Optional[IconValue] = None
    icon_color: OptionalColorValue = None
    content: Optional[Control] = None
    disabled_bgcolor: OptionalColorValue = None
    opacity_on_click: OptionalNumber = None
    min_size: OptionalNumber = None
    padding: OptionalPaddingValue = None
    alignment: Optional[Alignment] = None
    border_radius: OptionalBorderRadiusValue = None
    url: Optional[str] = None
    url_target: Optional[UrlTarget] = None
    autofocus: bool = False
    focus_color: OptionalColorValue = None
    on_click: OptionalControlEventCallable = None
    on_long_press: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None

    def __post_init__(self, ref: Optional[Ref[Any]]):
        super().__post_init__(ref)
        self.color = Colors.ON_PRIMARY
        self.bgcolor = Colors.PRIMARY
