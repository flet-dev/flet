import time
from dataclasses import field
from typing import List, Optional

from flet.core.border import BorderSide
from flet.core.box import BoxConstraints
from flet.core.buttons import OutlinedBorder
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.padding import OptionalPaddingValue, PaddingValue
from flet.core.text_style import TextStyle
from flet.core.textfield import KeyboardType, TextCapitalization
from flet.core.types import (
    ColorValue,
    ControlStateValue,
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
    bar_bgcolor: ControlStateValue[ColorValue] = None
    bar_overlay_color: ControlStateValue[ColorValue] = None
    bar_shadow_color: ControlStateValue[ColorValue] = None
    bar_surface_tint_color: ControlStateValue[ColorValue] = None
    bar_elevation: ControlStateValue[OptionalNumber] = None
    bar_border_side: ControlStateValue[BorderSide] = None
    bar_shape: ControlStateValue[OutlinedBorder] = None
    bar_text_style: ControlStateValue[TextStyle] = None
    bar_hint_text_style: ControlStateValue[TextStyle] = None
    bar_padding: ControlStateValue[PaddingValue] = None
    bar_scroll_padding: OptionalPaddingValue = None
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
    full_screen: Optional[bool] = None
    keyboard_type: Optional[KeyboardType] = None
    view_surface_tint_color: OptionalColorValue = None
    autofocus: Optional[bool] = None
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
        # self._set_attr_json("barBgcolor", self.__bar_bgcolor, wrap_attr_dict=True)
        # self._set_attr_json(
        #     "barOverlayColor", self.__bar_overlay_color, wrap_attr_dict=True
        # )
        # self._set_attr_json(
        #     "barHintTextStyle", self.__bar_hint_text_style, wrap_attr_dict=True
        # )
        # self._set_attr_json(
        #     "barSurfaceTintColor", self.__bar_surface_tint_color, wrap_attr_dict=True
        # )
        # self._set_attr_json("barElevation", self.__bar_elevation, wrap_attr_dict=True)
        # self._set_attr_json(
        #     "barBorderSide", self.__bar_border_side, wrap_attr_dict=True
        # )
        # self._set_attr_json("barShape", self.__bar_shape, wrap_attr_dict=True)
        # self._set_attr_json("barTextStyle", self.__bar_text_style, wrap_attr_dict=True)
        # self._set_attr_json("barPadding", self.__bar_padding, wrap_attr_dict=True)
        # self._set_attr_json(
        #     "barShadowColor", self.__bar_shadow_color, wrap_attr_dict=True
        # )

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
