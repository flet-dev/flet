from dataclasses import field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.border import Border
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.cupertino.cupertino_colors import CupertinoColors
from flet.controls.material.navigation_bar import NavigationBarDestination
from flet.controls.types import (
    ColorValue,
    Number,
    OptionalColorValue,
    OptionalControlEventCallable,
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
    selected_index: int = 0
    bgcolor: OptionalColorValue = None
    active_color: OptionalColorValue = None
    inactive_color: ColorValue = CupertinoColors.INACTIVE_GRAY
    border: Optional[Border] = None
    icon_size: Number = 30
    on_change: OptionalControlEventCallable = None
