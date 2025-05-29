from dataclasses import dataclass
from typing import Optional

from flet.controls.types import OptionalColorValue, OptionalNumber


@dataclass
class ChartGridLines:
    """
    Configures the appearance of horizontal and vertical grid lines within the chart.
    """

    interval: OptionalNumber = None
    """
    The interval between grid lines.

    Defaults to `1`.
    """

    color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) of a grid line.
    """

    width: OptionalNumber = None
    """
    The width of a grid line.

    Defaults to `1`.
    """

    dash_pattern: Optional[list[int]] = None
    """
    Defines dash effect of the line. The value is a circular list of dash offsets
    and lengths. For example, the list `[5, 10]` would result in dashes 5 pixels long
    followed by blank spaces 10 pixels long. By default, a solid line is drawn.
    """

