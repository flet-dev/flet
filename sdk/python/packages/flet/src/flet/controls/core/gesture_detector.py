from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import OptionalEventHandler
from flet.controls.events import (
    DragEndEvent,
    DragStartEvent,
    DragUpdateEvent,
    HoverEvent,
    LongPressEndEvent,
    LongPressStartEvent,
    ScaleEndEvent,
    ScaleStartEvent,
    ScaleUpdateEvent,
    ScrollEvent,
    TapEvent,
)
from flet.controls.types import MouseCursor, PointerDeviceType

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
    """
    A child Control contained by the gesture detector.
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    The mouse cursor for mouse pointers that are hovering over the control.

    Value is of type
    [`MouseCursor`](https://flet.dev/docs/reference/types/mousecursor).
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

    on_tap: OptionalEventHandler[TapEvent["GestureDetector"]] = None
    """
    A tap with a primary button has occurred.
    """

    on_tap_down: OptionalEventHandler[TapEvent["GestureDetector"]] = None
    """
    A pointer that might cause a tap with a primary button has contacted the screen
    at a particular location.

    Event handler argument is of type
    [`TapEvent`](https://flet.dev/docs/reference/types/tapevent).
    """

    on_tap_up: OptionalEventHandler[TapEvent["GestureDetector"]] = None
    """
    A pointer that will trigger a tap with a primary button has stopped contacting the
    screen at a particular location.

    Event handler argument is of type
    [`TapEvent`](https://flet.dev/docs/reference/types/tapevent).
    """

    on_multi_tap: OptionalEventHandler[TapEvent["GestureDetector"]] = None
    """
    Triggered when multiple pointers contacted the screen.

    Event handler argument is of type
    [`MultiTapEvent`](https://flet.dev/docs/reference/types/multitapevent).
    """

    on_multi_long_press: OptionalEventHandler[LongPressEndEvent["GestureDetector"]] = (
        None
    )
    """
    Called when a long press gesture with multiple pointers has been recognized.
    """

    on_secondary_tap: OptionalEventHandler[TapEvent["GestureDetector"]] = None
    """
    A tap with a secondary button has occurred.
    """

    on_secondary_tap_down: OptionalEventHandler[TapEvent["GestureDetector"]] = None
    """
    A pointer that might cause a tap with a secondary button has contacted the screen
    at a particular location.

    Event handler argument is of type
    [`TapEvent`](https://flet.dev/docs/reference/types/tapevent).
    """

    on_secondary_tap_up: OptionalEventHandler[TapEvent["GestureDetector"]] = None
    """
    A pointer that will trigger a tap with a secondary button has stopped contacting the
    screen at a particular location.

    Event handler argument is of type
    [`TapEvent`](https://flet.dev/docs/reference/types/tapevent).
    """

    on_long_press_start: OptionalEventHandler[
        LongPressStartEvent["GestureDetector"]
    ] = None
    """
    Called when a long press gesture with a primary button has been recognized.

    Triggered when a pointer has remained in contact with the screen at the same
    location for a long period of time.

    Event handler argument is of type
    [`LongPressStartEvent`](https://flet.dev/docs/reference/types/longpressstartevent).
    """

    on_long_press_end: OptionalEventHandler[LongPressEndEvent["GestureDetector"]] = None
    """
    A pointer that has triggered a long-press with a primary button has stopped
    contacting the screen.

    Event handler argument is of type
    [`LongPressEndEvent`](https://flet.dev/docs/reference/types/longpressendevent).
    """

    on_secondary_long_press_start: OptionalEventHandler[
        LongPressStartEvent["GestureDetector"]
    ] = None
    """
    Called when a long press gesture with a secondary button has been recognized.

    Triggered when a pointer has remained in contact with the screen at the same
    location for a long period of time.

    Event handler argument is of type
    [`LongPressStartEvent`](https://flet.dev/docs/reference/types/longpressstartevent).
    """

    on_secondary_long_press_end: OptionalEventHandler[
        LongPressEndEvent["GestureDetector"]
    ] = None
    """
    A pointer that has triggered a long-press with a secondary button has stopped
    contacting the screen.

    Event handler argument is of type
    [`LongPressEndEvent`](https://flet.dev/docs/reference/types/longpressendevent).
    """

    on_double_tap: OptionalEventHandler[TapEvent["GestureDetector"]] = None
    """
    The user has tapped the screen with a primary button at the same location twice
    in quick succession.
    """

    on_double_tap_down: OptionalEventHandler[TapEvent["GestureDetector"]] = None
    """
    A pointer that might cause a double tap has contacted the screen at a particular
    location.

    Triggered immediately after the down event of the second tap.

    Event handler argument is of type
    [`TapEvent`](https://flet.dev/docs/reference/types/tapevent).
    """

    on_horizontal_drag_start: OptionalEventHandler[
        DragStartEvent["GestureDetector"]
    ] = None
    """
    A pointer has contacted the screen with a primary button and has begun to move
    horizontally.

    Event handler argument is of type
    [`DragStartEvent`](https://flet.dev/docs/reference/types/dragstartevent).
    """

    on_horizontal_drag_update: OptionalEventHandler[
        DragUpdateEvent["GestureDetector"]
    ] = None
    """
    A pointer that is in contact with the screen and moving horizontally has moved in
    the horizontal direction.

    Event handler argument is of type
    [`DragUpdateEvent`](https://flet.dev/docs/reference/types/dragupdateevent).
    """

    on_horizontal_drag_end: OptionalEventHandler[DragEndEvent["GestureDetector"]] = None
    """
    A pointer moving horizontally is no longer in contact and was moving at a specific
    velocity.

    Event handler argument is of type
    [`DragEndEvent`](https://flet.dev/docs/reference/types/dragendevent).
    """

    on_vertical_drag_start: OptionalEventHandler[DragStartEvent["GestureDetector"]] = (
        None
    )
    """
    A pointer has contacted the screen and has begun to move vertically.

    Event handler argument is of type
    [`DragStartEvent`](https://flet.dev/docs/reference/types/dragstartevent).
    """

    on_vertical_drag_update: OptionalEventHandler[
        DragUpdateEvent["GestureDetector"]
    ] = None
    """
    A pointer moving vertically has moved in the vertical direction.

    Event handler argument is of type
    [`DragUpdateEvent`](https://flet.dev/docs/reference/types/dragupdateevent).
    """

    on_vertical_drag_end: OptionalEventHandler[DragEndEvent["GestureDetector"]] = None
    """
    A pointer moving vertically is no longer in contact and was moving at a specific
    velocity.

    Event handler argument is of type
    [`DragEndEvent`](https://flet.dev/docs/reference/types/dragendevent).
    """

    on_pan_start: OptionalEventHandler[DragStartEvent["GestureDetector"]] = None
    """
    A pointer has contacted the screen and has begun to move.

    Event handler argument is of type
    [`DragStartEvent`](https://flet.dev/docs/reference/types/dragstartevent).
    """

    on_pan_update: OptionalEventHandler[DragUpdateEvent["GestureDetector"]] = None
    """
    A pointer that is in contact with the screen and moving has moved again.

    Event handler argument is of type
    [`DragUpdateEvent`](https://flet.dev/docs/reference/types/dragupdateevent).
    """

    on_pan_end: OptionalEventHandler[DragEndEvent["GestureDetector"]] = None
    """
    A pointer is no longer in contact and was moving at a specific velocity.

    Event handler argument is of type
    [`DragEndEvent`](https://flet.dev/docs/reference/types/dragendevent).
    """

    on_scale_start: OptionalEventHandler[ScaleStartEvent["GestureDetector"]] = None
    """
    The pointers in contact with the screen have established a focal point and initial
    scale of `1.0`.

    Event handler argument is of type
    [`ScaleStartEvent`](https://flet.dev/docs/reference/types/scalestartevent).
    """

    on_scale_update: OptionalEventHandler[ScaleUpdateEvent["GestureDetector"]] = None
    """
    Event handler argument is of type
    [`ScaleUpdateEvent`](https://flet.dev/docs/reference/types/scaleupdateevent).
    """

    on_scale_end: OptionalEventHandler[ScaleEndEvent["GestureDetector"]] = None
    """
    Event handler argument is of type
    [`ScaleEndEvent`](https://flet.dev/docs/reference/types/scaleendevent).
    """

    on_hover: OptionalEventHandler[HoverEvent["GestureDetector"]] = None
    """
    Triggered when a mouse pointer has entered this control.

    Event handler argument is of type
    [`HoverEvent`](https://flet.dev/docs/reference/types/hoverevent).
    """

    on_enter: OptionalEventHandler[HoverEvent["GestureDetector"]] = None
    """
    Triggered when a mouse pointer has entered this control.

    Event handler argument is of type
    [`HoverEvent`](https://flet.dev/docs/reference/types/hoverevent).
    """

    on_exit: OptionalEventHandler[HoverEvent["GestureDetector"]] = None
    """
    Triggered when a mouse pointer has exited this control.

    Event handler argument is of type
    [`HoverEvent`](https://flet.dev/docs/reference/types/hoverevent).
    """

    on_scroll: OptionalEventHandler[ScrollEvent["GestureDetector"]] = None
    """
    Event handler argument is of type
    [`ScrollEvent`](https://flet.dev/docs/reference/types/scrollevent).
    """
