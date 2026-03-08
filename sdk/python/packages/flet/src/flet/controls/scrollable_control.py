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

__all__ = [
    "OnScrollEvent",
    "ScrollDirection",
    "ScrollType",
    "ScrollableControl",
    "Scrollbar",
    "ScrollbarOrientation",
]


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


class ScrollbarOrientation(Enum):
    """
    Defines the edge/side of the viewport where the scrollbar is shown.
    """

    LEFT = "left"
    """
    Places the scrollbar on the left/leading edge of a vertical scrollable.
    """

    RIGHT = "right"
    """
    Places the scrollbar on the right/trailing edge of a vertical scrollable.
    """

    TOP = "top"
    """
    Places the scrollbar above a horizontal scrollable.
    """

    BOTTOM = "bottom"
    """
    Places the scrollbar below a horizontal scrollable.
    """


@dataclass
class Scrollbar:
    """
    Configures the scrollbar that scrollable controls render for their content.
    """

    mode: ScrollMode = ScrollMode.AUTO
    """
    Scroll behavior mode baseline.

    This keeps parity with legacy [`ScrollMode`][flet.] values when `scroll`
    was enum-only.
    """

    thumb_visibility: Optional[bool] = None
    """
    Whether this scrollbar's thumb should be always be visible, even when not being
    scrolled. When `False`, the scrollbar will be shown during scrolling and
    will fade out otherwise.

    If `None`, then [`ScrollbarTheme.thumb_visibility`][flet.] is used.
    If that is also `None`, defaults to `False`.
    """

    track_visibility: Optional[bool] = None
    """
    Indicates whether the scrollbar track should be visible,
    so long as the [thumb][(c).thumb_visibility] is visible.

    If `None`, then [`ScrollbarTheme.track_visibility`][flet.] is used.
    If that is also `None`, defaults to `False`.
    """

    thickness: Optional[Number] = None
    """
    Controls the cross-axis size of the scrollbar in logical pixels.
    The thickness of the scrollbar in the cross axis of the scrollable.

    If `None`, the default value is platform dependent:
    `4.0` pixels on Android
    ([`Page.platform`][flet.] == [`PagePlatform.ANDROID`][flet.]);
    `3.0` pixels on iOS ([`Page.platform`][flet.] == [`PagePlatform.IOS`][flet.]);
    `8.0` pixels on the remaining platforms.
    """

    radius: Optional[Number] = None
    """
    Circular radius of the scrollbar thumb's rounded rectangle corners in logical
    pixels. If `None`, platform defaults are used.

    The radius of the scrollbar thumb's rounded rectangle corners.

    If `None`, the default value is platform dependent:
    no radius is applied on Android
    ([`Page.platform`][flet.] == [`PagePlatform.ANDROID`][flet.]);
    `1.5` pixels on iOS ([`Page.platform`][flet.] == [`PagePlatform.IOS`][flet.]);
    `8.0` pixels on the remaining platforms.
    """

    interactive: Optional[bool] = None
    """
    Whether this scroll bar should be interactive and respond to dragging on the
    thumb, or tapping in the track area.

    When `False`, the scrollbar will not respond to gesture or hover events, and will
    allow to click through it.

    If `None`, defaults to `True`, unless on Android, where it defaults to `False`.
    """

    orientation: Optional[ScrollbarOrientation] = None
    """
    Specifies where the scrollbar should appear relative to the scrollable.

    If `None`, for a vertical scroll, defaults to [`ScrollbarOrientation.RIGHT`][flet.]
    for left-to-right text direction and [`ScrollbarOrientation.LEFT`][flet.]
    for right-to-left text direction, while for a horizontal scroll, it defaults to
    [`ScrollbarOrientation.BOTTOM`][flet.].

    Note:
        [`ScrollbarOrientation.TOP`][flet.] and [`ScrollbarOrientation.BOTTOM`][flet.]
        can only be used with a vertical scroll; [`ScrollbarOrientation.LEFT`][flet.]
        and [`ScrollbarOrientation.RIGHT`][flet.] can only be used with a horizontal
        scroll.
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

    scroll: Optional[Union[ScrollMode, Scrollbar]] = None
    """
    Defines the scroll bar configuration of this control.

    Can be a [`Scrollbar`][flet.] instance for full control over the appearance of the
    scrollbar, or a [`ScrollMode`][flet.] value, for ready-made scrollbar behaviors.
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
