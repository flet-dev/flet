from typing import Optional

from flet.controls.alignment import Axis
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.types import OptionalControlEventCallable

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
    group: str = "default"
    content_when_dragging: Optional[Control] = None
    content_feedback: Optional[Control] = None
    axis: Optional[Axis] = None
    affinity: Optional[Axis] = None
    max_simultaneous_drags: Optional[int] = None
    on_drag_start: OptionalControlEventCallable = None
    on_drag_complete: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
        assert self.max_simultaneous_drags is None or (
            self.max_simultaneous_drags >= 0
        ), "max_simultaneous_drags must be greater than or equal to 0"
