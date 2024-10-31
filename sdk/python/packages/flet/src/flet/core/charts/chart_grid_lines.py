from dataclasses import dataclass
from typing import List, Optional

from flet.core.types import ColorValue


@dataclass
class ChartGridLines:
    interval: Optional[float] = None
    color: Optional[ColorValue] = None
    width: Optional[float] = None
    dash_pattern: Optional[List[int]] = None
