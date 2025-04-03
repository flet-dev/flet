import time
from dataclasses import dataclass, field
from typing import Optional

from flet.core.animation import AnimationCurve
from flet.core.control import Control, control
from flet.core.control_event import ControlEvent
from flet.core.types import OptionalEventCallable, OptionalNumber, ScrollMode

__all__ = ["ScrollableControl", "OnScrollEvent"]


@dataclass
class OnScrollEvent(ControlEvent):
    event_type: str = field(metadata={"data_field": "t"})
    pixels: float = field(metadata={"data_field": "p"})
    min_scroll_extent: float = field(metadata={"data_field": "minse"})
    max_scroll_extent: float = field(metadata={"data_field": "maxse"})
    viewport_dimension: float = field(metadata={"data_field": "vd"})
    scroll_delta: Optional[float] = field(metadata={"data_field": "sd"}, default=None)
    direction: Optional[str] = field(metadata={"data_field": "dir"}, default=None)
    overscroll: Optional[float] = field(metadata={"data_field": "os"}, default=None)
    velocity: Optional[float] = field(metadata={"data_field": "v"}, default=None)


@control(kw_only=True)
class ScrollableControl(Control):
    scroll: Optional[ScrollMode] = None
    auto_scroll: Optional[bool] = None
    reverse: Optional[bool] = None
    on_scroll_interval: OptionalNumber = None
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
