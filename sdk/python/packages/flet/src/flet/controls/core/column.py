from dataclasses import field

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.layout_control import LayoutControl
from flet.controls.scrollable_control import ScrollableControl
from flet.controls.types import CrossAxisAlignment, MainAxisAlignment, Number

__all__ = ["Column"]


@control("Column")
class Column(LayoutControl, ScrollableControl, AdaptiveControl):
    """
    Arranges child controls vertically, optionally aligning and spacing them within
    the available space.

    ```python
    ft.Column(
        width=220,
        height=120,
        spacing=12,
        controls=[
            ft.Text("Daily planning", size=20, weight=ft.FontWeight.W_600),
            ft.Text("Review pull requests"),
            ft.Text("Ship release"),
        ],
    )
    ```
    """

    controls: list[Control] = field(default_factory=list)
    """
    A list of controls to display.
    """

    alignment: MainAxisAlignment = MainAxisAlignment.START
    """
    How the child Controls should be placed vertically.
    """

    horizontal_alignment: CrossAxisAlignment = CrossAxisAlignment.START
    """
    Defines how the [`controls`][(c).] should be placed horizontally.
    """

    spacing: Number = 10
    """
    Spacing between the `controls`.

    It is applied only when [`alignment`][(c).] is
    `MainAxisAlignment.START`, `MainAxisAlignment.END` or `MainAxisAlignment.CENTER`.
    """

    tight: bool = False
    """
    Determines how vertical space is allocated.

    If `False` (default), children expand to fill the available vertical space.
    If `True`, only the minimum vertical space required by the children is used.
    """

    wrap: bool = False
    """
    Whether the [`controls`][(c).] should wrap into additional
    columns (runs) when they don't fit in a single vertical column.
    """

    run_spacing: Number = 10
    """
    The spacing between runs when [`wrap`][(c).] is `True`.
    """

    run_alignment: MainAxisAlignment = MainAxisAlignment.START
    """
    How the runs should be placed in the cross-axis when [`wrap`][(c).]
    is `True`.
    """

    intrinsic_width: bool = False
    """
    If `True`, the Column will be as wide as the widest child control.
    """

    def init(self):
        super().init()
        self._internals["host_expanded"] = True
