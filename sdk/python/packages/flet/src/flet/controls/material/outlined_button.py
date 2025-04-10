import asyncio
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.buttons import ButtonStyle
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import control
from flet.controls.types import (
    ClipBehavior,
    IconValueOrControl,
    OptionalColorValue,
    OptionalControlEventCallable,
    StrOrControl,
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

    icon: Optional[IconValueOrControl] = None
    icon_color: OptionalColorValue = None
    content: Optional[StrOrControl] = None
    style: Optional[ButtonStyle] = None
    autofocus: bool = False
    clip_behavior: ClipBehavior = ClipBehavior.NONE
    url: Optional[str] = None
    url_target: Optional[UrlTarget] = None
    text: Optional[str] = None  # todo(0.70.3): remove in favor of content
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

    async def focus_async(self):
        await self._invoke_method_async("focus")

    def focus(self):
        asyncio.create_task(self.focus_async())
