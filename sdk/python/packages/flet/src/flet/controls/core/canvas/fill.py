from typing import Optional

from flet.controls.base_control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint


@control("Fill")
class Fill(Shape):
    """
    Fills the canvas with the given `Paint`.

    To fill the canvas with a solid color and blend mode, consider `Color` shape
    instead.
    """

    paint: Optional[Paint] = None
    """
    A style to fill the canvas with. The value of this property is the instance of
    [`Paint`](https://flet.dev/docs/reference/types/paint) class.
    """

