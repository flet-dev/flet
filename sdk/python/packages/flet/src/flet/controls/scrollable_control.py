import asyncio
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from flet.controls.animation import AnimationCurve
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import ControlEvent
from flet.controls.duration import Duration, DurationValue, OptionalDurationValue
from flet.controls.types import (
    Number,
    OptionalEventCallable,
    OptionalNumber,
    OptionalString,
    ScrollMode,
)

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
    event_type: ScrollType
    pixels: float
    min_scroll_extent: float
    max_scroll_extent: float
    viewport_dimension: float
    scroll_delta: Optional[float] = None
    direction: Optional[ScrollDirection] = None
    overscroll: Optional[float] = None
    velocity: Optional[float] = None


@control(kw_only=True)
class ScrollableControl(Control):
    scroll: Optional[ScrollMode] = None
    auto_scroll: bool = False
    reverse: bool = False
    scroll_interval: Number = 10
    on_scroll: OptionalEventCallable[OnScrollEvent] = None

    def scroll_to(
        self,
        offset: OptionalNumber = None,
        delta: OptionalNumber = None,
        scroll_key: OptionalString = None,
        duration: OptionalDurationValue = None,
        curve: Optional[AnimationCurve] = None,
    ):
        asyncio.create_task(
            self.scroll_to_async(offset, delta, scroll_key, duration, curve)
        )

    async def scroll_to_async(
        self,
        offset: Optional[float] = None,
        delta: Optional[float] = None,
        scroll_key: Optional[str] = None,
        duration: OptionalDurationValue = None,
        curve: Optional[AnimationCurve] = None,
    ):
        await self._invoke_method_async(
            "scroll_to",
            {
                "offset": offset,
                "delta": delta,
                "scroll_key": scroll_key,
                "duration": duration,
                "curve": curve,
            },
        )
