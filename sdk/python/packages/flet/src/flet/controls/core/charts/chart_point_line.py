from dataclasses import dataclass
from typing import List, Optional

from flet.controls.types import OptionalColorValue


@dataclass
class ChartPointLine:
    color: OptionalColorValue = None
    width: Optional[float] = None
    dash_pattern: Optional[List[int]] = None
