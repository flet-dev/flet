from dataclasses import field
from typing import List, Optional

from flet.core.adaptive_control import AdaptiveControl
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.scrollable_control import ScrollableControl
from flet.core.types import (
    CrossAxisAlignment,
    MainAxisAlignment,
    Number,
    OptionalNumber,
)

__all__ = ["Row"]


@control("Row")
class Row(ConstrainedControl, ScrollableControl, AdaptiveControl):
    """
    A control that displays its children in a horizontal array.

    To cause a child control to expand and fill the available horizontal space, set its `expand` property.

    Example:

    ```
    import flet as ft


    def main(page: ft.Page):
        page.title = "Row example"

        page.add(
            ft.Row(
                controls=[
                    ft.Container(
                        expand=1,
                        content=ft.Text("Container 1"),
                        bgcolor=ft.colors.GREEN_100,
                    ),
                    ft.Container(
                        expand=2, content=ft.Text("Container 2"), bgcolor=ft.colors.RED_100
                    ),
                ],
            ),
        ),


    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/row
    """

    controls: List[Control] = field(default_factory=list)
    alignment: MainAxisAlignment = MainAxisAlignment.START
    vertical_alignment: CrossAxisAlignment = CrossAxisAlignment.CENTER
    spacing: Number = 10
    tight: bool = False
    wrap: bool = False
    run_spacing: Number = 10
    run_alignment: MainAxisAlignment = MainAxisAlignment.START
