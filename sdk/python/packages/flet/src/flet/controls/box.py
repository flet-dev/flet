from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union

from flet.controls.alignment import Alignment
from flet.controls.border import Border
from flet.controls.border_radius import BorderRadiusValue
from flet.controls.colors import Colors
from flet.controls.gradients import Gradient
from flet.controls.transform import Offset, OffsetValue
from flet.controls.types import (
    BlendMode,
    ColorValue,
    ImageRepeat,
    Number,
)

__all__ = [
    "BlurStyle",
    "BoxConstraints",
    "BoxDecoration",
    "BoxFit",
    "BoxShadow",
    "BoxShadowValue",
    "BoxShape",
    "ColorFilter",
    "DecorationImage",
    "FilterQuality",
]


@dataclass
class ColorFilter:
    """
    Defines a color filter.
    """

    color: Optional[ColorValue] = None
    """
    The color to use when applying the filter.
    """

    blend_mode: Optional[BlendMode] = None
    """
    The blend mode to apply to the color filter.
    """

    def copy(
        self,
        *,
        color: Optional[ColorValue] = None,
        blend_mode: Optional[BlendMode] = None,
    ) -> "ColorFilter":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return ColorFilter(
            color=color if color is not None else self.color,
            blend_mode=blend_mode if blend_mode is not None else self.blend_mode,
        )


class FilterQuality(Enum):
    """
    Quality levels for image sampling in Image and DecorationImage objects.
    """

    NONE = "none"
    """
    The fastest filtering method, albeit also the lowest quality.
    """

    LOW = "low"
    """
    Better quality than none, faster than medium.
    """

    MEDIUM = "medium"
    """
    The best all around filtering method that is only worse than high at extremely \
    large scale factors.
    """

    HIGH = "high"
    """
    Best possible quality when scaling up images by scale factors larger than 5-10x.
    When images are scaled down, this can be worse than medium for scales smaller than
    0.5x, or when animating the scale factor.
    This option is also the slowest.
    """


class BlurStyle(Enum):
    """
    Styles to use for blurs
    """

    NORMAL = "normal"
    """
    Fuzzy inside and outside. This is useful for painting shadows that are
    offset from the shape that ostensibly is casting the shadow.
    """

    SOLID = "solid"
    """
    Solid inside, fuzzy outside. This corresponds to drawing the shape, and
    additionally drawing the blur. This can make objects appear brighter,
    maybe even as if they were fluorescent.
    """

    OUTER = "outer"
    """
    Nothing inside, fuzzy outside. This is useful for painting shadows for
    partially transparent shapes, when they are painted separately but without
    an offset, so that the shadow doesn't paint below the shape.
    """

    INNER = "inner"
    """
    Fuzzy inside, nothing outside. This can make shapes appear to be lit from
    within.
    """


@dataclass
class BoxShadow:
    """
    Configuration for a box's shadow.
    """

    spread_radius: Number = 0.0
    """
    The amount the box should be inflated prior to applying the blur.
    """

    blur_radius: Number = 0.0
    """
    The standard deviation of the Gaussian to convolve with the shadow's shape.
    """

    color: ColorValue = Colors.BLACK
    """
    Color used to draw the shadow.
    """

    offset: OffsetValue = field(default_factory=lambda: Offset())
    """
    The displacement of the shadow from the casting element. Positive x/y offsets will \
    shift the shadow to the right and down, while negative offsets shift the shadow to \
    the left and up. The offsets are relative to the position of the element that is \
    casting it.
    """

    blur_style: BlurStyle = BlurStyle.NORMAL
    """
    The blur style to apply to this shadow.
    """

    def copy(
        self,
        *,
        spread_radius: Optional[Number] = None,
        blur_radius: Optional[Number] = None,
        color: Optional[ColorValue] = None,
        offset: Optional[OffsetValue] = None,
        blur_style: Optional[BlurStyle] = None,
    ) -> "BoxShadow":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return BoxShadow(
            spread_radius=spread_radius
            if spread_radius is not None
            else self.spread_radius,
            blur_radius=blur_radius if blur_radius is not None else self.blur_radius,
            color=color if color is not None else self.color,
            offset=offset if offset is not None else self.offset,
            blur_style=blur_style if blur_style is not None else self.blur_style,
        )


BoxShadowValue = Union[BoxShadow, list[BoxShadow]]
"""Type alias for box shadow values.

Represents shadows as either:
- a single [`BoxShadow`][flet.] object,
- or a list of [`BoxShadow`][flet.] objects.
"""


