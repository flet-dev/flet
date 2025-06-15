from dataclasses import field
from typing import Optional

from flet.controls.alignment import Axis
from flet.controls.base_control import control
from flet.controls.buttons import ButtonStyle
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import (
    IconValue,
    IconValueOrControl,
    StrOrControl,
)

__all__ = ["SegmentedButton", "Segment"]


@control("Segment")
class Segment(Control):
    value: str
    """
    Used to identify the `Segment`.
    """

    icon: Optional[IconValueOrControl] = None
    """
    The icon (typically an [`Icon`](https://flet.dev/docs/controls/icon)) to be
    displayed in the segment.
    """

    label: Optional[StrOrControl] = None
    """
    The label (usually a [`Text`](https://flet.dev/docs/controls/text)) to be
    displayed in the segment.
    """

    def before_update(self):
        super().before_update()
        assert (
            (isinstance(self.icon, IconValue))
            or (isinstance(self.icon, Control) and self.icon.visible)
            or (isinstance(self.label, str))
            or (isinstance(self.label, Control) and self.label.visible)
        ), "one of icon or label must be set and visible"


@control("SegmentedButton")
class SegmentedButton(ConstrainedControl):
    """
    A segmented button control.

    Online docs: https://flet.dev/docs/controls/segmentedbutton
    """

    segments: list[Segment]
    """
    A required parameter that describes the segments in the button. It's a list of
    `Segment` objects.
    """

    style: Optional[ButtonStyle] = None
    """
    Customizes this button's appearance.

    Value is of type [`ButtonStyle`](https://flet.dev/docs/reference/types/buttonstyle).
    """

    allow_empty_selection: bool = False
    """
    A boolean value that indicates if having no selected segments is allowed.

    If `True`, then it is acceptable for none of the segments to be selected and also
    that `selected` can be empty.

    If `False` (the default), there must be at least one segment selected. If the user
    taps on the only selected segment it will not be deselected, and `on_change` will
    not be called.
    """

    allow_multiple_selection: bool = False
    """
    A boolean value that indicates if multiple segments can be selected at one time.

    If `True`, more than one segment can be selected. When selecting a segment, the
    other `selected` segments will stay selected. Selecting an already selected segment
    will unselect it.

    If `False`(the default), only one segment may be selected at a time. When a segment
    is selected, any previously selected segment will be unselected.
    """

    selected: list[str] = field(default_factory=list)
    """
    A set of `Segment.value`s that indicate which segments are selected. It is updated
    when the user (un)selects a segment.
    """

    selected_icon: Optional[Control] = None
    """
    An `Icon` control that is used to indicate a segment is selected.

    If `show_selected_icon` is `True` then for `selected` segments this icon will be
    shown before the `Segment.label`, replacing the `Segment.icon` if it is specified.

    Defaults to an `Icon` with the `CHECK` icon.
    """

    show_selected_icon: bool = True
    """
    A boolean value that indicates if the `selected_icon` is displayed on the
    `selected` segments.

    If `True`, the `selected_icon` will be displayed at the start of the `selected`
    segments.

    If `False`, then the `selected_icon` is not used and will not be displayed on
    `selected` segments.
    """

    direction: Optional[Axis] = None
    """
    The orientation of the button's `segments`.

    Value is of type [`Axis`](https://flet.dev/docs/reference/types/axis) and defaults
    to `Axis.HORIZONTAL`.
    """

    padding: OptionalPaddingValue = None
    """
    Defines the button's size and padding. If specified, the button expands to fill its
    parent's space with this padding.

    When `None`, the button adopts its intrinsic content size.

    Value is of type
    [`PaddingValue`](https://flet.dev/docs/reference/types/aliases#paddingvalue).
    """

    on_change: OptionalControlEventHandler["SegmentedButton"] = None
    """
    Fires when the selection changes.
    """

    def before_update(self):
        super().before_update()
        assert any(segment.visible for segment in self.segments), (
            "segments must have at minimum one visible Segment"
        )
        assert len(self.selected) > 0 or self.allow_empty_selection, (
            "allow_empty_selection must be True for selected to be empty"
        )
        assert len(self.selected) < 2 or self.allow_multiple_selection, (
            "allow_multiple_selection must be True for selected to have more than one "
        )
        "item"
        assert len(self.selected) < 2 or self.allow_multiple_selection, (
            "allow_multiple_selection must be True for selected to have more than one "
        )
        "item"
