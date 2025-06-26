from typing import Optional

from flet.controls.alignment import Axis
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import OptionalControlEventHandler

__all__ = ["Draggable"]


@control("Draggable")
class Draggable(Control):
    """
    A control that can be dragged from to a `DragTarget`.

    When a draggable control recognizes the start of a drag gesture, it displays a
    `content_feedback` control that tracks the user's finger across the screen. If the
    user lifts their finger while on top of a `DragTarget`, that target is given the
    opportunity to complete drag-and-drop flow.

    Online docs: https://flet.dev/docs/controls/draggable
    """

    content: Control
    """
    `Draggable` control displays [`content`](#content) when zero drags are under way.

    If [`content_when_dragging`](#content_when_dragging) is not `None`, this control
    instead displays `content_when_dragging` when one or more drags are underway.
    Otherwise, this control always displays `content`.
    """

    group: str = "default"
    """
    A group this draggable belongs to.

    For [`DragTarget`](https://flet.dev/docs/controls/dragtarget) to accept incoming 
    drag both `Draggable` and `DragTarget` must be in the same `group`.
    """

    content_when_dragging: Optional[Control] = None
    """
    The `Control` to display instead of `content` when one or more drags are under way.

    If this is `None`, then this widget will always display `content` (and so the drag
    source representation will not change while a drag is under way).
    """

    content_feedback: Optional[Control] = None
    """
    The `Control` to show under the pointer when a drag is under way.
    """

    axis: Optional[Axis] = None
    """
    The axis to restrict this draggable's movement.

    When axis is set to `Axis.HORIZONTAL`, this control can only be dragged 
    horizontally. When axis is set to `Axis.VERTICAL`, this control can only be dragged 
    vertically.

    Value is of type [`Axis`](https://flet.dev/docs/reference/types/axis) and defaults
    to `None` - no restriction.
    """

    affinity: Optional[Axis] = None
    """
    Controls how this control competes with other gestures to initiate a drag.

    If set to `None`, this widget initiates a drag as soon as it recognizes a tap down
    gesture, regardless of any directionality.

    If set to `Axis.HORIZONTAL` or `Axis.VERTICAL`, then this control will compete with
    other horizontal (or vertical, respectively) gestures.

    Value is of type [`Axis`](https://flet.dev/docs/reference/types/axis).
    """

    max_simultaneous_drags: Optional[int] = None
    """
    The number of simultaneous drags to support.

    - Set this to `0` if you want to prevent the draggable from actually being dragged.
    - Set this to `1` if you want to only allow the drag source to have one item dragged
      at a time. In this case, consider supplying an "empty" widget for
      `content_when_dragging` to create the illusion of actually moving `content`.

    Defaults to `None` - no limit.
    """

    on_drag_start: OptionalControlEventHandler["Draggable"] = None
    """
    Fires when this draggable starts being dragged.
    """

    on_drag_complete: OptionalControlEventHandler["Draggable"] = None
    """
    Fires when this draggable is dropped and accepted by a DragTarget.
    """

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
        assert self.max_simultaneous_drags is None or (
            self.max_simultaneous_drags >= 0
        ), "max_simultaneous_drags must be greater than or equal to 0"
