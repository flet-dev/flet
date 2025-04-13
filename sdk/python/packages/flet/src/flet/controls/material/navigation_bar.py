from dataclasses import field
from enum import Enum
from typing import List, Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.border import Border
from flet.controls.buttons import OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import control
from flet.controls.control_state import OptionalControlStateValue
from flet.controls.duration import OptionalDurationValue
from flet.controls.types import (
    ColorValue,
    IconValueOrControl,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
)

__all__ = ["NavigationBar", "NavigationBarDestination", "NavigationBarLabelBehavior"]


class NavigationBarLabelBehavior(Enum):
    """Defines how the destinations' labels will be laid out and when they'll be displayed."""

    ALWAYS_SHOW = "alwaysShow"
    ALWAYS_HIDE = "alwaysHide"
    ONLY_SHOW_SELECTED = "onlyShowSelected"


@control("NavigationBarDestination")
class NavigationBarDestination(AdaptiveControl):
    """Defines the appearance of the button items that are arrayed within the navigation bar.

    The value must be a list of two or more NavigationBarDestination instances."""

    label: Optional[str] = None
    icon: Optional[IconValueOrControl] = None
    selected_icon: Optional[IconValueOrControl] = None
    bgcolor: OptionalColorValue = None


@control("NavigationBar")
class NavigationBar(ConstrainedControl, AdaptiveControl):
    """
    Material 3 Navigation Bar component.

    Navigation bars offer a persistent and convenient way to switch between primary destinations in an app.

    Example:

    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "NavigationBar Example"
        page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.EXPLORE, label="Explore"),
                ft.NavigationBarDestination(icon=ft.icons.COMMUTE, label="Commute"),
                ft.NavigationBarDestination(
                    icon=ft.icons.BOOKMARK_BORDER,
                    selected_icon=ft.icons.BOOKMARK,
                    label="Explore"
                ),
            ]
        )
        page.add(ft.Text("Body!"))

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/navigationbar
    """

    destinations: List[NavigationBarDestination] = field(default_factory=list)
    selected_index: int = 0
    bgcolor: OptionalColorValue = None
    label_behavior: Optional[NavigationBarLabelBehavior] = None
    elevation: OptionalNumber = None
    shadow_color: OptionalColorValue = None
    indicator_color: OptionalColorValue = None
    indicator_shape: Optional[OutlinedBorder] = None
    surface_tint_color: OptionalColorValue = None
    border: Optional[Border] = None
    animation_duration: OptionalDurationValue = None
    overlay_color: OptionalControlStateValue[ColorValue] = None
    on_change: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        # self._set_attr_json("overlayColor", self.__overlay_color, wrap_attr_dict=True)
