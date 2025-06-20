import dataclasses
from typing import Optional, Union

from flet.controls.types import Number, OptionalNumber
from flet.utils import deprecated

__all__ = [
    "BorderRadius",
    "BorderRadiusValue",
    "OptionalBorderRadiusValue",
    "all",
    "horizontal",
    "vertical",
    "only",
]


@dataclasses.dataclass
class BorderRadius:
    top_left: Number
    """
    Radius of the top left border corner.
    """

    top_right: Number
    """
    Radius of the top right border corner.
    """

    bottom_left: Number
    """
    Radius of the bottom left border corner.
    """

    bottom_right: Number
    """
    Radius of the bottom right border corner.
    """

    # Class Methods

    @classmethod
    def all(cls, value: Number) -> "BorderRadius":
        """Creates a `BorderRadius` where all radii are `radius`."""
        return BorderRadius(
            top_left=value, top_right=value, bottom_left=value, bottom_right=value
        )

    @classmethod
    def horizontal(cls, *, left: Number = 0, right: Number = 0) -> "BorderRadius":
        """
        Creates a horizontally symmetrical `BorderRadius` where the `left` and `right`
        sides of the rectangle have the same radii.

        Both `left` and `right` default to `0`.
        """
        return BorderRadius(
            top_left=left, top_right=right, bottom_left=left, bottom_right=right
        )

    @classmethod
    def vertical(cls, *, top: Number = 0, bottom: Number = 0) -> "BorderRadius":
        """
        Creates a vertically symmetric `BorderRadius` where the `top` and `bottom`
        sides of the rectangle have the same radii.

        Both `top` and `bottom` default to `0`.
        """
        return BorderRadius(
            top_left=top, top_right=top, bottom_left=bottom, bottom_right=bottom
        )

    @classmethod
    def only(
        cls,
        *,
        top_left: Number = 0,
        top_right: Number = 0,
        bottom_left: Number = 0,
        bottom_right: Number = 0,
    ) -> "BorderRadius":
        """
        Creates a border radius with only the given values.
        The other corners will be right angles.
        """
        return BorderRadius(
            top_left=top_left,
            top_right=top_right,
            bottom_left=bottom_left,
            bottom_right=bottom_right,
        )

    # Instance Methods

    def copy_with(
        self,
        *,
        top_left: OptionalNumber = None,
        top_right: OptionalNumber = None,
        bottom_left: OptionalNumber = None,
        bottom_right: OptionalNumber = None,
    ) -> "BorderRadius":
        """
        Returns a copy of this `BorderRadius` instance with the given fields replaced
        with the new values.
        """
        return BorderRadius(
            top_left=top_left if top_left is not None else self.top_left,
            top_right=top_right if top_right is not None else self.top_right,
            bottom_left=bottom_left if bottom_left is not None else self.bottom_left,
            bottom_right=bottom_right if bottom_right is not None else self.bottom_right,
        )

    # Arithmetics

    def __add__(self, other: "BorderRadius") -> "BorderRadius":
        """Adds two `BorderRadius` instances."""
        if not isinstance(other, BorderRadius):
            return NotImplemented
        return BorderRadius(
            top_left=self.top_left + other.top_left,
            top_right=self.top_right + other.top_right,
            bottom_left=self.bottom_left + other.bottom_left,
            bottom_right=self.bottom_right + other.bottom_right,
        )

    def __sub__(self, other: "BorderRadius") -> "BorderRadius":
        """Subtracts one `BorderRadius` from another."""
        if not isinstance(other, BorderRadius):
            return NotImplemented
        return BorderRadius(
            top_left=self.top_left - other.top_left,
            top_right=self.top_right - other.top_right,
            bottom_left=self.bottom_left - other.bottom_left,
            bottom_right=self.bottom_right - other.bottom_right,
        )

    def __mul__(self, other: Union["BorderRadius", Number]) -> "BorderRadius":
        """Multiplies `BorderRadius` by a scalar factor."""
        if isinstance(other, BorderRadius):
            return BorderRadius(
            top_left=self.top_left * other.top_left,
            top_right=self.top_right * other.top_right,
            bottom_left=self.bottom_left * other.bottom_left,
            bottom_right=self.bottom_right * other.bottom_right,
        )
        elif isinstance(other, Number):
            return BorderRadius(
                top_left=self.top_left * other,
                top_right=self.top_right * other,
                bottom_left=self.bottom_left * other,
                bottom_right=self.bottom_right * other,
            )
        return NotImplemented

    def __floordiv__(self, quotient: int) -> "BorderRadius":
        """Performs floor division on `BorderRadius`."""
        if quotient == 0:
            raise ZeroDivisionError("Division by zero is not possible")
        return BorderRadius(
            top_left=self.top_left // quotient,
            top_right=self.top_right // quotient,
            bottom_left=self.bottom_left // quotient,
            bottom_right=self.bottom_right // quotient,
        )


@deprecated(
    reason="Use BorderRadius.all() instead",
    version="0.70.0",
    delete_version="0.73.0",
    show_parentheses=True,
)
def all(value: float) -> BorderRadius:
    return BorderRadius(
        top_left=value, top_right=value, bottom_left=value, bottom_right=value
    )


@deprecated(
    reason="Use BorderRadius.horizontal() instead",
    version="0.70.0",
    delete_version="0.73.0",
    show_parentheses=True,
)
def horizontal(left: float = 0, right: float = 0) -> BorderRadius:
    return BorderRadius(
        top_left=left, top_right=right, bottom_left=left, bottom_right=right
    )


@deprecated(
    reason="Use BorderRadius.vertical() instead",
    version="0.70.0",
    delete_version="0.73.0",
    show_parentheses=True,
)
def vertical(top: float = 0, bottom: float = 0) -> BorderRadius:
    return BorderRadius(
        top_left=top, top_right=top, bottom_left=bottom, bottom_right=bottom
    )


@deprecated(
    reason="Use BorderRadius.only() instead",
    version="0.70.0",
    delete_version="0.73.0",
    show_parentheses=True,
)
def only(
        top_left: float = 0,
        top_right: float = 0,
        bottom_left: float = 0,
        bottom_right: float = 0,
) -> BorderRadius:
    return BorderRadius(
        top_left=top_left,
        top_right=top_right,
        bottom_left=bottom_left,
        bottom_right=bottom_right,
    )


BorderRadiusValue = Union[Number, BorderRadius]
OptionalBorderRadiusValue = Optional[BorderRadiusValue]
