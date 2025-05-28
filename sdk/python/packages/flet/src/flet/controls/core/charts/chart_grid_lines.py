from dataclasses import dataclass
from typing import Optional

from flet.controls.types import OptionalColorValue, OptionalNumber


@dataclass
class ChartGridLines:
    interval: OptionalNumber = None
    color: OptionalColorValue = None
    width: OptionalNumber = None
    dash_pattern: Optional[list[int]] = None
