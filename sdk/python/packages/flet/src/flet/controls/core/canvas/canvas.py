from dataclasses import dataclass, field
from typing import List, Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import ControlEvent
from flet.controls.core.canvas.shape import Shape
from flet.controls.types import OptionalEventCallable, OptionalNumber


@dataclass
class CanvasResizeEvent(ControlEvent):
    width: float = field(metadata={"data_field": "w"})
    height: float = field(metadata={"data_field": "h"})


@control("Canvas")
class Canvas(ConstrainedControl):
    shapes: List[Shape] = field(default_factory=list)
    content: Optional[Control] = None
    resize_interval: OptionalNumber = None
    on_resize: OptionalEventCallable[CanvasResizeEvent] = None
