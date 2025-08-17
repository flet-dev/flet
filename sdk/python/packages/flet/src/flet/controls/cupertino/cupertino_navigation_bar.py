from typing import Optional

from flet.controls.base_control import control
from flet.controls.border import Border
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import ControlEventHandler
from flet.controls.cupertino.cupertino_colors import CupertinoColors
from flet.controls.material.navigation_bar import NavigationBarDestination
from flet.controls.types import (
    ColorValue,
    Number,
)

__all__ = ["CupertinoNavigationBar"]


@control("CupertinoNavigationBar")
class CupertinoNavigationBar(ConstrainedControl):
    """
    An iOS-styled bottom navigation tab bar.

    Navigation bars offer a persistent and convenient way to switch between primary
    destinations in an app.

    Raises:
        AssertionError: If [`destinations`][(c).] does not contain at least two visible
            [`NavigationBarDestination`][flet.NavigationBarDestination]s.
            IndexError: If [`selected_index`][(c).] is out of range.
    """

    destinations: list[NavigationBarDestination]
    """
    The destinations of this navigation bar.

    Note:
        Must be a list of two or more [`NavigationBarDestination`][flet.NavigationBarDestination]s.
    """  # noqa: E501

    selected_index: int = 0
    """
    The index into [`destinations`][flet.CupertinoNavigationBar.destinations] for the
    currently selected [`NavigationBarDestination`][flet.NavigationBarDestination].

    Note:
        Must be a value between `0` and the length of visible
        [`destinations`][flet.CupertinoNavigationBar.destinations], inclusive.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The color of the navigation bar itself.
    """

    active_color: Optional[ColorValue] = None
    """
    The foreground color of the icon and
    title of the selected destination.
    """

    inactive_color: ColorValue = CupertinoColors.INACTIVE_GRAY
    """
    The foreground color of the icon and
    title of the unselected destinations.
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
        assert visible_destinations_count >= 2, (
            f"destinations must contain at minimum two visible controls, "
            f"got {visible_destinations_count}"
        )
        if not (0 <= self.selected_index < visible_destinations_count):
            raise IndexError(
                f"selected_index ({self.selected_index}) is out of range. "
                f"Expected a value between 0 and {visible_destinations_count - 1} "
                "inclusive."
            )
