from typing import Optional

from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.padding import OptionalPaddingValue
from flet.core.types import (
    Number,
    OptionalColorValue,
    OptionalControlEventCallable,
    UrlTarget,
)

__all__ = ["CupertinoListTile"]


@control("CupertinoListTile")
class CupertinoListTile(ConstrainedControl):
    """
    An iOS-style list tile. The CupertinoListTile is a Cupertino equivalent of Material ListTile.

    Example:

    ```
    import flet as ft


    def main(page: ft.Page):
        def tile_clicked(e):
            print("Tile Clicked!")

        page.add(
            ft.CupertinoListTile(
                notched=True,
                additional_info=ft.Text("Wed Jan 25"),
                bgcolor_activated=ft.colors.AMBER_ACCENT,
                leading=ft.Icon(name=ft.cupertino_icons.GAME_CONTROLLER),
                title=ft.Text("CupertinoListTile not notched"),
                subtitle=ft.Text("Subtitle"),
                trailing=ft.Icon(name=ft.cupertino_icons.ALARM),
                on_click=tile_clicked,
            ),

        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/cupertinolisttile
    """

    title: Optional[Control] = None
    subtitle: Optional[Control] = None
    leading: Optional[Control] = None
    trailing: Optional[Control] = None
    bgcolor: OptionalColorValue = None
    bgcolor_activated: Optional[str] = None
    padding: OptionalPaddingValue = None
    url: Optional[str] = None
    url_target: Optional[UrlTarget] = None
    toggle_inputs: bool = False
    additional_info: Optional[Control] = None
    leading_size: Number = 30.0
    leading_to_title: Number = 12.0
    notched: bool = False
    on_click: OptionalControlEventCallable = None
