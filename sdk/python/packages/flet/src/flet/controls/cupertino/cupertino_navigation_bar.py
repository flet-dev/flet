from typing import Annotated, Optional

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
from flet.controls.validation import V

__all__ = ["CupertinoNavigationBar"]


@control("CupertinoNavigationBar")
class CupertinoNavigationBar(LayoutControl):
    """
    An iOS-styled bottom navigation tab bar.

    Navigation bars offer a persistent and convenient way to switch between primary
    destinations in an app.
    """

    destinations: Annotated[
        list[NavigationBarDestination],
        V.visible_controls(min_count=2),
    ]
    """
    The destinations of this navigation bar.

    Raises:
        ValueError: If it does not contain at least
            two visible `NavigationBarDestination`s.
    """

    selected_index: int = 0
    """
    The index into [`destinations`][(c).] for the currently selected \
    [`NavigationBarDestination`][flet.].

    Raises:
        IndexError: If it is not greater than or equal to `0`.
        IndexError: If it is not less than the length of visible
            [`destinations`][(c).].
    """

    bgcolor: Optional[ColorValue] = None
    """
    The color of the navigation bar itself.
    """

    active_color: Optional[ColorValue] = None
    """
    The foreground color of the icon and title of the selected \
    [`destination`][(c).destinations].
    """

    inactive_color: ColorValue = CupertinoColors.INACTIVE_GRAY
    """
    The foreground color of the icon and title of the unselected \
    [`destinations`][(c).].
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
        if visible_destinations_count >= 2 and not (
            0 <= self.selected_index < visible_destinations_count
        ):
            raise IndexError(
                f"selected_index ({self.selected_index}) is out of range. "
                f"Expected a value between 0 and {visible_destinations_count - 1} "
                "inclusive."
            )
