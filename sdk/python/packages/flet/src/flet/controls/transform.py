from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Optional, Union

from flet.controls.alignment import Alignment
from flet.controls.types import Number

if TYPE_CHECKING:
    from flet.controls.box import FilterQuality

__all__ = [
    "Flip",
    "Matrix4",
    "Offset",
    "OffsetValue",
    "Rotate",
    "RotateValue",
    "Scale",
    "ScaleValue",
    "Transform",
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

    origin: Optional["Offset"] = None
    """
    The origin of the coordinate system (relative to the upper left corner),
    in logical pixels.
    """

    transform_hit_tests: bool = True
    """
    Whether to apply the transformation when performing hit tests.
    """

    filter_quality: Optional["FilterQuality"] = None
    """
    The filter quality with which to apply this transform as a bitmap operation.
    """

    def copy(
        self,
        *,
        scale: Optional[Number] = None,
        scale_x: Optional[Number] = None,
        scale_y: Optional[Number] = None,
        alignment: Optional[Alignment] = None,
        origin: Optional["Offset"] = None,
        transform_hit_tests: Optional[bool] = None,
        filter_quality: Optional["FilterQuality"] = None,
    ) -> "Scale":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return Scale(
            scale=scale if scale is not None else self.scale,
            scale_x=scale_x if scale_x is not None else self.scale_x,
            scale_y=scale_y if scale_y is not None else self.scale_y,
            alignment=alignment if alignment is not None else self.alignment,
            origin=origin if origin is not None else self.origin,
            transform_hit_tests=(
                transform_hit_tests
                if transform_hit_tests is not None
                else self.transform_hit_tests
            ),
            filter_quality=(
                filter_quality if filter_quality is not None else self.filter_quality
            ),
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

    origin: Optional["Offset"] = None
    """
    The origin of the coordinate system (relative to the upper left corner),
    in logical pixels.
    """

    transform_hit_tests: bool = True
    """
    Whether to apply the transformation when performing hit tests.
    """

    filter_quality: Optional["FilterQuality"] = None
    """
    The filter quality with which to apply this transform as a bitmap operation.
    """

    def copy(
        self,
        *,
        angle: Optional[Number] = None,
        alignment: Optional[Alignment] = None,
        origin: Optional["Offset"] = None,
        transform_hit_tests: Optional[bool] = None,
        filter_quality: Optional["FilterQuality"] = None,
    ) -> "Rotate":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return Rotate(
            angle=angle if angle is not None else self.angle,
            alignment=alignment if alignment is not None else self.alignment,
            origin=origin if origin is not None else self.origin,
            transform_hit_tests=(
                transform_hit_tests
                if transform_hit_tests is not None
                else self.transform_hit_tests
            ),
            filter_quality=(
                filter_quality if filter_quality is not None else self.filter_quality
            ),
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

    transform_hit_tests: bool = True
    """
    Whether to apply the transformation when performing hit tests.
    """

    filter_quality: Optional["FilterQuality"] = None
    """
    The filter quality with which to apply this transform as a bitmap operation.
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
        transform_hit_tests: Optional[bool] = None,
        filter_quality: Optional["FilterQuality"] = None,
    ) -> "Offset":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return Offset(
            x=x if x is not None else self.x,
            y=y if y is not None else self.y,
            transform_hit_tests=(
                transform_hit_tests
                if transform_hit_tests is not None
                else self.transform_hit_tests
            ),
            filter_quality=(
                filter_quality if filter_quality is not None else self.filter_quality
            ),
        )


@dataclass
class Flip:
    """
    Configuration for [`LayoutControl.flip`][flet.LayoutControl.flip].

    Mirrors a control across its x and/or y axis.
    """

    flip_x: bool = False
    """
    Whether to flip the x axis.
    """

    flip_y: bool = False
    """
    Whether to flip the y axis.
    """

    origin: Optional["Offset"] = None
    """
    The origin of the coordinate system (relative to the upper left corner).
    """

    transform_hit_tests: bool = True
    """
    Whether to apply the transformation when performing hit tests.
    """

    filter_quality: Optional["FilterQuality"] = None
    """
    The filter quality with which to apply this transform as a bitmap operation.
    """


@dataclass
class _Matrix4Call:
    """
    Internal serialized operation descriptor for [`Matrix4`][flet.].
    """

    name: str
    args: list[Any] = field(default_factory=list)


@dataclass
class Matrix4:
    """
    A recorded, replayable Matrix4 transform intent.

    This class records constructors and mutating method calls, then Flet replays
    them in Flutter to build a real `Matrix4` for
    [`Transform.matrix`][flet.Transform.matrix].
    """

    ctor: _Matrix4Call = field(default_factory=lambda: _Matrix4Call(name="identity"))
    """
    Recorded constructor call.
    """

    ops: list[_Matrix4Call] = field(default_factory=list)
    """
    Ordered list of recorded mutating operations.
    """

    @classmethod
    def identity(cls) -> "Matrix4":
        """
        Creates a matrix initialized with identity transform.
        """
        return cls(ctor=_Matrix4Call(name="identity"))

    @classmethod
    def translation_values(cls, x: Number, y: Number, z: Number) -> "Matrix4":
        """
        Creates a matrix initialized with translation components.
        """
        return cls(ctor=_Matrix4Call(name="translation_values", args=[x, y, z]))

    @classmethod
    def diagonal3_values(cls, x: Number, y: Number, z: Number) -> "Matrix4":
        """
        Creates a matrix initialized with diagonal scale values.
        """
        return cls(ctor=_Matrix4Call(name="diagonal3_values", args=[x, y, z]))

    @classmethod
    def rotation_z(cls, angle: Number) -> "Matrix4":
        """
        Creates a matrix initialized with a z-axis rotation in radians.
        """
        return cls(ctor=_Matrix4Call(name="rotation_z", args=[angle]))

    @classmethod
    def skew_x(cls, angle: Number) -> "Matrix4":
        """
        Creates a matrix initialized with x-axis skew in radians.
        """
        return cls(ctor=_Matrix4Call(name="skew_x", args=[angle]))

    @classmethod
    def skew_y(cls, angle: Number) -> "Matrix4":
        """
        Creates a matrix initialized with y-axis skew in radians.
        """
        return cls(ctor=_Matrix4Call(name="skew_y", args=[angle]))

    def translate(self, x: Number, y: Number, z: Number = 0) -> "Matrix4":
        """
        Appends translation operation.
        """
        self.ops.append(_Matrix4Call(name="translate", args=[x, y, z]))
        return self

    def scale(
        self,
        x: Number,
        y: Optional[Number] = None,
        z: Optional[Number] = None,
    ) -> "Matrix4":
        """
        Appends scale operation.

        If only `x` is provided then uniform scale is used.
        If `x` and `y` are provided then 2D scale is used.
        If all three are provided then 3D scale is used.
        """
        args: list[Any] = [x]
        if y is None and z is not None:
            args.extend([x, z])
        elif y is not None:
            args.append(y)
            if z is not None:
                args.append(z)
        self.ops.append(_Matrix4Call(name="scale", args=args))
        return self

    def rotate_z(self, angle: Number) -> "Matrix4":
        """
        Appends z-axis rotation operation in radians.
        """
        self.ops.append(_Matrix4Call(name="rotate_z", args=[angle]))
        return self

    def rotate_x(self, angle: Number) -> "Matrix4":
        """
        Appends x-axis rotation operation in radians.
        """
        self.ops.append(_Matrix4Call(name="rotate_x", args=[angle]))
        return self

    def rotate_y(self, angle: Number) -> "Matrix4":
        """
        Appends y-axis rotation operation in radians.
        """
        self.ops.append(_Matrix4Call(name="rotate_y", args=[angle]))
        return self

    def set_entry(self, row: int, col: int, value: Number) -> "Matrix4":
        """
        Appends raw matrix entry mutation.
        """
        self.ops.append(_Matrix4Call(name="set_entry", args=[row, col, value]))
        return self

    def multiply(self, other: "Matrix4") -> "Matrix4":
        """
        Appends multiplication by another recorded matrix.
        """
        if not isinstance(other, Matrix4):
            raise TypeError("other must be Matrix4")
        if other is self:
            raise ValueError("other must be a different Matrix4 instance")
        self.ops.append(_Matrix4Call(name="multiply", args=[other._snapshot()]))
        return self

    def _snapshot(self) -> "Matrix4":
        return Matrix4(
            ctor=_Matrix4Call(
                name=self.ctor.name,
                args=self._clone_args(self.ctor.args),
            ),
            ops=[
                _Matrix4Call(name=op.name, args=self._clone_args(op.args))
                for op in self.ops
            ],
        )

    def _clone_args(self, args: list[Any]) -> list[Any]:
        cloned: list[Any] = []
        for arg in args:
            if isinstance(arg, Matrix4):
                cloned.append(arg._snapshot())
            else:
                cloned.append(arg)
        return cloned


@dataclass
class Transform:
    """
    Configuration for [`LayoutControl.transform`][flet.LayoutControl.transform].

    Applies a generic matrix transform backed by recorded [`Matrix4`][flet.].
    """

    matrix: Matrix4
    """
    Matrix transform intent recorded in Python and replayed in Flutter.
    """

    origin: Optional["Offset"] = None
    """
    The origin of the coordinate system (relative to the upper left corner).
    """

    alignment: Optional[Alignment] = None
    """
    The alignment of the origin, relative to the size of the box.
    """

    transform_hit_tests: bool = True
    """
    Whether to apply the transformation when performing hit tests.
    """

    filter_quality: Optional["FilterQuality"] = None
    """
    The filter quality with which to apply this transform as a bitmap operation.
    """


# typing
RotateValue = Union[Number, Rotate]
"""Type alias for rotation values.

Represents rotation as either:
- a numeric angle in radians,
- or an explicit [`Rotate`][flet.] transform.
"""

ScaleValue = Union[Number, Scale]
"""Type alias for scale values.

Represents scale as either:
- a numeric uniform scale factor,
- or an explicit [`Scale`][flet.] transform.
"""

OffsetValue = Union[Offset, tuple[Number, Number]]
"""Type alias for offset values.

Represents offset as either:
- an [`Offset`][flet.] object,
- or an `(x, y)` tuple.
"""
