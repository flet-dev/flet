import dataclasses
from enum import Enum
from typing import Union


class Axis(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


@dataclasses.dataclass
class Alignment:
    x: Union[float, int]
    y: Union[float, int]


bottom_center = Alignment(0, 1)
bottom_left = Alignment(-1, 1)
bottom_right = Alignment(1, 1)
center = Alignment(0, 0)
center_left = Alignment(-1, 0)
center_right = Alignment(1, 0)
top_center = Alignment(0, -1)
top_left = Alignment(-1, -1)
top_right = Alignment(1, -1)
