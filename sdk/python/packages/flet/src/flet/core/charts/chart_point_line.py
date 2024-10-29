from dataclasses import dataclass, field
from typing import List, Optional

from flet.core.types import ColorValue


@dataclass
class ChartPointLine:
    color: Optional[ColorValue] = field(default=None)
    width: Optional[float] = field(default=None)
    dash_pattern: Optional[List[int]] = field(default=None)
