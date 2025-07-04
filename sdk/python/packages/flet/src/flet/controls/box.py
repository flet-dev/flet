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
    "BoxDecoration",
    "BoxShadow",
    "DecorationImage",
    "ColorFilter",
    "FilterQuality",
    "BlurStyle",
    "BoxShape",
    "BoxConstraints",
    "BoxFit",
    "ShadowValue",
]


@dataclass
class ColorFilter:
    """
    Defines a color filter that can be used with
    [`Container.color_filter`](https://flet.dev/docs/controls/container#color_filter).
    """

    color: Optional[ColorValue] = None
    """
    The [color](https://flet.dev/docs/reference/colors) to use when applying the filter.
    """

    blend_mode: Optional[BlendMode] = None
    """
    The blend mode to apply to the color filter.

    Value is of type [`BlendMode`](https://flet.dev/docs/reference/types/blendmode).
    """


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
    The best all around filtering method that is only worse than high at extremely
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
    NORMAL = "normal"
    SOLID = "solid"
    OUTER = "outer"
    INNER = "inner"


@dataclass
class BoxShadow:
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
    [Color](https://flet.dev/docs/reference/colors) used to draw the shadow.
    """

    offset: OffsetValue = field(default_factory=lambda: Offset())
    """
    An instance of `Offset` class - the displacement of the shadow from the casting
    element. Positive x/y offsets will shift the shadow to the right and down, while
    negative offsets shift the shadow to the left and up. The offsets are relative to
    the position of the element that is casting it.

    Value is of type [`Offset`](https://flet.dev/docs/reference/types/offset).
    """

    blur_style: BlurStyle = BlurStyle.NORMAL
    """
    Value is of type [`BlurStyle`](https://flet.dev/docs/reference/types/blurstyle).
    """


ShadowValue = Union[BoxShadow, list[BoxShadow]]


class BoxShape(Enum):
    RECTANGLE = "rectangle"
    CIRCLE = "circle"


class BoxFit(Enum):
    NONE = "none"
    CONTAIN = "contain"
    COVER = "cover"
    FILL = "fill"
    FIT_HEIGHT = "fitHeight"
    FIT_WIDTH = "fitWidth"
    SCALE_DOWN = "scaleDown"


@dataclass
class DecorationImage:
    """
    An image for a box decoration.
    """

    src: Optional[str] = None
    """
    The image to paint.
    """

    src_base64: Optional[str] = None
    """
    The base64-encoded image to paint.
    """

    src_bytes: Optional[bytes] = None
    """
    TBD
    """

    color_filter: Optional[ColorFilter] = None
    """
    A color filter to apply to the image before painting it.

    Value is of type [`ColorFilter`](https://flet.dev/docs/reference/types/colorfilter).
    """

    fit: Optional[BoxFit] = None
    """
    How the image should be inscribed into the box.

    Value is of type [`BoxFit`](https://flet.dev/docs/reference/types/imagefit).
    """

    alignment: Alignment = field(default_factory=lambda: Alignment.center())
    """
    The alignment of the image within its bounds.

    Value is of type [`Alignment`](https://flet.dev/docs/reference/types/alignment).
    """

    repeat: ImageRepeat = ImageRepeat.NO_REPEAT
    """
    How the image should be repeated to fill the box.

    Value is of type [`ImageRepeat`](https://flet.dev/docs/reference/types/imagerepeat).
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

    Value is of type [`FilterQuality`](https://flet.dev/docs/reference/types/filterquality).
    """

    invert_colors: bool = False
    """
    Whether to invert the colors of the image while drawing.
    """

    anti_alias: bool = False
    """
    Whether to paint the image in anti-aliased quality.
    """


@dataclass
class BoxDecoration:
    """
    BoxDecoration provides a description of how to paint a box.
    The box has a border, a body, and may cast a shadow.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The [color](https://flet.dev/docs/reference/colors) to fill in the background of
    the box.
    """

    image: Optional[DecorationImage] = None
    """
    An image to paint above the background `color` or `gradient`.

    Value is of type [`DecorationImage`](https://flet.dev/docs/reference/types/decorationimage).
    """

    border: Optional[Border] = None
    """
    A border to draw above the background `color`, `gradient`, or `image`.

    Value is of type [`Border`](https://flet.dev/docs/reference/types/border).
    """

    border_radius: Optional[BorderRadiusValue] = None
    """
    The border radius of the box.

    Value is of type [`BorderRadius`](https://flet.dev/docs/reference/types/borderradius).
    """

    shadow: Optional[ShadowValue] = None
    """
    A list of shadows cast by the box.

    Value is of type [`List[BoxShadow]`](https://flet.dev/docs/reference/types/boxshadow).
    """

    gradient: Optional[Gradient] = None
    """
    A gradient to use when filling the box.
    """

    shape: BoxShape = BoxShape.RECTANGLE
    """
    The shape to fill the `bgcolor`, `gradient`, and `image` into and to cast as the
    `shadow`.
    """

    blend_mode: Optional[BlendMode] = None
    """
    The blend mode to apply to the background `color` or `gradient`.

    Value is of type [`BlendMode`](https://flet.dev/docs/reference/types/blendmode).
    """

    def __post_init__(self):
        assert (
            self.blend_mode is None
            or self.bgcolor is not None
            or self.gradient is not None
        ), (
            "blend_mode applies to the BoxDecoration's background color or gradient, but no color or gradient was provided"
        )
        assert not (self.shape == BoxShape.CIRCLE and self.border_radius), (
            "border_radius must be None when shape is BoxShape.CIRCLE"
        )

    def copy_with(
        self,
        *,
        bgcolor: Optional[ColorValue] = None,
        image: Optional[DecorationImage] = None,
        border: Optional[Border] = None,
        border_radius: Optional[BorderRadiusValue] = None,
        shadow: Optional[ShadowValue] = None,
        gradient: Optional[Gradient] = None,
        shape: Optional[BoxShape] = None,
        blend_mode: Optional[BlendMode] = None,
    ):
        return BoxDecoration(
            bgcolor=bgcolor if bgcolor is not None else self.bgcolor,
            image=image if image is not None else self.image,
            border=border if border is not None else self.border,
            border_radius=border_radius
            if border_radius is not None
            else self.border_radius,
            shadow=shadow if shadow is not None else self.shadow,
            gradient=gradient if gradient is not None else self.gradient,
            shape=shape if shape is not None else self.shape,
            blend_mode=blend_mode if blend_mode is not None else self.blend_mode,
        )


@dataclass
class BoxConstraints:
    """
    Constraints that must be respected by a size of a box.

    A Size respects a BoxConstraints if, and only if, all of the following relations
    hold:

        min_width <= Size.width <= max_width
        min_height <= Size.height <= max_height

    Read more about BoxConstraints [here](https://api.flutter.dev/flutter/rendering/BoxConstraints-class.html).
    """

    min_width: Number = 0
    """
    The minimum width that satisfies the constraints, such that
    `0.0 <= min_width <= max_width`.

    Value is of type [`Number`](https://flet.dev/docs/reference/types/aliases#number).
    """

    min_height: Number = 0
    """
    The minimum height that satisfies the constraints, such that
    `0.0 <= min_height <= max_height`.

    Value is of type [`Number`](https://flet.dev/docs/reference/types/aliases#number).
    """

    max_width: Number = float("inf")
    """
    The maximum width that satisfies the constraints, such that
    `min_width <= max_width <= float("inf")`.

    Value is of type [`Number`](https://flet.dev/docs/reference/types/aliases#number)
    and defaults to infinity.
    """

    max_height: Number = float("inf")
    """
    The maximum height that satisfies the constraints, such that
    `min_height <= max_height <= float("inf")`.

    Value is of type [`Number`](https://flet.dev/docs/reference/types/aliases#number)
    and defaults to infinity.
    """

    def __post_init__(self):
        assert 0 <= self.min_width <= self.max_width <= float("inf"), (
            "min_width and max_width must be between 0 and infinity "
            "and min_width must be less than or equal to max_width"
        )
        assert 0 <= self.min_height <= self.max_height <= float("inf"), (
            "min_height and max_height must be between 0 and infinity "
            "and min_height must be less than or equal to max_height"
        )
