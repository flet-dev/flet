from dataclasses import field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.border import BorderSide
from flet.controls.box import BoxConstraints
from flet.controls.buttons import OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.material.textfield import KeyboardType, TextCapitalization
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ColorValue,
    Number,
)

__all__ = ["SearchBar"]


@control("SearchBar")
class SearchBar(ConstrainedControl):
    """
    Manages a "search view" route that allows the user to select one of the suggested
    completions for a search query.
    """

    controls: list[Control] = field(default_factory=list)
    """
    The list of controls to be displayed below the search bar when in search view.
    These controls are usually [`ListTile`][flet.ListTile]s and will be displayed
    in a [`ListView`][flet.ListView].
    """

    value: str = ""
    """
    The text in the search bar.
    """

    bar_leading: Optional[Control] = None
    """
    A control to display before the text input field when the search view is close.
    This is typically an `Icon` or an `IconButton`.
    """

    bar_trailing: Optional[list[Control]] = None
    """
    A list of controls to display after the text input field when
    the search view is close.

    These controls can represent additional modes of searching (e.g voice search),
    an avatar, or an overflow menu and are usually not more than two.
    """

    bar_hint_text: Optional[str] = None
    """
    Defines the text to be shown in the search bar when it is empty and the search
    view is close. Usually some text that suggests what sort of input the field
    accepts.
    """

    bar_bgcolor: Optional[ControlStateValue[ColorValue]] = None
    """
    Defines the background color of the
    search bar in all or specific
    [`ControlState`][flet.ControlState] states.
    """

    bar_overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Defines the highlight color that's
    typically used to indicate that the search bar is in `FOCUSED`, `HOVERED`, or
    `PRESSED` [`ControlState`][flet.ControlState]
    states.
    """

    bar_shadow_color: Optional[ControlStateValue[ColorValue]] = None
    """
    TBD
    """

    bar_elevation: Optional[ControlStateValue[Optional[Number]]] = None
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
    """

    view_leading: Optional[Control] = None
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

    view_elevation: Optional[Number] = None
    """
    Defines the elevation of the search view.
    """

    view_bgcolor: Optional[ColorValue] = None
    """
    Defines the background color of the
    search view.
    """

    view_hint_text: Optional[str] = None
    """
    Defines the text to be displayed when the search bar's input field is empty.
    """

    view_side: Optional[BorderSide] = None
    """
    Defines the color and weight of the search view's outline.
    """

    view_shape: Optional[OutlinedBorder] = None
    """
    Defines the shape of the search view.
    """

    view_header_text_style: Optional[TextStyle] = None
    """
    Defines the [`TextStyle`][flet.TextStyle] of the
    text being edited on the search view.
    """

    view_hint_text_style: Optional[TextStyle] = None
    """
    Defines the [`TextStyle`][flet.TextStyle] of
    `view_hint_text`.
    """

    view_size_constraints: Optional[BoxConstraints] = None
    """
    TBD
    """

    view_header_height: Optional[Number] = None
    """
    TBD
    """

    divider_color: Optional[ColorValue] = None
    """
    The color of the divider when in search view.
    """

    capitalization: Optional[TextCapitalization] = None
    """
    Enables automatic on-the-fly capitalization of entered text.
    """

    full_screen: bool = False
    """
    Defines whether the search view grows to fill the entire screen when the search
    bar is tapped. Defaults to `False`.
    """

    keyboard_type: KeyboardType = KeyboardType.TEXT
    """
    The type of action button to use for the keyboard.
    """

    autofocus: bool = False
    """
    Whether the text field should focus itself if nothing else is already focused.

    Defaults to `False`.
    """

    on_tap: Optional[ControlEventHandler["SearchBar"]] = None
    """
    Called when the search bar is tapped.
    """

    on_tap_outside_bar: Optional[ControlEventHandler["SearchBar"]] = None
    """
    TBD
    """

    on_submit: Optional[ControlEventHandler["SearchBar"]] = None
    """
    Called when user presses ENTER while focus is on SearchBar.
    """

    on_change: Optional[ControlEventHandler["SearchBar"]] = None
    """
    Called when the typed input in the search bar has changed.
    """

    on_focus: Optional[ControlEventHandler["SearchBar"]] = None
    """
    TBD
    """

    on_blur: Optional[ControlEventHandler["SearchBar"]] = None
    """
    TBD
    """

    def __contains__(self, item):
        return item in self.controls

    def before_update(self):
        super().before_update()

    # Public methods
    async def focus(self):
        await self._invoke_method("focus")

    async def blur(self):
        await self._invoke_method("blur")

    async def open_view(self):
        await self._invoke_method("open_view")

    async def close_view(self, text: Optional[str] = None):
        await self._invoke_method(
            "close_view", {"text": text if text is not None else self.value}
        )
