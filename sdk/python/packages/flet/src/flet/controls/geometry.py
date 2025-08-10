from dataclasses import dataclass
from typing import Optional

from flet.controls.transform import Offset
from flet.controls.types import Number

__all__ = [
    "Rect",
    "Size",
]


@dataclass
class Size:
    """
    A 2D size with width and height.
    """

    width: Number
    height: Number

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

    @classmethod
    def square(cls, dimension: Number) -> "Size":
        """Creates a square Size where width and height are the same."""
        return Size(dimension, dimension)

    @classmethod
    def from_width(cls, width: Number) -> "Size":
        """Creates a Size with the given width and an infinite height."""
        return Size(width, float("inf"))

    @classmethod
    def from_height(cls, height: Number) -> "Size":
        """Creates a Size with the given height and an infinite width."""
        return Size(float("inf"), height)

    @classmethod
    def from_radius(cls, radius: Number) -> "Size":
        """Creates a square Size whose width and height are twice the given radius."""
        return Size(radius * 2.0, radius * 2.0)

    @classmethod
    def zero(cls):
        return Size(0.0, 0.0)

    @classmethod
    def infinite(cls):
        return Size(float("inf"), float("inf"))

    def copy(
        self,
        *,
        width: Optional[Number] = None,
        height: Optional[Number] = None,
    ) -> "Size":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return Size(
            width=width if width is not None else self.width,
            height=height if height is not None else self.height,
        )


@dataclass
class Rect:
    """
    A 2D, axis-aligned, floating-point rectangle whose coordinates are relative
    to a given origin.
    """

    left: Number
    """The offset of the left edge of this rectangle from the x-axis."""

    top: Number
    """The offset of the top edge of this rectangle from the y-axis."""

    right: Number
    """The offset of the right edge of this rectangle from the x-axis."""

    bottom: Number
    """The offset of the bottom edge of this rectangle from the y-axis."""

    @property
    def width(self) -> Number:
        """The distance between the left and right edges of this rectangle."""
        return self.right - self.left

    @property
    def height(self) -> Number:
        """The distance between the top and bottom edges of this rectangle."""
        return self.bottom - self.top

    def copy(
        self,
        *,
        left: Optional[Number] = None,
        top: Optional[Number] = None,
        right: Optional[Number] = None,
        bottom: Optional[Number] = None,
    ) -> "Rect":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return Rect(
            left=left if left is not None else self.left,
            top=top if top is not None else self.top,
            right=right if right is not None else self.right,
            bottom=bottom if bottom is not None else self.bottom,
        )

    @property
    def size(self) -> Size:
        """
        The distance between the upper-left corner
        and the lower-right corner of this rectangle.
        """
        return Size(self.width, self.height)

    @classmethod
    def from_lwth(
        cls, *, left: Number, top: Number, width: Number, height: Number
    ) -> "Rect":
        """
        Construct a rectangle from its left and top edges,
        its width, and its height.
        """
        return Rect(left, top, left + width, top + height)

    @classmethod
    def from_center(cls, *, center: Offset, width: Number, height: Number):
        """
        Constructs a rectangle from its center point, width, and height.
        The `center` argument is assumed to be an offset from the origin.
        """
        return Rect(
            center.x - width / 2,
            center.y - height / 2,
            center.x + width / 2,
            center.y + height / 2,
        )

    @classmethod
    def from_points(cls, a: Offset, b: Offset):
        """
        Construct the smallest rectangle that encloses the given offsets,
        treating them as vectors from the origin.
        """
        return Rect(
            min(a.x, b.x),
            min(a.y, b.y),
            max(a.x, b.x),
            max(a.y, b.y),
        )
