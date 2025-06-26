import asyncio
from dataclasses import field
from typing import Optional, Union

from flet.controls.base_control import BaseControl, control
from flet.controls.box import BoxDecoration
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import OptionalControlEventHandler
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
    Number,
    OptionalColorValue,
)

__all__ = ["View"]


@control("View")
class View(ScrollableControl, ConstrainedControl):
    """
    View is the top most container for all other controls.

    A root view is automatically created when a new user session started. From layout
    perspective the View represents a `Column`(https://flet.dev/docs/controls/column/)
    control, so it has a similar behavior and shares same properties.

    Online docs: https://flet.dev/docs/controls/view
    """

    route: Optional[str] = None
    """
    View's route - not currently used by Flet framework, but can be used in a user 
    program to update [`page.route`](https://flet.dev/docs/controls/page#route) when a 
    view popped.
    """

    controls: list[BaseControl] = field(default_factory=list)
    """
    A list of `Control`s to display on the Page.

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

    Value is of a list of `Control`s.
    """

    appbar: Optional[Union[AppBar, CupertinoAppBar]] = None
    """
    A [`AppBar`](https://flet.dev/docs/controls/appbar) control to display at the top of
    the Page.
    """

    bottom_appbar: Optional[BottomAppBar] = None
    """
    TBD
    """

    floating_action_button: Optional[FloatingActionButton] = None
    """
    A [`FloatingActionButton`](https://flet.dev/docs/controls/floatingactionbutton)
    control to display on top of Page content.
    """

    floating_action_button_location: Optional[
        Union[FloatingActionButtonLocation, OffsetValue]
    ] = None
    """
    Describes position of [`floating_action_button`](#floating_action_button)

    Value is of type [`FloatingActionButtonLocation`](https://flet.dev/docs/controls/
    floatingactionbutton)
    """

    navigation_bar: Union[NavigationBar, CupertinoNavigationBar, None] = None
    """
    TBD
    """

    drawer: Optional[NavigationDrawer] = None
    """
    A [`NavigationDrawer`](https://flet.dev/docs/controls/navigationdrawer) control to
    display as a panel sliding from the start edge of the view.
    """

    end_drawer: Optional[NavigationDrawer] = None
    """
    A [`NavigationDrawer`](https://flet.dev/docs/controls/navigationdrawer) control to
    display as a panel sliding from the end edge of the view.
    """

    vertical_alignment: Optional[MainAxisAlignment] = None
    """
    How the child Controls should be placed vertically.

    Value is of type [`MainAxisAlignment`](https://flet.dev/docs/reference/types/
    mainaxisalignment) and defaults to `MainAxisAlignment.START`.
    """

    horizontal_alignment: Optional[CrossAxisAlignment] = None
    """
    How the child Controls should be placed horizontally.

    Value is of type [`CrossAxisAlignment`](https://flet.dev/docs/reference/types/
    crossaxisalignment) and defaults to `CrossAxisAlignment.START`.
    """

    spacing: Number = 10
    """
    Vertical spacing between controls on the Page. Default value is 10 virtual pixels.
    Spacing is applied only when `vertical_alignment` is set to 
    `MainAxisAlignment.START`, `MainAxisAlignment.END` or `MainAxisAlignment.CENTER`.

    Value is of type `Number` and defaults to `10`
    """

    padding: OptionalPaddingValue = None
    """
    A space between page contents and its edges.

    Value is of type [`PaddingValue`](https://flet.dev/docs/reference/types/aliases#
    paddingvalue) and defaults to `padding.all(10)`.
    """

    bgcolor: OptionalColorValue = None
    """
    Background [color](https://flet.dev/docs/reference/colors) of the view.
    """

    decoration: Optional[BoxDecoration] = None
    """
    The background decoration.

    Value is of type [`BoxDecoration`](https://flet.dev/docs/reference/types/
    boxdecoration).
    """

    foreground_decoration: Optional[BoxDecoration] = None
    """
    The foreground decoration.

    Value is of type [`BoxDecoration`](https://flet.dev/docs/reference/types/
    boxdecoration).
    """

    can_pop: bool = True
    on_confirm_pop: OptionalControlEventHandler["View"] = None

    def confirm_pop(self, should_pop: bool) -> None:
        asyncio.create_task(self.confirm_pop_async(should_pop))

    async def confirm_pop_async(self, should_pop: bool) -> None:
        await self._invoke_method_async("confirm_pop", {"should_pop": should_pop})

    # Magic methods
    def __contains__(self, item: Control) -> bool:
        return item in self.controls
