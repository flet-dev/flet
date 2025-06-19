from dataclasses import dataclass, field
from typing import Optional

from flet.controls.control_event import ControlEvent, Event, EventControlType
from flet.controls.duration import Duration, OptionalDuration
from flet.controls.types import PointerDeviceType

__all__ = [
    "TapEvent",
    "MultiTapEvent",
    "LongPressStartEvent",
    "LongPressEndEvent",
    "DragStartEvent",
    "DragUpdateEvent",
    "DragEndEvent",
    "ScaleStartEvent",
    "ScaleUpdateEvent",
    "ScaleEndEvent",
    "HoverEvent",
    "ScrollEvent",
    "PointerEvent",
]


@dataclass(kw_only=True)
class TapEvent(Event[EventControlType]):
    kind: Optional[str] = field(default=None, metadata={"data_field": "k"})
    local_x: Optional[float] = field(default=None, metadata={"data_field": "lx"})
    local_y: Optional[float] = field(default=None, metadata={"data_field": "ly"})
    global_x: Optional[float] = field(default=None, metadata={"data_field": "gx"})
    global_y: Optional[float] = field(default=None, metadata={"data_field": "gy"})


@dataclass(kw_only=True)
class MultiTapEvent(ControlEvent):
    correct_touches: bool = field(metadata={"data_field": "ct"})


@dataclass(kw_only=True)
class LongPressStartEvent(Event[EventControlType]):
    local_x: float = field(metadata={"data_field": "lx"})
    local_y: float = field(metadata={"data_field": "ly"})
    global_x: float = field(metadata={"data_field": "gx"})
    global_y: float = field(metadata={"data_field": "gy"})


@dataclass(kw_only=True)
class LongPressEndEvent(Event[EventControlType]):
    local_x: float = field(metadata={"data_field": "lx"})
    local_y: float = field(metadata={"data_field": "ly"})
    global_x: float = field(metadata={"data_field": "gx"})
    global_y: float = field(metadata={"data_field": "gy"})
    velocity_x: float = field(metadata={"data_field": "vx"})
    velocity_y: float = field(metadata={"data_field": "vy"})


@dataclass(kw_only=True)
class DragStartEvent(Event[EventControlType]):
    kind: PointerDeviceType = field(metadata={"data_field": "k"})
    local_x: float = field(metadata={"data_field": "lx"})
    local_y: float = field(metadata={"data_field": "ly"})
    global_x: float = field(metadata={"data_field": "gx"})
    global_y: float = field(metadata={"data_field": "gy"})
    timestamp: OptionalDuration = field(default=None, metadata={"data_field": "ts"})


@dataclass(kw_only=True)
class DragUpdateEvent(Event[EventControlType]):
    local_x: float = field(metadata={"data_field": "lx"})
    local_y: float = field(metadata={"data_field": "ly"})
    global_x: float = field(metadata={"data_field": "gx"})
    global_y: float = field(metadata={"data_field": "gy"})
    delta_x: float = field(metadata={"data_field": "dx"})
    delta_y: float = field(metadata={"data_field": "dy"})
    primary_delta: Optional[float] = field(default=None, metadata={"data_field": "pd"})
    timestamp: OptionalDuration = field(default=None, metadata={"data_field": "ts"})


@dataclass(kw_only=True)
class DragEndEvent(Event[EventControlType]):
    local_x: float = field(metadata={"data_field": "lx"})
    local_y: float = field(metadata={"data_field": "ly"})
    global_x: float = field(metadata={"data_field": "gx"})
    global_y: float = field(metadata={"data_field": "gy"})
    velocity_x: float = field(metadata={"data_field": "vx"})
    velocity_y: float = field(metadata={"data_field": "vy"})
    primary_velocity: Optional[float] = field(
        default=None, metadata={"data_field": "pv"}
    )


