from dataclasses import field
from typing import List, Optional, Union

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.box import BoxDecoration
from flet.controls.control import Control, control
from flet.controls.cupertino.cupertino_app_bar import CupertinoAppBar
from flet.controls.cupertino.cupertino_navigation_bar import CupertinoNavigationBar
from flet.controls.material.app_bar import AppBar
from flet.controls.material.bottom_app_bar import BottomAppBar
from flet.controls.material.floating_action_button import FloatingActionButton
from flet.controls.material.navigation_bar import NavigationBar
from flet.controls.material.navigation_drawer import NavigationDrawer
from flet.controls.padding import OptionalPaddingValue
from flet.controls.scrollable_control import ScrollableControl
from flet.controls.transform import OffsetValue
from flet.controls.types import (
    CrossAxisAlignment,
    FloatingActionButtonLocation,
    MainAxisAlignment,
    OptionalColorValue,
    OptionalNumber,
)

__all__ = ["View"]


@control("View")
class View(ScrollableControl, AdaptiveControl):
    """
    View is the top most container for all other controls.

    A root view is automatically created when a new user session started. From layout perspective the View represents a `Column`(https://flet.dev/docs/controls/column/) control, so it has a similar behavior and shares same properties.

    -----

    Online docs: https://flet.dev/docs/controls/view
    """

    route: Optional[str] = None
    controls: List[Control] = field(default_factory=list)
    appbar: Optional[Union[AppBar, CupertinoAppBar]] = None
    bottom_appbar: Optional[BottomAppBar] = None
    floating_action_button: Optional[FloatingActionButton] = None
    floating_action_button_location: Optional[
        Union[FloatingActionButtonLocation, OffsetValue]
    ] = None
    navigation_bar: Union[NavigationBar, CupertinoNavigationBar, None] = None
    drawer: Optional[NavigationDrawer] = None
    end_drawer: Optional[NavigationDrawer] = None
    vertical_alignment: Optional[MainAxisAlignment] = None
    horizontal_alignment: Optional[CrossAxisAlignment] = None
    spacing: OptionalNumber = None
    padding: OptionalPaddingValue = None
    bgcolor: OptionalColorValue = None
    decoration: Optional[BoxDecoration] = None
    foreground_decoration: Optional[BoxDecoration] = None

    # Magic methods
    def __contains__(self, item: Control) -> bool:
        return item in self.controls
