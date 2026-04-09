from dataclasses import dataclass, field
from typing import Annotated, Optional, cast

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import Event, EventHandler
from flet.controls.core.draggable import Draggable
from flet.controls.transform import Offset
from flet.utils.validation import V

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
    Source draggable control resolved from :attr:`src_id`.
    """

    def __post_init__(self):
        if self.src_id is not None:
            self.src = cast(Draggable, self.page.get_control(self.src_id))


@dataclass
class DragWillAcceptEvent(DragEventBase):
    """
    Event payload for :attr:`flet.DragTarget.on_will_accept`.
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
        Pointer position as an :class:`~flet.Offset`.
        """

        return Offset(self.x, self.y)


@dataclass
class DragTargetLeaveEvent(DragEventBase):
    """
    Event payload for :attr:`flet.DragTarget.on_leave`.
    """

    pass


@control("DragTarget")
class DragTarget(Control):
    """
    A control that completes drag operation when a :class:`~flet.Draggable` control is \
    dropped.

    When a `Draggable` is dragged on top of a `DragTarget`, the `DragTarget` is asked
    whether it will accept the data the `Draggable` is carrying. The `DragTarget` will
    accept incoming drag if it belongs to the same `group` as `Draggable`. If the user
    does drop the `Draggable` on top of the `DragTarget` (and the `DragTarget` has
    indicated that it will accept the `Draggable`'s data), then the `DragTarget` is
    asked to accept the `Draggable`'s data.
    """

    content: Annotated[
        Control,
        V.visible_control(),
    ]
    """
    The content of this control.

    Raises:
        ValueError: If it is not visible.
    """

    group: str = "default"
    """
    The group this target belongs to.

    Note:
        For a `DragTarget` to accept an incoming drop from a :class:`~flet.Draggable`,
        they must both be in the same `group`.
    """

    on_will_accept: Optional[EventHandler[DragWillAcceptEvent]] = None
    """
    Called when a draggable is dragged on this target.
    """

    on_accept: Optional[EventHandler[DragTargetEvent]] = None
    """
    Called when the user does drop an acceptable (same :attr:`group`) draggable on \
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
