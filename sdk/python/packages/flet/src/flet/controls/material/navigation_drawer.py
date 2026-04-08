from dataclasses import field
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.buttons import OutlinedBorder
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.padding import Padding, PaddingValue
from flet.controls.types import (
    ColorValue,
    IconDataOrControl,
    Number,
    StrOrControl,
)

__all__ = [
    "NavigationDrawer",
    "NavigationDrawerDestination",
]


@control("NavigationDrawerDestination")
class NavigationDrawerDestination(Control):
    """
    A :class:`~NavigationDrawer` destination.
    """

    label: StrOrControl
    """
    The label that appears below the :attr:`icon` of this destination.
    """

    icon: IconDataOrControl
    """
    An icon name (or `Control`) that's displayed for this destination.

    If :attr:`selected_icon` is provided, `icon` will only be displayed when this
    destination is not selected.

    The icon will use :attr:`flet.NavigationDrawerTheme.icon_theme`. If this is
    `None`, the default :class:`~flet.IconTheme` would use a size of `24.0` and
    :attr:`flet.ColorScheme.on_surface_variant`.
    """

    selected_icon: Optional[IconDataOrControl] = None
    """
    An icon name (or `Control`) that's displayed for this destination when selected.

    If provided, this destination will fade from :attr:`icon` to `selected_icon`
    when this destination goes from unselected to selected state.

    If not provided, :attr:`icon` will be displayed for both
    selected and unselected states.

    The icon will use :attr:`flet.NavigationDrawerTheme.icon_theme` with
    :attr:`flet.ControlState.SELECTED`. If this is `None`, the default
    :class:`~flet.IconTheme` would use a size of `24.0` and
    :attr:`flet.ColorScheme.on_secondary_container`.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The background color of the whole rectangular area behind this drawer destination.

    To customize only the indicator color consider using
    :attr:`flet.NavigationDrawer.indicator_color`.

    If it is `None`, no background color is set for this destination and
    :class:`~flet.NavigationDrawer.bgcolor` will be visible.
    """


@control("NavigationDrawer")
class NavigationDrawer(AdaptiveControl):
    """
    Material Design Navigation Drawer component.

    Navigation Drawer is a panel that slides in horizontally from the left or right
    edge of the view to show primary destinations in an app.

    Example:
    ```python
    ft.NavigationDrawer(
        tile_padding=ft.Padding(top=10),
        controls=[
            ft.NavigationDrawerDestination(label="Item 1"),
            ft.NavigationDrawerDestination(label="Item 2"),
            ft.NavigationDrawerDestination(label="Item 3"),
        ],
    )
    ```
    """

    controls: list[Control] = field(default_factory=list)
    """
    Defines the appearance of the items within the navigation drawer.

    The list contains :class:`~flet.NavigationDrawerDestination` items and/or other
    controls such as headlines and dividers.
    """

    selected_index: int = 0
    """
    The index for the current selected `NavigationDrawerDestination` or null if no \
    destination is selected.

    A valid selected_index is an integer between 0 and number of destinations - `1`. For
    an invalid `selected_index`, for example, `-1`, all destinations will appear
    unselected.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The color of this navigation drawer.
    """

    elevation: Optional[Number] = None
    """
    The elevation of this navigation drawer.
    """

    indicator_color: Optional[ColorValue] = None
    """
    The color of the selected destination indicator.
    """

    indicator_shape: Optional[OutlinedBorder] = None
    """
    The shape of the selected destination indicator.
    """

    shadow_color: Optional[ColorValue] = None
    """
    The color used for the drop shadow to indicate :attr:`elevation`.
    """

    tile_padding: PaddingValue = field(
        default_factory=lambda: Padding.symmetric(horizontal=12)
    )
    """
    Defines the padding for :attr:`destination` controls.
    """

    on_change: Optional[ControlEventHandler["NavigationDrawer"]] = None
    """
    Called when the selected destination changed.
    """

    on_dismiss: Optional[ControlEventHandler["NavigationDrawer"]] = None
    """
    Called when this drawer is dismissed.
    """
