import time
from dataclasses import field
from typing import List, Optional

from flet.controls.base_control import control
from flet.controls.border import BorderSide
from flet.controls.box import BoxConstraints
from flet.controls.buttons import OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_state import OptionalControlStateValue
from flet.controls.material.textfield import KeyboardType, TextCapitalization
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ColorValue,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
)

__all__ = ["SearchBar"]


@control("SearchBar")
class SearchBar(ConstrainedControl):
    """
    Manages a "search view" route that allows the user to select one of the suggested completions for a search query.

    -----

    Online docs: https://flet.dev/docs/controls/searchbar
    """

    controls: List[Control] = field(default_factory=list)
    value: Optional[str] = None
    bar_leading: Optional[Control] = None
    bar_trailing: Optional[List[Control]] = None
    bar_hint_text: Optional[str] = None
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
    view_leading: Optional[Control] = None
    view_trailing: Optional[List[Control]] = None
    view_elevation: OptionalNumber = None
    view_bgcolor: OptionalColorValue = None
    view_hint_text: Optional[str] = None
    view_side: Optional[BorderSide] = None
    view_shape: Optional[OutlinedBorder] = None
    view_header_text_style: Optional[TextStyle] = None
    view_hint_text_style: Optional[TextStyle] = None
    view_size_constraints: Optional[BoxConstraints] = None
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
    def focus(self):
        self._set_attr_json("focus", str(time.time()))
        self.update()

    def blur(self):
        self._set_attr_json("blur", str(time.time()))
        self.update()

    def open_view(self):
        m = {
            "n": "openView",
            "i": str(time.time()),
            "p": {},
        }
        self._set_attr_json("method", m)
        self.update()

    def close_view(self, text: str = ""):
        m = {
            "n": "closeView",
            "i": str(time.time()),
            "p": {"text": text},
        }
        self.value = text
        self._set_attr_json("method", m)
        self.update()
