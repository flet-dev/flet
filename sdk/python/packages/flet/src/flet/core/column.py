from dataclasses import field
from typing import Any, Callable, List, Optional, Sequence, Union

from flet.core.adaptive_control import AdaptiveControl
from flet.core.animation import AnimationValue
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.ref import Ref
from flet.core.scrollable_control import OnScrollEvent, ScrollableControl
from flet.core.types import (
    CrossAxisAlignment,
    MainAxisAlignment,
    OffsetValue,
    OptionalControlEventCallable,
    OptionalNumber,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    ScrollMode,
)


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
    alignment: Optional[MainAxisAlignment] = field(default=MainAxisAlignment.START)
    horizontal_alignment: Optional[CrossAxisAlignment] = field(
        default=CrossAxisAlignment.START
    )
    spacing: OptionalNumber = field(default=10)
    tight: Optional[bool] = field(default=False)
    wrap: Optional[bool] = field(default=False)
    run_spacing: OptionalNumber = field(default=0)
    run_alignment: Optional[MainAxisAlignment] = field(default=MainAxisAlignment.START)
