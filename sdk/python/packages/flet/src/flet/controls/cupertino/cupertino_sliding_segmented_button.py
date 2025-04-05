from dataclasses import field
from typing import List

from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control, control
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import OptionalColorValue, OptionalControlEventCallable

__all__ = ["CupertinoSlidingSegmentedButton"]


@control("CupertinoSlidingSegmentedButton")
class CupertinoSlidingSegmentedButton(ConstrainedControl):
    """
    A CupertinoSlidingSegmentedButton.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinoslidingsegmentedbutton
    """

    controls: List[Control] = field(default_factory=list)
    selected_index: int = field(default=0)
    bgcolor: OptionalColorValue = None
    thumb_color: OptionalColorValue = None
    padding: OptionalPaddingValue = None
    proportional_width: bool = False
    on_change: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert len(self.controls) >= 2 and any(
            c.visible for c in self.controls
        ), "controls must have at minimum two visible Controls"
