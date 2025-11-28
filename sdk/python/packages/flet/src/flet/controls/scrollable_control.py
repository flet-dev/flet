from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from flet.controls.animation import AnimationCurve
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import Event, EventHandler
from flet.controls.duration import DurationValue
from flet.controls.keys import ScrollKey
from flet.controls.types import (
    Number,
    ScrollMode,
)

__all__ = ["OnScrollEvent", "ScrollDirection", "ScrollType", "ScrollableControl"]


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
class OnScrollEvent(Event["ScrollableControl"]):
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
    """

    auto_scroll: bool = False
    """
    Whether the scrollbar should automatically move its position to the end when
    children updated.

    Note:
        Must be `False` for [`scroll_to()`][(c).scroll_to] method to work.
    """

    scroll_interval: Number = 10
    """
    Throttling in milliseconds for [`on_scroll`][(c).] event.
    """

    on_scroll: Optional[EventHandler[OnScrollEvent]] = None
    """
    Called when scroll position is changed by a user.
    """

    async def scroll_to(
        self,
        offset: Optional[float] = None,
        delta: Optional[float] = None,
        scroll_key: Union[ScrollKey, str, int, float, bool, None] = None,
        duration: DurationValue = 0,
        curve: AnimationCurve = AnimationCurve.EASE,
    ):
        """
        Moves the scroll position.

        Args:
            offset: Absolute scroll target in pixels. A negative value is interpreted
                relative to the end (e.g. `-1` to jump to the very end).
            delta: Relative scroll change in pixels. Positive values scroll forward,
                negative values scroll backward.
            scroll_key: Key of the target control to scroll to.
            duration: The scroll animation duration.
            curve: The scroll animation curve.

        Notes:
            - Exactly one of `offset`, `delta` or `scroll_key` should be provided.
            - [`auto_scroll`][(c).] must be `False`.
            - This method is ineffective for controls (e.g.
                [`ListView`][flet.], [`GridView`][flet.]) that build items dynamically.

        Examples:
            ```python
            await products.scroll_to(offset=100, duration=1000)
            await products.scroll_to(offset=-1, duration=1000)  # to the end
            await products.scroll_to(delta=50)  # forward 50px
            await products.scroll_to(scroll_key="item_20", duration=500)
            ```
        """

        await self._invoke_method(
            "scroll_to",
            {
                "offset": offset,
                "delta": delta,
                "scroll_key": scroll_key,
                "duration": duration,
                "curve": curve,
            },
        )
