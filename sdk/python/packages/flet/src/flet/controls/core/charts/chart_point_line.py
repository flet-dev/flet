from dataclasses import dataclass
from typing import Optional

from flet.controls.types import OptionalColorValue


@dataclass
class ChartPointLine:
    color: OptionalColorValue = None
    """
    The line's [color](https://flet.dev/docs/reference/colors).
    """

    width: Optional[float] = None
    """
    The line's width.
    """

    dash_pattern: Optional[list[int]] = None
    """
    The line's dash pattern.
    """

