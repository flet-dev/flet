from dataclasses import field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import ControlEvent
from flet.controls.core.list_view import ListView
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import (
    ClipBehavior,
    MouseCursor,
    Number,
    OptionalEventCallable,
    OptionalNumber,
)

__all__ = ["ReorderableListView", "OnReorderEvent"]


class OnReorderEvent(ControlEvent):
    new_index: Optional[int]
    old_index: Optional[int]


@control("ReorderableListView")
class ReorderableListView(ListView):
    """
    A scrollable list of controls that can be reordered.

    Online docs: https://flet.dev/docs/controls/reorderablelistview
    """

    controls: list[Control] = field(default_factory=list)
    horizontal: bool = False
    item_extent: OptionalNumber = None
    first_item_prototype: bool = False
    padding: OptionalPaddingValue = None
    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    cache_extent: OptionalNumber = None
    anchor: Number = 0.0
    auto_scroller_velocity_scalar: OptionalNumber = None
    header: Optional[Control] = None
    footer: Optional[Control] = None
    build_controls_on_demand: bool = True
    show_default_drag_handles: bool = True
    mouse_cursor: Optional[MouseCursor] = None
    on_reorder: OptionalEventCallable[OnReorderEvent] = None
    on_reorder_start: OptionalEventCallable[OnReorderEvent] = None
    on_reorder_end: OptionalEventCallable[OnReorderEvent] = None
