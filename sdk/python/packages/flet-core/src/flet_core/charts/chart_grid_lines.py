import dataclasses
from dataclasses import field
from typing import List, Optional


@dataclasses.dataclass
class ChartGridLines:
    interval: Optional[float] = field(default=None)
    color: Optional[str] = field(default=None)
    width: Optional[float] = field(default=None)
    dash_pattern: Optional[List[int]] = field(default=None)
