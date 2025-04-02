from typing import Optional, Union

from flet.core.adaptive_control import AdaptiveControl
from flet.core.app_bar import AppBar
from flet.core.bottom_app_bar import BottomAppBar
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.cupertino_app_bar import CupertinoAppBar
from flet.core.cupertino_navigation_bar import CupertinoNavigationBar
from flet.core.floating_action_button import FloatingActionButton
from flet.core.navigation_bar import NavigationBar
from flet.core.navigation_drawer import NavigationDrawer
from flet.core.types import ColorValue, FloatingActionButtonLocation, OffsetValue

# todo: deprecate show_* in favor of a open/close methods, or page.open/close
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
    bottom_sheet: Optional[Control] = None
    drawer: Optional[NavigationDrawer] = None
    end_drawer: Optional[NavigationDrawer] = None
    floating_action_button: Optional[FloatingActionButton] = None
    floating_action_button_location: Optional[
        Union[FloatingActionButtonLocation, OffsetValue]
    ] = None
    bgcolor: Optional[ColorValue] = None

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"

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
