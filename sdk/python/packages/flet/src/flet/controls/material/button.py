from dataclasses import field
from typing import Optional, Union

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.buttons import ButtonStyle
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.layout_control import LayoutControl
from flet.controls.types import (
    ClipBehavior,
    ColorValue,
    IconDataOrControl,
    Number,
    StrOrControl,
    Url,
)

__all__ = ["Button"]


@control("Button")
class Button(LayoutControl, AdaptiveControl):
    """
    A customizable button control that can display text, icons, or both. It supports
    various styles, colors, and event handlers for user interaction.

    Example:
        ```python
        import flet as ft


        def main(page: ft.Page):
            def on_click(e):
                print("Button clicked!")

            page.add(
                ft.Button(
                    content="Click Me",
                    icon=ft.Icons.ADD,
                    color="white",
                    bgcolor="blue",
                    on_click=on_click,
                )
            )


        ft.run(main)
        ```
    """

    content: Optional[StrOrControl] = None
    icon: Optional[IconDataOrControl] = None
    icon_color: Optional[ColorValue] = None
    color: Optional[ColorValue] = field(default=None, metadata={"skip": True})
    bgcolor: Optional[ColorValue] = field(default=None, metadata={"skip": True})
    elevation: Number = field(default=1, metadata={"skip": True})
    style: Optional[ButtonStyle] = field(default=None, metadata={"skip": True})
    autofocus: Optional[bool] = None
    clip_behavior: Optional[ClipBehavior] = None
    url: Optional[Union[str, Url]] = None
    on_click: Optional[ControlEventHandler["Button"]] = None
    on_long_press: Optional[ControlEventHandler["Button"]] = None
    on_hover: Optional[ControlEventHandler["Button"]] = None
    on_focus: Optional[ControlEventHandler["Button"]] = None
    on_blur: Optional[ControlEventHandler["Button"]] = None

    def before_update(self):
        super().before_update()
        assert (
            self.icon
            or isinstance(self.content, str)
            or (isinstance(self.content, Control) and self.content.visible)
        ), "At least icon or content (string or visible Control) must be provided"

        if (
            self.style is not None
            or self.color is not None
            or self.bgcolor is not None
            or self.elevation != 1
        ):
            self._internals["style"] = (self.style or ButtonStyle()).copy(
                color=self.color,
                bgcolor=self.bgcolor,
                elevation=self.elevation,
            )

    async def focus(self):
        await self._invoke_method("focus")
