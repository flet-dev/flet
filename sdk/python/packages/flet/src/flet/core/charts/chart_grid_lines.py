from dataclasses import dataclass
from typing import List, Optional

from flet.core.types import OptionalColorValue, OptionalNumber


@dataclass
class ChartGridLines:
    interval: OptionalNumber = None
    color: OptionalColorValue = None
    width: OptionalNumber = None
    dash_pattern: Optional[List[int]] = None
