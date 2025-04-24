import asyncio
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.box import BoxConstraints
from flet.controls.buttons import ButtonStyle
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import (
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

    Online docs: https://flet.dev/docs/controls/iconbutton
    """

    def __setattr__(self, name, value):
        if name == "content" and value is not None:
            deprecated_warning(
                name="content",
                reason="Use 'icon' instead.",
                version="0.70.0",
                delete_version="0.73.0",
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
    content: Optional[Control] = None  # todo(0.70.3): remove in favor of icon

    async def focus_async(self):
        await self._invoke_method_async("focus")

    def focus(self):
        asyncio.create_task(self.focus_async())
