from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

import flet as ft

__all__ = [
    "ChartCirclePoint",
    "ChartCrossPoint",
    "ChartDataPointTooltip",
    "ChartEventType",
    "ChartGridLines",
    "ChartPointLine",
    "ChartPointShape",
    "ChartSquarePoint",
    "HorizontalAlignment",
]


@dataclass
class ChartGridLines:
    """
    Configures the appearance of horizontal and vertical grid lines within the chart.
    """

    interval: Optional[ft.Number] = None
    """
    The interval between grid lines.
    """

    color: Optional[ft.ColorValue] = None
    """
    The color of a grid line.
    """

    width: ft.Number = 2.0
    """
    The width of a grid line.
    """

    dash_pattern: Optional[list[int]] = None
    """
    Defines dash effect of the line. The value is a circular list of dash offsets
    and lengths. For example, the list `[5, 10]` would result in dashes 5 pixels long
    followed by blank spaces 10 pixels long. By default, a solid line is drawn.
    """

    def copy(
        self,
        *,
        interval: Optional[ft.Number] = None,
        color: Optional[ft.ColorValue] = None,
        width: Optional[ft.Number] = None,
        dash_pattern: Optional[list[int]] = None,
    ) -> "ChartGridLines":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return ChartGridLines(
            interval=interval if interval is not None else self.interval,
            color=color if color is not None else self.color,
            width=width if width is not None else self.width,
            dash_pattern=dash_pattern.copy()
            if dash_pattern is not None
            else (self.dash_pattern.copy() if self.dash_pattern is not None else None),
        )


@dataclass
class ChartPointShape:
    """
    Base class for chart point shapes.

    See usable subclasses:

    * [`ChartCirclePoint`][(p).]
    * [`ChartCrossPoint`][(p).]
    * [`ChartSquarePoint`][(p).]
    """

    _type: Optional[str] = field(init=False, repr=False, compare=False, default=None)


@dataclass
class ChartCirclePoint(ChartPointShape):
    """Draws a circle."""

    color: Optional[ft.ColorValue] = None
    """
    The fill color to use for the circle.
    """

    radius: Optional[ft.Number] = None
    """
    The radius of the circle.
    """

    stroke_color: Optional[ft.ColorValue] = None
    """
    The stroke color to use for the circle
    """

    stroke_width: ft.Number = 0
    """
    The stroke width to use for the circle.
    """

    def __post_init__(self):
        self._type = "ChartCirclePoint"

    def copy(
        self,
        *,
        color: Optional[ft.ColorValue] = None,
        radius: Optional[ft.Number] = None,
        stroke_color: Optional[ft.ColorValue] = None,
        stroke_width: Optional[ft.Number] = None,
    ) -> "ChartCirclePoint":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return ChartCirclePoint(
            color=color if color is not None else self.color,
            radius=radius if radius is not None else self.radius,
            stroke_color=stroke_color
            if stroke_color is not None
            else self.stroke_color,
            stroke_width=stroke_width
            if stroke_width is not None
            else self.stroke_width,
        )


@dataclass
class ChartSquarePoint(ChartPointShape):
    """Draws a square."""

    color: Optional[ft.ColorValue] = None
    """
    The fill color to use for the square.
    """

    size: ft.Number = 4.0
    """
    The size of the square.
    """

    stroke_color: Optional[ft.ColorValue] = None
    """
    The stroke color to use for the square.
    """

    stroke_width: ft.Number = 1.0
    """
    The stroke width to use for the square.
    """

    def __post_init__(self):
        self._type = "ChartSquarePoint"

    def copy(
        self,
        *,
        color: Optional[ft.ColorValue] = None,
        size: Optional[ft.Number] = None,
        stroke_color: Optional[ft.ColorValue] = None,
        stroke_width: Optional[ft.Number] = None,
    ) -> "ChartSquarePoint":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return ChartSquarePoint(
            color=color if color is not None else self.color,
            size=size if size is not None else self.size,
            stroke_color=stroke_color
            if stroke_color is not None
            else self.stroke_color,
            stroke_width=stroke_width
            if stroke_width is not None
            else self.stroke_width,
        )


@dataclass
class ChartCrossPoint(ChartPointShape):
    """Draws a cross-mark (X)."""

    color: Optional[ft.ColorValue] = None
    """
    The fill color to use for the
    cross-mark(X).
    """

    size: ft.Number = 8.0
    """
    The size of the cross-mark.
    """

    width: ft.Number = 2.0
    """
    The thickness of the cross-mark.
    """

    def __post_init__(self):
        self._type = "ChartCrossPoint"

    def copy(
        self,
        *,
        color: Optional[ft.ColorValue] = None,
        size: Optional[ft.Number] = None,
        width: Optional[ft.Number] = None,
    ) -> "ChartCrossPoint":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return ChartCrossPoint(
            color=color if color is not None else self.color,
            size=size if size is not None else self.size,
            width=width if width is not None else self.width,
        )


