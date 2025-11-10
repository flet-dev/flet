from dataclasses import dataclass, field
from typing import Optional

from flet.controls.control_event import ControlEvent, Event, EventControlType
from flet.controls.duration import Duration
from flet.controls.transform import Offset
from flet.controls.types import PointerDeviceType

__all__ = [
    "DragDownEvent",
    "DragEndEvent",
    "DragStartEvent",
    "DragUpdateEvent",
    "ForcePressEvent",
    "HoverEvent",
    "LongPressDownEvent",
    "LongPressEndEvent",
    "LongPressMoveUpdateEvent",
    "LongPressStartEvent",
    "MultiTapEvent",
    "PointerEvent",
    "ScaleEndEvent",
    "ScaleStartEvent",
    "ScaleUpdateEvent",
    "ScrollEvent",
    "TapEvent",
    "TapMoveEvent",
]


@dataclass(kw_only=True)
class TapEvent(Event[EventControlType]):
    kind: Optional[PointerDeviceType] = field(
        default=None, metadata={"data_field": "k"}
    )
    """
    The kind of the device that initiated the event.
    """

    local_position: Optional[Offset] = field(default=None, metadata={"data_field": "l"})
    """
    The local position at which the pointer contacted the screen.
    """

    global_position: Optional[Offset] = field(
        default=None, metadata={"data_field": "g"}
    )
    """
    The global position at which the pointer contacted the screen.
    """


@dataclass(kw_only=True)
class TapMoveEvent(Event[EventControlType]):
    kind: PointerDeviceType = field(metadata={"data_field": "k"})
    """
    The kind of the device that initiated the event.
    """

    local_position: Offset = field(metadata={"data_field": "l"})
    """
    The local position at which the pointer is located.
    """

    global_position: Offset = field(metadata={"data_field": "g"})
    """
    The global position at which the pointer is located.
    """

    delta: Offset = field(metadata={"data_field": "d"})
    """
    The movement delta since the previous update.
    """


@dataclass(kw_only=True)
class MultiTapEvent(ControlEvent):
    correct_touches: bool = field(metadata={"data_field": "ct"})


@dataclass(kw_only=True)
class LongPressDownEvent(Event[EventControlType]):
    kind: Optional[PointerDeviceType] = field(
        default=None, metadata={"data_field": "k"}
    )
    """
    The kind of the device that initiated the event.
    """

    local_position: Offset = field(metadata={"data_field": "l"})
    """
    The local position at which the pointer contacted the screen.
    """

    global_position: Offset = field(metadata={"data_field": "g"})
    """
    The global position at which the pointer contacted the screen.
    """


@dataclass(kw_only=True)
class LongPressStartEvent(Event[EventControlType]):
    local_position: Optional[Offset] = field(default=None, metadata={"data_field": "l"})
    """
    The local position at which the pointer initially contacted the screen.
    """

    global_position: Optional[Offset] = field(
        default=None, metadata={"data_field": "g"}
    )
    """
    The global position at which the pointer initially contacted the screen.
    """


@dataclass(kw_only=True)
class LongPressMoveUpdateEvent(Event[EventControlType]):
    local_position: Offset = field(metadata={"data_field": "l"})
    """
    The current local position of the pointer.
    """

    global_position: Offset = field(metadata={"data_field": "g"})
    """
    The current global position of the pointer.
    """

    offset_from_origin: Offset = field(metadata={"data_field": "ofo"})
    """
    Delta from the point where the long press started, in global coordinates.
    """

    local_offset_from_origin: Offset = field(metadata={"data_field": "lofo"})
    """
    Delta from the point where the long press started, in local coordinates.
    """


