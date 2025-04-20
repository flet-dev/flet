from typing import Optional

from flet.controls.base_control import control
from flet.controls.border import Border
from flet.controls.control import Control
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import Brightness, OptionalColorValue

__all__ = ["CupertinoAppBar"]


@control("CupertinoAppBar")
class CupertinoAppBar(Control):
    """
    An iOS-styled application bar.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.theme_mode = ft.ThemeMode.LIGHT

        page.appbar = ft.CupertinoAppBar(
            leading=ft.Icon(ft.icons.PALETTE),
            bgcolor=ft.colors.SURFACE_VARIANT,
            trailing=ft.Icon(ft.icons.WB_SUNNY_OUTLINED),
            middle=ft.Text("AppBar Example"),
        )
        page.add(ft.Text("Body!"))


    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/cupertinoappbar
    """

    leading: Optional[Control] = None
    middle: Optional[Control] = None
    title: Optional[Control] = None
    trailing: Optional[Control] = None
    bgcolor: OptionalColorValue = None
    automatically_imply_leading: Optional[bool] = None
    automatically_imply_middle: Optional[bool] = None
    automatically_imply_title: Optional[bool] = None
    border: Optional[Border] = None
    padding: OptionalPaddingValue = None
    transition_between_routes: Optional[bool] = None
    previous_page_title: Optional[str] = None
    brightness: Optional[Brightness] = None
    automatic_background_visibility: Optional[bool] = None
    enable_background_filter_blur: Optional[bool] = None
    large: Optional[bool] = None
