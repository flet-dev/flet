from typing import List, Optional, Set

from flet.controls.alignment import Axis
from flet.controls.buttons import ButtonStyle
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control, control
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import OptionalControlEventCallable

__all__ = ["SegmentedButton", "Segment"]


@control("Segment")
class Segment(Control):
    value: str
    icon: Optional[Control] = None
    label: Optional[Control] = None


class SegmentedButton(ConstrainedControl):
    """
    A segmented button control.

    -----

    Online docs: https://flet.dev/docs/controls/segmentedbutton
    """

    segments: List[Segment]
    style: Optional[ButtonStyle] = None
    allow_empty_selection: Optional[bool] = None
    allow_multiple_selection: Optional[bool] = None
    selected: Optional[Set] = None
    selected_icon: Optional[Control] = None
    show_selected_icon: Optional[bool] = None
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
        # style = self.__style or ButtonStyle()
        # style.side = self._wrap_attr_dict(style.side)
        # style.shape = self._wrap_attr_dict(style.shape)
        # style.padding = self._wrap_attr_dict(style.padding)

    #
    # # selected
    # @property
    # def selected(self) -> Optional[Set]:
    #     s = self._get_attr("selected")
    #     return set(json.loads(s)) if s else s
    #
    # @selected.setter
    # def selected(self, value: Optional[Set]):
    #     self._set_attr(
    #         "selected",
    #         (
    #             json.dumps(list(value), separators=(",", ":"))
    #             if value is not None
    #             else None
    #         ),
    #     )
