from dataclasses import field
from enum import Enum
from typing import List, Optional

from flet.core.buttons import OutlinedBorder
from flet.core.control import Control, control
from flet.core.types import (
    ColorValue,
    IconValueOrControl,
    OptionalControlEventCallable,
    OptionalNumber,
    PaddingValue,
)


@control("NavigationDrawerDestination")
class NavigationDrawerDestination(Control):
    """Displays an icon with a label, for use in NavigationDrawer destinations."""

    label: Optional[str] = None
    icon: Optional[IconValueOrControl] = None
    selected_icon: Optional[IconValueOrControl] = None
    bgcolor: Optional[ColorValue] = None


class NavigationDrawerPosition(Enum):
    START = "start"
    END = "end"


@control("NavigationDrawer")
class NavigationDrawer(Control):
    """
    Material Design Navigation Drawer component.

    Navigation Drawer is a panel slides in horizontally from the left or right edge of a page to show primary destinations in an app.

    Example:

    ```
    import flet as ft


    def main(page: ft.Page):
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        def handle_dismissal(e):
            page.add(ft.Text("Drawer dismissed"))

        def handle_change(e):
            page.add(ft.Text(f"Selected Index changed: {e.selected_index}"))
            # page.close(drawer)

        drawer = ft.NavigationDrawer(
            on_dismiss=handle_dismissal,
            on_change=handle_change,
            controls=[
                ft.Container(height=12),
                ft.NavigationDrawerDestination(
                    label="Item 1",
                    icon=ft.icons.DOOR_BACK_DOOR_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.DOOR_BACK_DOOR),
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.icons.MAIL_OUTLINED),
                    label="Item 2",
                    selected_icon=ft.icons.MAIL,
                ),
                ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.icons.PHONE_OUTLINED),
                    label="Item 3",
                    selected_icon=ft.icons.PHONE,
                ),
            ],
        )

        page.add(ft.ElevatedButton("Show drawer", on_click=lambda e: page.open(drawer)))


    ft.app(main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/navigationdrawer
    """

    controls: List[Control] = field(default_factory=list)
    open: bool = field(default=False)
    selected_index: int = field(default=0)
    bgcolor: Optional[ColorValue] = None
    elevation: OptionalNumber = None
    indicator_color: Optional[ColorValue] = None
    indicator_shape: Optional[OutlinedBorder] = None
    shadow_color: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    tile_padding: Optional[PaddingValue] = None
    position: NavigationDrawerPosition = field(default=NavigationDrawerPosition.START)
    on_change: OptionalControlEventCallable = None
    on_dismiss: OptionalControlEventCallable = None
