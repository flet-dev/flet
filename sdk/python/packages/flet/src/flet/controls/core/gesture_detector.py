from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import EventHandler
from flet.controls.events import (
    DragEndEvent,
    DragStartEvent,
    DragUpdateEvent,
    HoverEvent,
    LongPressEndEvent,
    LongPressStartEvent,
    PointerEvent,
    ScaleEndEvent,
    ScaleStartEvent,
    ScaleUpdateEvent,
    ScrollEvent,
    TapEvent,
)
from flet.controls.layout_control import LayoutControl
from flet.controls.types import MouseCursor, PointerDeviceType

__all__ = ["GestureDetector"]


@control("GestureDetector")
class GestureDetector(LayoutControl, AdaptiveControl):
    """
    A control that detects gestures.

    Attempts to recognize gestures that correspond to its non-None callbacks.

    If this control has a [`content`][(c).], it defers to that child control for
    its sizing behavior, else it grows to fit the parent instead.
    """

    content: Optional[Control] = None
    """
    A child Control contained by the gesture detector.
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    The mouse cursor for mouse pointers that are hovering over the control.
    """

    drag_interval: int = 0
    """
    Throttling in milliseconds for horizontal drag, vertical drag and pan update events.

    When a user moves a pointer a lot of events are being generated to do precise
    tracking. `drag_interval` allows sending drag update events to a Flet program every
    X milliseconds, thus preserving the bandwidth (web and mobile apps).

    Default is `0` - no throttling, all events are sent to a Flet program, very smooth
    tracking.
    """

    hover_interval: int = 0
    """
    Throttling in milliseconds for `on_hover` event.
    """

    multi_tap_touches: int = 0
    """
    The minimum number of pointers to trigger `on_multi_tap` event.
    """

    exclude_from_semantics: bool = False
    """
    TBD
    """

    trackpad_scroll_causes_scale: bool = False
    """
    TBD
    """

    allowed_devices: Optional[list[PointerDeviceType]] = None
    """
    TBD
    """

    on_tap: Optional[EventHandler[TapEvent["GestureDetector"]]] = None
    """
    Called when a tap with a primary button has occurred.
    """

    on_tap_down: Optional[EventHandler[TapEvent["GestureDetector"]]] = None
    """
    Called when a pointer that might cause a tap with a primary button has contacted
    the screen at a particular location.
    """

    on_tap_up: Optional[EventHandler[TapEvent["GestureDetector"]]] = None
    """
    Called when a pointer that will trigger a tap with a primary button has stopped
    contacting the screen at a particular location.
    """

    on_multi_tap: Optional[EventHandler[TapEvent["GestureDetector"]]] = None
    """
    Called when multiple pointers contacted the screen.
    """

    on_multi_long_press: Optional[
        EventHandler[LongPressEndEvent["GestureDetector"]]
    ] = None
    """
    Called when a long press gesture with multiple pointers has been recognized.
    """

    on_secondary_tap: Optional[EventHandler[TapEvent["GestureDetector"]]] = None
    """
    A tap with a secondary button has occurred.
    """

    on_secondary_tap_down: Optional[EventHandler[TapEvent["GestureDetector"]]] = None
    """
    Called when a pointer that might cause a tap with a secondary button has contacted
    the screen at a particular location.
    """

    on_secondary_tap_up: Optional[EventHandler[TapEvent["GestureDetector"]]] = None
    """
    Called when a pointer that will trigger a tap with a secondary button has stopped
    contacting the screen at a particular location.
    """

    on_long_press_start: Optional[
        EventHandler[LongPressStartEvent["GestureDetector"]]
    ] = None
    """
    Called when a long press gesture with a primary button has been recognized.

    Triggered when a pointer has remained in contact with the screen at the same
    location for a long period of time.
    """

    on_long_press_end: Optional[EventHandler[LongPressEndEvent["GestureDetector"]]] = (
        None
    )
    """
    Called when a pointer that has triggered a long-press with a primary button has
    stopped contacting the screen.
    """

    on_secondary_long_press_start: Optional[
        EventHandler[LongPressStartEvent["GestureDetector"]]
    ] = None
    """
    Called when a long press gesture with a secondary button has been recognized.

    Triggered when a pointer has remained in contact with the screen at the same
    location for a long period of time.
    """

    on_secondary_long_press_end: Optional[
        EventHandler[LongPressEndEvent["GestureDetector"]]
    ] = None
    """
    Called when a pointer that has triggered a long-press with a secondary button has
    stopped contacting the screen.
    """

    on_double_tap: Optional[EventHandler[TapEvent["GestureDetector"]]] = None
    """
    The user has tapped the screen with a primary button at the same location twice
    in quick succession.
    """

    on_double_tap_down: Optional[EventHandler[TapEvent["GestureDetector"]]] = None
    """
    Called when a pointer that might cause a double tap has contacted the screen at
    a particular location.

    Triggered immediately after the down event of the second tap.
    """

    on_horizontal_drag_start: Optional[
        EventHandler[DragStartEvent["GestureDetector"]]
    ] = None
    """
    Called when a pointer has contacted the screen with a primary button and has
    begun to move horizontally.
    """

    on_horizontal_drag_update: Optional[
        EventHandler[DragUpdateEvent["GestureDetector"]]
    ] = None
    """
    Called when a pointer that is in contact with the screen and moving horizontally
    has moved in the horizontal direction.
    """

    on_horizontal_drag_end: Optional[EventHandler[DragEndEvent["GestureDetector"]]] = (
        None
    )
    """
    Called when a pointer moving horizontally is no longer in contact and was
    moving at a specific velocity.
    """

    on_vertical_drag_start: Optional[
        EventHandler[DragStartEvent["GestureDetector"]]
    ] = None
    """
    Called when a pointer has contacted the screen and has begun to move vertically.
    """

    on_vertical_drag_update: Optional[
        EventHandler[DragUpdateEvent["GestureDetector"]]
    ] = None
    """
    A pointer moving vertically has moved in the vertical direction.
    """

    on_vertical_drag_end: Optional[EventHandler[DragEndEvent["GestureDetector"]]] = None
    """
    Called when a pointer moving vertically is no longer in contact and was
    moving at a specific velocity.
    """

    on_pan_start: Optional[EventHandler[DragStartEvent["GestureDetector"]]] = None
    """
    Called when a pointer has contacted the screen and has begun to move.
    """

    on_pan_update: Optional[EventHandler[DragUpdateEvent["GestureDetector"]]] = None
    """
    Called when a pointer that is in contact with the screen and moving has moved again.
    """

    on_pan_end: Optional[EventHandler[DragEndEvent["GestureDetector"]]] = None
    """
    Called when a pointer is no longer in contact and was moving at a specific velocity.
    """

    on_right_pan_start: Optional[EventHandler[PointerEvent["GestureDetector"]]] = None
    """
    Pointer has contacted the screen while secondary button pressed
    and has begun to move.
    """

    on_right_pan_update: Optional[EventHandler[PointerEvent["GestureDetector"]]] = None
    """
    A pointer that is in contact with the screen, secondary button pressed
    and moving has moved again.
    """

    on_right_pan_end: Optional[EventHandler[PointerEvent["GestureDetector"]]] = None
    """
    A pointer with secondary button pressed is no longer in contact
    and was moving at a specific velocity.
    """

    on_scale_start: Optional[EventHandler[ScaleStartEvent["GestureDetector"]]] = None
    """
    Called when the pointers in contact with the screen have established a focal
    point and initial scale of `1.0`.
    """

    on_scale_update: Optional[EventHandler[ScaleUpdateEvent["GestureDetector"]]] = None
    """
    TBD
    """

    on_scale_end: Optional[EventHandler[ScaleEndEvent["GestureDetector"]]] = None
    """
    TBD
    """

    on_hover: Optional[EventHandler[HoverEvent["GestureDetector"]]] = None
    """
    Called when a mouse pointer has entered this control.
    """

    on_enter: Optional[EventHandler[HoverEvent["GestureDetector"]]] = None
    """
    Called when a mouse pointer has entered this control.
    """

    on_exit: Optional[EventHandler[HoverEvent["GestureDetector"]]] = None
    """
    Called when a mouse pointer has exited this control.
    """

    on_scroll: Optional[EventHandler[ScrollEvent["GestureDetector"]]] = None
    """
    TBD
    """
