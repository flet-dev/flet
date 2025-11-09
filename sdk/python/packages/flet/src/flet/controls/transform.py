from dataclasses import dataclass
from typing import Optional, Union

from flet.controls.alignment import Alignment
from flet.controls.types import Number

__all__ = [
    "Offset",
    "OffsetValue",
    "Rotate",
    "RotateValue",
    "Scale",
    "ScaleValue",
]


@dataclass
class Scale:
    """
    Scaling configuration for an object.
    """

    scale: Optional[Number] = None
    """
    `scale_x` and `scale_y` get the value of `scale` if `scale` is provided.
    """

    scale_x: Optional[Number] = None
    """
    The scalar by which to multiply the x-axis.
    """

    scale_y: Optional[Number] = None
    """
    The scalar by which to multiply the y-axis.
    """

    alignment: Optional[Alignment] = None
    """
    Gives the origin of scale.
    """

    def copy(
        self,
        *,
        scale: Optional[Number] = None,
        scale_x: Optional[Number] = None,
        scale_y: Optional[Number] = None,
        alignment: Optional[Alignment] = None,
    ) -> "Scale":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return Scale(
            scale=scale if scale is not None else self.scale,
            scale_x=scale_x if scale_x is not None else self.scale_x,
            scale_y=scale_y if scale_y is not None else self.scale_y,
            alignment=alignment if alignment is not None else self.alignment,
        )


@dataclass
class Rotate:
    """
    Rotation configuration of an object.
    """

    angle: Number
    """
    The rotation in clockwise radians.
    """

    alignment: Optional[Alignment] = None
    """
    The alignment of the rotation.
    """

    def copy(
        self,
        *,
        angle: Optional[Number] = None,
        alignment: Optional[Alignment] = None,
    ) -> "Rotate":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return Rotate(
            angle=angle if angle is not None else self.angle,
            alignment=alignment if alignment is not None else self.alignment,
        )


@dataclass
class Offset:
    """
    A 2D floating-point offset.
    """

    x: Number = 0
    """
    The horizontal offset.
    """

    y: Number = 0
    """
    The vertical offset.
    """

    @property
    def distance(self) -> float:
        """The magnitude of the offset."""
        return (self.x**2 + self.y**2) ** 0.5

    def copy(
        self,
        *,
        x: Optional[Number] = None,
        y: Optional[Number] = None,
    ) -> "Offset":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return Offset(
            x=x if x is not None else self.x,
            y=y if y is not None else self.y,
        )


# typing
RotateValue = Union[Number, Rotate]
ScaleValue = Union[Number, Scale]
OffsetValue = Union[Offset, tuple[Number, Number]]
