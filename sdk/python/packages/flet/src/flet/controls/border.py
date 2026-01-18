from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union

from flet.controls.colors import Colors
from flet.controls.types import ColorValue, Number
from flet.utils import deprecated

__all__ = [
    "Border",
    "BorderSide",
    "BorderSideStrokeAlign",
    "BorderSideStrokeAlignValue",
    "BorderStyle",
    "all",
    "only",
    "symmetric",
]


class BorderSideStrokeAlign(float, Enum):
    INSIDE = -1.0
    """
    The border is drawn fully inside of the border path.
    """

    CENTER = 0.0
    """
    The border is drawn on the center of the border path, with half of the
    `BorderSide.width` on the inside, and the other half on the outside of
    the path.
    """

    OUTSIDE = 1.0
    """
    The border is drawn on the outside of the border path.
    """


class BorderStyle(Enum):
    NONE = "none"
    """Skip the border."""

    SOLID = "solid"
    """Draw the border as a solid line."""


@dataclass
class BorderSide:
    """
    Creates the side of a border.

    By default, the border is `1.0` logical pixels wide and solid black color.
    """

    width: Number = 1.0
    """
    The width of this side of the border, in logical pixels.

    Setting width to 0.0 will result in a hairline border. This means that
    the border will have the width of one physical pixel. Hairline
    rendering takes shortcuts when the path overlaps a pixel more than once.
    This means that it will render faster than otherwise, but it might
    double-hit pixels, giving it a slightly darker/lighter result.

    Tip:
        To omit the border entirely, set the [`style`][(c).]
        to [`BorderStyle.NONE`][flet.].

    Raises:
        ValueError: If it is less than zero.
    """

    color: ColorValue = Colors.BLACK
    """
    The color of this side of the border.
    """

    stroke_align: "BorderSideStrokeAlignValue" = BorderSideStrokeAlign.INSIDE
    """
    The relative position of the stroke on a `BorderSide` in an
    `OutlinedBorder` or `Border`.
    """

    style: BorderStyle = BorderStyle.SOLID
    """
    The style of this side of the border.

    Tip:
        To omit a side, set `style` to [`BorderStyle.NONE`][flet.]. This skips
        painting the border, but the border still has a `width`.
    """

    def __post_init__(self):
        if self.width < 0.0:
            raise ValueError(
                f"width must be greater than or equal to 0.0, got {self.width}"
            )

    # Properties

    @property
    def stroke_inset(self):
        """
        The amount of the stroke width that lies inside this `BorderSide`.

        For example, this will return the `width` for a `stroke_align` of `-`1, half
        the `width` for a `stroke_align` of `0`, and `0` for a `stroke_align` of `1`.
        """
        return self.width * (1 - (1 + self.stroke_align) / 2)

    @property
    def stroke_outset(self):
        """
        The amount of the stroke width that lies outside this `BorderSide`.

        For example, this will return `0` for a `stroke_align` of `-1`, half the
        `width` for a `stroke_align` of `0`, and the `width` for a
        `stroke_align` of `1`.
        """
        return self.width * (1 + self.stroke_align) / 2

    @property
    def stroke_offset(self):
        """
        The offset of the stroke, taking into account the stroke alignment.

        For example, this will return the negative `width` of the stroke
        for a `stroke_align` of -1, 0 for a `stroke_align` of 0, and the
        `width` for a `stroke_align` of -1.
        """
        return self.width * self.stroke_align

    # Instance Methods

    def copy(
        self,
        *,
        width: Optional[Number] = None,
        color: Optional[ColorValue] = None,
        stroke_align: Optional["BorderSideStrokeAlignValue"] = None,
    ) -> "BorderSide":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return BorderSide(
            width=width if width is not None else self.width,
            color=color if color is not None else self.color,
            stroke_align=stroke_align
            if stroke_align is not None
            else self.stroke_align,
        )

    # Static Methods

    @staticmethod
    def none() -> "BorderSide":
        """A hairline black border that is not rendered."""
        return BorderSide(width=0.0, style=BorderStyle.NONE)


