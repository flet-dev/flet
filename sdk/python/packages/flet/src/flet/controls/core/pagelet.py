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

    Use it for projects that require "page within a page" layouts with its own AppBar, BottomBar, Drawer, such as demos and galleries.

    Example:
    ```
    import flet as ft


    def main(page: ft.Page):
        page.add(
            ft.Pagelet(
                appbar=ft.CupertinoAppBar(middle=ft.Text("AppBar title")),
                content=ft.Text("This is pagelet"),
            )
        )


    ft.app(target=main)
        ```

        -----

        Online docs: https://flet.dev/docs/controls/pagelet
    """

    content: Control
    appbar: Optional[Union[AppBar, CupertinoAppBar]] = None
    navigation_bar: Optional[Union[NavigationBar, CupertinoNavigationBar]] = None
    bottom_app_bar: Optional[BottomAppBar] = None
    bottom_sheet: OptionalControl = None
    drawer: Optional[NavigationDrawer] = None
    end_drawer: Optional[NavigationDrawer] = None
    floating_action_button: Optional[Control] = None
    floating_action_button_location: Optional[
        Union[FloatingActionButtonLocation, OffsetValue]
    ] = None
    bgcolor: OptionalColorValue = None

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
