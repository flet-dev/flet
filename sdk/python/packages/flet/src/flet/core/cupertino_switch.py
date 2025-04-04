from dataclasses import field
from typing import Optional

from flet.core.constrained_control import ConstrainedControl
from flet.core.types import (
    ColorValue,
    ControlStateValue,
    IconValue,
    LabelPosition,
    OptionalControlEventCallable,
    OptionalNumber,
)
from flet.utils.deprecated import deprecated_warning

__all__ = ["CupertinoSwitch"]


class CupertinoSwitch(ConstrainedControl):
    """
    An iOS-style switch. Used to toggle the on/off state of a single setting.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.add(
            ft.CupertinoSwitch(label="Cupertino Switch", value=True),
            ft.Switch(label="Material Checkbox", value=True),
            ft.Container(height=20),
            ft.Text(
                "Adaptive Switch shows as CupertinoSwitch on macOS and iOS and as Switch on other platforms:"
            ),
            ft.Switch(adaptive=True, label="Adaptive Switch", value=True),
        )

    ft.app(target=main)
    ```
    -----

    Online docs: https://flet.dev/docs/controls/cupertinoswitch
    """

    label: Optional[str] = None
    value: bool = field(default=False)
    label_position: LabelPosition = field(default=LabelPosition.RIGHT)
    thumb_color: Optional[ColorValue] = None
    focus_color: Optional[ColorValue] = None
    autofocus: bool = field(default=False)
    on_label_color: Optional[ColorValue] = None
    off_label_color: Optional[ColorValue] = None
    active_thumb_image: Optional[str] = None
    inactive_thumb_image: Optional[str] = None
    active_track_color: Optional[ColorValue] = None
    inactive_thumb_color: Optional[ColorValue] = None
    inactive_track_color: Optional[ColorValue] = None
    track_outline_color: ControlStateValue[ColorValue] = None
    track_outline_width: ControlStateValue[OptionalNumber] = None
    thumb_icon: ControlStateValue[IconValue] = None
    on_change: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None
    on_image_error: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        # self._set_attr_json(
        #     "trackOutlineColor", self.__track_outline_color, wrap_attr_dict=True
        # )
        # self._set_attr_json(
        #     "trackOutlineWidth", self.__track_outline_width, wrap_attr_dict=True
        # )
        # self._set_attr_json("thumbIcon", self.__thumb_icon, wrap_attr_dict=True)
