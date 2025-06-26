from dataclasses import field

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.scrollable_control import ScrollableControl
from flet.controls.types import CrossAxisAlignment, MainAxisAlignment, Number

__all__ = ["Row"]


@control("Row")
class Row(ConstrainedControl, ScrollableControl, AdaptiveControl):
    """
    A control that displays its children in a horizontal array.

    To cause a child control to expand and fill the available horizontal space, set
    its `expand` property.

    Online docs: https://flet.dev/docs/controls/row
    """

    controls: list[Control] = field(default_factory=list)
    """
    A list of Controls to display inside the Row.
    """

    alignment: MainAxisAlignment = MainAxisAlignment.START
    """
    How the child Controls should be placed horizontally.

    Value is of type
    [`MainAxisAlignment`](https://flet.dev/docs/reference/types/mainaxisalignment)
    and defaults to `MainAxisAlignment.START`.
    """

    vertical_alignment: CrossAxisAlignment = CrossAxisAlignment.CENTER
    """
    How the child Controls should be placed vertically.

    Value is of type
    [`CrossAxisAlignment`](https://flet.dev/docs/reference/types/crossaxisalignment)
    and defaults to `CrossAxisAlignment.START`.
    """

    spacing: Number = 10
    """
    Spacing between controls in a row.

    Default value is `10` virtual pixels. Spacing is applied only when `alignment` is
    set to `MainAxisAlignment.START`, `MainAxisAlignment.END` or 
    `MainAxisAlignment.CENTER`.
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

    Defaults to `10`.
    """

    run_alignment: MainAxisAlignment = MainAxisAlignment.START
    """
    How the runs should be placed in the cross-axis when `wrap=True`.

    Value is of type
    [`MainAxisAlignment`](https://flet.dev/docs/reference/types/mainaxisalignment)
    and defaults to `MainAxisAlignment.START`.
    """
