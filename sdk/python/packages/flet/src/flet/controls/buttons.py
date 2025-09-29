from dataclasses import dataclass, field
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.border import BorderSide
from flet.controls.border_radius import BorderRadiusValue
from flet.controls.control_state import ControlStateValue
from flet.controls.duration import DurationValue
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ColorValue,
    MouseCursor,
    Number,
    VisualDensity,
)

__all__ = [
    "BeveledRectangleBorder",
    "ButtonStyle",
    "CircleBorder",
    "ContinuousRectangleBorder",
    "OutlinedBorder",
    "RoundedRectangleBorder",
    "ShapeBorder",
    "StadiumBorder",
]


@dataclass
class ShapeBorder:
    """
    Base class for shape outlines. Not intended to be used directly.

    See subclasses/implementations:

    - [`OutlinedBorder`][flet.]
    """


@dataclass
class OutlinedBorder(ShapeBorder):
    """
    An abstract class that can be used to create custom borders.

    See subclasses/implementations:

    - [`BeveledRectangleBorder`][flet.]
    - [`ContinuousRectangleBorder`][flet.]
    - [`CircleBorder`][flet.]
    - [`RoundedRectangleBorder`][flet.]
    - [`StadiumBorder`][flet.]
    """

    side: Optional[BorderSide] = None
    """
    The border outline's color and weight.
    """

    _type: Optional[str] = field(init=False, repr=False, compare=False, default=None)


@dataclass
class StadiumBorder(OutlinedBorder):
    """
    A border that looks like a stadium.
    """

    def __post_init__(self):
        self._type = "stadium"

    def copy(
        self,
        *,
        side: Optional[BorderSide] = None,
    ) -> "StadiumBorder":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return StadiumBorder(
            side=side if side is not None else self.side,
        )


@dataclass
class RoundedRectangleBorder(OutlinedBorder):
    """
    A border with rounded rectangle corners.
    """

    radius: Optional[BorderRadiusValue] = None
    """
    The radius for each corner.
    """

    def __post_init__(self):
        self._type = "roundedRectangle"

    def copy(
        self,
        *,
        side: Optional[BorderSide] = None,
        radius: Optional[BorderRadiusValue] = None,
    ) -> "RoundedRectangleBorder":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return RoundedRectangleBorder(
            side=side if side is not None else self.side,
            radius=radius if radius is not None else self.radius,
        )


@dataclass
class CircleBorder(OutlinedBorder):
    """
    A border with a circle shape.
    """

    eccentricity: Number = 0.0

    def __post_init__(self):
        self._type = "circle"

    def copy(
        self,
        *,
        side: Optional[BorderSide] = None,
        eccentricity: Optional[Number] = None,
    ) -> "CircleBorder":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return CircleBorder(
            side=side if side is not None else self.side,
            eccentricity=eccentricity
            if eccentricity is not None
            else self.eccentricity,
        )


@dataclass
class BeveledRectangleBorder(RoundedRectangleBorder):
    """
    A border with beveled rectangle corners.
    """

    def __post_init__(self):
        self._type = "beveledRectangle"

    def copy(
        self,
        *,
        side: Optional[BorderSide] = None,
        radius: Optional[BorderRadiusValue] = None,
    ) -> "BeveledRectangleBorder":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return BeveledRectangleBorder(
            side=side if side is not None else self.side,
            radius=radius if radius is not None else self.radius,
        )


@dataclass
class ContinuousRectangleBorder(RoundedRectangleBorder):
    """
    A border with continuous rectangle corners.
    """

    def __post_init__(self):
        self._type = "continuousRectangle"

    def copy(
        self,
        *,
        side: Optional[BorderSide] = None,
        radius: Optional[BorderRadiusValue] = None,
    ) -> "ContinuousRectangleBorder":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return ContinuousRectangleBorder(
            side=side if side is not None else self.side,
            radius=radius if radius is not None else self.radius,
        )