@dataclass(kw_only=True)
class ScaleStartEvent(Event[EventControlType]):
    focal_point_x: float = field(metadata={"data_field": "fpx"})
    focal_point_y: float = field(metadata={"data_field": "fpy"})
    local_focal_point_x: float = field(metadata={"data_field": "lfpx"})
    local_focal_point_y: float = field(metadata={"data_field": "lfpy"})
    pointer_count: int = field(metadata={"data_field": "pc"})
    timestamp: OptionalDuration = field(metadata={"data_field": "ts"})


@dataclass(kw_only=True)
class ScaleEndEvent(Event[EventControlType]):
    pointer_count: int = field(metadata={"data_field": "pc"})
    velocity_x: float = field(metadata={"data_field": "vx"})
    velocity_y: float = field(metadata={"data_field": "vy"})


@dataclass(kw_only=True)
class ScaleUpdateEvent(Event[EventControlType]):
    focal_point_x: float = field(metadata={"data_field": "fpx"})
    focal_point_y: float = field(metadata={"data_field": "fpy"})
    focal_point_delta_x: float = field(metadata={"data_field": "fpdx"})
    focal_point_delta_y: float = field(metadata={"data_field": "fpdy"})
    local_focal_point_x: float = field(metadata={"data_field": "lfpx"})
    local_focal_point_y: float = field(metadata={"data_field": "lfpy"})
    pointer_count: int = field(metadata={"data_field": "pc"})
    horizontal_scale: float = field(metadata={"data_field": "hs"})
    vertical_scale: float = field(metadata={"data_field": "vs"})
    scale: float = field(metadata={"data_field": "s"})
    rotation: float = field(metadata={"data_field": "rot"})
    timestamp: OptionalDuration = field(metadata={"data_field": "ts"})


@dataclass(kw_only=True)
class PointerEvent(Event[EventControlType]):
    kind: PointerDeviceType = field(metadata={"data_field": "k"})
    local_x: float = field(metadata={"data_field": "lx"})
    local_y: float = field(metadata={"data_field": "ly"})
    global_x: float = field(metadata={"data_field": "gx"})
    global_y: float = field(metadata={"data_field": "gy"})
    timestamp: Duration = field(metadata={"data_field": "ts"})
    view_id: int = field(metadata={"data_field": "vId"})
    buttons: float = field(metadata={"data_field": "btt"})
    obscured: bool = field(metadata={"data_field": "obs"})
    device: float = field(metadata={"data_field": "dev"})
    pressure: float = field(metadata={"data_field": "ps"})
    pressure_min: float = field(metadata={"data_field": "pMin"})
    pressure_max: float = field(metadata={"data_field": "pMax"})
    distance: float = field(metadata={"data_field": "dist"})
    distance_max: float = field(metadata={"data_field": "distMax"})
    size: float = field(metadata={"data_field": "size"})
    radius_major: float = field(metadata={"data_field": "rMj"})
    radius_minor: float = field(metadata={"data_field": "rMn"})
    radius_min: float = field(metadata={"data_field": "rMin"})
    radius_max: float = field(metadata={"data_field": "rMax"})
    orientation: float = field(metadata={"data_field": "or"})
    tilt: float = field(metadata={"data_field": "tilt"})
    embedder_id: float = field(metadata={"data_field": "eId"})
    delta_x: Optional[float] = field(metadata={"data_field": "dx"})
    delta_y: Optional[float] = field(metadata={"data_field": "dy"})


@dataclass(kw_only=True)
class ScrollEvent(Event[EventControlType]):
    local_x: float = field(metadata={"data_field": "lx"})
    local_y: float = field(metadata={"data_field": "ly"})
    global_x: float = field(metadata={"data_field": "gx"})
    global_y: float = field(metadata={"data_field": "gy"})
    scroll_delta_x: float = field(metadata={"data_field": "sdx"})
    scroll_delta_y: float = field(metadata={"data_field": "sdy"})


HoverEvent = PointerEvent
