import dataclasses
from dataclasses import field
from typing import Dict, Optional, Union

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


@dataclasses.dataclass
class ChartDotMarker:
    pass


@dataclasses.dataclass
class ChartCircleDotMarker(ChartDotMarker):
    type: str = field(default="circle")
    color: Optional[str] = field(default=None)
    radius: Optional[float] = field(default=None)
    stroke_color: Optional[str] = field(default=None)
    stroke_width: Optional[float] = field(default=None)


@dataclasses.dataclass
class ChartSquareDotMarker(ChartDotMarker):
    type: str = field(default="square")
    color: Optional[str] = field(default=None)
    size: Optional[float] = field(default=None)
    stroke_color: Optional[str] = field(default=None)
    stroke_width: Optional[float] = field(default=None)


@dataclasses.dataclass
class ChartCrossDotMarker(ChartDotMarker):
    type: str = field(default="cross")
    color: Optional[str] = field(default=None)
    size: Optional[float] = field(default=None)
    width: Optional[float] = field(default=None)
