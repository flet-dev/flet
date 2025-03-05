from dataclasses import dataclass

from flet.core.types import Number

__all__ = [
    "Size",
    "copy",
    "square",
    "from_width",
    "from_height",
    "from_radius",
    "zero",
    "infinite",
]


@dataclass(frozen=True)
class Size:
    """
    A class representing a 2D size with width and height.
    """

    width: float
    height: float

    @property
    def aspect_ratio(self) -> float:
        """Returns the aspect ratio (width / height)."""
        if self.height != 0.0:
            return self.width / self.height
        if self.width > 0.0:
            return float("inf")
        if self.width < 0.0:
            return float("-inf")
        return 0.0

    def is_infinite(self) -> bool:
        """Checks if either dimension is infinite."""
        return self.width == float("inf") or self.height == float("inf")

    def is_finite(self) -> bool:
        """Checks if both dimensions are finite."""
        return self.width != float("inf") and self.height != float("inf")


def copy(source: "Size") -> Size:
    """Creates a copy of the given Size object."""
    return Size(source.width, source.height)


def square(dimension: Number) -> Size:
    """Creates a square Size where width and height are the same."""
    return Size(dimension, dimension)


def from_width(width: Number) -> Size:
    """Creates a Size with the given width and an infinite height."""
    return Size(width, float("inf"))


def from_height(height: Number) -> Size:
    """Creates a Size with the given height and an infinite width."""
    return Size(float("inf"), height)


def from_radius(radius: Number) -> Size:
    """Creates a square Size whose width and height are twice the given radius."""
    return Size(radius * 2.0, radius * 2.0)


# Constants
zero = Size(0.0, 0.0)
infinite = Size(float("inf"), float("inf"))
