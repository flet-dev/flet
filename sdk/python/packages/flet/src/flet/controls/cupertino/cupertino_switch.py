from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_state import OptionalControlStateValue
from flet.controls.types import (
    ColorValue,
    IconValue,
    LabelPosition,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
)

__all__ = ["CupertinoSwitch"]


@control("CupertinoSwitch")
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
                "Adaptive Switch shows as CupertinoSwitch on macOS and iOS and "
                "as Switch on other platforms:"
            ),
            ft.Switch(adaptive=True, label="Adaptive Switch", value=True),
        )

    ft.app(target=main)
    ```
    -----

    Online docs: https://flet.dev/docs/controls/cupertinoswitch
    """

    label: Optional[str] = None
    value: bool = False
    label_position: LabelPosition = LabelPosition.RIGHT
    thumb_color: OptionalColorValue = None
    focus_color: OptionalColorValue = None
    autofocus: bool = False
    on_label_color: OptionalColorValue = None
    off_label_color: OptionalColorValue = None
    active_thumb_image: Optional[str] = None
    inactive_thumb_image: Optional[str] = None
    active_track_color: OptionalColorValue = None
    inactive_thumb_color: OptionalColorValue = None
    inactive_track_color: OptionalColorValue = None
    track_outline_color: OptionalControlStateValue[ColorValue] = None
    track_outline_width: OptionalControlStateValue[OptionalNumber] = None
    thumb_icon: OptionalControlStateValue[IconValue] = None
    on_change: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None
    on_image_error: OptionalControlEventCallable = None
