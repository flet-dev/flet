from dataclasses import dataclass
from typing import List, Optional

from flet.controls.types import OptionalColorValue, OptionalNumber


@dataclass
class ChartGridLines:
    interval: OptionalNumber = None
    color: OptionalColorValue = None
    width: OptionalNumber = None
    dash_pattern: Optional[List[int]] = None
