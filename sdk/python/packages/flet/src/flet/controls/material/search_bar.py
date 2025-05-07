import asyncio
from dataclasses import field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.border import BorderSide, OptionalBorderSide
from flet.controls.box import OptionalBoxConstraints
from flet.controls.buttons import OptionalOutlinedBorder, OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control, OptionalControl
from flet.controls.control_state import OptionalControlStateValue
from flet.controls.material.textfield import KeyboardType, TextCapitalization
from flet.controls.padding import PaddingValue
from flet.controls.text_style import OptionalTextStyle, TextStyle
from flet.controls.types import (
    ColorValue,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
    OptionalString,
)

__all__ = ["SearchBar"]


@control("SearchBar")
class SearchBar(ConstrainedControl):
    """
    Manages a "search view" route that allows the user to select one of the suggested
    completions for a search query.

    Online docs: https://flet.dev/docs/controls/searchbar
    """

    controls: list[Control] = field(default_factory=list)
    value: str = ""
    bar_leading: OptionalControl = None
    bar_trailing: Optional[list[Control]] = None
    bar_hint_text: OptionalString = None
    bar_bgcolor: OptionalControlStateValue[ColorValue] = None
    bar_overlay_color: OptionalControlStateValue[ColorValue] = None
    bar_shadow_color: OptionalControlStateValue[ColorValue] = None
    bar_surface_tint_color: OptionalControlStateValue[ColorValue] = None
    bar_elevation: OptionalControlStateValue[OptionalNumber] = None
    bar_border_side: OptionalControlStateValue[BorderSide] = None
    bar_shape: OptionalControlStateValue[OutlinedBorder] = None
    bar_text_style: OptionalControlStateValue[TextStyle] = None
    bar_hint_text_style: OptionalControlStateValue[TextStyle] = None
    bar_padding: OptionalControlStateValue[PaddingValue] = None
    bar_scroll_padding: PaddingValue = 20
    view_leading: OptionalControl = None
    view_trailing: Optional[list[Control]] = None
    view_elevation: OptionalNumber = None
    view_bgcolor: OptionalColorValue = None
    view_hint_text: OptionalString = None
    view_side: OptionalBorderSide = None
    view_shape: OptionalOutlinedBorder = None
    view_header_text_style: OptionalTextStyle = None
    view_hint_text_style: OptionalTextStyle = None
    view_size_constraints: OptionalBoxConstraints = None
    view_header_height: OptionalNumber = None
    divider_color: OptionalColorValue = None
    capitalization: Optional[TextCapitalization] = None
    full_screen: bool = False
    keyboard_type: KeyboardType = KeyboardType.TEXT
    view_surface_tint_color: OptionalColorValue = None
    autofocus: bool = False
    on_tap: OptionalControlEventCallable = None
    on_tap_outside_bar: OptionalControlEventCallable = None
    on_submit: OptionalControlEventCallable = None
    on_change: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None

    def __contains__(self, item):
        return item in self.controls

    def before_update(self):
        super().before_update()

    # Public methods
    async def focus_async(self):
        await self._invoke_method_async("focus")

    def focus(self):
        asyncio.create_task(self.focus_async())

    async def blur_async(self):
        await self._invoke_method_async("blur")

    def blur(self):
        asyncio.create_task(self.blur_async())

    def open_view(self):
        asyncio.create_task(self.open_view_async())

    async def open_view_async(self):
        await self._invoke_method_async("open_view")

    def close_view(self, text: Optional[str] = None):
        asyncio.create_task(self.close_view_async(text))

    async def close_view_async(self, text: Optional[str] = None):
        await self._invoke_method_async(
            "close_view", {"text": text if text is not None else self.value}
        )
