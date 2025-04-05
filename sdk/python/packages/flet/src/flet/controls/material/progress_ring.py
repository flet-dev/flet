from typing import Optional

from flet.controls.box import BoxConstraints
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import control
from flet.controls.padding import PaddingValue
from flet.controls.types import Number, OptionalColorValue, OptionalNumber, StrokeCap

__all__ = ["ProgressRing"]


@control("ProgressRing")
class ProgressRing(ConstrainedControl):
    """
    A material design circular progress indicator, which spins to indicate that the application is busy.

    A control that shows progress along a circle.

    Example:

    ```
    from time import sleep
    import flet as ft

    def main(page: ft.Page):
        pr = ft.ProgressRing(width=16, height=16, stroke_width = 2)

        page.add(
            ft.Text("Circular progress indicator", style="headlineSmall"),
            ft.Row([pr, ft.Text("Wait for the completion...")]),
            ft.Text("Indeterminate circular progress", style="headlineSmall"),
            ft.Column(
                [ft.ProgressRing(), ft.Text("I'm going to run for ages...")],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        for i in range(0, 101):
            pr.value = i * 0.01
            sleep(0.1)
            page.update()

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/progressring
    """

    value: OptionalNumber = None
    stroke_width: Number = 4.0
    color: OptionalColorValue = None
    bgcolor: OptionalColorValue = None
    stroke_align: Number = 0.0
    stroke_cap: Optional[StrokeCap] = None
    semantics_label: Optional[str] = None
    semantics_value: OptionalNumber = None
    track_gap: OptionalNumber = None
    size_constraints: Optional[BoxConstraints] = None
    padding: Optional[PaddingValue] = None
    year_2023: Optional[bool] = None
