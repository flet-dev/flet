import asyncio
from dataclasses import field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.border import BorderSide, OptionalBorderSide
from flet.controls.box import OptionalBoxConstraints
from flet.controls.buttons import OptionalOutlinedBorder, OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control, OptionalControl
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.material.textfield import KeyboardType, TextCapitalization
from flet.controls.padding import PaddingValue
from flet.controls.text_style import OptionalTextStyle, TextStyle
from flet.controls.types import (
    ColorValue,
    OptionalColorValue,
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
    """
    The list of controls to be displayed below the search bar when in search view.
    These controls are usually `ListTile`s and will be displayed in a `ListView`.
    """

    value: str = ""
    """
    The text in the search bar.
    """

    bar_leading: OptionalControl = None
    """
    A `Control` to display before the text input field when the search view is close.
    This is typically an `Icon` or an `IconButton`.
    """

    bar_trailing: Optional[list[Control]] = None
    """
    A `Control` to display after the text input field when the search view is close.

    These controls can represent additional modes of searching (e.g voice search),
    an avatar, or an overflow menu and are usually not more than two.
    """

    bar_hint_text: OptionalString = None
    """
    Defines the text to be shown in the search bar when it is empty and the search
    view is close. Usually some text that suggests what sort of input the field
    accepts.
    """

    bar_bgcolor: Optional[ControlStateValue[ColorValue]] = None
    """
    Defines the background [color](https://flet.dev/docs/reference/colors) of the
    search bar in all or specific
    [`ControlState`](https://flet.dev/docs/reference/types/controlstate) states.
    """

    bar_overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Defines the highlight [color](https://flet.dev/docs/reference/colors) that's
    typically used to indicate that the search bar is in `FOCUSED`, `HOVERED`, or
    `PRESSED` [`ControlState`](https://flet.dev/docs/reference/types/controlstate)
    states.
    """

    bar_shadow_color: Optional[ControlStateValue[ColorValue]] = None
    """
    TBD
    """

    bar_surface_tint_color: Optional[ControlStateValue[ColorValue]] = None
    """
    TBD
    """

    bar_elevation: Optional[ControlStateValue[OptionalNumber]] = None
    """
    TBD
    """

    bar_border_side: Optional[ControlStateValue[BorderSide]] = None
    """
    TBD
    """

    bar_shape: Optional[ControlStateValue[OutlinedBorder]] = None
    """
    TBD
    """

    bar_text_style: Optional[ControlStateValue[TextStyle]] = None
    """
    TBD
    """

    bar_hint_text_style: Optional[ControlStateValue[TextStyle]] = None
    """
    TBD
    """

    bar_padding: Optional[ControlStateValue[PaddingValue]] = None
    """
    TBD
    """

    bar_scroll_padding: PaddingValue = 20
    """
    Configures the padding around a Scrollable when the text field scrolls into view.

    If the bar's text field is partially off-screen or covered (e.g., by the
    keyboard), it scrolls into view, ensuring it is positioned at the specified
    distance from the Scrollable edges.

    Value is of type [`Padding`](https://flet.dev/docs/reference/types/padding).
    """

    view_leading: OptionalControl = None
    """
    A `Control` to display before the text input field when the search view is open.
    Typically an `Icon` or an `IconButton`.

    Defaults to a back button which closes/pops the search view.
    """

    view_trailing: Optional[list[Control]] = None
    """
    A list of `Control`s to display after the text input field when the search view is
    open.

    Defaults to a close button which closes/pops the search view.
    """

    view_elevation: OptionalNumber = None
    """
    Defines the elevation of the search view.
    """

    view_bgcolor: OptionalColorValue = None
    """
    Defines the background [color](https://flet.dev/docs/reference/colors) of the
    search view.
    """

    view_hint_text: OptionalString = None
    """
    Defines the text to be displayed when the search bar's input field is empty.
    """

    view_side: OptionalBorderSide = None
    """
    Defines the color and weight of the search view's outline.

    Value is of type [`BorderSide`](https://flet.dev/docs/reference/types/borderside).
    """

    view_shape: OptionalOutlinedBorder = None
    """
    Defines the shape of the search view.

    Value is of type
    [`OutlinedBorder`](https://flet.dev/docs/reference/types/outlinedborder).
    """

    view_header_text_style: OptionalTextStyle = None
    """
    Defines the [`TextStyle`](https://flet.dev/docs/reference/types/textstyle) of the
    text being edited on the search view.
    """

    view_hint_text_style: OptionalTextStyle = None
    """
    Defines the [`TextStyle`](https://flet.dev/docs/reference/types/textstyle) of
    `view_hint_text`.
    """

    view_size_constraints: OptionalBoxConstraints = None
    """
    TBD
    """

    view_header_height: OptionalNumber = None
    """
    TBD
    """

    divider_color: OptionalColorValue = None
    """
    The color of the divider when in search view.
    """

    capitalization: Optional[TextCapitalization] = None
    """
    Enables automatic on-the-fly capitalization of entered text.

    Value is of type
    [`TextCapitalization`](https://flet.dev/docs/reference/types/textcapitalization).
    """

    full_screen: bool = False
    """
    Defines whether the search view grows to fill the entire screen when the search
    bar is tapped. Defaults to `False`.
    """

    keyboard_type: KeyboardType = KeyboardType.TEXT
    """
    The type of action button to use for the keyboard.

    Value is of type
    [`KeyboardType`](https://flet.dev/docs/reference/types/keyboardtype) and defaults
    to `KeyboardType TEXT`.
    """

    view_surface_tint_color: OptionalColorValue = None
    """
    Defines the color of the search view's surface tint.
    """

    autofocus: bool = False
    """
    Whether the text field should focus itself if nothing else is already focused.

    Defaults to `False`.
    """

    on_tap: OptionalControlEventHandler["SearchBar"] = None
    """
    Fires when the search bar is tapped.
    """

    on_tap_outside_bar: OptionalControlEventHandler["SearchBar"] = None
    """
    TBD
    """

    on_submit: OptionalControlEventHandler["SearchBar"] = None
    """
    Fires when user presses ENTER while focus is on SearchBar.
    """

    on_change: OptionalControlEventHandler["SearchBar"] = None
    """
    Fires when the typed input in the search bar has changed.
    """

    on_focus: OptionalControlEventHandler["SearchBar"] = None
    """
    TBD
    """

    on_blur: OptionalControlEventHandler["SearchBar"] = None
    """
    TBD
    """

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
