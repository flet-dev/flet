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
    alignment: MainAxisAlignment = MainAxisAlignment.START
    horizontal_alignment: CrossAxisAlignment = CrossAxisAlignment.START
    spacing: Number = 10
    tight: bool = False
    wrap: bool = False
    run_spacing: Number = 0
    run_alignment: MainAxisAlignment = MainAxisAlignment.START
