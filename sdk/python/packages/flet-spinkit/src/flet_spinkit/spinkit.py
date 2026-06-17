from enum import Enum
from typing import Optional

import flet as ft

__all__ = [
    "ChasingDots",
    "Circle",
    "CubeGrid",
    "DancingSquare",
    "DoubleBounce",
    "DualRing",
    "FadingCircle",
    "FadingCube",
    "FadingFour",
    "FadingGrid",
    "FoldingCube",
    "HourGlass",
    "PianoWave",
    "PouringHourGlass",
    "PouringHourGlassRefined",
    "Pulse",
    "PulsingGrid",
    "PumpingHeart",
    "Ring",
    "Ripple",
    "RotatingCircle",
    "RotatingPlain",
    "SpinningCircle",
    "SpinningLines",
    "SquareCircle",
    "ThreeBounce",
    "ThreeInOut",
    "WanderingCubes",
    "Wave",
    "WaveSpinner",
    "WaveType",
]


class WaveType(Enum):
    """Controls how the wave animation is aligned."""

    START = "start"
    """Wave animation starts from the first item."""

    CENTER = "center"
    """Wave animation radiates from the center."""

    END = "end"
    """Wave animation starts from the last item."""


@ft.control("SpinKitRotatingPlain")
class RotatingPlain(ft.LayoutControl):
    """A plain rotating square spinner."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitDoubleBounce")
class DoubleBounce(ft.LayoutControl):
    """Two overlapping circles that bounce in and out."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitWave")
class Wave(ft.LayoutControl):
    """A row of bars that animate in a wave pattern."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""

    wave_type: Optional[WaveType] = None
    """Controls the wave propagation direction.

    Defaults to :attr:`WaveType.START`.
    """

    item_count: Optional[int] = None
    """Number of bars in the wave. Defaults to 5."""


@ft.control("SpinKitWanderingCubes")
class WanderingCubes(ft.LayoutControl):
    """Two cubes that rotate and wander around each other."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitFadingFour")
class FadingFour(ft.LayoutControl):
    """Four dots arranged in a square that fade in sequence."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitFadingCube")
class FadingCube(ft.LayoutControl):
    """A cube made of four smaller cubes that fade and rotate."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitPulse")
class Pulse(ft.LayoutControl):
    """A circle that pulses in and out."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitChasingDots")
class ChasingDots(ft.LayoutControl):
    """Two dots that chase each other in a circular path."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitThreeBounce")
class ThreeBounce(ft.LayoutControl):
    """Three dots that bounce sequentially."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitCircle")
class Circle(ft.LayoutControl):
    """A ring of dots that fade sequentially around a circle."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitCubeGrid")
class CubeGrid(ft.LayoutControl):
    """A 3x3 grid of cubes that scale and fade in a wave."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitFadingCircle")
class FadingCircle(ft.LayoutControl):
    """A ring of dots that fade sequentially."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitRotatingCircle")
class RotatingCircle(ft.LayoutControl):
    """A circle that rotates with a color gradient effect."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitFoldingCube")
class FoldingCube(ft.LayoutControl):
    """Four cubes that fold and unfold in sequence."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitPumpingHeart")
class PumpingHeart(ft.LayoutControl):
    """A heart shape that pumps in and out."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitHourGlass")
class HourGlass(ft.LayoutControl):
    """An hourglass shape that rotates."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitPouringHourGlass")
class PouringHourGlass(ft.LayoutControl):
    """An hourglass that pours dots from top to bottom."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitPouringHourGlassRefined")
class PouringHourGlassRefined(ft.LayoutControl):
    """A refined version of the pouring hourglass with smoother animation."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitFadingGrid")
class FadingGrid(ft.LayoutControl):
    """A 3x3 grid of dots that fade in a spiral sequence."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitRing")
class Ring(ft.LayoutControl):
    """A ring that spins with a gap."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""

    line_width: Optional[ft.Number] = None
    """The stroke width of the ring. Defaults to 7."""


@ft.control("SpinKitRipple")
class Ripple(ft.LayoutControl):
    """Two concentric circles that expand outward like a ripple."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""

    border_width: Optional[ft.Number] = None
    """The stroke width of the ripple rings. Defaults to 6."""


@ft.control("SpinKitDualRing")
class DualRing(ft.LayoutControl):
    """Two concentric rings that spin in opposite directions."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""

    line_width: Optional[ft.Number] = None
    """The stroke width of the rings. Defaults to 7."""


@ft.control("SpinKitSpinningCircle")
class SpinningCircle(ft.LayoutControl):
    """A circle that spins continuously."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitSpinningLines")
class SpinningLines(ft.LayoutControl):
    """Multiple lines radiating from the center that spin."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""

    line_width: Optional[ft.Number] = None
    """The stroke width of the lines. Defaults to 2."""


@ft.control("SpinKitSquareCircle")
class SquareCircle(ft.LayoutControl):
    """A square and a circle that morph between shapes."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitThreeInOut")
class ThreeInOut(ft.LayoutControl):
    """Three dots that move in and out of view."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitDancingSquare")
class DancingSquare(ft.LayoutControl):
    """A square that dances by rotating and scaling."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitPianoWave")
class PianoWave(ft.LayoutControl):
    """A row of bars that animate like piano keys."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""

    item_count: Optional[int] = None
    """Number of bars. Defaults to 5."""


@ft.control("SpinKitPulsingGrid")
class PulsingGrid(ft.LayoutControl):
    """A 3x3 grid of dots that pulse in sequence."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitWaveSpinner")
class WaveSpinner(ft.LayoutControl):
    """A circular wave spinner."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""
