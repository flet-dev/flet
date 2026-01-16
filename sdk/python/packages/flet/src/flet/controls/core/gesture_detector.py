from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler, EventHandler
from flet.controls.events import (
    DragDownEvent,
    DragEndEvent,
    DragStartEvent,
    DragUpdateEvent,
    ForcePressEvent,
    HoverEvent,
    LongPressDownEvent,
    LongPressEndEvent,
    LongPressMoveUpdateEvent,
    LongPressStartEvent,
    PointerEvent,
    ScaleEndEvent,
    ScaleStartEvent,
    ScaleUpdateEvent,
    ScrollEvent,
    TapEvent,
    TapMoveEvent,
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
    Throttling in milliseconds for [`on_hover`][(c).] event.
    """

    multi_tap_touches: int = 0
    """
    The minimum number of pointers to trigger [`on_multi_tap`][(c).] event.
    """

    exclude_from_semantics: bool = False
    """
    TBD
    """

    on_force_press_start: Optional[EventHandler[ForcePressEvent["GestureDetector"]]] = (
        None
    )
    """
    Called when a pointer has pressed with a force exceeding the start pressure.
    """

    on_force_press_peak: Optional[EventHandler[ForcePressEvent["GestureDetector"]]] = (
        None
    )
    """
    Called when a pointer has pressed with a force exceeding the peak pressure.
    """

    on_force_press_update: Optional[
        EventHandler[ForcePressEvent["GestureDetector"]]
    ] = None
    """
    Called for each update after a force press has started.
    """

    on_force_press_end: Optional[EventHandler[ForcePressEvent["GestureDetector"]]] = (
        None
    )
    """
    Called when the pointer that triggered a force press is no longer
    in contact with the screen.
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

    on_tap_move: Optional[EventHandler[TapMoveEvent["GestureDetector"]]] = None
    """
    Called when a pointer that triggered a tap has moved.
    """

    on_tap_cancel: Optional[ControlEventHandler["GestureDetector"]] = None
    """
    The pointer that previously triggered [`on_tap_down`][(c).] will not
    end up causing a tap.
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

    on_secondary_tap: Optional[ControlEventHandler["GestureDetector"]] = None
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

    on_secondary_tap_cancel: Optional[ControlEventHandler["GestureDetector"]] = None
    """
    The pointer that previously triggered [`on_secondary_tap_down`][(c).]
    will not end up causing a tap.
    """

    on_tertiary_tap_down: Optional[EventHandler[TapEvent["GestureDetector"]]] = None
    """
    Called when a pointer that might cause a tap with a tertiary button has contacted
    the screen at a particular location.
    """

    on_tertiary_tap_up: Optional[EventHandler[TapEvent["GestureDetector"]]] = None
    """
    Called when a pointer that will trigger a tap with a tertiary button has stopped
    contacting the screen at a particular location.
    """

    on_tertiary_tap_cancel: Optional[ControlEventHandler["GestureDetector"]] = None
    """
    The pointer that previously triggered [`on_tertiary_tap_down`][(c).]
    will not end up causing a tap.
    """

    on_long_press_down: Optional[
        EventHandler[LongPressDownEvent["GestureDetector"]]
    ] = None
    """
    Called when a pointer that might cause a long press with a primary button
    has contacted the screen.
    """

    on_long_press_cancel: Optional[ControlEventHandler["GestureDetector"]] = None
    """
    The pointer that previously triggered [`on_long_press_down`][(c).]
    will not end up causing a long-press.
    """

    on_long_press: Optional[ControlEventHandler["GestureDetector"]] = None
    """
    Called when a long press gesture with a primary button has been recognized.
    """

    on_long_press_start: Optional[
        EventHandler[LongPressStartEvent["GestureDetector"]]
    ] = None
    """
    Triggered when a pointer has remained in contact with the screen at the same
    location for a long period of time.
    """

    on_long_press_move_update: Optional[
        EventHandler[LongPressMoveUpdateEvent["GestureDetector"]]
    ] = None
    """
    Called when, after a long press has been accepted, the pointer moves.
    """

    on_long_press_up: Optional[ControlEventHandler["GestureDetector"]] = None
    """
    Called when a pointer that has triggered a long press with a primary button
    is no longer in contact with the screen.
    """

    on_long_press_end: Optional[EventHandler[LongPressEndEvent["GestureDetector"]]] = (
        None
    )
    """
    Called when a pointer that has triggered a long-press with a primary button has
    stopped contacting the screen.
    """

    on_secondary_long_press_down: Optional[
        EventHandler[LongPressDownEvent["GestureDetector"]]
    ] = None
    """
    Called when a pointer that might cause a long press with a secondary button
    has contacted the screen.
    """

    on_secondary_long_press_cancel: Optional[ControlEventHandler["GestureDetector"]] = (
        None
    )
    """
    The pointer that previously triggered [`on_secondary_long_press_down`][(c).]
    not end up causing a long-press.
    """

    on_secondary_long_press: Optional[ControlEventHandler["GestureDetector"]] = None
    """
    Called when a long press gesture with a secondary button has been recognized.
    """

    on_secondary_long_press_start: Optional[
        EventHandler[LongPressStartEvent["GestureDetector"]]
    ] = None
    """
    Triggered when a pointer has remained in contact with the screen at the same
    location for a long period of time.
    """

    on_secondary_long_press_move_update: Optional[
        EventHandler[LongPressMoveUpdateEvent["GestureDetector"]]
    ] = None
    """
    Called when, after a secondary long press has been accepted, the pointer moves.
    """

    on_secondary_long_press_up: Optional[ControlEventHandler["GestureDetector"]] = None
    """
    Called when a pointer that has triggered a long press with a secondary button
    is no longer in contact with the screen.
    """

    on_secondary_long_press_end: Optional[
        EventHandler[LongPressEndEvent["GestureDetector"]]
    ] = None
    """
    Called when a pointer that has triggered a long-press with a secondary button has
    stopped contacting the screen.
    """

    on_tertiary_long_press_down: Optional[
        EventHandler[LongPressDownEvent["GestureDetector"]]
    ] = None
    """
    Called when a pointer that might cause a long press with a tertiary button
    has contacted the screen.
    """

    on_tertiary_long_press_cancel: Optional[ControlEventHandler["GestureDetector"]] = (
        None
    )
    """
    The pointer that previously triggered [`on_tertiary_long_press_down`][(c).]
    will not end up causing a long-press.
    """

    on_tertiary_long_press: Optional[ControlEventHandler["GestureDetector"]] = None
    """
    Called when a long press gesture with a tertiary button has been recognized.
    """

    on_tertiary_long_press_start: Optional[
        EventHandler[LongPressStartEvent["GestureDetector"]]
    ] = None
    """
    Triggered when a pointer has remained in contact with the screen at the same
    location for a long period of time.
    """

    on_tertiary_long_press_move_update: Optional[
        EventHandler[LongPressMoveUpdateEvent["GestureDetector"]]
    ] = None
    """
    Called when, after a tertiary long press has been accepted, the pointer moves.
    """

    on_tertiary_long_press_up: Optional[ControlEventHandler["GestureDetector"]] = None
    """
    Called when a pointer that has triggered a long press with a tertiary button
    is no longer in contact with the screen.
    """

    on_tertiary_long_press_end: Optional[
        EventHandler[LongPressEndEvent["GestureDetector"]]
    ] = None
    """
    Called when a pointer that has triggered a long-press with a tertiary button has
    stopped contacting the screen.
    """

    on_double_tap: Optional[ControlEventHandler["GestureDetector"]] = None
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

    on_double_tap_cancel: Optional[ControlEventHandler["GestureDetector"]] = None
    """
    The pointer sequence that was expected to cause a double tap will not do so.
    """

    on_horizontal_drag_down: Optional[
        EventHandler[DragDownEvent["GestureDetector"]]
    ] = None
    """
    Called when a pointer has contacted the screen and might begin to
    move horizontally.
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

    on_horizontal_drag_cancel: Optional[ControlEventHandler["GestureDetector"]] = None
    """
    The pointer that previously triggered [`on_horizontal_drag_down`][(c).]
    will not end up causing a horizontal drag.
    """

    on_vertical_drag_down: Optional[EventHandler[DragDownEvent["GestureDetector"]]] = (
        None
    )
    """
    Called when a pointer has contacted the screen and might begin to
    move vertically.
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

    on_vertical_drag_cancel: Optional[ControlEventHandler["GestureDetector"]] = None
    """
    The pointer that previously triggered [`on_vertical_drag_down`][(c).]
    will not end up causing a vertical drag.
    """

    on_pan_down: Optional[EventHandler[DragDownEvent["GestureDetector"]]] = None
    """
    Called when a pointer has contacted the screen and might begin to move.
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

    on_pan_cancel: Optional[ControlEventHandler["GestureDetector"]] = None
    """
    The pointer that previously triggered [`on_pan_down`][(c).] will not end up
    causing a pan gesture.
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
