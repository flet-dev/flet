from dataclasses import field
from typing import Any, List, Optional, Sequence, Union

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
    OptionalEventCallable,
    OptionalNumber,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    ScrollMode,
)


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

    controls: Optional[Sequence[Control]] = field(default_factory=list)
    alignment: Optional[MainAxisAlignment] = None
    vertical_alignment: Optional[CrossAxisAlignment] = None
    spacing: OptionalNumber = None
    tight: Optional[bool] = None
    wrap: Optional[bool] = None
    run_spacing: OptionalNumber = None
    run_alignment: Optional[MainAxisAlignment] = None
