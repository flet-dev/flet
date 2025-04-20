import asyncio
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.buttons import ButtonStyle
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.types import (
    ClipBehavior,
    IconValueOrControl,
    OptionalColorValue,
    OptionalControlEventCallable,
    StrOrControl,
    UrlTarget,
)
from flet.utils.deprecated import deprecated_warning

__all__ = ["TextButton"]


@control("TextButton")
class TextButton(ConstrainedControl, AdaptiveControl):
    """
    Text buttons are used for the lowest priority actions, especially when presenting multiple options. Text buttons can be placed on a variety of backgrounds. Until the button is interacted with, its container isn’t visible.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "Basic text buttons"
        page.add(
            ft.TextButton(text="Text button"),
            ft.TextButton("Disabled button", disabled=True),
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/textbutton
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
    style: Optional[ButtonStyle] = None
    autofocus: bool = False
    url: Optional[str] = None
    url_target: Optional[UrlTarget] = None
    clip_behavior: Optional[ClipBehavior] = None
    on_click: OptionalControlEventCallable = None
    on_long_press: OptionalControlEventCallable = None
    on_hover: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None
    text: Optional[str] = None  # todo(0.70.3): remove in favor of content

    # def before_update(self):
    #     super().before_update()
    #     if self.__style is not None:
    #         self.__style.side = self._wrap_attr_dict(self.__style.side)
    #         self.__style.shape = self._wrap_attr_dict(self.__style.shape)
    #         self.__style.padding = self._wrap_attr_dict(self.__style.padding)
    #     self._set_attr_json("style", self.__style)

    async def focus_async(self):
        await self._invoke_method_async("focus")

    def focus(self):
        asyncio.create_task(self.focus_async())