@dataclass(kw_only=True)
class LongPressEndEvent(Event[EventControlType]):
    local_position: Optional[Offset] = field(default=None, metadata={"data_field": "l"})
    """
    The local position at which the pointer contacted the screen.
    """

    global_position: Optional[Offset] = field(
        default=None, metadata={"data_field": "g"}
    )
    """
    The global position at which the pointer lifted from the screen.
    """

    velocity: Offset = field(metadata={"data_field": "v"})
    """
    The pointer's velocity when it stopped contacting the screen,
    in pixels per second.

    Defaults to zero if not specified in the constructor.
    """


@dataclass(kw_only=True)
class DragDownEvent(Event[EventControlType]):
    local_position: Offset = field(metadata={"data_field": "l"})
    """
    The local position at which the pointer contacted the screen.
    """

    global_position: Offset = field(metadata={"data_field": "g"})
    """
    The global position at which the pointer contacted the screen.
    """


@dataclass(kw_only=True)
class DragStartEvent(Event[EventControlType]):
    kind: PointerDeviceType = field(metadata={"data_field": "k"})
    """
    The kind of the device that initiated the event.
    """

    local_position: Offset = field(metadata={"data_field": "l"})
    """
    The local position in the coordinate system of the event receiver at which
    the pointer contacted the screen.
    """

    global_position: Offset = field(metadata={"data_field": "g"})
    """
    The global position at which the pointer contacted the screen.

    Defaults to the origin if not specified in the constructor.
    """

    timestamp: Optional[Duration] = field(default=None, metadata={"data_field": "ts"})
    """
    Recorded timestamp of the source pointer event that triggered the drag event.

    Could be `None` if triggered from proxied events such as accessibility.
    """


@dataclass(kw_only=True)
class DragUpdateEvent(Event[EventControlType]):
    local_position: Offset = field(metadata={"data_field": "l"})
    """
    The local position in the coordinate system of the event receiver
    at which the pointer contacted the screen.
    """

    global_position: Offset = field(metadata={"data_field": "g"})
    """
    The pointer's global position when it triggered this update.
    """

    local_delta: Optional[Offset] = field(default=None, metadata={"data_field": "ld"})
    """
    The amount the pointer has moved in the local coordinate space of the event receiver
    since the start of the drag.
    """

    global_delta: Optional[Offset] = field(default=None, metadata={"data_field": "gd"})
    """
    The amount the pointer has moved in the global coordinate space
    since the start of the drag.
    """

    primary_delta: Optional[float] = field(default=None, metadata={"data_field": "pd"})
    """
    The amount the pointer has moved along the primary axis in the coordinate space
    of the event receiver since the previous update.
    """

    timestamp: Optional[Duration] = field(default=None, metadata={"data_field": "ts"})
    """
    Recorded timestamp of the source pointer event that triggered the drag event.

    Could be `None` if triggered from proxied events such as accessibility.
    """


@dataclass(kw_only=True)
class DragEndEvent(Event[EventControlType]):
    local_position: Offset = field(metadata={"data_field": "l"})
    """
    The local position in the coordinate system of the event receiver
    when the drag gesture has been completed.
    """

    global_position: Offset = field(metadata={"data_field": "g"})
    """
    The global position the pointer is located at when the drag gesture
    has been completed.
    """

    velocity: Offset = field(metadata={"data_field": "v"})
    """
    The velocity vector the pointer was moving when it stopped contacting the screen,
    in logical pixels per second.
    """

    primary_velocity: Optional[float] = field(
        default=None, metadata={"data_field": "pv"}
    )
    """
    The velocity the pointer was moving along the primary axis when it stopped
    contacting the screen, in logical pixels per second.
    """


@dataclass(kw_only=True)
class ForcePressEvent(Event[EventControlType]):
    local_position: Offset = field(metadata={"data_field": "l"})
    """
    The local position at which the pointer applied pressure.
    """

    global_position: Offset = field(metadata={"data_field": "g"})
    """
    The global position at which the pointer applied pressure.
    """

    pressure: float = field(metadata={"data_field": "p"})
    """
    The normalized pressure value reported by the device.
    """


