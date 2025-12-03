from dataclasses import field
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.buttons import OutlinedBorder
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.padding import PaddingValue
from flet.controls.types import (
    ColorValue,
    IconDataOrControl,
    Number,
)

__all__ = [
    "NavigationDrawer",
    "NavigationDrawerDestination",
]


@control("NavigationDrawerDestination")
class NavigationDrawerDestination(Control):
    """
    Displays an icon with a label, for use in NavigationDrawer destinations.
    """

    label: Optional[str] = None
    """
    The text label that appears below the icon of this `NavigationDrawerDestination`.
    """

    icon: Optional[IconDataOrControl] = None
    """
    The [name of the icon](https://flet.dev/docs/reference/icons) or `Control` of the
    destination.

    Example with icon name:
    ```
    icon=ft.Icons.BOOKMARK
    ```
    Example with Control:
    ```
    icon=ft.Icon(ft.Icons.BOOKMARK)
    ```

    If `selected_icon` is provided, this will only be displayed when the destination is
    not selected.
    """

    selected_icon: Optional[IconDataOrControl] = None
    """
    The [name](https://flet.dev/docs/reference/icons) of alternative icon or `Control`
    displayed when this destination is selected.

    Example with icon name:
    ```
    selected_icon=ft.Icons.BOOKMARK
    ```
    Example with Control:
    ```
    selected_icon=ft.Icon(ft.Icons.BOOKMARK)
    ```

    If this icon is not provided, the NavigationDrawer will display `icon` in either
    state.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The color of this destination.
    """


@control("NavigationDrawer")
class NavigationDrawer(AdaptiveControl):
    """
    Material Design Navigation Drawer component.

    Navigation Drawer is a panel slides in horizontally from the left or right edge of
    a page to show primary destinations in an app.

    ```python
    ft.NavigationDrawer(
        controls=[
            ft.NavigationDrawerDestination(label="Item 1"),
            ft.NavigationDrawerDestination(label="Item 2"),
            ft.NavigationDrawerDestination(label="Item 3"),
        ],
        tile_padding=ft.Padding(top=10),
    )
    ```

    """

    controls: list[Control] = field(default_factory=list)
    """
    Defines the appearance of the items within the navigation drawer.

    The list contains `NavigationDrawerDestination` items and/or other controls such as
    headlines and dividers.
    """

    selected_index: int = 0
    """
    The index for the current selected `NavigationDrawerDestination` or null if no
    destination is selected.

    A valid selected_index is an integer between 0 and number of destinations - `1`. For
    an invalid `selected_index`, for example, `-1`, all destinations will appear
    unselected.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The color of the navigation drawer itself.
    """

    elevation: Optional[Number] = None
    """
    The elevation of the navigation drawer itself.
    """

    indicator_color: Optional[ColorValue] = None
    """
    The color of the selected destination
    indicator.
    """

    indicator_shape: Optional[OutlinedBorder] = None
    """
    The shape of the selected destination indicator.
    """

    shadow_color: Optional[ColorValue] = None
    """
    The color used for the drop shadow to
    indicate `elevation`.
    """

    tile_padding: Optional[PaddingValue] = None
    """
    Defines the padding for `destination` controls.
    """

    on_change: Optional[ControlEventHandler["NavigationDrawer"]] = None
    """
    Called when selected destination changed.
    """

    on_dismiss: Optional[ControlEventHandler["NavigationDrawer"]] = None
    """
    Called when the drawer is dismissed.
    """
