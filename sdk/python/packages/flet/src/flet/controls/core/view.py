from dataclasses import field
from typing import Optional, Union

from flet.controls.base_control import BaseControl, control
from flet.controls.box import BoxDecoration
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.cupertino.cupertino_app_bar import CupertinoAppBar
from flet.controls.cupertino.cupertino_navigation_bar import CupertinoNavigationBar
from flet.controls.layout_control import LayoutControl
from flet.controls.material.app_bar import AppBar
from flet.controls.material.bottom_app_bar import BottomAppBar
from flet.controls.material.floating_action_button import FloatingActionButton
from flet.controls.material.navigation_bar import NavigationBar
from flet.controls.material.navigation_drawer import NavigationDrawer
from flet.controls.padding import Padding, PaddingValue
from flet.controls.scrollable_control import ScrollableControl
from flet.controls.services.service import Service
from flet.controls.transform import OffsetValue
from flet.controls.types import (
    ColorValue,
    CrossAxisAlignment,
    FloatingActionButtonLocation,
    MainAxisAlignment,
    Number,
)

__all__ = ["View"]


@control("View")
class View(ScrollableControl, LayoutControl):
    """
    View is the top most container for all other controls.

    A root view is automatically created when a new user session started.
    From layout perspective the View represents a :class:`~flet.Column`
    control, so it has a similar behavior and shares same properties.
    """

    controls: list[BaseControl] = field(default_factory=list)
    """
    A list of controls to display.
    """

    route: str = field(default_factory=lambda: "/")
    """
    View's route - not currently used by Flet framework, but can be used in a user \
    program to update :attr:`flet.Page.route` when a view popped.
    """

    appbar: Optional[Union[AppBar, CupertinoAppBar]] = None
    """
    An :class:`~flet.AppBar` control to display at the top of the `Page`.
    """

    bottom_appbar: Optional[BottomAppBar] = None
    """
    A :class:`~flet.BottomAppBar` control to display at the bottom of the `Page`.
    """

    floating_action_button: Optional[FloatingActionButton] = None
    """
    A :class:`~flet.FloatingActionButton` control to display on top of `Page` content.
    """

    floating_action_button_location: Optional[
        Union[FloatingActionButtonLocation, OffsetValue]
    ] = None
    """
    Describes position of :attr:`floating_action_button`
    """

    navigation_bar: Union[NavigationBar, CupertinoNavigationBar, None] = None
    """
    A navigation bar (:class:`~flet.NavigationBar` or \
    :class:`~flet.CupertinoNavigationBar`) control to display at the bottom of the \
    `Page`.
    """

    drawer: Optional[NavigationDrawer] = None
    """
    A :class:`~flet.NavigationDrawer` control to display as a panel sliding from the \
    start edge of the view.
    """

    end_drawer: Optional[NavigationDrawer] = None
    """
    A :class:`~flet.NavigationDrawer` control to display as a panel sliding from the \
    end edge of the view.
    """

    vertical_alignment: MainAxisAlignment = MainAxisAlignment.START
    """
    Defines how the child :attr:`controls` should be placed vertically.
    """

    horizontal_alignment: CrossAxisAlignment = CrossAxisAlignment.START
    """
    How the child Controls should be placed horizontally.
    """

    spacing: Number = 10
    """
    The vertical spacing between :attr:`controls` on the `Page`.

    Note:
        Has effect only when :attr:`vertical_alignment`
        is set to :attr:`flet.MainAxisAlignment.START`,
        :attr:`flet.MainAxisAlignment.END`, or :attr:`flet.MainAxisAlignment.CENTER`.
    """

    padding: Optional[PaddingValue] = field(default_factory=lambda: Padding.all(10))
    """
    A space between page contents and its edges.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Background color of the view.
    """

    decoration: Optional[BoxDecoration] = None
    """
    The background decoration.
    """

    foreground_decoration: Optional[BoxDecoration] = None
    """
    The foreground decoration.
    """

    fullscreen_dialog: bool = False
    """
    If `True`, the view is a fullscreen modal dialog.
    """

    services: list[Service] = field(default_factory=list, metadata={"skip": True})
    """
    A list of :class:`~flet.Service` controls associated with this view.
    """

    can_pop: bool = True
    """
    Whether the view can be popped.
    """

    on_confirm_pop: Optional[ControlEventHandler["View"]] = None
    """
    An event handler that is called when the view is about to be popped.
    You can use this event to confirm or cancel the pop action by calling
    :meth:`confirm_pop` method.
    """

    def init(self):
        super().init()
        self._internals["host_expanded"] = True

    # Magic methods
    def __contains__(self, item: Control) -> bool:
        return item in self.controls

    async def confirm_pop(self, should_pop: bool) -> None:
        """
        Resolves a pending pop-confirmation request for this view.

        Call this from :attr:`on_confirm_pop` to allow or cancel the current
        back-navigation attempt.

        Args:
            should_pop: `True` to proceed with popping this view, `False` to
                keep the view on the navigation stack.

        Notes:
            - This method only has effect while a pop confirmation is pending.
            - If not called, the frontend confirmation wait times out and the
                pop is canceled.
        """
        await self._invoke_method("confirm_pop", {"should_pop": should_pop})

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
