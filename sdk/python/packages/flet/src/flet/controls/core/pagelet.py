from typing import Optional, Union

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.cupertino.cupertino_app_bar import CupertinoAppBar
from flet.controls.cupertino.cupertino_navigation_bar import CupertinoNavigationBar
from flet.controls.layout_control import LayoutControl
from flet.controls.material.app_bar import AppBar
from flet.controls.material.bottom_app_bar import BottomAppBar
from flet.controls.material.navigation_bar import NavigationBar
from flet.controls.material.navigation_drawer import NavigationDrawer
from flet.controls.transform import OffsetValue
from flet.controls.types import ColorValue, FloatingActionButtonLocation

__all__ = ["Pagelet"]


@control("Pagelet")
class Pagelet(LayoutControl, AdaptiveControl):
    """
    Implements the basic Material Design visual layout structure.

    Use it for projects that require a "page within a page" layouts with its own
    [`AppBar`][flet..], [`BottomAppBar`][flet..], [`NavigationDrawer`][flet..],
    such as demos and galleries.

    Raises:
        AssertionError: If [`content`][(c).] is not visible.
    """

    content: Control
    """
    A child Control contained by the Pagelet.

    The control in the content of the Pagelet is positioned at the top-left of the
    available space between the app bar and the bottom of the Pagelet.
    """

    appbar: Optional[Union[AppBar, CupertinoAppBar]] = None
    """
    An [`AppBar`][flet.AppBar] control to display at the top
    of the Pagelet.
    """

    navigation_bar: Optional[Union[NavigationBar, CupertinoNavigationBar]] = None
    """
    A navigation bar ([`NavigationBar`][flet.NavigationBar] or
    [`CupertinoNavigationBar`][flet.CupertinoNavigationBar]) control to display
    at the bottom of the `Pagelet`.

    Note:
        If both the `navigation_bar` and [`bottom_appbar`][flet.Pagelet.bottom_appbar]
        properties are specified, `navigation_bar` takes precedence and will
        be displayed.
    """

    bottom_appbar: Optional[BottomAppBar] = None
    """
    A [`BottomAppBar`][flet.BottomAppBar] control to display at
    the bottom of the `Pagelet`.

    Note:
        If both the `bottom_appbar` and [`navigation_bar`][flet.Pagelet.navigation_bar]
        properties are specified, `bottom_appbar` takes precedence and will
        be displayed.
    """

    bottom_sheet: Optional[Control] = None
    """
    The persistent bottom sheet to show information that supplements the primary
    content of the Pagelet.
    """

    drawer: Optional[NavigationDrawer] = None
    """
    A [`NavigationDrawer`][flet.NavigationDrawer] control to
    display as a panel sliding from the start edge of the page.
    """

    end_drawer: Optional[NavigationDrawer] = None
    """
    A [`NavigationDrawer`][flet.NavigationDrawer] control to
    display as a panel sliding from the end edge of the page.
    """

    floating_action_button: Optional[Control] = None
    """
    A [`FloatingActionButton`][flet.FloatingActionButton]
    control to display on top of Pagelet content.
    """

    floating_action_button_location: Optional[
        Union[FloatingActionButtonLocation, OffsetValue]
    ] = FloatingActionButtonLocation.END_FLOAT
    """
    Defines a position for the `FloatingActionButton`.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Background color of the Pagelet.
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
