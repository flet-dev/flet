from dataclasses import dataclass
from typing import Optional

from flet.controls.types import OptionalColorValue


@dataclass
class ChartPointLine:
    color: OptionalColorValue = None
    width: Optional[float] = None
    dash_pattern: Optional[list[int]] = None