@dataclass
class ChartPointLine:
    """Defines style of a line."""

    color: Optional[ft.ColorValue] = None
    """
    The line's color.
    """

    width: ft.Number = 2
    """
    The line's width.
    """

    dash_pattern: Optional[list[int]] = None
    """
    The line's dash pattern.
    """

    gradient: Optional[ft.Gradient] = None
    """
    The line's gradient.
    """

    def copy(
        self,
        *,
        color: Optional[ft.ColorValue] = None,
        width: Optional[ft.Number] = None,
        dash_pattern: Optional[list[int]] = None,
        gradient: Optional[ft.Gradient] = None,
    ) -> "ChartPointLine":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return ChartPointLine(
            color=color if color is not None else self.color,
            width=width if width is not None else self.width,
            dash_pattern=dash_pattern.copy()
            if dash_pattern is not None
            else self.dash_pattern.copy()
            if self.dash_pattern is not None
            else None,
            gradient=gradient if gradient is not None else self.gradient,
        )


class ChartEventType(Enum):
    """The type of event that occurred on the chart."""

    PAN_END = "panEnd"
    """
    When a pointer that was previously in contact with
    the screen and moving is no longer in contact with the screen.
    """

    PAN_CANCEL = "panCancel"
    """
    When the pointer that previously triggered a pan-start did not complete.
    """

    POINTER_EXIT = "pointerExit"
    """
    The pointer has moved with respect to the device while the
    pointer is or is not in contact with the device, and exited our chart.
    """

    LONG_PRESS_END = "longPressEnd"
    """
    When a pointer stops contacting the screen after a long press
    gesture was detected. Also reports the position where the
    pointer stopped contacting the screen.
    """

    TAP_UP = "tapUp"
    """
    When a pointer that will trigger a tap has stopped contacting the screen.
    """

    TAP_CANCEL = "tapCancel"
    """
    When the pointer that previously triggered a tap-down will not end up causing a tap.
    """

    POINTER_ENTER = "pointerEnter"
    """
    The pointer has moved with respect to the device while the pointer is or is
    not in contact with the device, and it has entered our chart.
    """

    POINTER_HOVER = "pointerHover"
    """
    The pointer has moved with respect to the device while the pointer is not
    in contact with the device.
    """

    PAN_DOWN = "panDown"
    """
    When a pointer has contacted the screen and might begin to move
    """

    PAN_START = "panStart"
    """
    When a pointer has contacted the screen and has begun to move.
    """

    PAN_UPDATE = "panUpdate"
    """
    When a pointer that is in contact with the screen and moving
    has moved again.
    """

    LONG_PRESS_MOVE_UPDATE = "longPressMoveUpdate"
    """
    When a pointer is moving after being held in contact at the same
    location for a long period of time. Reports the new position and its offset
    from the original down position.
    """

    LONG_PRESS_START = "longPressStart"
    """
    When a pointer has remained in contact with the screen at the
    same location for a long period of time.
    """

    TAP_DOWN = "tapDown"
    """
    When a pointer that might cause a tap has contacted the
    screen.
    """

    UNDEFINED = "undefined"
    """
    An undefined event.
    """


@dataclass
class ChartDataPointTooltip:
    """
    Configuration of the tooltip for data points in charts.
    """

    text: Optional[str] = None
    """
    The text to display in this tooltip.
    """

    text_style: ft.TextStyle = field(default_factory=lambda: ft.TextStyle())
    """
    A text style to display tooltip with.
    """

    text_align: ft.TextAlign = ft.TextAlign.CENTER
    """
    The text alignment of the tooltip.
    """

    text_spans: Optional[list[ft.TextSpan]] = None
    """
    Additional text spans to show on this tooltip.
    """

    rtl: bool = False
    """
    Whether the text is right-to-left.
    """

    def copy(
        self,
        *,
        text: Optional[str] = None,
        text_style: Optional[ft.TextStyle] = None,
        text_align: Optional[ft.TextAlign] = None,
        text_spans: Optional[list[ft.TextSpan]] = None,
        rtl: Optional[bool] = None,
    ) -> "ChartDataPointTooltip":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return ChartDataPointTooltip(
            text=text if text is not None else self.text,
            text_style=text_style if text_style is not None else self.text_style,
            text_align=text_align if text_align is not None else self.text_align,
            text_spans=text_spans.copy()
            if text_spans is not None
            else self.text_spans.copy()
            if self.text_spans is not None
            else None,
            rtl=rtl if rtl is not None else self.rtl,
        )


class HorizontalAlignment(Enum):
    """Defines an element's horizontal alignment to given point."""

    LEFT = "left"
    """Element shown on the left side of the given point."""

    CENTER = "center"
    """Element shown horizontally center aligned to a given point."""

    RIGHT = "right"
    """Element shown on the right side of the given point."""
