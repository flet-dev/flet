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
    """
    The kind of scroll notification emitted by `ScrollableControl`.
    """

    START = "start"
    """
    Scrolling has started.
    """

    UPDATE = "update"
    """
    Scroll position changed.

    See [`OnScrollEvent.scroll_delta`][flet.].
    """

    END = "end"
    """
    Scrolling has ended.
    """

    USER = "user"
    """
    User scroll direction changed.

    See [`OnScrollEvent.direction`][flet.].
    """

    OVERSCROLL = "overscroll"
    """
    Viewport was overscrolled.

    See [`overscroll`][flet.OnScrollEvent.] and
    [`velocity`][flet.OnScrollEvent.] are available.
    """


class ScrollDirection(Enum):
    """
    User scroll direction reported by Flutter user-scroll notifications.

    Used by [`OnScrollEvent.direction`][flet.] when
    [`OnScrollEvent.event_type`][flet.] is [`ScrollType.USER`][flet.].
    """

    IDLE = "idle"
    """
    No active user-driven scroll direction.
    """

    FORWARD = "forward"
    """
    Scrolling in the forward axis direction.
    """

    REVERSE = "reverse"
    """
    Scrolling in the reverse axis direction.
    """


@dataclass
class OnScrollEvent(Event["ScrollableControl"]):
    """
    Payload for [`ScrollableControl.on_scroll`][flet.] handlers.
    """

    event_type: ScrollType
    """
    Logical type of the scroll notification.

    Determines which optional fields are populated:
    - [`ScrollType.UPDATE`][flet.]: [`scroll_delta`][(c).]
    - [`ScrollType.USER`][flet.]: [`direction`][(c).direction]
    - [`ScrollType.OVERSCROLL`][flet.]: [`overscroll`][(c).] and [`velocity`][(c).]
    """

    pixels: float
    """
    Current scroll offset in logical pixels.
    """

    min_scroll_extent: float
    """
    Minimum in-range value for [`pixels`][(c).].

    [`pixels`][(c).] may still be [`out_of_range`][(c).] during overscroll.
    For unbounded scrollables this value can be negative infinity.
    """

    max_scroll_extent: float
    """
    Maximum in-range value for [`pixels`][(c).].

    [`pixels`][(c).] may still be [`out_of_range`][(c).] during overscroll.
    For unbounded scrollables this value can be positive infinity.
    """

    viewport_dimension: float
    """
    Visible viewport extent along the scroll axis, in logical pixels.
    """

    scroll_delta: Optional[float] = None
    """
    Delta in logical pixels since the previous update.

    Populated for [`ScrollType.UPDATE`][flet.] notifications.
    """

    direction: Optional[ScrollDirection] = None
    """
    User scroll direction reported by Flutter.

    Populated for [`ScrollType.USER`][flet.] notifications.
    """

    overscroll: Optional[float] = None
    """
    Logical pixels that were prevented from being applied to `pixels`.

    Negative values indicate overscroll on the start side; positive values
    indicate overscroll on the end side. Populated for [`ScrollType.OVERSCROLL`][flet.].
    """

    velocity: Optional[float] = None
    """
    Scroll velocity when overscroll occurred, in logical pixels per second.

    Populated for [`ScrollType.OVERSCROLL`][flet.].
    """

    @property
    def out_of_range(self) -> bool:
        """
        Whether [`pixels`][(c).] is outside scroll extents.

        Returns:
            `True` if [`pixels`][(c).] < [`min_scroll_extent`][(c).] or
                [`pixels`][(c).] > [`max_scroll_extent`][(c).]; otherwise `False`.
        """
        return (
            self.pixels < self.min_scroll_extent or self.pixels > self.max_scroll_extent
        )

    @property
    def at_edge(self) -> bool:
        """
        Whether [`pixels`][(c).] is exactly at either scroll edge.

        Returns:
            `True` when `pixels` equals `min_scroll_extent` or
                `max_scroll_extent`; otherwise `False`.
        """
        return (
            self.pixels == self.min_scroll_extent
            or self.pixels == self.max_scroll_extent
        )

    @property
    def extent_before(self) -> float:
        """
        Quantity of content conceptually "before" the viewport.

        This corresponds to the content preceding the visible region in the
        current scroll direction.
        """
        return max(self.pixels - self.min_scroll_extent, 0.0)

    @property
    def extent_after(self) -> float:
        """
        Quantity of content conceptually "after" the viewport.

        This corresponds to the content following the visible region in the
        current scroll direction.
        """
        return max(self.max_scroll_extent - self.pixels, 0.0)

    @property
    def extent_total(self) -> float:
        """
        Total conceptual content extent available to the scrollable.

        Equivalent to: [`max_scroll_extent`][(c).] - [`min_scroll_extent`][(c).]
        + [`viewport_dimension`][(c).].
        """
        return self.max_scroll_extent - self.min_scroll_extent + self.viewport_dimension


@control(kw_only=True)
class ScrollableControl(Control):
    """
    Shared scroll behavior for controls that expose a scrollable viewport.

    This mixin-style control is inherited by controls such as
    [`Column`][flet.], [`Row`][flet.], [`View`][flet.],
    [`ListView`][flet.], and [`GridView`][flet.]. It provides a common API for:

    - enabling/disabling scrolling and scrollbar visibility via [`scroll`][(c).];
    - receiving throttled scroll notifications via [`on_scroll`][(c).] and
        [`scroll_interval`][(c).];
    - imperatively changing position with [`scroll_to()`][(c).scroll_to].
    """

    scroll: Optional[ScrollMode] = None
    """
    Enables a vertical scrolling for the Column to prevent its content overflow.
    """

    auto_scroll: bool = False
    """
    Whether the scrollbar should automatically move its position to the end when \
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
