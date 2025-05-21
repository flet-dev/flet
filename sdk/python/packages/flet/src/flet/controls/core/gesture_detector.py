from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.events import (
    DragEndEvent,
    DragStartEvent,
    DragUpdateEvent,
    HoverEvent,
    LongPressEndEvent,
    ScaleEndEvent,
    ScaleStartEvent,
    ScaleUpdateEvent,
    ScrollEvent,
    TapEvent,
)
from flet.controls.types import MouseCursor, OptionalEventCallable, PointerDeviceType

__all__ = ["GestureDetector"]


@control("GestureDetector")
class GestureDetector(ConstrainedControl, AdaptiveControl):
    """
    A control that detects gestures.

    Attempts to recognize gestures that correspond to its non-null callbacks.

    If this control has a content, it defers to that child control for its sizing 
    behavior. If it does not have a content, it grows to fit the parent instead.

    Online docs: https://flet.dev/docs/controls/gesturedetector
    """

    content: Optional[Control] = None
    mouse_cursor: Optional[MouseCursor] = None
    drag_interval: int = 0
    hover_interval: int = 0
    multi_tap_touches: int = 0
    exclude_from_semantics: bool = False
    trackpad_scroll_causes_scale: bool = False
    allowed_devices: Optional[list[PointerDeviceType]] = None
    on_tap: OptionalEventCallable[TapEvent] = None
    on_tap_down: OptionalEventCallable[TapEvent] = None
    on_tap_up: OptionalEventCallable[TapEvent] = None
    on_multi_tap: OptionalEventCallable[TapEvent] = None
    on_multi_long_press: OptionalEventCallable[LongPressEndEvent] = None
    on_secondary_tap: OptionalEventCallable[TapEvent] = None
    on_secondary_tap_down: OptionalEventCallable[TapEvent] = None
    on_secondary_tap_up: OptionalEventCallable[TapEvent] = None
    on_long_press_start: OptionalEventCallable[LongPressEndEvent] = None
    on_long_press_end: OptionalEventCallable[LongPressEndEvent] = None
    on_secondary_long_press_start: OptionalEventCallable[LongPressEndEvent] = None
    on_secondary_long_press_end: OptionalEventCallable[LongPressEndEvent] = None
    on_double_tap: OptionalEventCallable[TapEvent] = None
    on_double_tap_down: OptionalEventCallable[TapEvent] = None
    on_horizontal_drag_start: OptionalEventCallable[DragStartEvent] = None
    on_horizontal_drag_update: OptionalEventCallable[DragUpdateEvent] = None
    on_horizontal_drag_end: OptionalEventCallable[DragEndEvent] = None
    on_vertical_drag_start: OptionalEventCallable[DragStartEvent] = None
    on_vertical_drag_update: OptionalEventCallable[DragUpdateEvent] = None
    on_vertical_drag_end: OptionalEventCallable[DragEndEvent] = None
    on_pan_start: OptionalEventCallable[DragStartEvent] = None
    on_pan_update: OptionalEventCallable[DragUpdateEvent] = None
    on_pan_end: OptionalEventCallable[DragEndEvent] = None
    on_scale_start: OptionalEventCallable[ScaleStartEvent] = None
    on_scale_update: OptionalEventCallable[ScaleUpdateEvent] = None
    on_scale_end: OptionalEventCallable[ScaleEndEvent] = None
    on_hover: OptionalEventCallable[HoverEvent] = None
    on_enter: OptionalEventCallable[HoverEvent] = None
    on_exit: OptionalEventCallable[HoverEvent] = None
    on_scroll: OptionalEventCallable[ScrollEvent] = None
