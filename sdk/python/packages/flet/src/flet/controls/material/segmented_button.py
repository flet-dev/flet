from dataclasses import field
from typing import List, Optional

from flet.controls.alignment import Axis
from flet.controls.base_control import control
from flet.controls.buttons import ButtonStyle
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import OptionalControlEventCallable

__all__ = ["SegmentedButton", "Segment"]


@control("Segment")
class Segment(Control):
    value: str
    icon: Optional[Control] = None
    label: Optional[Control] = None

    def before_update(self):
        super().before_update()
        assert (self.icon is not None and self.icon.visible) or (
            self.label is not None and self.label.visible
        ), "one of icon or label must be set and visible"


@control("SegmentedButton")
class SegmentedButton(ConstrainedControl):
    """
    A segmented button control.

    -----

    Online docs: https://flet.dev/docs/controls/segmentedbutton
    """

    segments: List[Segment]
    style: Optional[ButtonStyle] = None
    allow_empty_selection: bool = False
    allow_multiple_selection: bool = False
    selected: List[str] = field(default_factory=list)
    selected_icon: Optional[Control] = None
    show_selected_icon: bool = True
    direction: Optional[Axis] = None
    padding: OptionalPaddingValue = None
    on_change: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert any(
            segment.visible for segment in self.segments
        ), "segments must have at minimum one visible Segment"
        assert (
            len(self.selected) > 0 or self.allow_empty_selection
        ), "allow_empty_selection must be True for selected to be empty"
        assert (
            len(self.selected) < 2 or self.allow_multiple_selection
        ), "allow_multiple_selection must be True for selected to have more than one item"
