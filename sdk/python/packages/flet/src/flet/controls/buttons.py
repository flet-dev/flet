from dataclasses import dataclass
from typing import Optional

from flet.controls.alignment import OptionalAlignment
from flet.controls.border import BorderSide, OptionalBorderSide
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.control_state import OptionalControlStateValue
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
    type: str = ""


@dataclass
class StadiumBorder(OutlinedBorder):
    """
    Creates a border that looks like a stadium.
    """

    def __post_init__(self):
        self.type = "stadium"


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
        self.type = "roundedRectangle"


@dataclass
class CircleBorder(OutlinedBorder):
    """
    Creates a border with a circle shape.
    """

    eccentricity: Number = 0.0

    def __post_init__(self):
        self.type = "circle"


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
        self.type = "beveledRectangle"


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
        self.type = "continuousRectangle"


@dataclass
class ButtonStyle:
    """
    Allows controlling all visual aspects of a button, such as shape, foreground,
    background and shadow colors, content padding, border width and radius.

    Most of these style attributes could be configured for all or particular
    [`ControlState`](https://flet.dev/docs/reference/types/controlstate) of a button,
    such as `HOVERED`, `FOCUSED`, `DISABLED` and others.
    """

    color: OptionalControlStateValue[ColorValue] = None
    """
    The color for the button's Text and Icon control descendants.
    """

    bgcolor: OptionalControlStateValue[ColorValue] = None
    """
    The button's background fill color.
    """

    overlay_color: OptionalControlStateValue[ColorValue] = None
    """
    The highlight color that's typically used to indicate that the button is
    focused, hovered, or pressed.
    """

    shadow_color: OptionalControlStateValue[ColorValue] = None
    """
    The shadow color of the button's Material.
    """

    surface_tint_color: OptionalControlStateValue[ColorValue] = None
    """
    The surface tint color of the button's Material.
    """

    elevation: OptionalControlStateValue[OptionalNumber] = None
    """
    The elevation of the button's Material.
    """

    animation_duration: OptionalDurationValue = None
    """
    Defines the duration in milliseconds of animated changes for shape and
    elevation.
    """

    padding: OptionalControlStateValue[PaddingValue] = None
    """
    The padding between the button's boundary and its content.

    Value is of type [`Padding`](https://flet.dev/docs/reference/types/padding).
    """

    side: OptionalControlStateValue[BorderSide] = None
    """
    An instance of [`BorderSide`](https://flet.dev/docs/reference/types/borderside)
    class, the color and weight of the button's outline.
    """

    shape: OptionalControlStateValue[OutlinedBorder] = None
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

    text_style: OptionalControlStateValue[TextStyle] = None
    """
    The text style of the button's `Text` control descendants.

    Value is of type [`TextStyle`](https://flet.dev/docs/reference/types/textstyle).
    """

    icon_size: OptionalControlStateValue[OptionalNumber] = None
    """
    The icon's size inside of the button.
    """

    icon_color: OptionalControlStateValue[ColorValue] = None
    """
    The icon's [color](https://flet.dev/docs/reference/colors) inside the button.

    If not set or `None`, then the `color` will be used.
    """

    visual_density: Optional[VisualDensity] = None
    """
    Defines how compact the button's layout will be.

    Value is of type [`VisualDensity`](https://flet.dev/docs/reference/types/visualdensity).
    """

    mouse_cursor: OptionalControlStateValue[MouseCursor] = None
    """
    The cursor to be displayed when the mouse pointer enters or is hovering
    over the button.
    """


# Typing
OptionalButtonStyle = Optional[ButtonStyle]
OptionalOutlinedBorder = Optional[OutlinedBorder]
