from typing import Annotated, Optional, Union

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
from flet.utils.validation import V

__all__ = ["Pagelet"]


@control("Pagelet")
class Pagelet(LayoutControl, AdaptiveControl):
    """
    Implements the basic Material Design visual layout structure.

    Use it for projects that require a "page within a page" layouts with its own
    :class:`~flet.AppBar`, :class:`~flet.BottomAppBar`, :class:`~flet.NavigationDrawer`,
    such as demos and galleries.
    """

    content: Annotated[
        Control,
        V.visible_control(),
    ]
    """
    A child Control contained by this Pagelet.

    The control in the content of the Pagelet is positioned at the top-left of the
    available space between the app bar and the bottom of the Pagelet.

    Raises:
        ValueError: If it is not visible.
    """

    appbar: Optional[Union[AppBar, CupertinoAppBar]] = None
    """
    An :class:`~flet.AppBar` control to display at the top of the Pagelet.
    """

    navigation_bar: Optional[Union[NavigationBar, CupertinoNavigationBar]] = None
    """
    A navigation bar (:class:`~flet.NavigationBar` or \
    :class:`~flet.CupertinoNavigationBar`) control to display at the bottom of the \
    `Pagelet`.

    Note:
        If both the `navigation_bar` and :attr:`bottom_appbar`
        properties are specified, `navigation_bar` takes precedence and will
        be displayed.
    """

    bottom_appbar: Optional[BottomAppBar] = None
    """
    A :class:`~flet.BottomAppBar` control to display at the bottom of this Pagelet.

    Note:
        If both the `bottom_appbar` and :attr:`navigation_bar`
        properties are specified, `bottom_appbar` takes precedence and will
        be displayed.
    """

    bottom_sheet: Optional[Control] = None
    """
    The persistent bottom sheet to show information that supplements the primary \
    content of this Pagelet.
    """

    drawer: Optional[NavigationDrawer] = None
    """
    A :class:`~flet.NavigationDrawer` control to display as a panel sliding from the \
    start edge of the page.
    """

    end_drawer: Optional[NavigationDrawer] = None
    """
    A :class:`~flet.NavigationDrawer` control to display as a panel sliding from the \
    end edge of the page.
    """

    floating_action_button: Optional[Control] = None
    """
    A :class:`~flet.FloatingActionButton`
    control to display on top of this Pagelet's content.
    """

    floating_action_button_location: Optional[
        Union[FloatingActionButtonLocation, OffsetValue]
    ] = FloatingActionButtonLocation.END_FLOAT
    """
    Defines the position of the :attr:`floating_action_button`.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Background color of this Pagelet.
    """

    async def show_drawer(self):
        """
        Show the drawer.

        Raises:
            ValueError: If no :attr:`drawer` is defined.
        """
        if self.drawer is None:
            raise ValueError("No drawer defined")
        await self._invoke_method("show_drawer")

    async def close_drawer(self):
        """
        Close the drawer.
        """
        await self._invoke_method("close_drawer")

    async def show_end_drawer(self):
        """
        Show the end drawer.

        Raises:
            ValueError: If no :attr:`end_drawer` is defined.
        """
        if self.end_drawer is None:
            raise ValueError("No end_drawer defined")
        await self._invoke_method("show_end_drawer")

    async def close_end_drawer(self):
        """
        Close the end drawer.
        """
        await self._invoke_method("close_end_drawer")
