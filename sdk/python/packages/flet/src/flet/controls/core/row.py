from dataclasses import field

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.layout_control import LayoutControl
from flet.controls.scrollable_control import ScrollableControl
from flet.controls.types import CrossAxisAlignment, MainAxisAlignment, Number

__all__ = ["Row"]


@control("Row")
class Row(LayoutControl, ScrollableControl, AdaptiveControl):
    """
    Displays its children in a horizontal array.

    To cause a child control to expand and fill the available horizontal space, set
    its [`expand`][(c).] property.
    """

    controls: list[Control] = field(default_factory=list)
    """
    A list of Controls to display.
    """

    alignment: MainAxisAlignment = MainAxisAlignment.START
    """
    Defines how the child [`controls`][(c).] should be placed horizontally.
    """

    vertical_alignment: CrossAxisAlignment = CrossAxisAlignment.CENTER
    """
    Defines how the child [`controls`][(c).] should be placed vertically.
    """

    spacing: Number = 10
    """
    The spacing between the child [`controls`][(c).].

    Note:
        Has effect only when [`alignment`][(c).] is set to
        [`MainAxisAlignment.START`][flet.], [`MainAxisAlignment.END`][flet.],
        or [`MainAxisAlignment.CENTER`][flet.].
    """

    tight: bool = False
    """
    Specifies how much space should be occupied horizontally.

    Defaults to `False`, meaning all space is allocated to children.
    """

    wrap: bool = False
    """
    When set to `True` the Row will put child controls into additional rows (runs) if
    they don't fit a single row.
    """

    run_spacing: Number = 10
    """
    Spacing between runs when `wrap=True`.
    """

    run_alignment: MainAxisAlignment = MainAxisAlignment.START
    """
    How the runs should be placed in the cross-axis when `wrap=True`.
    """

    intrinsic_height: bool = False
    """
    If `True`, the Row will be as tall as the tallest child control.
    """

    def init(self):
        super().init()
        self._internals["host_expanded"] = True
