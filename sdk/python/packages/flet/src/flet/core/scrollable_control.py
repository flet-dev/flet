import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from flet.core.animation import AnimationCurve
from flet.core.control import Control, control
from flet.core.control_event import ControlEvent
from flet.core.types import Number, OptionalEventCallable, ScrollMode

__all__ = ["ScrollableControl", "OnScrollEvent", "ScrollType", "ScrollDirection"]


class ScrollType(Enum):
    START = "start"
    UPDATE = "update"
    END = "end"
    USER = "user"
    OVERSCROLL = "overscroll"


class ScrollDirection(Enum):
    IDLE = "idle"
    FORWARD = "forward"
    REVERSE = "reverse"


@dataclass
class OnScrollEvent(ControlEvent):
    event_type: ScrollType = field(metadata={"data_field": "t"})
    pixels: float = field(metadata={"data_field": "p"})
    min_scroll_extent: float = field(metadata={"data_field": "minse"})
    max_scroll_extent: float = field(metadata={"data_field": "maxse"})
    viewport_dimension: float = field(metadata={"data_field": "vd"})
    scroll_delta: Optional[float] = field(metadata={"data_field": "sd"}, default=None)
    direction: Optional[ScrollDirection] = field(
        metadata={"data_field": "dir"}, default=None
    )
    overscroll: Optional[float] = field(metadata={"data_field": "os"}, default=None)
    velocity: Optional[float] = field(metadata={"data_field": "v"}, default=None)


@control(kw_only=True)
class ScrollableControl(Control):
    scroll: Optional[ScrollMode] = None
    auto_scroll: bool = False
    reverse: bool = False
    on_scroll_interval: Number = 10
    on_scroll: OptionalEventCallable[OnScrollEvent] = None

    def scroll_to(
        self,
        offset: Optional[float] = None,
        delta: Optional[float] = None,
        key: Optional[str] = None,
        duration: Optional[int] = None,
        curve: Optional[AnimationCurve] = None,
    ):
        m = {
            "n": "scroll_to",
            "i": str(time.time()),
            "p": {
                "offset": offset,
                "delta": delta,
                "key": key,
                "duration": duration,
                "curve": curve.value if curve is not None else None,
            },
        }
        self._set_attr_json("method", m)
        self.update()
