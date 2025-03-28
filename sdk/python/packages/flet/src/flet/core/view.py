from dataclasses import field
from typing import List, Optional, Union

from flet.core.adaptive_control import AdaptiveControl
from flet.core.app_bar import AppBar
from flet.core.bottom_app_bar import BottomAppBar
from flet.core.box import BoxDecoration
from flet.core.control import Control, OptionalNumber, control
from flet.core.cupertino_app_bar import CupertinoAppBar
from flet.core.cupertino_navigation_bar import CupertinoNavigationBar
from flet.core.floating_action_button import FloatingActionButton
from flet.core.navigation_bar import NavigationBar
from flet.core.navigation_drawer import NavigationDrawer
from flet.core.scrollable_control import ScrollableControl
from flet.core.types import (
    ColorValue,
    CrossAxisAlignment,
    FloatingActionButtonLocation,
    MainAxisAlignment,
    OffsetValue,
    PaddingValue,
)


@control("View")
class View(ScrollableControl, AdaptiveControl):
    """
    View is the top most container for all other controls.

    A root view is automatically created when a new user session started. From layout perspective the View represents a `Column`(https://flet.dev/docs/controls/column/) control, so it has a similar behavior and shares same properties.

    -----

    Online docs: https://flet.dev/docs/controls/view
    """

    route: Optional[str] = None
    controls: List[Control] = field(default_factory=lambda: [])
    appbar: Union[AppBar, CupertinoAppBar, None] = None
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
    padding: Optional[PaddingValue] = None
    bgcolor: Optional[ColorValue] = None
    decoration: Optional[BoxDecoration] = None
    foreground_decoration: Optional[BoxDecoration] = None

    # Magic methods
    def __contains__(self, item: Control) -> bool:
        return item in self.controls
