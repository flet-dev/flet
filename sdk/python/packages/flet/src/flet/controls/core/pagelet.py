from typing import Optional, Union

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control, OptionalControl
from flet.controls.cupertino.cupertino_app_bar import CupertinoAppBar
from flet.controls.cupertino.cupertino_navigation_bar import CupertinoNavigationBar
from flet.controls.material.app_bar import AppBar
from flet.controls.material.bottom_app_bar import BottomAppBar
from flet.controls.material.navigation_bar import NavigationBar
from flet.controls.material.navigation_drawer import NavigationDrawer
from flet.controls.transform import OffsetValue
from flet.controls.types import FloatingActionButtonLocation, OptionalColorValue

__all__ = ["Pagelet"]


@control("Pagelet")
class Pagelet(ConstrainedControl, AdaptiveControl):
    """
    Pagelet implements the basic Material Design visual layout structure.

    Use it for projects that require "page within a page" layouts with its own AppBar,
    BottomBar, Drawer, such as demos and galleries.

    Online docs: https://flet.dev/docs/controls/pagelet
    """

    content: Control
    """
    A child Control contained by the Pagelet.

    The control in the content of the Pagelet is positioned at the top-left of the
    available space between the app bar and the bottom of the Pagelet.
    """

    appbar: Optional[Union[AppBar, CupertinoAppBar]] = None
    """
    An [`AppBar`](https://flet.dev/docs/controls/appbar) control to display at the top
    of the Pagelet.
    """

    navigation_bar: Optional[Union[NavigationBar, CupertinoNavigationBar]] = None
    """
    [`NavigationBar`](https://flet.dev/docs/controls/navigationbar) control to display
    at the bottom of the page.

    If both [`bottom_appbar`](https://flet.dev/docs/controls/pagelet#bottom_appbar) and
    [`navigation_bar`](https://flet.dev/docs/controls/pagelet#navigation_bar)
    properties are provided, `NavigationBar` will be displayed.
    """

    bottom_appbar: Optional[BottomAppBar] = None
    """
    [`BottomAppBar`](https://flet.dev/docs/controls/bottomappbar) control to display at
    the bottom of the Pagelet.

    If both [`bottom_appbar`](https://flet.dev/docs/controls/pagelet#bottom_appbar) and
    [`navigation_bar`](https://flet.dev/docs/controls/pagelet#navigation_bar)
    properties are provided, `NavigationBar` will be displayed.
    """

    bottom_sheet: OptionalControl = None
    """
    The persistent bottom sheet to show information that supplements the primary
    content of the Pagelet. Can be any control.
    """

    drawer: Optional[NavigationDrawer] = None
    """
    A [`NavigationDrawer`](https://flet.dev/docs/controls/navigationdrawer) control to
    display as a panel sliding from the start edge of the page.
    """

    end_drawer: Optional[NavigationDrawer] = None
    """
    A [`NavigationDrawer`](https://flet.dev/docs/controls/navigationdrawer) control to
    display as a panel sliding from the end edge of the page.
    """

    floating_action_button: Optional[Control] = None
    """
    A [`FloatingActionButton`](https://flet.dev/docs/controls/floatingactionbutton)
    control to display on top of Pagelet content.
    """

    floating_action_button_location: Optional[
        Union[FloatingActionButtonLocation, OffsetValue]
    ] = None
    """
    Defines a position for the `FloatingActionButton`.

    Value can be of type `OffsetValue` or
    [`FloatingActionButtonLocation`](https://flet.dev/docs/reference/types/floatingactionbuttonlocation).
    Defaults to `FloatingActionButtonLocation.END_FLOAT`.
    """

    bgcolor: OptionalColorValue = None
    """
    Background [color](https://flet.dev/docs/reference/colors) of the Pagelet.
    """

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"

    # todo: deprecate show_* in favor of a open/close methods, or page.open/close
    # Drawer
    #
    def show_drawer(self, drawer: NavigationDrawer):
        self.drawer = drawer
        self.drawer.open = True
        self.update()

    def close_drawer(self):
        if self.drawer is not None:
            self.drawer.open = False
            self.update()

    # End_drawer
    #
    def show_end_drawer(self, end_drawer: NavigationDrawer):
        self.end_drawer = end_drawer
        self.end_drawer.open = True
        self.update()

    def close_end_drawer(self):
        if self.end_drawer is not None:
            self.end_drawer.open = False
            self.update()
