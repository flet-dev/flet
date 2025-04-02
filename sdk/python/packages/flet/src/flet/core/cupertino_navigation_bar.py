from dataclasses import field
from typing import List, Optional

from flet.core.border import Border
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import control
from flet.core.navigation_bar import NavigationBarDestination
from flet.core.types import ColorValue, OptionalControlEventCallable, OptionalNumber

__all__ = ["CupertinoNavigationBar"]


@control("CupertinoNavigationBar")
class CupertinoNavigationBar(ConstrainedControl):
    """
    An iOS-styled bottom navigation tab bar.

    Navigation bars offer a persistent and convenient way to switch between primary destinations in an app.

    Example:

    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "CupertinoNavigationBar Example"
        page.navigation_bar = ft.CupertinoNavigationBar(
            bgcolor=ft.colors.AMBER_100,
            inactive_color=ft.colors.GREY,
            active_color=ft.colors.BLACK,
            on_change=lambda e: print("Selected tab:", e.control.selected_index),
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.EXPLORE, label="Explore"),
                ft.NavigationBarDestination(icon=ft.icons.COMMUTE, label="Commute"),
                ft.NavigationBarDestination(
                    icon=ft.icons.BOOKMARK_BORDER,
                    selected_icon=ft.icons.BOOKMARK,
                    label="Explore",
                ),
            ]
        )
        page.add(ft.SafeArea(ft.Text("Body!")))


    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/cupertinonavigationbar
    """

    destinations: List[NavigationBarDestination] = field(default_factory=list)
    selected_index: int = field(default=0)
    bgcolor: Optional[ColorValue] = None
    active_color: Optional[ColorValue] = None
    inactive_color: Optional[ColorValue] = None
    border: Optional[Border] = None
    icon_size: OptionalNumber = None
    on_change: OptionalControlEventCallable = None
