from dataclasses import field
from typing import List, Optional

from flet.controls.core.list_view import ListView
from flet.core.control import Control, control
from flet.core.control_event import ControlEvent
from flet.core.padding import OptionalPaddingValue
from flet.core.types import (
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

    -----

    Online docs: https://flet.dev/docs/controls/reorderablelistview
    """

    controls: List[Control] = field(default_factory=list)
    horizontal: bool = False
    item_extent: OptionalNumber = None
    first_item_prototype: Optional[bool] = None
    padding: OptionalPaddingValue = None
    clip_behavior: Optional[ClipBehavior] = None
    cache_extent: OptionalNumber = None
    anchor: Number = 0.0
    auto_scroller_velocity_scalar: OptionalNumber = None
    header: Optional[Control] = None
    footer: Optional[Control] = None
    build_controls_on_demand: bool = True
    show_default_drag_handles: Optional[bool] = None
    mouse_cursor: Optional[MouseCursor] = None
    on_reorder: OptionalEventCallable[OnReorderEvent] = None
    on_reorder_start: OptionalEventCallable[OnReorderEvent] = None
    on_reorder_end: OptionalEventCallable[OnReorderEvent] = None
