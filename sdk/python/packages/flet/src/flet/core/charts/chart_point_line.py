from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ChartPointLine:
    color: Optional[str] = field(default=None)
    width: Optional[float] = field(default=None)
    dash_pattern: Optional[List[int]] = field(default=None)
