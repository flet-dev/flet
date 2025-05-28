import asyncio
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from flet.controls.animation import AnimationCurve
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import ControlEvent
from flet.controls.duration import OptionalDurationValue
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
    """
    Enables a vertical scrolling for the Column to prevent its content overflow.

    Value is of type [`ScrollMode`](/docs/reference/types/scrollmode) and defaults to 
    `ScrollMode.None`.
    """
    auto_scroll: bool = False
    """
    `True` if scrollbar should automatically move its position to the end when children 
    updated. Must be `False` for `scroll_to()` method to work.
    """
    reverse: bool = False
    """
    Defines whether the scroll view scrolls in the reading direction.

    Defaults to `False`.
    """
    scroll_interval: Number = 10
    """
    Throttling in milliseconds for `on_scroll` event.

    Defaults to `10`.
    """
    on_scroll: OptionalEventCallable[OnScrollEvent] = None
    """
    Fires when scroll position is changed by a user.

    Event handler argument is an instance of [`OnScrollEvent`](/docs/reference/types/onscrollevent) 
    class.
    """

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
