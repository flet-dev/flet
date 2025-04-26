from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from flet.controls.types import Number

__all__ = [
    "Alignment",
    "Axis",
    "OptionalAlignment",
    "OptionalAxis",
]


class Axis(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


@dataclass
class Alignment:
    x: Number
    y: Number

    @classmethod
    def bottom_center(cls) -> "Alignment":
        return Alignment(0, 1)

    @classmethod
    def bottom_left(cls) -> "Alignment":
        return Alignment(-1, 1)

    @classmethod
    def bottom_right(cls) -> "Alignment":
        return Alignment(1, 1)

    @classmethod
    def center(cls) -> "Alignment":
        return Alignment(0, 0)

    @classmethod
    def center_left(cls) -> "Alignment":
        return Alignment(-1, 0)

    @classmethod
    def center_right(cls) -> "Alignment":
        return Alignment(1, 0)

    @classmethod
    def top_center(cls) -> "Alignment":
        return Alignment(0, -1)

    @classmethod
    def top_left(cls) -> "Alignment":
        return Alignment(-1, -1)

    @classmethod
    def top_right(cls) -> "Alignment":
        return Alignment(1, -1)


# Constants
# bottom_center = Alignment(0, 1)
# bottom_left = Alignment(-1, 1)
# bottom_right = Alignment(1, 1)
# center = Alignment(0, 0)
# center_left = Alignment(-1, 0)
# center_right = Alignment(1, 0)
# top_center = Alignment(0, -1)
# top_left = Alignment(-1, -1)
# top_right = Alignment(1, -1)

# Typing
OptionalAlignment = Optional[Alignment]
OptionalAxis = Optional[Axis]
