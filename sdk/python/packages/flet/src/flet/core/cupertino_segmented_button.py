from dataclasses import field
from typing import List, Optional

from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.types import ColorValue, OptionalControlEventCallable, PaddingValue

__all__ = ["CupertinoSegmentedButton"]


@control("CupertinoSegmentedButton")
class CupertinoSegmentedButton(ConstrainedControl):
    """
    An iOS-style segmented button.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinosegmentedbutton
    """

    controls: List[Control] = field(default_factory=list)
    selected_index: int = field(default=0)
    selected_color: Optional[ColorValue] = None
    unselected_color: Optional[ColorValue] = None
    border_color: Optional[ColorValue] = None
    padding: Optional[PaddingValue] = None
    click_color: Optional[ColorValue] = None
    on_change: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert (
            len(self.controls) >= 2
        ), "CupertinoSegmentedButton must have at minimum two visible controls"
        if not (0 <= self.selected_index < len(self.controls)):
            raise IndexError(
                f"selected_index {self.selected_index} is out of range. "
                f"Expected a value between 0 and {len(self.controls) - 1}."
            )
