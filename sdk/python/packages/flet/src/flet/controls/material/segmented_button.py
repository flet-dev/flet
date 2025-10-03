from dataclasses import field
from typing import Optional

from flet.controls.alignment import Axis
from flet.controls.base_control import control
from flet.controls.buttons import ButtonStyle
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.layout_control import LayoutControl
from flet.controls.padding import PaddingValue
from flet.controls.types import (
    IconData,
    IconDataOrControl,
    StrOrControl,
)

__all__ = ["Segment", "SegmentedButton"]


@control("Segment")
class Segment(Control):
    """
    A segment for a [`SegmentedButton`][flet.].
    """

    value: str
    """
    Used to identify the `Segment`.
    """

    icon: Optional[IconDataOrControl] = None
    """
    The icon (typically an [`Icon`][flet.]) to be
    displayed in the segment.
    """

    label: Optional[StrOrControl] = None
    """
    The label (usually a [`Text`][flet.]) to be
    displayed in the segment.

    Raises:
        ValueError: If neither [`icon`][(c).] nor [`label`][(c).] is set.
    """

    def before_update(self):
        super().before_update()
        if not (
            (isinstance(self.icon, IconData))
            or (isinstance(self.icon, Control) and self.icon.visible)
            or (isinstance(self.label, str))
            or (isinstance(self.label, Control) and self.label.visible)
        ):
            raise ValueError("one of icon or label must be set and visible")


@control("SegmentedButton")
class SegmentedButton(LayoutControl):
    """
    A segmented button control.
    """

    segments: list[Segment]
    """
    The segments of this button.

    Raises:
        ValueError: If [`segments`][(c).] is empty or does not have at least one
            visible `Segment`.
    """

    style: Optional[ButtonStyle] = None
    """
    Customizes this button's appearance.
    """

    allow_empty_selection: bool = False
    """
    A boolean value that indicates if having no selected segments is allowed.

    If `True`, then it is acceptable for none of the segments to be selected and also
    that `selected` can be empty.

    If `False` (the default), there must be at least one segment selected. If the user
    taps on the only selected segment it will not be deselected, and `on_change` will
    not be called.

    Raises:
        ValueError: If [`selected`][(c).] is empty while
            [`allow_empty_selection`][(c).] is `False`.
    """

    allow_multiple_selection: bool = False
    """
    A boolean value that indicates if multiple segments can be selected at one time.

    If `True`, more than one segment can be selected. When selecting a segment, the
    other `selected` segments will stay selected. Selecting an already selected segment
    will unselect it.

    If `False` (the default), only one segment may be selected at a time. When a segment
    is selected, any previously selected segment will be unselected.

    Raises:
        ValueError: If [`selected`][(c).] has more than one item while
            [`allow_multiple_selection`][(c).] is `False`.
    """

    selected: list[str] = field(default_factory=list)
    """
    A set of `Segment.value`s that indicate which segments are selected. It is updated
    when the user (un)selects a segment.

    Raises:
        ValueError: If [`selected`][(c).] violates the constraints defined by
            [`allow_empty_selection`][(c).] or
            [`allow_multiple_selection`][(c).].
    """

    selected_icon: Optional[IconDataOrControl] = None
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

    Defaults
    to `Axis.HORIZONTAL`.
    """

    padding: Optional[PaddingValue] = None
    """
    Defines the button's size and padding. If specified, the button expands to fill its
    parent's space with this padding.

    When `None`, the button adopts its intrinsic content size.
    """

    on_change: Optional[ControlEventHandler["SegmentedButton"]] = None
    """
    Called when the selection changes.

    The [`data`][flet.Event.] property of the event handler argument
    contains a list of strings identifying the selected segments.
    """

    def before_update(self):
        super().before_update()
        if not any(segment.visible for segment in self.segments):
            raise ValueError("segments must have at minimum one visible Segment")
        if len(self.selected) == 0 and not self.allow_empty_selection:
            raise ValueError(
                "allow_empty_selection must be True for selected to be empty"
            )
        if len(self.selected) >= 2 and not self.allow_multiple_selection:
            raise ValueError(
                "allow_multiple_selection must be True for selected to "
                "have more than one item"
            )
