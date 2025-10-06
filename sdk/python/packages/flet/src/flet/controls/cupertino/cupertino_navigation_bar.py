from typing import Optional

from flet.controls.base_control import control
from flet.controls.border import Border
from flet.controls.control_event import ControlEventHandler
from flet.controls.cupertino.cupertino_colors import CupertinoColors
from flet.controls.layout_control import LayoutControl
from flet.controls.material.navigation_bar import NavigationBarDestination
from flet.controls.types import (
    ColorValue,
    Number,
)

__all__ = ["CupertinoNavigationBar"]


@control("CupertinoNavigationBar")
class CupertinoNavigationBar(LayoutControl):
    """
    An iOS-styled bottom navigation tab bar.

    Navigation bars offer a persistent and convenient way to switch between primary
    destinations in an app.
    """

    destinations: list[NavigationBarDestination]
    """
    The destinations of this navigation bar.

    Note:
        Must be a list of two or more [`NavigationBarDestination`][flet.]s.

    Raises:
        ValueError: If [`destinations`][(c).] does not contain at least two visible
            [`NavigationBarDestination`][flet.]s.
    """

    selected_index: int = 0
    """
    The index into [`destinations`][(c).] for the
    currently selected [`NavigationBarDestination`][flet.].

    Note:
        Must be a value between `0` and the length of visible
        [`destinations`][(c).], inclusive.

    Raises:
        IndexError: If [`selected_index`][(c).] is out of range relative to the
            visible destinations.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The color of the navigation bar itself.
    """

    active_color: Optional[ColorValue] = None
    """
    The foreground color of the icon and title of the
    selected [`destination`][(c).destinations].
    """

    inactive_color: ColorValue = CupertinoColors.INACTIVE_GRAY
    """
    The foreground color of the icon and title of the unselected [`destinations`][(c).].
    """

    border: Optional[Border] = None
    """
    Defines the border of this navigation bar.
    """

    icon_size: Number = 30
    """
    The size of all destination icons.
    """

    on_change: Optional[ControlEventHandler["CupertinoNavigationBar"]] = None
    """
    Called when selected destination changed.
    """

    def before_update(self):
        super().before_update()
        visible_destinations_count = len([d for d in self.destinations if d.visible])
        if visible_destinations_count < 2:
            raise ValueError(
                f"destinations must contain at minimum two visible controls, "
                f"got {visible_destinations_count}"
            )
        if not (0 <= self.selected_index < visible_destinations_count):
            raise IndexError(
                f"selected_index ({self.selected_index}) is out of range. "
                f"Expected a value between 0 and {visible_destinations_count - 1} "
                "inclusive."
            )
