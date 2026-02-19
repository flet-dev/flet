from dataclasses import dataclass, field
from typing import Optional, cast

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import Event, EventHandler
from flet.controls.core.draggable import Draggable
from flet.controls.transform import Offset

__all__ = [
    "DragTarget",
    "DragTargetEvent",
    "DragTargetLeaveEvent",
    "DragWillAcceptEvent",
]


@dataclass
class DragEventBase(Event["DragTarget"]):
    """
    Base payload for drag-target events that carry draggable source information.
    """

    src_id: Optional[int]
    """
    ID of the draggable source control, if available.
    """

    src: Draggable = field(init=False)
    """
    Source draggable control resolved from [`src_id`][(c).].
    """

    def __post_init__(self):
        if self.src_id is not None:
            self.src = cast(Draggable, self.page.get_control(self.src_id))


@dataclass
class DragWillAcceptEvent(DragEventBase):
    """
    Event payload for [`DragTarget.on_will_accept`][flet.].
    """

    accept: bool
    """
    Whether this target will accept the dragged source.
    """


@dataclass
class DragTargetEvent(DragEventBase):
    """
    Event payload for drag move and accepted-drop callbacks.
    """

    x: float
    """
    Horizontal pointer position relative to target bounds.
    """

    y: float
    """
    Vertical pointer position relative to target bounds.
    """

    @property
    def offset(self) -> Offset:
        """
        Pointer position as an [`Offset`][flet.].
        """

        return Offset(self.x, self.y)


@dataclass
class DragTargetLeaveEvent(DragEventBase):
    """
    Event payload for [`DragTarget.on_leave`][flet.].
    """

    pass


@control("DragTarget")
class DragTarget(Control):
    """
    A control that completes drag operation when a [`Draggable`][flet.] control is \
    dropped.

    When a `Draggable` is dragged on top of a `DragTarget`, the `DragTarget` is asked
    whether it will accept the data the `Draggable` is carrying. The `DragTarget` will
    accept incoming drag if it belongs to the same `group` as `Draggable`. If the user
    does drop the `Draggable` on top of the `DragTarget` (and the `DragTarget` has
    indicated that it will accept the `Draggable`'s data), then the `DragTarget` is
    asked to accept the `Draggable`'s data.
    """

    content: Control
    """
    The content of this control.

    Must be visible.

    Raises:
        ValueError: If [`content`][(c).] is not visible.
    """

    group: str = "default"
    """
    The group this target belongs to.

    Note:
        For a `DragTarget` to accept an incoming drop from a [`Draggable`][flet.],
        they must both be in the same `group`.
    """

    on_will_accept: Optional[EventHandler[DragWillAcceptEvent]] = None
    """
    Called when a draggable is dragged on this target.
    """

    on_accept: Optional[EventHandler[DragTargetEvent]] = None
    """
    Called when the user does drop an acceptable (same [`group`][(c).]) draggable on \
    this target.

    Use `page.get_control(e.src_id)` to retrieve Control reference by its ID.
    """

    on_leave: Optional[EventHandler[DragTargetLeaveEvent]] = None
    """
    Called when a draggable leaves this target.
    """

    on_move: Optional[EventHandler[DragTargetEvent]] = None
    """
    Called when a draggable moves within this target.
    """

    def before_update(self):
        super().before_update()
        if not self.content.visible:
            raise ValueError("content must be visible")
