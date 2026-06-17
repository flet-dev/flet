from enum import Enum
from typing import Optional

import flet as ft

__all__ = [
    "SpinKitChasingDots",
    "SpinKitCircle",
    "SpinKitCubeGrid",
    "SpinKitDancingSquare",
    "SpinKitDoubleBounce",
    "SpinKitDualRing",
    "SpinKitFadingCircle",
    "SpinKitFadingCube",
    "SpinKitFadingFour",
    "SpinKitFadingGrid",
    "SpinKitFoldingCube",
    "SpinKitHourGlass",
    "SpinKitPianoWave",
    "SpinKitPouringHourGlass",
    "SpinKitPouringHourGlassRefined",
    "SpinKitPulse",
    "SpinKitPulsingGrid",
    "SpinKitPumpingHeart",
    "SpinKitRing",
    "SpinKitRipple",
    "SpinKitRotatingCircle",
    "SpinKitRotatingPlain",
    "SpinKitSpinningCircle",
    "SpinKitSpinningLines",
    "SpinKitSquareCircle",
    "SpinKitThreeBounce",
    "SpinKitThreeInOut",
    "SpinKitWanderingCubes",
    "SpinKitWave",
    "SpinKitWaveSpinner",
    "SpinKitWaveType",
]


class SpinKitWaveType(Enum):
    """Controls how the wave animation is aligned."""

    START = "start"
    """Wave animation starts from the first item."""

    CENTER = "center"
    """Wave animation radiates from the center."""

    END = "end"
    """Wave animation starts from the last item."""


@ft.control("SpinKitRotatingPlain")
class SpinKitRotatingPlain(ft.LayoutControl):
    """A plain rotating square spinner."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitDoubleBounce")
class SpinKitDoubleBounce(ft.LayoutControl):
    """Two overlapping circles that bounce in and out."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitWave")
class SpinKitWave(ft.LayoutControl):
    """A row of bars that animate in a wave pattern."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""

    wave_type: Optional[SpinKitWaveType] = None
    """Controls the wave propagation direction.

    Defaults to :attr:`SpinKitWaveType.START`.
    """

    item_count: Optional[int] = None
    """Number of bars in the wave. Defaults to 5."""


@ft.control("SpinKitWanderingCubes")
class SpinKitWanderingCubes(ft.LayoutControl):
    """Two cubes that rotate and wander around each other."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitFadingFour")
class SpinKitFadingFour(ft.LayoutControl):
    """Four dots arranged in a square that fade in sequence."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitFadingCube")
class SpinKitFadingCube(ft.LayoutControl):
    """A cube made of four smaller cubes that fade and rotate."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitPulse")
class SpinKitPulse(ft.LayoutControl):
    """A circle that pulses in and out."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitChasingDots")
class SpinKitChasingDots(ft.LayoutControl):
    """Two dots that chase each other in a circular path."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitThreeBounce")
class SpinKitThreeBounce(ft.LayoutControl):
    """Three dots that bounce sequentially."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitCircle")
class SpinKitCircle(ft.LayoutControl):
    """A ring of dots that fade sequentially around a circle."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitCubeGrid")
class SpinKitCubeGrid(ft.LayoutControl):
    """A 3×3 grid of cubes that scale and fade in a wave."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitFadingCircle")
class SpinKitFadingCircle(ft.LayoutControl):
    """A ring of dots that fade sequentially."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitRotatingCircle")
class SpinKitRotatingCircle(ft.LayoutControl):
    """A circle that rotates with a color gradient effect."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitFoldingCube")
class SpinKitFoldingCube(ft.LayoutControl):
    """Four cubes that fold and unfold in sequence."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitPumpingHeart")
class SpinKitPumpingHeart(ft.LayoutControl):
    """A heart shape that pumps in and out."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitHourGlass")
class SpinKitHourGlass(ft.LayoutControl):
    """An hourglass shape that rotates."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitPouringHourGlass")
class SpinKitPouringHourGlass(ft.LayoutControl):
    """An hourglass that pours dots from top to bottom."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitPouringHourGlassRefined")
class SpinKitPouringHourGlassRefined(ft.LayoutControl):
    """A refined version of the pouring hourglass with smoother animation."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitFadingGrid")
class SpinKitFadingGrid(ft.LayoutControl):
    """A 3×3 grid of dots that fade in a spiral sequence."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitRing")
class SpinKitRing(ft.LayoutControl):
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
class SpinKitRipple(ft.LayoutControl):
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
class SpinKitDualRing(ft.LayoutControl):
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
class SpinKitSpinningCircle(ft.LayoutControl):
    """A circle that spins continuously."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitSpinningLines")
class SpinKitSpinningLines(ft.LayoutControl):
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
class SpinKitSquareCircle(ft.LayoutControl):
    """A square and a circle that morph between shapes."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitThreeInOut")
class SpinKitThreeInOut(ft.LayoutControl):
    """Three dots that move in and out of view."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitDancingSquare")
class SpinKitDancingSquare(ft.LayoutControl):
    """A square that dances by rotating and scaling."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitPianoWave")
class SpinKitPianoWave(ft.LayoutControl):
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
class SpinKitPulsingGrid(ft.LayoutControl):
    """A 3×3 grid of dots that pulse in sequence."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""


@ft.control("SpinKitWaveSpinner")
class SpinKitWaveSpinner(ft.LayoutControl):
    """A circular wave spinner."""

    color: Optional[ft.ColorValue] = None
    """The color of the spinner."""

    size: Optional[ft.Number] = None
    """The size of the spinner in pixels. Defaults to 50."""

    duration: Optional[ft.DurationValue] = None
    """The duration of one animation cycle."""