@dataclass
class Border:
    """
    A border comprised of four sides: `top`, `right`, `bottom`, `left`.

    Each side of the border is an instance of
    [`BorderSide`][flet.].
    """

    top: BorderSide = field(default_factory=lambda: BorderSide.none())
    """
    Top side of the border.
    """

    right: BorderSide = field(default_factory=lambda: BorderSide.none())
    """
    Right side of the border.
    """

    bottom: BorderSide = field(default_factory=lambda: BorderSide.none())
    """
    Bottom side of the border.
    """

    left: BorderSide = field(default_factory=lambda: BorderSide.none())
    """
    Left side of the border.
    """

    # Class Methods

    @classmethod
    def all(
        cls,
        width: Optional[Number] = None,
        color: Optional[ColorValue] = None,
        side: Optional[BorderSide] = None,
    ) -> "Border":
        """
        Creates a border whose sides are all the same.

        If `side` is not `None`, it gets used and both `width` and `color` are ignored.
        """
        if side is not None:
            return Border(top=side, right=side, bottom=side, left=side)
        bs = BorderSide(width or 1.0, color or Colors.BLACK)
        return Border(left=bs, top=bs, right=bs, bottom=bs)

    @classmethod
    def symmetric(
        cls,
        *,
        vertical: Optional[BorderSide] = None,
        horizontal: Optional[BorderSide] = None,
    ) -> "Border":
        """
        Creates a border with symmetrical vertical and horizontal sides.

        The `vertical` argument applies to the `left` and `right` sides,
        and the `horizontal` argument applies to the `top` and `bottom` sides.
        """
        if vertical is None:
            vertical = BorderSide(width=0.0, style=BorderStyle.NONE)
        if horizontal is None:
            horizontal = BorderSide(width=0.0, style=BorderStyle.NONE)
        return Border(left=horizontal, top=vertical, right=horizontal, bottom=vertical)

    @classmethod
    def only(
        cls,
        *,
        left: Optional[BorderSide] = None,
        top: Optional[BorderSide] = None,
        right: Optional[BorderSide] = None,
        bottom: Optional[BorderSide] = None,
    ) -> "Border":
        """Creates a `Border` from the given values."""
        return Border(
            left=left or BorderSide(width=0.0, style=BorderStyle.NONE),
            top=top or BorderSide(width=0.0, style=BorderStyle.NONE),
            right=right or BorderSide(width=0.0, style=BorderStyle.NONE),
            bottom=bottom or BorderSide(width=0.0, style=BorderStyle.NONE),
        )

    # Instance Methods

    def copy(
        self,
        *,
        left: Optional[BorderSide] = None,
        top: Optional[BorderSide] = None,
        right: Optional[BorderSide] = None,
        bottom: Optional[BorderSide] = None,
    ) -> "Border":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return Border(
            left=left if left is not None else self.left,
            top=top if top is not None else self.top,
            right=right if right is not None else self.right,
            bottom=bottom if bottom is not None else self.bottom,
        )


@deprecated(
    reason="Use Border.all() instead.",
    version="0.80.0",
    delete_version="0.83.0",
    show_parentheses=True,
)
def all(width: Optional[Number] = None, color: Optional[ColorValue] = None) -> Border:
    bs = BorderSide(width or 1.0, color or Colors.BLACK)
    return Border(left=bs, top=bs, right=bs, bottom=bs)


@deprecated(
    reason="Use Border.symmetric() instead.",
    version="0.80.0",
    delete_version="0.83.0",
    show_parentheses=True,
)
def symmetric(
    vertical: Optional[BorderSide] = None, horizontal: Optional[BorderSide] = None
) -> Border:
    return Border(left=horizontal, top=vertical, right=horizontal, bottom=vertical)


@deprecated(
    reason="Use Border.only() instead.",
    version="0.80.0",
    delete_version="0.83.0",
    show_parentheses=True,
)
def only(
    left: Optional[BorderSide] = None,
    top: Optional[BorderSide] = None,
    right: Optional[BorderSide] = None,
    bottom: Optional[BorderSide] = None,
) -> Border:
    return Border(left=left, top=top, right=right, bottom=bottom)


BorderSideStrokeAlignValue = Union[BorderSideStrokeAlign, Number]