@dataclass
class ButtonStyle:
    """
    Allows controlling all visual aspects of a button, such as shape, foreground,
    background and shadow colors, content padding, border width and radius.

    Most of these style attributes could be configured for all or particular
    [`ControlState`][flet.] of a button,
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

    elevation: Optional[ControlStateValue[Optional[Number]]] = None
    """
    The elevation of the button's Material.
    """

    animation_duration: Optional[DurationValue] = None
    """
    Defines the duration in milliseconds of animated changes for shape and
    elevation.
    """

    padding: Optional[ControlStateValue[PaddingValue]] = None
    """
    The padding between the button's boundary and its content.
    """

    side: Optional[ControlStateValue[BorderSide]] = None
    """
    Defines the button's border outline.
    """

    shape: Optional[ControlStateValue[OutlinedBorder]] = None
    """
    The shape of the button's underlying Material.
    """

    alignment: Optional[Alignment] = None
    """
    The alignment of the button's content.
    """

    enable_feedback: Optional[bool] = None
    """
    Whether detected gestures should provide acoustic and/or haptic feedback.
    """

    text_style: Optional[ControlStateValue[TextStyle]] = None
    """
    The text style of the button's `Text` control descendants.
    """

    icon_size: Optional[ControlStateValue[Optional[Number]]] = None
    """
    The icon's size inside of the button.
    """

    icon_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The icon's color inside the button.

    If not set or `None`, then the `color` will be used.
    """

    visual_density: Optional[VisualDensity] = None
    """
    Defines how compact the button's layout will be.
    """

    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    The cursor to be displayed when the mouse pointer enters or is hovering
    over the button.
    """

    def copy(
        self,
        *,
        color: Optional[ControlStateValue[ColorValue]] = None,
        bgcolor: Optional[ControlStateValue[ColorValue]] = None,
        overlay_color: Optional[ControlStateValue[ColorValue]] = None,
        shadow_color: Optional[ControlStateValue[ColorValue]] = None,
        elevation: Optional[ControlStateValue[Optional[Number]]] = None,
        animation_duration: Optional[DurationValue] = None,
        padding: Optional[ControlStateValue[PaddingValue]] = None,
        side: Optional[ControlStateValue[BorderSide]] = None,
        shape: Optional[ControlStateValue[OutlinedBorder]] = None,
        alignment: Optional[Alignment] = None,
        enable_feedback: Optional[bool] = None,
        text_style: Optional[ControlStateValue[TextStyle]] = None,
        icon_size: Optional[ControlStateValue[Optional[Number]]] = None,
        icon_color: Optional[ControlStateValue[ColorValue]] = None,
        visual_density: Optional[VisualDensity] = None,
        mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None,
    ) -> "ButtonStyle":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return ButtonStyle(
            color=color if color is not None else self.color,
            bgcolor=bgcolor if bgcolor is not None else self.bgcolor,
            overlay_color=overlay_color
            if overlay_color is not None
            else self.overlay_color,
            shadow_color=shadow_color
            if shadow_color is not None
            else self.shadow_color,
            elevation=elevation if elevation is not None else self.elevation,
            animation_duration=animation_duration
            if animation_duration is not None
            else self.animation_duration,
            padding=padding if padding is not None else self.padding,
            side=side if side is not None else self.side,
            shape=shape if shape is not None else self.shape,
            alignment=alignment if alignment is not None else self.alignment,
            enable_feedback=enable_feedback
            if enable_feedback is not None
            else self.enable_feedback,
            text_style=text_style if text_style is not None else self.text_style,
            icon_size=icon_size if icon_size is not None else self.icon_size,
            icon_color=icon_color if icon_color is not None else self.icon_color,
            visual_density=visual_density
            if visual_density is not None
            else self.visual_density,
            mouse_cursor=mouse_cursor
            if mouse_cursor is not None
            else self.mouse_cursor,
        )
