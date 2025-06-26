import asyncio
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from flet.controls.animation import AnimationCurve
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import Event, OptionalEventHandler
from flet.controls.duration import OptionalDurationValue
from flet.controls.keys import ScrollKey
from flet.controls.types import (
    Number,
    OptionalNumber,
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

    Value is of type [`ScrollMode`](https://flet.dev/docs/reference/types/scrollmode) 
    and defaults to `ScrollMode.None`.
    """
    auto_scroll: bool = False
    """
    `True` if scrollbar should automatically move its position to the end when children 
    updated. Must be `False` for `scroll_to()` method to work.
    """
    scroll_interval: Number = 10
    """
    Throttling in milliseconds for `on_scroll` event.

    Defaults to `10`.
    """
    on_scroll: OptionalEventHandler[OnScrollEvent] = None
    """
    Fires when scroll position is changed by a user.

    Event handler argument is an instance of [`OnScrollEvent`](https://flet.dev/docs/reference/types/onscrollevent) 
    class.
    """

    def scroll_to(
        self,
        offset: OptionalNumber = None,
        delta: OptionalNumber = None,
        scroll_key: Union[ScrollKey, str, int, float, bool, None] = None,
        duration: OptionalDurationValue = None,
        curve: Optional[AnimationCurve] = None,
    ):
        """
        Moves scroll position to either absolute `offset`, relative `delta` or jump to
        the control with specified `key`.

        `offset` is an absolute value between minimum and maximum extents of a
        scrollable control, for example:

        ```python
        products.scroll_to(offset=100, duration=1000)
        ```

        `offset` could be a negative to scroll from the end of a scrollable. For
        example, to scroll to the very end:

        ```python
        products.scroll_to(offset=-1, duration=1000)
        ```

        `delta` allows moving scroll relatively to the current position. Use positive
        `delta` to scroll forward and negative `delta` to scroll backward. For example,
        to move scroll on 50 pixels forward:

        ```python
        products.scroll_to(delta=50)
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

            def scroll_to_key(e):
                cl.scroll_to(key="20", duration=1000)

            page.add(
                ft.Container(cl, border=ft.border.all(1)),
                ft.ElevatedButton("Scroll to key '20'", on_click=scroll_to_key),
            )

        ft.app(main)
        ```

        Note:
            `scroll_to()` method won't work with `ListView` and `GridView` controls
            building their items dynamically.

        `duration` is scrolling animation duration in milliseconds. Defaults to `0` -
        no animation.

        `curve` configures animation curve. Property value is [`AnimationCurve`](https://flet.dev/docs/reference/types/animationcurve)
        enum.
        Defaults to `AnimationCurve.EASE`.
        """
        asyncio.create_task(
            self.scroll_to_async(offset, delta, scroll_key, duration, curve)
        )

    async def scroll_to_async(
        self,
        offset: Optional[float] = None,
        delta: Optional[float] = None,
        scroll_key: Union[ScrollKey, str, int, float, bool, None] = None,
        duration: OptionalDurationValue = None,
        curve: Optional[AnimationCurve] = None,
    ):
        """
        Moves scroll position to either absolute `offset`, relative `delta` or jump to
        the control with specified `key`.

        `offset` is an absolute value between minimum and maximum extents of a
        scrollable control, for example:

        ```python
        products.scroll_to(offset=100, duration=1000)
        ```

        `offset` could be a negative to scroll from the end of a scrollable. For
        example, to scroll to the very end:

        ```python
        products.scroll_to(offset=-1, duration=1000)
        ```

        `delta` allows moving scroll relatively to the current position. Use positive
        `delta` to scroll forward and negative `delta` to scroll backward. For example,
        to move scroll on 50 pixels forward:

        ```python
        products.scroll_to(delta=50)
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

            def scroll_to_key(e):
                cl.scroll_to(key="20", duration=1000)

            page.add(
                ft.Container(cl, border=ft.border.all(1)),
                ft.ElevatedButton("Scroll to key '20'", on_click=scroll_to_key),
            )

        ft.app(main)
        ```

        Note:
            `scroll_to()` method won't work with `ListView` and `GridView` controls
            building their items dynamically.

        `duration` is scrolling animation duration in milliseconds. Defaults to `0` -
        no animation.

        `curve` configures animation curve. Property value is [`AnimationCurve`](https://flet.dev/docs/reference/types/animationcurve)
        enum.
        Defaults to `AnimationCurve.EASE`.
        """

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
