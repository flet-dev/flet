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

    Defaults to `ScrollMode.None`.
    """

    auto_scroll: bool = False
    """
    `True` if scrollbar should automatically move its position to the end when children
    updated. Must be `False` for `scroll_to()` method to work.
    """

    scroll_interval: Number = 10
    """
    Throttling in milliseconds for `on_scroll` event.
    """

    on_scroll: Optional[EventHandler[OnScrollEvent]] = None
    """
    Called when scroll position is changed by a user.
    class.
    """

    async def scroll_to(
        self,
        offset: Optional[float] = None,
        delta: Optional[float] = None,
        scroll_key: Union[ScrollKey, str, int, float, bool, None] = None,
        duration: Optional[DurationValue] = None,
        curve: Optional[AnimationCurve] = None,
    ):
        """
        Moves scroll position to either absolute `offset`, relative `delta` or jump to
        the control with specified `key`.

        `offset` is an absolute value between minimum and maximum extents of a
        scrollable control, for example:

        ```python
        await products.scroll_to(offset=100, duration=1000)
        ```

        `offset` could be a negative to scroll from the end of a scrollable. For
        example, to scroll to the very end:

        ```python
        await products.scroll_to(offset=-1, duration=1000)
        ```

        `delta` allows moving scroll relatively to the current position. Use positive
        `delta` to scroll forward and negative `delta` to scroll backward. For example,
        to move scroll on 50 pixels forward:

        ```python
        await products.scroll_to(delta=50)
        ```

        `key` allows moving scroll position to a control with specified `key`. Most of
        Flet controls have `key` property which is translated to Flutter as
        "global key". `key` must be unique for the entire page/view. For example:

        ```python
        import flet as ft


        def main(page: ft.Page):
            cl = ft.Column(
                spacing=10,
                height=200,
                width=200,
                scroll=ft.ScrollMode.ALWAYS,
            )
            for i in range(0, 50):
                cl.controls.append(ft.Text(f"Text line {i}", key=str(i)))

            async def scroll_to_key(e):
                await cl.scroll_to(scroll_key="20", duration=1000)

            page.add(
                ft.Container(cl, border=ft.border.all(1)),
                ft.ElevatedButton("Scroll to key '20'", on_click=scroll_to_key),
            )


        ft.run(main)
        ```

        Note:
            `scroll_to()` method won't work with `ListView` and `GridView` controls
            building their items dynamically.

        `duration` is scrolling animation duration in milliseconds. Defaults to `0` -
        no animation.

        `curve` configures animation curve. Property value is
        [`AnimationCurve`][flet.AnimationCurve]
        enum.

        Defaults to `AnimationCurve.EASE`.
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