@dataclass(kw_only=True)
class ScaleStartEvent(Event[EventControlType]):
    local_focal_point: Offset = field(metadata={"data_field": "lfp"})
    """
    The initial focal point of the pointers in contact with the screen,
    in local coordinates.
    """

    global_focal_point: Offset = field(metadata={"data_field": "gfp"})
    """
    The initial focal point of the pointers in contact with the screen,
    in global coordinates.
    """

    pointer_count: int = field(metadata={"data_field": "pc"})
    """
    The number of pointers being tracked by the gesture recognizer.

    Typically this is the number of fingers being used to pan the
    control using the gesture recognizer.
    """

    timestamp: Optional[Duration] = field(default=None, metadata={"data_field": "ts"})
    """
    Recorded timestamp of the source pointer event that triggered the scale event.

    Could be `None` if triggered from proxied events such as accessibility.
    """


@dataclass(kw_only=True)
class ScaleEndEvent(Event[EventControlType]):
    pointer_count: int = field(metadata={"data_field": "pc"})
    """
    The number of pointers being tracked by the gesture recognizer.

    Typically this is the number of fingers being used to pan the control
    using the gesture recognizer.
    """

    velocity: Offset = field(metadata={"data_field": "v"})
    """
    The velocity of the last pointer to be lifted off of the screen,
    in pixels per second.
    """


@dataclass(kw_only=True)
class ScaleUpdateEvent(Event[EventControlType]):
    local_focal_point: Offset = field(metadata={"data_field": "lfp"})
    """
    The focal point of the pointers in contact with the screen,
    in local coordinates.
    """

    global_focal_point: Offset = field(metadata={"data_field": "gfp"})
    """
    The focal point of the pointers in contact with the screen,
    in global coordinates.
    """

    focal_point_delta: Offset = field(metadata={"data_field": "fpd"})
    """
    The amount the gesture's focal point has moved in the coordinate space of the
    event receiver since the previous update.
    """

    pointer_count: int = field(metadata={"data_field": "pc"})
    """
    The number of pointers being tracked by the gesture recognizer.

    Typically this is the number of fingers being used to pan the widget using the
    gesture recognizer. Due to platform limitations, trackpad gestures count as two
    fingers even if more than two fingers are used.
    """

    horizontal_scale: float = field(metadata={"data_field": "hs"})
    """
    The scale implied by the average distance along the horizontal axis
    between the pointers in contact with the screen.

    This value must be greater than or equal to zero.
    """

    vertical_scale: float = field(metadata={"data_field": "vs"})
    """
    The scale implied by the average distance along the vertical axis
    between the pointers in contact with the screen.

    This value must be greater than or equal to zero.
    """

    scale: float = field(metadata={"data_field": "s"})
    """
    The scale implied by the average distance between the pointers in contact
    with the screen.

    This value must be greater than or equal to zero.
    """

    rotation: float = field(metadata={"data_field": "rot"})
    """
    The angle (in radians) implied by the first two pointers to enter
    in contact with the screen.
    """

    timestamp: Optional[Duration] = field(default=None, metadata={"data_field": "ts"})
    """
    Recorded timestamp of the source pointer event that triggered the scale event.

    Could be `None` if triggered from proxied events such as accessibility.
    """


