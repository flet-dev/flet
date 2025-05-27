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

    To cause a child control to expand and fill the available horizontal space, set its 
    `expand` property.

    Online docs: https://flet.dev/docs/controls/row
    """

    controls: list[Control] = field(default_factory=list)
    alignment: MainAxisAlignment = MainAxisAlignment.START
    vertical_alignment: CrossAxisAlignment = CrossAxisAlignment.CENTER
    spacing: Number = 10
    tight: bool = False
    wrap: bool = False
    run_spacing: Number = 10
    run_alignment: MainAxisAlignment = MainAxisAlignment.START
