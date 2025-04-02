from dataclasses import field
from typing import List, Optional

from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.types import ColorValue, OptionalControlEventCallable, PaddingValue

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
    bgcolor: Optional[ColorValue] = None
    thumb_color: Optional[ColorValue] = None
    padding: Optional[PaddingValue] = None
    on_change: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert len(self.controls) >= 2 and any(
            c.visible for c in self.controls
        ), "controls must have at minimum two visible Controls"