class BoxShape(Enum):
    """
    The shape to use when rendering a [`Border`][flet.] or [`BoxDecoration`][flet.].
    """

    RECTANGLE = "rectangle"
    """
    An axis-aligned rectangle, optionally with rounded corners.

    The amount of corner rounding, if any, is determined by the border radius
    specified by classes such as [`BoxDecoration`][flet.] or [`Border`][flet.].
    The rectangle's edges match those of the box in which it is painted.
    """

    CIRCLE = "circle"
    """
    A circle centered in the middle of the box into which the [`Border`][flet.] or
    [`BoxDecoration`][flet.] is painted. The diameter of the circle is the shortest
    dimension of the box, either the width or the height, such that the circle
    touches the edges of the box.
    """


class BoxFit(Enum):
    """
    How a box should be inscribed into another box.
    """

    NONE = "none"
    """
    Align the source within the target box (by default, centering) and discard
    any portions of the source that lie outside the box.

    The source image is not resized.

    ![](https://flutter.github.io/assets-for-api-docs/assets/painting/box_fit_none.png)
    """  # noqa: E501

    CONTAIN = "contain"
    """
    As large as possible while still containing the source entirely within the
    target box.

    ![](https://flutter.github.io/assets-for-api-docs/assets/painting/box_fit_contain.png)
    """  # noqa: E501

    COVER = "cover"
    """
    As small as possible while still covering the entire target box.

    ![](https://flutter.github.io/assets-for-api-docs/assets/painting/box_fit_cover.png)
    """  # noqa: E501

    FILL = "fill"
    """
    Fill the target box by distorting the source's aspect ratio.

    ![](https://flutter.github.io/assets-for-api-docs/assets/painting/box_fit_fill.png)
    """  # noqa: E501

    FIT_HEIGHT = "fitHeight"
    """
    Make sure the full height of the source is shown, regardless of
    whether this means the source overflows the target box horizontally.

    ![](https://flutter.github.io/assets-for-api-docs/assets/painting/box_fit_fitHeight.png)
    """  # noqa: E501

    FIT_WIDTH = "fitWidth"
    """
    Make sure the full width of the source is shown, regardless of
    whether this means the source overflows the target box vertically.

    ![](https://flutter.github.io/assets-for-api-docs/assets/painting/box_fit_fitWidth.png)
    """  # noqa: E501

    SCALE_DOWN = "scaleDown"
    """
    Align the source within the target box (by default, centering) and, if
    necessary, scale the source down to ensure that the source fits within the box.

    This is the same as [`CONTAIN`][(c).] if that would shrink the image, otherwise it
    is the same as [`NONE`][(c).].

    ![](https://flutter.github.io/assets-for-api-docs/assets/painting/box_fit_scaleDown.png)
    """  # noqa: E501


@dataclass
class DecorationImage:
    """
    An image for a box decoration.
    """

    src: Optional[Union[str, bytes]] = None
    """
    The image source to paint.

    Accepts URLs, asset paths, base64 strings (with or without `data:` prefixes),
    or raw bytes.
    """

    color_filter: Optional[ColorFilter] = None
    """
    A color filter to apply to the image before painting it.
    """

    fit: Optional[BoxFit] = None
    """
    How the image should be inscribed into the box.
    """

    alignment: Alignment = field(default_factory=lambda: Alignment.CENTER)
    """
    The alignment of the image within its bounds.
    """

    repeat: ImageRepeat = ImageRepeat.NO_REPEAT
    """
    How the image should be repeated to fill the box.
    """

    match_text_direction: bool = False
    """
    Whether to paint the image in the direction of the TextDirection.
    """

    scale: Number = 1.0
    """
    The scale(image pixels to be shown per logical pixels) to apply to the image.
    """

    opacity: Number = 1.0
    """
    The opacity of the image.
    """

    filter_quality: FilterQuality = FilterQuality.MEDIUM
    """
    The quality of the image filter.
    """

    invert_colors: bool = False
    """
    Whether to invert the colors of the image while drawing.
    """

    anti_alias: bool = False
    """
    Whether to paint the image in anti-aliased quality.
    """

    def copy(
        self,
        *,
        src: Optional[Union[str, bytes]] = None,
        color_filter: Optional[ColorFilter] = None,
        fit: Optional[BoxFit] = None,
        alignment: Optional[Alignment] = None,
        repeat: Optional[ImageRepeat] = None,
        match_text_direction: Optional[bool] = None,
        scale: Optional[Number] = None,
        opacity: Optional[Number] = None,
        filter_quality: Optional[FilterQuality] = None,
        invert_colors: Optional[bool] = None,
        anti_alias: Optional[bool] = None,
    ) -> "DecorationImage":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return DecorationImage(
            src=src if src is not None else self.src,
            color_filter=color_filter
            if color_filter is not None
            else self.color_filter,
            fit=fit if fit is not None else self.fit,
            alignment=alignment if alignment is not None else self.alignment,
            repeat=repeat if repeat is not None else self.repeat,
            match_text_direction=match_text_direction
            if match_text_direction is not None
            else self.match_text_direction,
            scale=scale if scale is not None else self.scale,
            opacity=opacity if opacity is not None else self.opacity,
            filter_quality=filter_quality
            if filter_quality is not None
            else self.filter_quality,
            invert_colors=invert_colors
            if invert_colors is not None
            else self.invert_colors,
            anti_alias=anti_alias if anti_alias is not None else self.anti_alias,
        )


