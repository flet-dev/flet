from dataclasses import field
from typing import Annotated, Optional

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
from flet.utils.validation import V, ValidationRules

__all__ = ["Segment", "SegmentedButton"]


@control("Segment")
class Segment(Control):
    """
    A segment for a :class:`~flet.SegmentedButton`.
    """

    value: str
    """
    Used to identify this segment.
    """

    icon: Optional[IconDataOrControl] = None
    """
    The icon to be displayed in the segment.

    Typically an :class:`~flet.Icon`.

    Raises:
        ValueError: If neither it nor :attr:`label` is set and visible.
    """

    label: Optional[StrOrControl] = None
    """
    The label (usually a :class:`~flet.Text`) to be displayed in the segment.

    Raises:
        ValueError: If neither it nor :attr:`icon` is set and visible.
    """

    __validation_rules__: ValidationRules = (
        V.ensure(
            lambda ctrl: (
                (
                    isinstance(ctrl.icon, IconData)
                    or (isinstance(ctrl.icon, Control) and ctrl.icon.visible)
                )
                or (
                    isinstance(ctrl.label, str)
                    or (isinstance(ctrl.label, Control) and ctrl.label.visible)
                )
            ),
            message="at least icon or label must be set and visible",
        ),
    )


@control("SegmentedButton")
class SegmentedButton(LayoutControl):
    """
    A segmented button control.
    """

    segments: Annotated[
        list[Segment],
        V.visible_controls(min_count=1),
    ]
    """
    The segments of this button.

    Raises:
        ValueError: If it does not contain at least one visible `Segment`.
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
        ValueError: If :attr:`selected` is empty while
            :attr:`allow_empty_selection` is `False`.
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
        ValueError: If :attr:`selected` has more than one item while
            :attr:`allow_multiple_selection` is `False`.
    """

    selected: list[str] = field(default_factory=list)
    """
    A set of `Segment.value`s that indicate which segments are selected. It is updated \
    when the user (un)selects a segment.

    Raises:
        ValueError: If :attr:`selected` violates the constraints defined by
            :attr:`allow_empty_selection` or
            :attr:`allow_multiple_selection`.
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
    A boolean value that indicates if the `selected_icon` is displayed on the \
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
    Defines the button's size and padding. If specified, the button expands to fill \
    its parent's space with this padding.

    When `None`, the button adopts its intrinsic content size.
    """

    on_change: Optional[ControlEventHandler["SegmentedButton"]] = None
    """
    Called when the selection changes.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains a list of strings identifying the selected segments.
    """

    __validation_rules__: ValidationRules = (
        V.ensure(
            lambda ctrl: len(ctrl.selected) > 0 or ctrl.allow_empty_selection,
            message="allow_empty_selection must be True for selected to be empty",
        ),
        V.ensure(
            lambda ctrl: len(ctrl.selected) < 2 or ctrl.allow_multiple_selection,
            message=(
                "allow_multiple_selection must be True for selected to "
                "have more than one item"
            ),
        ),
    )
