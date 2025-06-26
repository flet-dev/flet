from dataclasses import field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.border import Border
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.cupertino.cupertino_colors import CupertinoColors
from flet.controls.material.navigation_bar import NavigationBarDestination
from flet.controls.types import (
    ColorValue,
    Number,
    OptionalColorValue,
)

__all__ = ["CupertinoNavigationBar"]


@control("CupertinoNavigationBar")
class CupertinoNavigationBar(ConstrainedControl):
    """
    An iOS-styled bottom navigation tab bar.

    Navigation bars offer a persistent and convenient way to switch between primary
    destinations in an app.

    Online docs: https://flet.dev/docs/controls/cupertinonavigationbar
    """

    destinations: list[NavigationBarDestination] = field(default_factory=list)
    """
    Defines the appearance of the button items that are arrayed within the navigation 
    bar.

    The value must be a list of two or more 
    [`NavigationBarDestination`](https://flet.dev/docs/controls/navigationbar#navigationbardestination-properties) 
    instances.
    """

    selected_index: int = 0
    """
    The index into `destinations` for the current selected `NavigationBarDestination`.
    """

    bgcolor: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) of the navigation bar itself.
    """

    active_color: OptionalColorValue = None
    """
    The foreground [color](https://flet.dev/docs/reference/colors) of the icon and 
    title of the selected destination.
    """

    inactive_color: ColorValue = CupertinoColors.INACTIVE_GRAY
    """
    The foreground [color](https://flet.dev/docs/reference/colors) of the icon and 
    title of the unselected destinations.
    """

    border: Optional[Border] = None
    """
    Defines the border of this navigation bar.

    The value is an instance of 
    [`Border`](https://flet.dev/docs/reference/types/border) class.
    """

    icon_size: Number = 30
    """
    The size of all destination icons.

    Defaults to `30`.
    """

    on_change: OptionalControlEventHandler["CupertinoNavigationBar"] = None
    """
    Fires when selected destination changed.
    """
