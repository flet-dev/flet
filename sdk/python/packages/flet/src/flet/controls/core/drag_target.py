from dataclasses import dataclass, field
from typing import Annotated, Optional, cast

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import Event, EventHandler
from flet.controls.core.draggable import Draggable
from flet.controls.transform import Offset
from flet.utils.deprecated import deprecated
from flet.utils.validation import V

__all__ = [
    "DragTarget",
    "DragTargetEvent",
    "DragTargetLeaveEvent",
    "DragWillAcceptEvent",
]


@dataclass
class DragWillAcceptEvent(Event["DragTarget"]):
    """
    Event payload for :attr:`flet.DragTarget.on_will_accept`.
    """

    src_id: Optional[int]
    """
    ID of the :class:`~flet.Draggable` source control, if available.
    """

    src: Draggable = field(init=False)
    """
    Source :class:`~flet.Draggable` control resolved from :attr:`src_id`.
    """

    accept: bool
    """
    Whether this target will accept the dragged source.
    """

    def __post_init__(self):
        if self.src_id is not None:
            self.src = cast(Draggable, self.page.get_control(self.src_id))


@dataclass
class DragTargetEvent(Event["DragTarget"]):
    """
    Event payload for drag move and accepted-drop callbacks.
    """

    src_id: Optional[int]
    """
    ID of the :class:`~flet.Draggable` source control, if available.
    """

    src: Draggable = field(init=False)
    """
    Source :class:`~flet.Draggable` control resolved from :attr:`src_id`.
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
        if self.src_id is not None:
            self.src = cast(Draggable, self.page.get_control(self.src_id))

    @property
    @deprecated(
        reason="Use `local_position.x` for target-relative coordinates or "
        "`global_position.x` for global coordinates instead.",
        docs_reason="Use [`local_position.x`](../types/dragtargetevent.md#flet.DragTargetEvent.local_position) for target-relative coordinates or "  # noqa: E501
        "[`global_position.x`](../types/dragtargetevent.md#flet.DragTargetEvent.global_position) for global coordinates instead.",  # noqa: E501
        version="0.85.0",
        delete_version="0.88.0",
    )
    def x(self) -> float:
        """
        Horizontal pointer position in the global coordinate space.
        """

        return self.global_position.x

    @property
    @deprecated(
        reason="Use `local_position.y` for target-relative coordinates or "
        "`global_position.y` for global coordinates instead.",
        docs_reason="Use [`local_position.y`](../types/dragtargetevent.md#flet.DragTargetEvent.local_position) for target-relative coordinates or "  # noqa: E501
        "[`global_position.y`](../types/dragtargetevent.md#flet.DragTargetEvent.global_position) for global coordinates instead.",  # noqa: E501
        version="0.85.0",
        delete_version="0.88.0",
    )
    def y(self) -> float:
        """
        Vertical pointer position in the global coordinate space.
        """

        return self.global_position.y

    @property
    @deprecated(
        reason="Use `local_position` for target-relative coordinates or "
        "`global_position` for global coordinates instead.",
        docs_reason="Use [`local_position`](../types/dragtargetevent.md#flet.DragTargetEvent.local_position) for target-relative coordinates or "  # noqa: E501
        "[`global_position`](../types/dragtargetevent.md#flet.DragTargetEvent.global_position) for global coordinates instead.",  # noqa: E501
        version="0.85.0",
        delete_version="0.88.0",
    )
    def offset(self) -> Offset:
        """
        Pointer position in global coordinates.
        """

        return self.global_position


@dataclass
class DragTargetLeaveEvent(Event["DragTarget"]):
    """
    Event payload for :attr:`flet.DragTarget.on_leave`.
    """

    src_id: Optional[int]
    """
    ID of the :class:`~flet.Draggable` source control, if available.
    """

    src: Draggable = field(init=False)
    """
    Source :class:`~flet.Draggable` control resolved from :attr:`src_id`.
    """

    def __post_init__(self):
        if self.src_id is not None:
            self.src = cast(Draggable, self.page.get_control(self.src_id))


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
