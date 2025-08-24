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

    A root view is automatically created when a new user session started. From layout
    perspective the View represents a [`Column`][flet.Column]
    control, so it has a similar behavior and shares same properties.
    """

    route: Optional[str] = None
    """
    View's route - not currently used by Flet framework, but can be used in a user
    program to update [`Page.route`][flet.Page.route] when a view popped.
    """

    controls: list[BaseControl] = field(default_factory=list)
    """
    A list of controls to display.

    /// details | Example
        type: example
    For example, to add a new control to a page:

    ```python
    page.controls.append(ft.Text("Hello!"))
    page.update()
    ```

    or to get the same result as above using `page.add()` shortcut method:

    ```python
    page.add(ft.Text("Hello!"))
    ```

    To remove the top most control on the page:

    ```python
    page.controls.pop()
    page.update()
    ```
    ///
    """

    appbar: Optional[Union[AppBar, CupertinoAppBar]] = None
    """
    An [`AppBar`][flet.AppBar] control to display at the top of
    the `Page`.
    """

    bottom_appbar: Optional[BottomAppBar] = None
    """
    A [`BottomAppBar`][flet.BottomAppBar] control to display at the bottom of
    the `Page`.
    """

    floating_action_button: Optional[FloatingActionButton] = None
    """
    A [`FloatingActionButton`][flet.FloatingActionButton] control to display on top
    of `Page` content.
    """

    floating_action_button_location: Optional[
        Union[FloatingActionButtonLocation, OffsetValue]
    ] = None
    """
    Describes position of [`floating_action_button`][flet.View.floating_action_button]
    """

    navigation_bar: Union[NavigationBar, CupertinoNavigationBar, None] = None
    """
    A navigation bar ([`NavigationBar`][flet.NavigationBar] or
    [`CupertinoNavigationBar`][flet.CupertinoNavigationBar]) control to display
    at the bottom of the `Page`.
    """

    drawer: Optional[NavigationDrawer] = None
    """
    A [`NavigationDrawer`][flet.NavigationDrawer] control to
    display as a panel sliding from the start edge of the view.
    """

    end_drawer: Optional[NavigationDrawer] = None
    """
    A [`NavigationDrawer`][flet.NavigationDrawer] control to
    display as a panel sliding from the end edge of the view.
    """

    vertical_alignment: MainAxisAlignment = MainAxisAlignment.START
    """
    Defines how the child [`controls`][flet.View.controls] should be placed vertically.
    """

    horizontal_alignment: CrossAxisAlignment = CrossAxisAlignment.START
    """
    How the child Controls should be placed horizontally.
    """

    spacing: Number = 10
    """
    The vertical spacing between [`controls`][flet.View.controls] on the `Page`.

    Note:
        Has effect only when [`vertical_alignment`][flet.View.vertical_alignment]
        is set to
        [`MainAxisAlignment.START`][flet.MainAxisAlignment.START],
        [`MainAxisAlignment.END`][flet.MainAxisAlignment.END],
        or [`MainAxisAlignment.CENTER`][flet.MainAxisAlignment.CENTER].
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

    can_pop: bool = True
    on_confirm_pop: Optional[ControlEventHandler["View"]] = None

    async def confirm_pop(self, should_pop: bool) -> None:
        await self._invoke_method("confirm_pop", {"should_pop": should_pop})

    def init(self):
        super().init()
        self._internals["host_expanded"] = True

    # Magic methods
    def __contains__(self, item: Control) -> bool:
        return item in self.controls
