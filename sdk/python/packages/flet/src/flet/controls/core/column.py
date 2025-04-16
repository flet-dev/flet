from dataclasses import field
from typing import List

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.scrollable_control import ScrollableControl
from flet.controls.types import CrossAxisAlignment, MainAxisAlignment, Number

__all__ = ["Column"]


@control("Column")
class Column(ConstrainedControl, ScrollableControl, AdaptiveControl):
    """
    Container allows to decorate a control with background color and border and position it with padding, margin and alignment.

    Example:

    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "Column example"

        page.add(
            ft.Column(
                expand=True,
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

    Online docs: https://flet.dev/docs/controls/column
    """

    controls: List[Control] = field(default_factory=list)
    alignment: MainAxisAlignment = MainAxisAlignment.START
    horizontal_alignment: CrossAxisAlignment = CrossAxisAlignment.START
    spacing: Number = 10
    tight: bool = False
    wrap: bool = False
    run_spacing: Number = 0
    run_alignment: MainAxisAlignment = MainAxisAlignment.START
