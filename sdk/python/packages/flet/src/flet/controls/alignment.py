from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, Optional

from flet.controls.types import Number

__all__ = [
    "Alignment",
    "Axis",
]


class Axis(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


@dataclass
class Alignment:
    """
    Defines an alignment relative to the center.

    ![overview](https://raw.githubusercontent.com/flet-dev/examples/v1-docs/python/controls/types/alignment/media/overview.png){width="80%"}
    /// caption
    ///
    """

    x: Number
    """
    Represents the horizontal distance from the center.

    It's value ranges between `-1.0` and `1.0` inclusive.
    """

    y: Number
    """
    Represents the vertical distance from the center.

    It's value ranges between `-1.0` and `1.0` inclusive.
    """

    BOTTOM_CENTER: ClassVar["AlignmentProperty"]
    """
    Represents the bottom center and is equivalent to `Alignment(0.0, 1.0)`.
    """

    BOTTOM_LEFT: ClassVar["AlignmentProperty"]
    """
    Represents the bottom left corner and is equivalent to `Alignment(-1.0, 1.0)`.
    """

    BOTTOM_RIGHT: ClassVar["AlignmentProperty"]
    """
    Represents the bottom right corner and is equivalent to `Alignment(1.0, 1.0)`.
    """

    CENTER: ClassVar["AlignmentProperty"]
    """
    Represents the center and is equivalent to `Alignment(0.0, 0.0)`.
    """

    CENTER_LEFT: ClassVar["AlignmentProperty"]
    """
    Represents the center left and is equivalent to `Alignment(-1.0, 0.0)`.
    """

    CENTER_RIGHT: ClassVar["AlignmentProperty"]
    """
    Represents the center right and is equivalent to `Alignment(1.0, 0.0)`.
    """

    TOP_CENTER: ClassVar["AlignmentProperty"]
    """
    Represents the top center and is equivalent to `Alignment(0.0, -1.0)`.
    """

    TOP_LEFT: ClassVar["AlignmentProperty"]
    """
    Represents the top left corner and is equivalent to `Alignment(-1.0, -1.0)`.
    """

    TOP_RIGHT: ClassVar["AlignmentProperty"]
    """
    Represents the top right corner and is equivalent to `Alignment(1.0, -1.0)`.
    """

    def copy(
        self,
        *,
        x: Optional[Number] = None,
        y: Optional[Number] = None,
    ) -> "Alignment":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return Alignment(
            x=x if x is not None else self.x,
            y=y if y is not None else self.y,
        )


class AlignmentProperty:
    def __init__(self, factory):
        self.factory = factory

    def __get__(self, instance, owner) -> Alignment:
        return self.factory()


Alignment.BOTTOM_CENTER = AlignmentProperty(lambda: Alignment(0.0, 1.0))
Alignment.BOTTOM_LEFT = AlignmentProperty(lambda: Alignment(-1.0, 1.0))
Alignment.BOTTOM_RIGHT = AlignmentProperty(lambda: Alignment(1.0, 1.0))
Alignment.CENTER = AlignmentProperty(lambda: Alignment(0.0, 0.0))
Alignment.CENTER_LEFT = AlignmentProperty(lambda: Alignment(-1.0, 0.0))
Alignment.CENTER_RIGHT = AlignmentProperty(lambda: Alignment(1.0, 0.0))
Alignment.TOP_CENTER = AlignmentProperty(lambda: Alignment(0.0, -1.0))
Alignment.TOP_LEFT = AlignmentProperty(lambda: Alignment(-1.0, -1.0))
Alignment.TOP_RIGHT = AlignmentProperty(lambda: Alignment(1.0, -1.0))
