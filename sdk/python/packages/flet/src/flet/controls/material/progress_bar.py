from typing import Optional

from flet.controls.base_control import control
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.types import OptionalColorValue, OptionalNumber

__all__ = ["ProgressBar"]


@control("ProgressBar")
class ProgressBar(ConstrainedControl):
    """
    A material design linear progress indicator, also known as a progress bar.

    A control that shows progress along a line.

    Online docs: https://flet.dev/docs/controls/progressbar
    """

    value: OptionalNumber = None
    """
    The value of this progress indicator.

    A value of `0.0` means no progress and `1.0` means that progress is complete. The
    value will be clamped to be in the range `0.0` - `1.0`.

    Defaults to `None`, meaning that this progress indicator is indeterminate -
    displays a predetermined animation that does not indicate how much actual progress
    is being made.
    """

    bar_height: OptionalNumber = 4.0
    """
    The minimum height of the line used to draw the linear indicator.

    Defaults to `4`.
    """

    color: OptionalColorValue = None
    """
    The progress indicator's [color](https://flet.dev/docs/reference/colors).
    """

    bgcolor: OptionalColorValue = None
    """
    [Color](https://flet.dev/docs/reference/colors) of the track being filled by the
    linear indicator.
    """

    border_radius: OptionalBorderRadiusValue = None
    """
    The border radius of both the indicator and the track.

    Border radius is an instance of
    [`BorderRadius`](https://flet.dev/docs/reference/types/borderradius) class.

    Defaults to `border_radius.all(0)` - rectangular shape.
    """

    semantics_label: Optional[str] = None
    """
    The [`Semantics.label`](https://flet.dev/docs/controls/semantics#label) for this
    progress indicator.
    """

    semantics_value: OptionalNumber = None
    """
    The [`Semantics.value`](https://flet.dev/docs/controls/semantics#value) for this
    progress indicator.
    """

    stop_indicator_color: OptionalColorValue = None
    """
    TBD
    """

    stop_indicator_radius: OptionalNumber = None
    """
    TBD
    """

    track_gap: OptionalNumber = None
    """
    TBD
    """

    year_2023: Optional[bool] = None
    """
    TBD
    """

    def before_update(self):
        super().before_update()
        assert self.value is None or self.value >= 0, "value cannot be negative"
        assert (
            self.bar_height is None or self.bar_height >= 0
        ), "bar_height cannot be negative"
        assert (
            self.semantics_value is None or self.semantics_value >= 0
        ), "semantics_value cannot be negative"
