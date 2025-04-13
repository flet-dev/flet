from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import control
from flet.controls.control_state import OptionalControlStateValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ColorValue,
    IconValue,
    LabelPosition,
    MouseCursor,
    OnFocusEvent,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalEventCallable,
    OptionalNumber,
    StrOrControl,
)

__all__ = ["Switch"]


@control("Switch")
class Switch(ConstrainedControl, AdaptiveControl):
    """
    A toggle represents a physical switch that allows someone to choose between two mutually exclusive options.

    or example, "On/Off", "Show/Hide". Choosing an option should produce an immediate result.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        def theme_changed(e):
            page.theme_mode = (
                ft.ThemeMode.DARK
                if page.theme_mode == ft.ThemeMode.LIGHT
                else ft.ThemeMode.LIGHT
            )
            c.label = (
                "Light theme" if page.theme_mode == ft.ThemeMode.LIGHT else "Dark theme"
            )
            page.update()

        page.theme_mode = ft.ThemeMode.LIGHT
        c = ft.Switch(label="Light theme", on_change=theme_changed)
        page.add(c)

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/switch
    """

    label: Optional[StrOrControl] = None
    label_position: Optional[LabelPosition] = None
    label_style: Optional[TextStyle] = None
    value: bool = False
    autofocus: bool = False
    active_color: OptionalColorValue = None
    active_track_color: OptionalColorValue = None
    focus_color: OptionalColorValue = None
    inactive_thumb_color: OptionalColorValue = None
    inactive_track_color: OptionalColorValue = None
    thumb_color: OptionalControlStateValue[ColorValue] = None
    thumb_icon: OptionalControlStateValue[IconValue] = None
    track_color: OptionalControlStateValue[ColorValue] = None
    adaptive: Optional[bool] = None
    hover_color: OptionalColorValue = None
    splash_radius: OptionalNumber = None
    overlay_color: OptionalControlStateValue[ColorValue] = None
    track_outline_color: OptionalControlStateValue[ColorValue] = None
    track_outline_width: OptionalControlStateValue[OptionalNumber] = None
    mouse_cursor: Optional[MouseCursor] = None
    on_change: OptionalControlEventCallable = None
    on_focus: OptionalEventCallable[OnFocusEvent] = None
    on_blur: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert (
            self.splash_radius is None or self.splash_radius >= 0
        ), "splash_radius cannot be negative"
        #     super().before_update()
        #     self._set_attr_json("thumbColor", self.__thumb_color, wrap_attr_dict=True)
        #     self._set_attr_json("overlayColor", self.__overlay_color, wrap_attr_dict=True)
        #     self._set_attr_json(
        #         "trackOutlineColor", self.__track_outline_color, wrap_attr_dict=True
        #     )
        #     self._set_attr_json(
        #         "trackOutlineWidth", self.__track_outline_width, wrap_attr_dict=True
        #     )
        #     self._set_attr_json("thumbIcon", self.__thumb_icon, wrap_attr_dict=True)
        #     self._set_attr_json("trackColor", self.__track_color, wrap_attr_dict=True)
