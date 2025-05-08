from dataclasses import field

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.cupertino.cupertino_colors import CupertinoColors
from flet.controls.padding import Padding, PaddingValue
from flet.controls.types import (
    ColorValue,
    OptionalColorValue,
    OptionalControlEventCallable,
)

__all__ = ["CupertinoSlidingSegmentedButton"]


@control("CupertinoSlidingSegmentedButton")
class CupertinoSlidingSegmentedButton(ConstrainedControl):
    """
    A CupertinoSlidingSegmentedButton.

    Online docs: https://flet.dev/docs/controls/cupertinoslidingsegmentedbutton
    """

    controls: list[Control] = field(default_factory=list)
    selected_index: int = 0
    bgcolor: ColorValue = CupertinoColors.TERTIARY_SYSTEM_FILL
    thumb_color: OptionalColorValue = None
    padding: PaddingValue = field(
        default_factory=lambda: Padding.symmetric(vertical=2, horizontal=3)
    )
    proportional_width: bool = False
    on_change: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert (
            sum(c.visible for c in self.controls) >= 2
        ), "controls must have at minimum two visible Controls"
