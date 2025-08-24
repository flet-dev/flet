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
    Container allows to decorate a control with background color and border and
    position it with padding, margin and alignment.
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
    Defines how the [`controls`][flet.Column.controls] should be placed horizontally.
    """

    spacing: Number = 10
    """
    Spacing between the `controls`.

    It is applied only when [`alignment`][flet.Column.alignment] is
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
    Whether the [`controls`][flet.Column.controls] should wrap into additional
    columns (runs) when they don't fit in a single vertical column.
    """

    run_spacing: Number = 10
    """
    The spacing between runs when [`wrap`][flet.Column.wrap] is `True`.
    """

    run_alignment: MainAxisAlignment = MainAxisAlignment.START
    """
    How the runs should be placed in the cross-axis when [`wrap`][flet.Column.wrap]
    is `True`.
    """

    def init(self):
        super().init()
        self._internals["host_expanded"] = True
