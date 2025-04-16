import asyncio
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.buttons import ButtonStyle
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.types import (
    ClipBehavior,
    IconValueOrControl,
    Number,
    OptionalColorValue,
    OptionalControlEventCallable,
    StrOrControl,
    UrlTarget,
)
from flet.utils.deprecated import deprecated_warning

__all__ = ["ElevatedButton"]


@control("ElevatedButton")
class ElevatedButton(ConstrainedControl, AdaptiveControl):
    """
        Elevated buttons are essentially filled tonal buttons with a shadow. To prevent shadow creep, only use them when absolutely necessary, such as when the button requires visual separation from a patterned background.

        Example:
        ```
        import flet as ft
    import warnings

        def main(page: ft.Page):
            page.title = "Basic elevated buttons"
            page.add(
                ft.ElevatedButton(text="Elevated button"),
                ft.ElevatedButton("Disabled button", disabled=True),
            )

        ft.app(target=main)
        ```

        -----

        Online docs: https://flet.dev/docs/controls/elevatedbutton
    """

    def __setattr__(self, name, value):
        if name == "text" and value is not None:
            deprecated_warning(
                name="text",
                reason="Use content instead.",
                version="0.70.0",
                delete_version="0.73.0",
            )
        super().__setattr__(name, value)

    content: Optional[StrOrControl] = None
    icon: Optional[IconValueOrControl] = None
    icon_color: OptionalColorValue = None
    color: OptionalColorValue = None
    bgcolor: OptionalColorValue = None
    elevation: Number = 1
    style: Optional[ButtonStyle] = None
    autofocus: Optional[bool] = None
    clip_behavior: Optional[ClipBehavior] = None
    url: Optional[str] = None
    url_target: Optional[UrlTarget] = None
    on_click: OptionalControlEventCallable = None
    on_long_press: OptionalControlEventCallable = None
    on_hover: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None
    text: Optional[str] = None  # todo(0.70.3): remove in favor of content

    def before_update(self):
        super().before_update()
        assert (
            self.icon
            or self.text  # todo(0.70.3): remove line
            or isinstance(self.content, str)
            or (isinstance(self.content, Control) and self.content.visible)
        ), "at least text, icon, or content (string or visible Control) must be provided"

    async def focus_async(self):
        await self._invoke_method_async("focus")

    def focus(self):
        asyncio.create_task(self.focus_async())
