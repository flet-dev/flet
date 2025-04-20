from dataclasses import field
from typing import List

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import OptionalColorValue, OptionalControlEventCallable

__all__ = ["CupertinoSegmentedButton"]


@control("CupertinoSegmentedButton")
class CupertinoSegmentedButton(ConstrainedControl):
    """
    An iOS-style segmented button.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinosegmentedbutton
    """

    controls: List[Control] = field(default_factory=list)
    selected_index: int = 0
    selected_color: OptionalColorValue = None
    unselected_color: OptionalColorValue = None
    border_color: OptionalColorValue = None
    padding: OptionalPaddingValue = None
    click_color: OptionalColorValue = None
    disabled_color: OptionalColorValue = None
    disabled_text_color: OptionalColorValue = None
    on_change: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert (
            len(self.controls) >= 2
        ), "controls must contain minimum two visible controls"
        if not (0 <= self.selected_index < len(self.controls)):
            raise IndexError(
                f"selected_index {self.selected_index} is out of range. "
                f"Expected a value between 0 and {len(self.controls) - 1}."
            )
