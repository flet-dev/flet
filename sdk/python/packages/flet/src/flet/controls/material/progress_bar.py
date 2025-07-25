from typing import Optional

from flet.controls.base_control import control
from flet.controls.border_radius import BorderRadiusValue
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.types import ColorValue, Number

__all__ = ["ProgressBar"]


@control("ProgressBar")
class ProgressBar(ConstrainedControl):
    """
    A material design linear progress indicator, also known as a progress bar.

    A control that shows progress along a line.
    """

    value: Optional[Number] = None
    """
    The value of this progress indicator.

    A value of `0.0` means no progress and `1.0` means that progress is complete. The
    value will be clamped to be in the range `0.0` - `1.0`.

    Defaults to `None`, meaning that this progress indicator is indeterminate -
    displays a predetermined animation that does not indicate how much actual progress
    is being made.
    """

    bar_height: Optional[Number] = None
    """
    The minimum height of the line used to draw the linear indicator.
    """

    color: Optional[ColorValue] = None
    """
    The progress indicator's color.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Color of the track being filled by the linear indicator.
    """

    border_radius: Optional[BorderRadiusValue] = None
    """
    The border radius of both the indicator and the track.

    Defaults to `BorderRadius.all(0)` - rectangular shape.
    """

    semantics_label: Optional[str] = None
    """
    The semantics label for this progress indicator.
    """

    semantics_value: Optional[Number] = None
    """
    The semantics label for this progress indicator.
    """

    stop_indicator_color: Optional[ColorValue] = None
    """
    The color of the stop indicator.

    If [`ProgressBar.year2023`][flet.ProgressBar.year_2023] is `True` or 
    [`Theme.use_material3`][flet.Theme.use_material3] is `False`, then no stop 
    indicator will be drawn.

    If not set, then the 
    [`ProgressIndicatorTheme.stop_indicator_color`][flet.ProgressIndicatorTheme.stop_indicator_color] 
    will be used. If that is not set, then the 
    [`ColorScheme.primary`][flet.ColorScheme.primary] will be used.   
    """

    stop_indicator_radius: Optional[Number] = None
    """
    The radius of the stop indicator.

    If [`ProgressBar.year2023`][flet.ProgressBar.year_2023] is `True` or 
    [`Theme.use_material3`][flet.Theme.use_material3] is `False`, then no stop 
    indicator will be drawn.

    Set `stop_indicator_radius` to `0` to hide the stop indicator.

    If not set, then the 
    [`ProgressIndicatorTheme.stop_indicator_radius`][flet.ProgressIndicatorTheme.stop_indicator_radius] 
    will be used. If that is not set, then defaults to `2`.
    """

    track_gap: Optional[Number] = None
    """
    The gap between the indicator and the track. 
    
    If [`ProgressBar.year2023`][flet.ProgressBar.year_2023] is `True` or 
    [`Theme.use_material3`][flet.Theme.use_material3] is `False`, then no track gap 
    will be drawn.

    Set `track_gap` to `0` to hide the track gap.

    If not set, then the 
    [`ProgressIndicatorTheme.track_gap`][flet.ProgressIndicatorTheme.track_gap] will be 
    used. If that is not set, then defaults to `4`.
    """

    year_2023: Optional[bool] = None
    """
    If this is set to `False`, the ProgressBar will use the latest Material Design 3 
    appearance, which was introduced in December 2023.

    When `True`, the ProgressBar will use the 2023 Material Design 3 appearance.

    If not set, then the 
    [`ProgressIndicatorTheme.year_2023`][flet.ProgressIndicatorTheme.year_2023] will be 
    used, which is `False` by default.

    If [`Theme.use_material3`][flet.Theme.use_material3] is `False`, then this property 
    is ignored.
    """

    def before_update(self):
        super().before_update()
        assert self.value is None or self.value >= 0, f"value must be greater than or equal to 0, got {self.value}"
        assert self.bar_height is None or self.bar_height >= 0, (
            f"bar_height must be greater than or equal to 0, got {self.bar_height}"
        )
        assert self.semantics_value is None or self.semantics_value >= 0, (
            f"semantics_value must be greater than or equal to 0, got {self.semantics_value}"
        )
