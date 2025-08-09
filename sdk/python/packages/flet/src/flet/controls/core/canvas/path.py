from dataclasses import dataclass, field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.border_radius import BorderRadiusValue
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint

__all__ = ["Path"]


@control("Path")
class Path(Shape):
    """
    Draws a path with given [`elements`][(c).]
    with the given [`paint`][(c).].

    Whether this shape is filled, stroked, or both, is controlled by `paint.style`.
    If the path is filled, then sub-paths within it are implicitly closed
    (see `Path.Close`).
    """

    @dataclass(kw_only=True)
    class PathElement:
        _type: Optional[str] = field(
            init=False, repr=False, compare=False, default=None
        )

    elements: list[PathElement] = field(default_factory=list)
    """
    The list of path elements.
    """

    paint: Paint = field(default_factory=lambda: Paint())
    """
    A style to draw a path with.
    """

    @dataclass
    class MoveTo(PathElement):
        """
        Starts a new sub-path at the given point (`x`,`y`).
        """

        x: float
        y: float

        def __post_init__(self):
            self._type = "MoveTo"

    @dataclass
    class LineTo(PathElement):
        """
        Adds a straight line segment from the current point to the given point
        (`x`,`y`).
        """

        x: float
        y: float

        def __post_init__(self):
            self._type = "LineTo"

    @dataclass
    class QuadraticTo(PathElement):
        """
        Adds a bezier segment that curves from the current point to the given point
        (`x`,`y`), using the control points (`cp1x`,`cp1y`) and the weight `w`.
        """

        cp1x: float
        cp1y: float
        x: float
        y: float
        w: float = 1
        """
        If the weight is greater than 1, then the curve is a hyperbola;
        if the weight equals 1, it's a parabola;
        and if it is less than 1, it is an ellipse.
        """

        def __post_init__(self):
            self._type = "QuadraticTo"

    @dataclass
    class CubicTo(PathElement):
        """
        Adds a cubic bezier segment that curves from the current point to the given
        point (`x`,`y`), using the control points (`cp1x`,`cp1y`) and (`cp2x`,`cp2y`).
        """

        cp1x: float
        cp1y: float
        cp2x: float
        cp2y: float
        x: float
        y: float

        def __post_init__(self):
            self._type = "CubicTo"

    @dataclass
    class SubPath(PathElement):
        """
        Adds the sub-path described by `elements` to the given point (`x`,`y`).
        """

        elements: list["Path.PathElement"]
        x: float
        y: float

        def __post_init__(self):
            self._type = "SubPath"

    @dataclass
    class Arc(PathElement):
        """
        Adds a new sub-path with one arc segment that consists of the arc that follows
        the edge of the oval bounded by the given rectangle with top left corner at `x`
        and `y` and dimensions `width` and `height`, from `start_angle` radians around
        the oval up to `start_angle` + `sweep_angle` radians around the oval, with zero
        radians being the point on the right hand side of the oval that crosses the
        horizontal line that intersects the center of the rectangle and with positive
        angles going clockwise around the oval.
        """

        x: float
        """
        Top-left corner `x` of the rectangle bounding the arc.
        """

        y: float
        """
        Top-left corner `y` of the rectangle bounding the arc.
        """

        width: float
        """
        Width of the rectangle bounding the arc.
        """

        height: float
        """
        Height of the rectangle bounding the arc.
        """

        start_angle: float
        """
        Starting angle in radians of the arc.
        """

        sweep_angle: float
        """
        Sweep angle in radians from `start_angle`.
        """

        def __post_init__(self):
            self._type = "Arc"

    @dataclass
    class ArcTo(PathElement):
        """
        Appends up to four conic curves weighted to describe an oval of `radius` and
        rotated by `rotation` (measured in degrees and clockwise).

        The first curve begins from the last point in the path and the last ends at `x`
        and `y`. The curves follow a path in a direction determined by `clockwise`
        (bool) and `large_arc` (bool) in such a way that the sweep angle is always less
        than 360 degrees.

        A simple line is appended if either radius is zero or the last point in
        the path (`x`,`y`). The radii are scaled to fit the last path point if both are
        greater than zero but too small to describe an arc.
        """

        x: float
        """
        Destination `x` coordinate of arc endpoint.
        """

        y: float
        """
        Destination `y` coordinate of arc endpoint.
        """

        radius: float = 0
        """
        Radius of the arc.
        """

        rotation: float = 0
        """
        Rotation of the arc in degrees.
        """

        large_arc: bool = False
        """
        Whether to use the large arc sweep.
        """

        clockwise: bool = True
        """
        Whether the arc should be drawn clockwise.
        """

        def __post_init__(self):
            self._type = "ArcTo"

    @dataclass
    class Oval(PathElement):
        """
        Adds a new sub-path that consists of a curve that forms the ellipse that fills
        the given rectangle.
        """

        x: float
        """
        The x-axis coordinate of the top-left of the bounding rectangle.
        """

        y: float
        """
        The y-axis coordinate of the top-left of the bounding rectangle.
        """

        width: float
        """
        Width of the bounding rectangle.
        """

        height: float
        """
        Height of the bounding rectangle.
        """

        def __post_init__(self):
            self._type = "Oval"

    @dataclass
    class Rect(PathElement):
        """
        Adds a rectangle as a new sub-path.
        """

        x: float
        """
        The x-axis coordinate of the top-left of the rectangle.
        """

        y: float
        """
        The y-axis coordinate of the top-left of the rectangle.
        """

        width: float
        """
        Width of the rectangle.
        """

        height: float
        """
        Height of the rectangle.
        """

        border_radius: Optional[BorderRadiusValue] = None
        """
        Optional border radius to round rectangle corners.
        """

        def __post_init__(self):
            self._type = "Rect"

    @dataclass
    class Close(PathElement):
        """
        Closes the last sub-path, as if a straight line had been drawn from the
        current point to the first point of the sub-path.
        """

        def __post_init__(self):
            self._type = "Close"
