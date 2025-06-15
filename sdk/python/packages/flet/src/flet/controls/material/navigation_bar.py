from dataclasses import field
from enum import Enum
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.border import Border
from flet.controls.buttons import OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.duration import OptionalDurationValue
from flet.controls.types import (
    ColorValue,
    IconValueOrControl,
    OptionalColorValue,
    OptionalNumber,
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

    label: Optional[str] = None
    """
    The text label that appears below the icon of this `NavigationBarDestination`.
    """

    icon: Optional[IconValueOrControl] = None
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

    selected_icon: Optional[IconValueOrControl] = None
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

    bgcolor: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) of this destination.
    """


@control("NavigationBar")
class NavigationBar(ConstrainedControl, AdaptiveControl):
    """
    Material 3 Navigation Bar component.

    Navigation bars offer a persistent and convenient way to switch between primary
    destinations in an app.

    Online docs: https://flet.dev/docs/controls/navigationbar
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

    bgcolor: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) of the navigation bar itself.
    """

    label_behavior: Optional[NavigationBarLabelBehavior] = None
    """
    Defines how the destinations' labels will be laid out and when they'll be displayed.

    Can be used to show all labels, show only the selected label, or hide all labels.

    Value is of type
    [`NavigationBarLabelBehavior`](https://flet.dev/docs/reference/types/navigationbarlabelbehavior)
    and defaults to `NavigationBarLabelBehavior.ALWAYS_SHOW`.
    """

    elevation: OptionalNumber = None
    """
    The elevation of the navigation bar itself.
    """

    shadow_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) used for the drop shadow to 
    indicate `elevation`.
    """

    indicator_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) of the selected destination 
    indicator.
    """

    indicator_shape: Optional[OutlinedBorder] = None
    """
    The shape of the selected destination indicator.

    Value is of type
    [`OutlinedBorder`](https://flet.dev/docs/reference/types/outlinedborder).
    """

    surface_tint_color: OptionalColorValue = None
    """
    The surface tint of the Material that holds the NavigationDrawer's contents.
    """

    border: Optional[Border] = None
    """
    TBD
    """

    animation_duration: OptionalDurationValue = None
    """
    The transition time for each destination as it goes between selected and unselected.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The highlight [color](https://flet.dev/docs/reference/colors) of the
    `NavigationDestination` in various
    [`ControlState`](https://flet.dev/docs/reference/types/controlstate) states.

    The following [`ControlState`](https://flet.dev/docs/reference/types/controlstate) 
    values are supported: `PRESSED`, `HOVERED` and `FOCUSED`.
    """

    on_change: OptionalControlEventHandler["NavigationBar"] = None
    """
    Fires when selected destination changed.
    """
