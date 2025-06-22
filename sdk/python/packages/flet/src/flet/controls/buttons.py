from dataclasses import dataclass, field
from typing import Optional

from flet.controls.alignment import OptionalAlignment
from flet.controls.border import BorderSide, OptionalBorderSide
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.control_state import ControlStateValue
from flet.controls.duration import OptionalDurationValue
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ColorValue,
    MouseCursor,
    Number,
    OptionalBool,
    OptionalNumber,
    VisualDensity,
)

__all__ = [
    "BeveledRectangleBorder",
    "ButtonStyle",
    "CircleBorder",
    "ContinuousRectangleBorder",
    "OutlinedBorder",
    "RoundedRectangleBorder",
    "StadiumBorder",
    "OptionalButtonStyle",
    "OptionalOutlinedBorder",
]


@dataclass(kw_only=True)
class OutlinedBorder:
    """
    An abstract class that can be used to create custom borders.
    """

    side: OptionalBorderSide = None
    """
    The border outline's color and weight.
    """

    _type: Optional[str] = field(init=False, repr=False, compare=False, default=None)


@dataclass
class StadiumBorder(OutlinedBorder):
    """
    Creates a border that looks like a stadium.
    """

    def __post_init__(self):
        self._type = "stadium"


@dataclass
class RoundedRectangleBorder(OutlinedBorder):
    """
    Creates a border with rounded rectangle corners.
    """

    radius: OptionalBorderRadiusValue = None
    """
    Border radius, an instance of [`BorderRadius`](/docs/reference/types/borderradius) 
    or a number.
    """

    def __post_init__(self):
        self._type = "roundedRectangle"


@dataclass
class CircleBorder(OutlinedBorder):
    """
    Creates a border with a circle shape.
    """

    eccentricity: Number = 0.0

    def __post_init__(self):
        self._type = "circle"


@dataclass
class BeveledRectangleBorder(OutlinedBorder):
    """
    Creates a border with beveled rectangle corners.
    """

    radius: OptionalBorderRadiusValue = None
    """
    Border radius, an instance of [`BorderRadius`](/docs/reference/types/borderradius) 
    or a number.
    """

    def __post_init__(self):
        self._type = "beveledRectangle"


@dataclass
class ContinuousRectangleBorder(OutlinedBorder):
    """
    Creates a border with continuous rectangle corners.
    """

    radius: OptionalBorderRadiusValue = None
    """
    Border radius, an instance of [`BorderRadius`](/docs/reference/types/borderradius) 
    or a number.
    """

    def __post_init__(self):
        self._type = "continuousRectangle"


@dataclass
class ButtonStyle:
    """
    Allows controlling all visual aspects of a button, such as shape, foreground,
    background and shadow colors, content padding, border width and radius.

    Most of these style attributes could be configured for all or particular
    [`ControlState`](https://flet.dev/docs/reference/types/controlstate) of a button,
    such as `HOVERED`, `FOCUSED`, `DISABLED` and others.
    """

    color: Optional[ControlStateValue[ColorValue]] = None
    """
    The color for the button's Text and Icon control descendants.
    """

    bgcolor: Optional[ControlStateValue[ColorValue]] = None
    """
    The button's background fill color.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The highlight color that's typically used to indicate that the button is
    focused, hovered, or pressed.
    """

    shadow_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The shadow color of the button's Material.
    """

    surface_tint_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The surface tint color of the button's Material.
    """

    elevation: Optional[ControlStateValue[OptionalNumber]] = None
    """
    The elevation of the button's Material.
    """

    animation_duration: OptionalDurationValue = None
    """
    Defines the duration in milliseconds of animated changes for shape and
    elevation.
    """

    padding: Optional[ControlStateValue[PaddingValue]] = None
    """
    The padding between the button's boundary and its content.

    Value is of type [`Padding`](https://flet.dev/docs/reference/types/padding).
    """

    side: Optional[ControlStateValue[BorderSide]] = None
    """
    An instance of [`BorderSide`](https://flet.dev/docs/reference/types/borderside)
    class, the color and weight of the button's outline.
    """

    shape: Optional[ControlStateValue[OutlinedBorder]] = None
    """
    The shape of the button's underlying Material.

    Value is of type [`OutlinedBorder`](https://flet.dev/docs/reference/types/outlinedborder).
    """

    alignment: OptionalAlignment = None
    """
    The alignment of the button's content.

    Value is of type [`Alignment`](https://flet.dev/docs/reference/types/alignment).
    """

    enable_feedback: OptionalBool = None
    """
    Whether detected gestures should provide acoustic and/or haptic feedback.

    Value is of type `bool`.
    """

    text_style: Optional[ControlStateValue[TextStyle]] = None
    """
    The text style of the button's `Text` control descendants.

    Value is of type [`TextStyle`](https://flet.dev/docs/reference/types/textstyle).
    """

    icon_size: Optional[ControlStateValue[OptionalNumber]] = None
    """
    The icon's size inside of the button.
    """

    icon_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The icon's [color](https://flet.dev/docs/reference/colors) inside the button.

    If not set or `None`, then the `color` will be used.
    """

    visual_density: Optional[VisualDensity] = None
    """
    Defines how compact the button's layout will be.

    Value is of type [`VisualDensity`](https://flet.dev/docs/reference/types/visualdensity).
    """

    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    The cursor to be displayed when the mouse pointer enters or is hovering
    over the button.
    """


# Typing
OptionalButtonStyle = Optional[ButtonStyle]
OptionalOutlinedBorder = Optional[OutlinedBorder]
