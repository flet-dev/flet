import dataclasses
from enum import Enum
from typing import Optional

from flet.controls.types import Number

__all__ = [
    "Alignment",
    "Axis",
    "OptionalAlignment",
    "OptionalAxis",
    "bottom_center",
    "bottom_left",
    "bottom_right",
    "center",
    "center_left",
    "center_right",
    "top_center",
    "top_left",
    "top_right",
]


class Axis(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


@dataclasses.dataclass
class Alignment:
    x: Number
    y: Number


# Constants
bottom_center = Alignment(0, 1)
bottom_left = Alignment(-1, 1)
bottom_right = Alignment(1, 1)
center = Alignment(0, 0)
center_left = Alignment(-1, 0)
center_right = Alignment(1, 0)
top_center = Alignment(0, -1)
top_left = Alignment(-1, -1)
top_right = Alignment(1, -1)

# Typing
OptionalAlignment = Optional[Alignment]
OptionalAxis = Optional[Axis]
