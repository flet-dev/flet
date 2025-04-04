import asyncio
import warnings
from typing import Optional

from flet.core.adaptive_control import AdaptiveControl
from flet.core.alignment import Alignment
from flet.core.box import BoxConstraints
from flet.core.buttons import ButtonStyle
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.padding import OptionalPaddingValue
from flet.core.types import (
    IconValueOrControl,
    MouseCursor,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
    UrlTarget,
    VisualDensity,
)
from flet.utils.deprecated import deprecated_warning

__all__ = ["IconButton"]


@control("IconButton")
class IconButton(ConstrainedControl, AdaptiveControl):
    """
    An icon button is a round button with an icon in the middle that reacts to touches by filling with color (ink).

    Icon buttons are commonly used in the toolbars, but they can be used in many other places as well.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "Icon buttons"
        page.add(
            ft.Row(
                [
                    ft.IconButton(
                        icon=ft.icons.PAUSE_CIRCLE_FILLED_ROUNDED,
                        icon_color="blue400",
                        icon_size=20,
                        tooltip="Pause record",
                    ),
                    ft.IconButton(
                        icon=ft.icons.DELETE_FOREVER_ROUNDED,
                        icon_color="pink600",
                        icon_size=40,
                        tooltip="Delete record",
                    ),
                ]
            ),
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/iconbutton
    """

    def __setattr__(self, name, value):
        if name == "content" and value != None:
            deprecated_warning(
                name="content",
                reason="Use 'icon' instead.",
                version="0.70.0",
                delete_version="0.70.3",
            )
        super().__setattr__(name, value)

    icon: Optional[IconValueOrControl] = None
    icon_color: OptionalColorValue = None
    icon_size: OptionalNumber = None
    selected: bool = False
    selected_icon: Optional[IconValueOrControl] = None
    selected_icon_color: OptionalColorValue = None
    bgcolor: OptionalColorValue = None
    highlight_color: OptionalColorValue = None
    style: Optional[ButtonStyle] = None
    content: Optional[Control] = None  # deprecated
    autofocus: bool = False
    disabled_color: OptionalColorValue = None
    hover_color: OptionalColorValue = None
    focus_color: OptionalColorValue = None
    splash_color: OptionalColorValue = None
    splash_radius: OptionalNumber = None
    alignment: Optional[Alignment] = None
    padding: OptionalPaddingValue = None
    enable_feedback: Optional[bool] = True
    url: Optional[str] = None
    url_target: Optional[UrlTarget] = None
    mouse_cursor: Optional[MouseCursor] = None
    visual_density: Optional[VisualDensity] = None
    size_constraints: Optional[BoxConstraints] = None
    on_click: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None

    # def before_update(self):
    #     super().before_update()
    #     if self.__style is not None:
    #         self.__style.side = self._wrap_attr_dict(self.__style.side)
    #         self.__style.shape = self._wrap_attr_dict(self.__style.shape)
    #         self.__style.padding = self._wrap_attr_dict(self.__style.padding)

    async def focus_async(self):
        await self._invoke_method_async("focus")

    def focus(self):
        asyncio.create_task(self.focus_async())
