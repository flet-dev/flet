import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from flet.controls.blur import BlurValue
from flet.controls.gradients import GradientTileMode
from flet.controls.transform import OffsetValue
from flet.controls.types import (
    BlendMode,
    ColorValue,
    Number,
    StrokeCap,
    StrokeJoin,
)

__all__ = [
    "Paint",
    "PaintGradient",
    "PaintLinearGradient",
    "PaintRadialGradient",
    "PaintSweepGradient",
    "PaintingStyle",
]


class PaintingStyle(Enum):
    FILL = "fill"
    STROKE = "stroke"


@dataclass(kw_only=True)
class PaintGradient:
    _type: Optional[str] = field(init=False, repr=False, compare=False, default=None)


@dataclass
class PaintLinearGradient(PaintGradient):
    """
    More information on Linear gradient
    https://api.flutter.dev/flutter/dart-ui/Gradient/Gradient.linear.html
    """

    begin: Optional[OffsetValue]
    """
    The offset at which
    stop 0.0 of the gradient is placed.
    """

    end: Optional[OffsetValue]
    """
    The offset at which
    stop 1.0 of the gradient is placed.
    """

    colors: list[str]
    """
    The https://flet.dev/docs/reference/colors the gradient should obtain at each of
    the stops. This list must contain at least two colors.

    Note:
        If [`color_stops`][(c).] is not `None`,
        this list must have the same length as `color_stops`.
    """

    color_stops: Optional[list[Number]] = None
    """
    A list of values from `0.0` to `1.0` that denote fractions along the gradient.

    Note:
        If non-none, this list must have the same length as
        [`colors`][(c).].
        If the first value is not `0.0`, then a stop with position `0.0` and a color
        equal to the first color in `colors` is implied. If the last value is not
        `1.0`, then a stop with position `1.0` and a color equal to the last color
        in `colors` is implied.
    """

    tile_mode: GradientTileMode = GradientTileMode.CLAMP
    """
    How this gradient should tile the plane beyond in the region before `begin` and
    after `end`.
    """

    def __post_init__(self):
        self._type = "linear"

    def copy(
        self,
        *,
        begin: Optional[OffsetValue] = None,
        end: Optional[OffsetValue] = None,
        colors: Optional[list[str]] = None,
        color_stops: Optional[list[Number]] = None,
        tile_mode: Optional[GradientTileMode] = None,
    ) -> "PaintLinearGradient":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return PaintLinearGradient(
            begin=begin if begin is not None else self.begin,
            end=end if end is not None else self.end,
            colors=colors if colors is not None else self.colors.copy(),
            color_stops=color_stops
            if color_stops is not None
            else (self.color_stops.copy() if self.color_stops is not None else None),
            tile_mode=tile_mode if tile_mode is not None else self.tile_mode,
        )


@dataclass
class PaintRadialGradient(PaintGradient):
    """
    More information on Radial gradient
    https://api.flutter.dev/flutter/dart-ui/Gradient/Gradient.radial.html
    """

    center: Optional[OffsetValue]
    """
    The center of the gradient.
    """

    radius: Number
    """
    The radius of the gradient.
    """

    colors: list[ColorValue]
    """
    The https://flet.dev/docs/reference/colors the gradient should obtain at each of
    the stops. This list must contain at least two colors.

    If `stops` is provided, this list must have the same length as `stops`.
    """

    color_stops: Optional[list[Number]] = None
    """
    A list of values from `0.0` to `1.0` that denote fractions along the gradient.

    If provided, this list must have the same length as `colors`. If the first value
    is not `0.0`, then a stop with position `0.0` and a color equal to the first color
    in `colors` is implied. If the last value is not `1.0`, then a stop with position
    `1.0` and a color equal to the last color in `colors` is implied.
    """

    tile_mode: GradientTileMode = GradientTileMode.CLAMP
    """
    How this gradient should tile the plane beyond in the region before `begin` and
    after `end`.
    """

    focal: Optional[OffsetValue] = None
    """
    The focal point of the gradient. If specified, the gradient will appear to be
    focused along the vector from `center` to focal.
    """

    focal_radius: Number = 0.0
    """
    The radius of the focal point of gradient, as a fraction of the shortest side of
    the paint box.

    For example, if a radial gradient is painted on a box that is `100.0` pixels wide
    and `200.0` pixels tall, then a radius of `1.0` will place the `1.0` stop at
    `100.0` pixels from the focal point.
    """

    def __post_init__(self):
        self._type = "radial"

    def copy(
        self,
        *,
        center: Optional[OffsetValue] = None,
        radius: Optional[Number] = None,
        colors: Optional[list[str]] = None,
        color_stops: Optional[list[Number]] = None,
        tile_mode: Optional[GradientTileMode] = None,
        focal: Optional[OffsetValue] = None,
        focal_radius: Optional[Number] = None,
    ) -> "PaintRadialGradient":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return PaintRadialGradient(
            center=center if center is not None else self.center,
            radius=radius if radius is not None else self.radius,
            colors=colors if colors is not None else self.colors.copy(),
            color_stops=color_stops
            if color_stops is not None
            else (self.color_stops.copy() if self.color_stops is not None else None),
            tile_mode=tile_mode if tile_mode is not None else self.tile_mode,
            focal=focal if focal is not None else self.focal,
            focal_radius=focal_radius
            if focal_radius is not None
            else self.focal_radius,
        )