@dataclass(kw_only=True)
class PointerEvent(Event[EventControlType]):
    kind: PointerDeviceType = field(metadata={"data_field": "k"})
    """
    The kind of input device for which the event was generated.
    """

    local_position: Offset = field(metadata={"data_field": "l"})
    """
    The position transformed into the event receiver's local coordinate
    system according to transform.
    """

    global_position: Offset = field(metadata={"data_field": "g"})
    """
    Coordinate of the position of the pointer, in logical pixels in
    the global coordinate space.
    """

    timestamp: Duration = field(metadata={"data_field": "ts"})
    """
    Time of event dispatch, relative to an arbitrary timeline.
    """

    device: float = field(metadata={"data_field": "dev"})
    """
    Unique identifier for the pointing device, reused across interactions.
    """

    pressure: float = field(metadata={"data_field": "ps"})
    """
    The pressure of the touch.

    This value is a number ranging from 0.0, indicating a touch with no discernible
    pressure, to 1.0, indicating a touch with "normal" pressure, and possibly beyond,
    indicating a stronger touch.
    For devices that do not detect pressure (e.g. mice), returns 1.0.
    """

    pressure_min: float = field(metadata={"data_field": "pMin"})
    """
    The minimum value that `pressure` can return for this pointer.

    For devices that do not detect pressure (e.g. mice), returns 1.0.
    This will always be a number less than or equal to 1.0.
    """

    pressure_max: float = field(metadata={"data_field": "pMax"})
    """
    The maximum value that `pressure` can return for this pointer.
    For devices that do not detect pressure (e.g. mice), returns 1.0.
    This will always be a greater than or equal to 1.0.
    """

    distance: float = field(metadata={"data_field": "dist"})
    """
    The distance of the detected object from the input surface.
    For instance, this value could be the distance of a stylus or
    finger from a touch screen, in arbitrary units on an arbitrary
    (not necessarily linear) scale. If the pointer is down, this is 0.0 by definition.
    """

    distance_max: float = field(metadata={"data_field": "distMax"})
    """
    The maximum value that `distance` can return for this pointer.

    If this input device cannot detect "hover touch" input events,
    then this will be `0.0`.
    """

    size: float = field(metadata={"data_field": "size"})
    """
    The area of the screen being pressed.

    This value is scaled to a range between 0 and 1.
    It can be used to determine fat touch events. This value is only
    set on Android and is a device specific approximation within the range
    of detectable values. So, for example, the value of 0.1 could mean a
    touch with the tip of the finger, 0.2 a touch with full finger,
    and 0.3 the full palm.
    """

    radius_major: float = field(metadata={"data_field": "rMj"})
    """
    The radius of the contact ellipse along the major axis, in logical pixels.
    """

    radius_minor: float = field(metadata={"data_field": "rMn"})
    """
    The radius of the contact ellipse along the minor axis, in logical pixels.
    """

    radius_min: float = field(metadata={"data_field": "rMin"})
    """
    The minimum value that could be reported for `radius_major` and `radius_minor`
    for this pointer, in logical pixels.
    """

    radius_max: float = field(metadata={"data_field": "rMax"})
    """
    The maximum value that could be reported for `radius_major` and `radius_minor`
    for this pointer, in logical pixels.
    """

    orientation: float = field(metadata={"data_field": "or"})
    """
    The orientation angle of the detected object, in radians.
    """

    tilt: float = field(metadata={"data_field": "tilt"})
    """
    The tilt angle of the detected object, in radians.
    """

    local_delta: Optional[Offset] = field(default=None, metadata={"data_field": "ld"})
    """
    The delta of the pointer's position since the event start, in logical pixels,
    within the local coordinate space.
    """

    global_delta: Optional[Offset] = field(default=None, metadata={"data_field": "gd"})
    """
    The delta of the pointer's position since the event start, in logical pixels,
    within the global coordinate space.
    """


@dataclass(kw_only=True)
class ScrollEvent(Event[EventControlType]):
    """The pointer issued a scroll event."""

    local_position: Offset = field(metadata={"data_field": "l"})
    """
    The coordinate of the position of the pointer, in logical pixels
    in the local coordinate space.
    """

    global_position: Offset = field(metadata={"data_field": "g"})
    """
    The coordinate of the position of the pointer, in logical pixels
    in the global coordinate space.
    """

    scroll_delta: Offset = field(metadata={"data_field": "sd"})
    """
    The amount to scroll, in logical pixels.
    """


HoverEvent = PointerEvent
