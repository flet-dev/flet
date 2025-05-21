from dataclasses import field

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
    Container allows to decorate a control with background color and border and
    position it with padding, margin and alignment.

    Online docs: https://flet.dev/docs/controls/column
    """

    controls: list[Control] = field(default_factory=list)
    """
    A list of Controls to display inside the Column.
    """

    alignment: MainAxisAlignment = MainAxisAlignment.START
    """
    How the child Controls should be placed vertically.

    Value is of type
    [`MainAxisAlignment`](https://flet.dev/docs/reference/types/mainaxisalignment).
    """

    horizontal_alignment: CrossAxisAlignment = CrossAxisAlignment.START
    """
    How the child Controls should be placed horizontally.

    Value is of type
    [`CrossAxisAlignment`](https://flet.dev/docs/reference/types/crossaxisalignment)
    and defaults to `CrossAxisAlignment.START`.
    """

    spacing: Number = 10
    """
    Spacing between the `controls`.

    It is applied only when `alignment` is set to `MainAxisAlignment.START`,
    `MainAxisAlignment.END` or `MainAxisAlignment.CENTER`.

    Default value is `10` virtual pixels.
    """

    tight: bool = False
    """
    Specifies how much space should be occupied vertically.

    Defaults to `False` - allocate all space to children.
    """

    wrap: bool = False
    """
    When set to `True` the Column will put child controls into additional columns
    (runs) if they don't fit a single column.
    """

    run_spacing: Number = 10
    """
    Spacing between runs when `wrap=True`. Default value is 10.
    """

    run_alignment: MainAxisAlignment = MainAxisAlignment.START
    """
    How the runs should be placed in the cross-axis when `wrap=True`.

    Value is of type
    [`MainAxisAlignment`](https://flet.dev/docs/reference/types/mainaxisalignment)
    and defaults to `MainAxisAlignment.START`.
    """
