from dataclasses import dataclass
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
    """
    Used to define an alignment relative to the center.
    """

    x: Number
    """
    Represents the horizontal distance from the center. It's value ranges between
    `-1.0` and `1.0`.
    """

    y: Number
    """
    Represents the vertical distance from the center. It's value ranges between
    `-1.0` and `1.0`.
    """

    @classmethod
    def bottom_center(cls) -> "Alignment":
        """
        Represents the bottom center and is equivalent to `Alignment(0.0, 1.0)`.
        """
        return Alignment(0, 1)

    @classmethod
    def bottom_left(cls) -> "Alignment":
        """
        Represents the bottom left corner and is equivalent to `Alignment(-1.0, 1.0)`.
        """
        return Alignment(-1, 1)

    @classmethod
    def bottom_right(cls) -> "Alignment":
        """
        Represents the bottom right corner and is equivalent to `Alignment(1.0, 1.0)`.
        """
        return Alignment(1, 1)

    @classmethod
    def center(cls) -> "Alignment":
        """
        Represents the center and is equivalent to `Alignment(0.0, 0.0)`.
        """
        return Alignment(0, 0)

    @classmethod
    def center_left(cls) -> "Alignment":
        """
        Represents the center left and is equivalent to `Alignment(-1.0, 0.0)`.
        """
        return Alignment(-1, 0)

    @classmethod
    def center_right(cls) -> "Alignment":
        """
        Represents the center right and is equivalent to `Alignment(1.0, 0.0)`.
        """
        return Alignment(1, 0)

    @classmethod
    def top_center(cls) -> "Alignment":
        """
        Represents the top center and is equivalent to `Alignment(0.0, -1.0)`.
        """
        return Alignment(0, -1)

    @classmethod
    def top_left(cls) -> "Alignment":
        """
        Represents the top left corner and is equivalent to `Alignment(-1.0, -1.0)`.
        """
        return Alignment(-1, -1)

    @classmethod
    def top_right(cls) -> "Alignment":
        """
        Represents the top right corner and is equivalent to `Alignment(1.0, -1.0)`.
        """
        return Alignment(1, -1)
    

# Typing
OptionalAlignment = Optional[Alignment]
OptionalAxis = Optional[Axis]