@dataclass
class PaintSweepGradient(PaintGradient):
    """
    More information on Sweep gradient
    https://api.flutter.dev/flutter/dart-ui/Gradient/Gradient.sweep.html
    """

    center: Optional[OffsetValue]
    """
    The center of the gradient.
    """

    colors: list[str]
    """
    The https://flet.dev/docs/reference/colors the gradient should obtain at each of
    the stops. This list must contain at least two colors.

    If `stops` is provided, this list must have the same length as `stops`.
    """

    color_stops: Optional[list[Number]] = None
    """
    A list of values from `0.0` to `1.0` that denote fractions along the gradient.

    If provided, this list must have the same length as `colors`. If the first value
    is not `0.0`, then a stop with position `0.0` and a color equal to the first color
    in `colors` is implied. If the last value is not `1.0`, then a stop with position
    `1.0` and a color equal to the last color in `colors` is implied.
    """

    tile_mode: GradientTileMode = GradientTileMode.CLAMP
    """
    How this gradient should tile the plane beyond in the region before `begin` and
    after `end`.
    """

    start_angle: Number = 0.0
    """
    The angle in https://en.wikipedia.org/wiki/Radian at which stop 0.0 of the
    gradient is placed. Defaults to 0.0.
    """

    end_angle: Number = math.pi * 2
    """
    The angle in radians at which stop 1.0 of the gradient is placed. Defaults to
    math.pi * 2.
    """

    rotation: Optional[Number] = None
    """
    The rotation of the gradient in https://en.wikipedia.org/wiki/Radian, around the
    center-point of its bounding box.
    """

    def __post_init__(self):
        self._type = "sweep"

    def copy(
        self,
        *,
        center: Optional[OffsetValue] = None,
        colors: Optional[list[str]] = None,
        color_stops: Optional[list[Number]] = None,
        tile_mode: Optional[GradientTileMode] = None,
        start_angle: Optional[Number] = None,
        end_angle: Optional[Number] = None,
        rotation: Optional[Number] = None,
    ) -> "PaintSweepGradient":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return PaintSweepGradient(
            center=center if center is not None else self.center,
            colors=colors if colors is not None else self.colors.copy(),
            color_stops=color_stops
            if color_stops is not None
            else (self.color_stops.copy() if self.color_stops is not None else None),
            tile_mode=tile_mode if tile_mode is not None else self.tile_mode,
            start_angle=start_angle if start_angle is not None else self.start_angle,
            end_angle=end_angle if end_angle is not None else self.end_angle,
            rotation=rotation if rotation is not None else self.rotation,
        )


@dataclass
class Paint:
    """
    A description of the style to use when drawing a shape on the canvas.
    """

    color: Optional[ColorValue] = None
    """
    The https://flet.dev/docs/reference/colors to use when stroking or filling a shape.
    Defaults to opaque black.
    """

    blend_mode: Optional[BlendMode] = None
    """
    A blend mode to apply when a shape is drawn or a layer is composited.

    Defaults to `BlendMode.SRC_OVER`.
    """

    blur_image: Optional[BlurValue] = None
    """
    Blur image when drawing it on a canvas.
    """

    anti_alias: Optional[bool] = None
    """
    Whether to apply anti-aliasing to lines and images drawn on the canvas.

    Defaults to `True`.
    """

    gradient: Optional[PaintGradient] = None
    """
    Configures gradient paint.
    """

    stroke_cap: Optional[StrokeCap] = None
    """
    TBD
    """

    stroke_join: Optional[StrokeJoin] = None
    """
    TBD
    """

    stroke_miter_limit: Optional[Number] = None
    """
    TBD
    """

    stroke_width: Optional[Number] = None
    """
    TBD
    """

    stroke_dash_pattern: Optional[list[Number]] = None
    """
    TBD
    """

    style: Optional[PaintingStyle] = None
    """
    TBD
    """

    def copy(
        self,
        *,
        color: Optional[ColorValue] = None,
        blend_mode: Optional[BlendMode] = None,
        blur_image: Optional[BlurValue] = None,
        anti_alias: Optional[bool] = None,
        gradient: Optional[PaintGradient] = None,
        stroke_cap: Optional[StrokeCap] = None,
        stroke_join: Optional[StrokeJoin] = None,
        stroke_miter_limit: Optional[Number] = None,
        stroke_width: Optional[Number] = None,
        stroke_dash_pattern: Optional[list[Number]] = None,
        style: Optional[PaintingStyle] = None,
    ) -> "Paint":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return Paint(
            color=color if color is not None else self.color,
            blend_mode=blend_mode if blend_mode is not None else self.blend_mode,
            blur_image=blur_image if blur_image is not None else self.blur_image,
            anti_alias=anti_alias if anti_alias is not None else self.anti_alias,
            gradient=gradient if gradient is not None else self.gradient,
            stroke_cap=stroke_cap if stroke_cap is not None else self.stroke_cap,
            stroke_join=stroke_join if stroke_join is not None else self.stroke_join,
            stroke_miter_limit=stroke_miter_limit
            if stroke_miter_limit is not None
            else self.stroke_miter_limit,
            stroke_width=stroke_width
            if stroke_width is not None
            else self.stroke_width,
            stroke_dash_pattern=stroke_dash_pattern
            if stroke_dash_pattern is not None
            else (
                self.stroke_dash_pattern.copy()
                if self.stroke_dash_pattern is not None
                else None
            ),
            style=style if style is not None else self.style,
        )