@dataclass
class BoxDecoration:
    """
    BoxDecoration provides a description of how to paint a box.
    The box has a border, a body, and may cast a shadow.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The color to fill in the background of the box.
    """

    image: Optional[DecorationImage] = None
    """
    An image to paint above the background [`bgcolor`][(c).] or [`gradient`][(c).].
    """

    border: Optional[Border] = None
    """
    A border to draw above the background [`bgcolor`][(c).], [`gradient`][(c).], and \
    [`image`][(c).].
    """

    border_radius: Optional[BorderRadiusValue] = None
    """
    The border radius of the box.
    """

    shadows: Optional[BoxShadowValue] = None
    """
    A list of shadows cast by the box.
    """

    gradient: Optional[Gradient] = None
    """
    A gradient to use when filling the box.
    """

    shape: BoxShape = BoxShape.RECTANGLE
    """
    The shape to fill the [`bgcolor`][(c).], [`gradient`][(c).], and [`image`][(c).]
    into and to cast as the [`shadows`][(c).].
    """

    blend_mode: Optional[BlendMode] = None
    """
    The blend mode to apply to the background [`bgcolor`][(c).] or [`gradient`][(c).].
    """

    def __post_init__(self):
        if not (
            self.blend_mode is None
            or self.bgcolor is not None
            or self.gradient is not None
        ):
            raise ValueError(
                "blend_mode applies to the BoxDecoration's background color "
                "or gradient, but no color or gradient was provided"
            )
        if self.shape == BoxShape.CIRCLE and self.border_radius:
            raise ValueError("border_radius must be None when shape is BoxShape.CIRCLE")

    def copy(
        self,
        *,
        bgcolor: Optional[ColorValue] = None,
        image: Optional[DecorationImage] = None,
        border: Optional[Border] = None,
        border_radius: Optional[BorderRadiusValue] = None,
        shadows: Optional[BoxShadowValue] = None,
        gradient: Optional[Gradient] = None,
        shape: Optional[BoxShape] = None,
        blend_mode: Optional[BlendMode] = None,
    ):
        """Returns a new `BoxDecoration` with selected fields overridden."""
        return BoxDecoration(
            bgcolor=bgcolor if bgcolor is not None else self.bgcolor,
            image=image if image is not None else self.image,
            border=border if border is not None else self.border,
            border_radius=border_radius
            if border_radius is not None
            else self.border_radius,
            shadows=shadows if shadows is not None else self.shadows,
            gradient=gradient if gradient is not None else self.gradient,
            shape=shape if shape is not None else self.shape,
            blend_mode=blend_mode if blend_mode is not None else self.blend_mode,
        )


@dataclass
class BoxConstraints:
    """
    Constraints that must be respected by a size of a box.

    A [`Size`][flet.] respects a BoxConstraints if, and only if,
    all of the following relations hold:

        min_width <= Size.width <= max_width
        min_height <= Size.height <= max_height

    Read more about BoxConstraints
    [here](https://api.flutter.dev/flutter/rendering/BoxConstraints-class.html).
    """

    min_width: Number = 0
    """
    The minimum width that satisfies the constraints, \
    such that `0.0 <= min_width <= max_width`.
    """

    min_height: Number = 0
    """
    The minimum height that satisfies the constraints, \
    such that `0.0 <= min_height <= max_height`.
    """

    max_width: Number = float("inf")
    """
    The maximum width that satisfies the constraints, \
    such that `min_width <= max_width <= float("inf")`.
    """

    max_height: Number = float("inf")
    """
    The maximum height that satisfies the constraints, \
    such that `min_height <= max_height <= float("inf")`.
    """

    def __post_init__(self):
        if not (0 <= self.min_width <= self.max_width <= float("inf")):
            raise ValueError(
                "min_width and max_width must be between 0 and infinity "
                "and min_width must be less than or equal to max_width"
            )
        if not (0 <= self.min_height <= self.max_height <= float("inf")):
            raise ValueError(
                "min_height and max_height must be between 0 and infinity "
                "and min_height must be less than or equal to max_height"
            )

    def copy(
        self,
        *,
        min_width: Optional[Number] = None,
        min_height: Optional[Number] = None,
        max_width: Optional[Number] = None,
        max_height: Optional[Number] = None,
    ) -> "BoxConstraints":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return BoxConstraints(
            min_width=min_width if min_width is not None else self.min_width,
            min_height=min_height if min_height is not None else self.min_height,
            max_width=max_width if max_width is not None else self.max_width,
            max_height=max_height if max_height is not None else self.max_height,
        )
