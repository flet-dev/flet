import dataclasses
from dataclasses import field
from typing import List, Optional

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


@dataclasses.dataclass
class GridLines:
    show: bool = field(default=True)
    interval: Optional[float] = field(default=None)
    color: Optional[str] = field(default=None)
    stroke_width: Optional[float] = field(default=None)
    dash_pattern: Optional[List[int]] = field(default=None)
