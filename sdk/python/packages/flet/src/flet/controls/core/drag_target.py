from dataclasses import dataclass
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import Event, OptionalEventHandler
from flet.controls.transform import Offset

__all__ = [
    "DragTarget",
    "DragTargetEvent",
    "DragWillAcceptEvent",
    "DragTargetLeaveEvent",
]


@dataclass
class DragWillAcceptEvent(Event["DragTarget"]):
    accept: bool
    src_id: int


@dataclass
class DragTargetEvent(Event["DragTarget"]):
    src_id: int
    x: float
    y: float

    @property
    def offset(self) -> Offset:
        return Offset(self.x, self.y)


@dataclass
class DragTargetLeaveEvent(Event["DragTarget"]):
    src_id: Optional[int]


@control("DragTarget")
class DragTarget(Control):
    """
    A control that completes drag operation when a `Draggable` widget is dropped.

    When a draggable is dragged on top of a drag target, the drag target is asked
    whether it will accept the data the draggable is carrying. The drag target will
    accept incoming drag if it belongs to the same group as draggable. If the user
    does drop the draggable on top of the drag target (and the drag target has
    indicated that it will accept the draggable's data), then the drag target is
    asked to accept the draggable's data.

    Online docs: https://flet.dev/docs/controls/dragtarget
    """

    content: Control
    """
    The `Control` that is a visual representation of the drag target.
    """

    group: str = "default"
    """
    The group this target belongs to. Note that for this target to accept an
    incoming drop from a [`Draggable`](https://flet.dev/docs/controls/draggable), they
    must both be in the same group.
    """

    on_will_accept: OptionalEventHandler[DragWillAcceptEvent] = None
    """
    Fires when a draggable is dragged on this target.

    `data` field of event details contains `true` (String) if both the draggable
    and this target are in the same `group`; otherwise `false` (String).
    """

    on_accept: OptionalEventHandler[DragTargetEvent] = None
    """
    Fires when the user does drop an acceptable (same `group`) draggable on
    this target.

    Event handler argument is an instance of
    [`DragTargetEvent`](https://flet.dev/docs/reference/types/dragtargetevent).

    Use `page.get_control(e.src_id)` to retrieve Control reference by its ID.
    """

    on_leave: OptionalEventHandler[DragTargetLeaveEvent] = None
    """
    Fires when a draggable leaves this target.
    """

    on_move: OptionalEventHandler[DragTargetEvent] = None
    """
    Fires when a draggable moves within this target.

    Event handler argument is of type
    [`DragTargetEvent`](https://flet.dev/docs/reference/types/dragtargetevent).
    """

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
