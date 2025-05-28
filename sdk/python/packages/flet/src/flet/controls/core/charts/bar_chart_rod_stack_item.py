from typing import Optional

from flet.controls.base_control import control
from flet.controls.border import BorderSide
from flet.controls.control import Control
from flet.controls.types import OptionalColorValue, OptionalNumber


@control("i")
class BarChartRodStackItem(Control):
    from_y: OptionalNumber = None
    """
    The starting position of this item inside a bar rod.
    """

    to_y: OptionalNumber = None
    """
    The ending position of this item inside a bar rod.
    """

    color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) of this item.
    """

    border_side: Optional[BorderSide] = None
    """
    A border around this item.

    Value is of type [`BorderSide`](https://flet.dev/docs/reference/types/borderside).
    """
