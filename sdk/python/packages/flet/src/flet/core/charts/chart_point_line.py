from dataclasses import dataclass
from typing import List, Optional

from flet.core.types import OptionalColorValue


@dataclass
class ChartPointLine:
    color: OptionalColorValue = None
    width: Optional[float] = None
    dash_pattern: Optional[List[int]] = None
