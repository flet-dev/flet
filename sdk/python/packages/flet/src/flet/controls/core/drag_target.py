from dataclasses import dataclass, field
from typing import Annotated, Optional

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


def _resolve_source(event: Event["DragTarget"]) -> Optional[Draggable]:
    """Returns the `Draggable` that `event.src_id` identifies in the page, if any."""
    source = event.page.get_control(event.src_id)
    return source if isinstance(source, Draggable) else None


@dataclass
class DragWillAcceptEvent(Event["DragTarget"]):
    """
    Event payload for :attr:`flet.DragTarget.on_will_accept`.
    """

    src_id: Optional[int]
    """
    ID of the :class:`~flet.Draggable` source control, if available.
    """

    src: Optional[Draggable] = field(init=False)
    """
    Source :class:`~flet.Draggable` control resolved from :attr:`src_id`.

    It is `None` if :attr:`src_id` doesn't identify a :class:`flet.Draggable` in the
    page.
    """

    accept: bool
    """
    Whether this target will accept the dragged source.
    """

    def __post_init__(self):
        self.src = _resolve_source(self)


@dataclass
class DragTargetEvent(Event["DragTarget"]):
    """
    Event payload for drag move and accepted-drop callbacks.
    """

    src_id: Optional[int]
    """
    ID of the :class:`~flet.Draggable` source control, if available.
    """

    src: Optional[Draggable] = field(init=False)
    """
    Source :class:`~flet.Draggable` control resolved from :attr:`src_id`.

    It is `None` if :attr:`src_id` doesn't identify a :class:`flet.Draggable` in the
    page, or if the event is an accepted drop and the source isn't in the same
    :attr:`flet.DragTarget.group`.
    """

    local_position: Offset = field(metadata={"data_field": "l"})
    """
    Pointer position relative to the target bounds.
    """

    global_position: Offset = field(metadata={"data_field": "g"})
    """
    Pointer position in the global coordinate space.
    """

    def __post_init__(self):
        self.src = _resolve_source(self)
        if self.name == "accept" and self.src and self.src.group != self.control.group:
            self.src = None


@dataclass
class DragTargetLeaveEvent(Event["DragTarget"]):
    """
    Event payload for :attr:`flet.DragTarget.on_leave`.
    """

    src_id: Optional[int]
    """
    ID of the :class:`~flet.Draggable` source control, if available.
    """

    src: Optional[Draggable] = field(init=False)
    """
    Source :class:`~flet.Draggable` control resolved from :attr:`src_id`.

    It is `None` if :attr:`src_id` doesn't identify a :class:`flet.Draggable` in the
    page.
    """

    def __post_init__(self):
        self.src = _resolve_source(self)


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
    Called when a :class:`~flet.Draggable` is dragged on this target.
    """

    on_accept: Optional[EventHandler[DragTargetEvent]] = None
    """
    Called when the user does drop an acceptable (same :attr:`group`) \
    :class:`~flet.Draggable` on this target.
    """

    on_leave: Optional[EventHandler[DragTargetLeaveEvent]] = None
    """
    Called when a :class:`~flet.Draggable` leaves this target.
    """

    on_move: Optional[EventHandler[DragTargetEvent]] = None
    """
    Called when a :class:`~flet.Draggable` moves within this target.
    """
