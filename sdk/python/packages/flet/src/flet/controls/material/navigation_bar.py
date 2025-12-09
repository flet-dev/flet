from dataclasses import field
from enum import Enum
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.border import Border
from flet.controls.buttons import OutlinedBorder
from flet.controls.control_event import ControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.duration import DurationValue
from flet.controls.layout_control import LayoutControl
from flet.controls.padding import PaddingValue
from flet.controls.types import (
    ColorValue,
    IconDataOrControl,
    Number,
)

__all__ = ["NavigationBar", "NavigationBarDestination", "NavigationBarLabelBehavior"]


class NavigationBarLabelBehavior(Enum):
    """
    Defines how the destinations' labels will be laid out and when they'll
    be displayed.
    """

    ALWAYS_SHOW = "alwaysShow"
    ALWAYS_HIDE = "alwaysHide"
    ONLY_SHOW_SELECTED = "onlyShowSelected"


@control("NavigationBarDestination")
class NavigationBarDestination(AdaptiveControl):
    """
    Defines the appearance of the button items that are arrayed within the
    navigation bar.

    The value must be a list of two or more NavigationBarDestination instances.
    """

    icon: IconDataOrControl
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

    To make the NavigationBar more accessible, consider choosing an icon with a stroked
    and filled version, such as `ft.Icons.CLOUD` and `ft.Icons.CLOUD_QUEUE`. The icon
    should be set to the stroked version and `selected_icon` to the filled version.
    """

    label: Optional[str] = None
    """
    The text label that appears below the icon of this `NavigationBarDestination`.
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

    If this icon is not provided, the NavigationBar will display `icon` in either state.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The color of this destination.
    """


@control("NavigationBar")
class NavigationBar(LayoutControl, AdaptiveControl):
    """
    Material 3 Navigation Bar component.

    Navigation bars offer a persistent and convenient way to switch between primary
    destinations in an app.

    ```python
    ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.CIRCLE, label="Item 1"),
            ft.NavigationBarDestination(icon=ft.Icons.SQUARE, label="Item 2"),
            ft.NavigationBarDestination(icon=ft.Icons.HEXAGON, label="Item 3"),
        ],
    )
    ```

    """

    destinations: list[NavigationBarDestination] = field(default_factory=list)
    """
    Defines the appearance of the button items that are arrayed within the navigation
    bar.

    The value must be a list of two or more `NavigationBarDestination` instances.
    """

    selected_index: int = 0
    """
    The index into `destinations` for the current selected `NavigationBarDestination` or
    `None` if no destination is selected.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The color of the navigation bar itself.
    """

    label_behavior: Optional[NavigationBarLabelBehavior] = None
    """
    Defines how the destinations' labels will be laid out and when they'll be displayed.

    Can be used to show all labels, show only the selected label, or hide all labels.

    Defaults to `NavigationBarLabelBehavior.ALWAYS_SHOW`.
    """

    label_padding: Optional[PaddingValue] = None
    """
    The padding around the
    [`NavigationBarDestination.label`][flet.].
    """

    elevation: Optional[Number] = None
    """
    The elevation of the navigation bar itself.
    """

    shadow_color: Optional[ColorValue] = None
    """
    The color used for the drop shadow to
    indicate `elevation`.
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

    border: Optional[Border] = None
    """
    TBD
    """

    animation_duration: Optional[DurationValue] = None
    """
    The transition time for each destination as it goes between selected and unselected.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The highlight color of the `NavigationBarDestination` in various
    [`ControlState`][flet.] states.

    The following [`ControlState`][flet.]
    values are supported: `PRESSED`, `HOVERED` and `FOCUSED`.
    """

    on_change: Optional[ControlEventHandler["NavigationBar"]] = None
    """
    Called when selected destination changed.
    """
