from typing import List, Optional

from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control, control
from flet.controls.control_event import ControlEvent
from flet.controls.core.canvas.shape import Shape
from flet.controls.types import OptionalEventCallable, OptionalNumber


class CanvasResizeEvent(ControlEvent):
    width: float
    height: float


@control("Canvas")
class Canvas(ConstrainedControl):
    shapes: Optional[List[Shape]] = None
    content: Optional[Control] = None
    resize_interval: OptionalNumber = None
    on_resize = OptionalEventCallable[CanvasResizeEvent]
