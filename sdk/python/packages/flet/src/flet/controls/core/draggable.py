from typing import Optional

from flet.controls.alignment import Axis
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler

__all__ = ["Draggable"]


@control("Draggable")
class Draggable(Control):
    """
    A control that can be dragged from to a [`DragTarget`][flet.].

    When a draggable control recognizes the start of a drag gesture, it displays the
    [`content_feedback`][(c).] control that tracks the user's finger across the screen.
    If the user lifts their finger while on top of a `DragTarget`, this target is
    given the opportunity to complete drag-and-drop flow.
    """

    content: Control
    """
    The control to display when the draggable is not being dragged.

    If the draggable is being dragged, the
    [`content_when_dragging`][(c).] is displayed instead.

    Raises:
        ValueError: If [`content`][(c).] is not visible.
    """

    group: str = "default"
    """
    The group this draggable belongs to.

    Note:
        For a [`DragTarget`][flet.] to accept an incoming drop from a `Draggable`,
        they must both be in the same `group`.
    """

    content_when_dragging: Optional[Control] = None
    """
    The control to display instead of [`content`][(c).] when this draggable
    is being dragged.

    If set, this control visually replaces `content` during an active drag operation,
    allowing you to show a different appearance or an "empty" placeholder.
    If `None`, the original `content` remains visible while dragging.
    """

    content_feedback: Optional[Control] = None
    """
    The control to show under the pointer when a drag is under way.
    """

    axis: Optional[Axis] = None
    """
    Restricts the draggable's movement to a specific axis.

    - `Axis.HORIZONTAL`: Only allows horizontal dragging.
    - `Axis.VERTICAL`: Only allows vertical dragging.
    - `None`: Allows dragging in any direction.
    """

    affinity: Optional[Axis] = None
    """
    Specifies the axis along which this control competes with other gestures to
    initiate a drag.

    - If `None`, the drag starts as soon as a tap down gesture is recognized,
        regardless of direction.
    - If set to `Axis.HORIZONTAL` or `Axis.VERTICAL`, the control will only initiate a
        drag when the gesture matches the specified axis, allowing it to compete
        with other gestures in that direction.
    """

    max_simultaneous_drags: Optional[int] = None
    """
    Specifies how many simultaneous drag operations are allowed for this draggable.

    - `0` - disables dragging entirely.
    - `1` - allows only one drag at a time.
        For a better user experience, you may want to provide an "empty" widget for
        [`content_when_dragging`][(c).]
        to visually indicate the item is being moved.
    - Set to any positive integer to allow that many concurrent drags.
    - If `None`, there is no limit on the number of simultaneous drags.

    Raises:
        ValueError: If [`max_simultaneous_drags`][(c).] is set to a negative value.
    """

    on_drag_start: Optional[ControlEventHandler["Draggable"]] = None
    """
    Called when this draggable starts being dragged.
    """

    on_drag_complete: Optional[ControlEventHandler["Draggable"]] = None
    """
    Called when this draggable is dropped and accepted by a [`DragTarget`][flet.].
    """

    def before_update(self):
        super().before_update()
        if not self.content.visible:
            raise ValueError("content must be visible")
        if self.max_simultaneous_drags is not None and self.max_simultaneous_drags < 0:
            raise ValueError(
                f"max_simultaneous_drags must be greater than or equal to 0, "
                f"got {self.max_simultaneous_drags}"
            )
