from typing import Optional

from flet.controls.base_control import control
from flet.controls.box import BoxConstraints
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.padding import PaddingValue
from flet.controls.types import ColorValue, Number, StrokeCap

__all__ = ["ProgressRing"]


@control("ProgressRing")
class ProgressRing(ConstrainedControl):
    """
    A material design circular progress indicator, which spins to indicate that the
    application is busy.

    A control that shows progress along a circle.
    """

    value: Optional[Number] = None
    """
    The value of this progress indicator.

    A value of `0.0` means no progress and `1.0` means that progress is complete.
    The value will be clamped to be in the range `0.0` - `1.0`. If `None`, this
    progress indicator is indeterminate, which means the indicator displays a
    predetermined animation that does not indicate how much actual progress is being
    made.
    """

    stroke_width: Number = 4.0
    """
    The width of the line used to draw the circle.
    """

    color: Optional[ColorValue] = None
    """
    The progress indicator's [color](https://flet.dev/docs/reference/colors).
    """

    bgcolor: Optional[ColorValue] = None
    """
    [Color](https://flet.dev/docs/reference/colors) of the circular track being filled
    by the circular indicator.
    """

    stroke_align: Number = 0.0
    """
    The relative position of the stroke.

    Value typically ranges be `-1.0` (inside stroke) and `1.0` (outside stroke).

    Defaults to `0` - centered.
    """

    stroke_cap: Optional[StrokeCap] = None
    """
    The progress indicator's line ending.

    Type: [`StrokeCap`][flet.StrokeCap]
    """

    semantics_label: Optional[str] = None
    """
    The semantics label for this progress indicator.
    """

    semantics_value: Optional[Number] = None
    """
    The `Semantics.value` for this progress indicator.
    """

    track_gap: Optional[Number] = None
    """
    TBD
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    TBD
    """

    padding: Optional[PaddingValue] = None
    """
    TBD
    """

    year_2023: Optional[bool] = None
    """
    TBD
    """
