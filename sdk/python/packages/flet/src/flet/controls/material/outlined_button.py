import time
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.buttons import ButtonStyle
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control, control
from flet.controls.types import (
    ClipBehavior,
    IconValue,
    OptionalColorValue,
    OptionalControlEventCallable,
    UrlTarget,
)

__all__ = ["OutlinedButton"]


@control("OutlinedButton")
class OutlinedButton(ConstrainedControl, AdaptiveControl):
    """
    Outlined buttons are medium-emphasis buttons. They contain actions that are important, but aren’t the primary action in an app. Outlined buttons pair well with filled buttons to indicate an alternative, secondary action.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "Basic outlined buttons"
        page.add(
            ft.OutlinedButton(text="Outlined button"),
            ft.OutlinedButton("Disabled button", disabled=True),
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/outlinedbutton
    """

    text: Optional[str] = None
    icon: Optional[IconValue] = None
    icon_color: OptionalColorValue = None
    content: Optional[Control] = None
    style: Optional[ButtonStyle] = None
    autofocus: bool = False
    clip_behavior: Optional[ClipBehavior] = None
    url: Optional[str] = None
    url_target: Optional[UrlTarget] = None
    on_click: OptionalControlEventCallable = None
    on_long_press: OptionalControlEventCallable = None
    on_hover: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert (
            self.text or self.icon or (self.content and self.content.visible)
        ), "at minimum, text, icon or a visible content must be provided"

    def focus(self):
        self._set_attr_json("focus", str(time.time()))
        self.update()
