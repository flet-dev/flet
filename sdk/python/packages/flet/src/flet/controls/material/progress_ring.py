from typing import Optional

from flet.controls.base_control import control
from flet.controls.box import BoxConstraints
from flet.controls.layout_control import LayoutControl
from flet.controls.padding import PaddingValue
from flet.controls.types import ColorValue, Number, StrokeCap

__all__ = ["ProgressRing"]


@control("ProgressRing")
class ProgressRing(LayoutControl):
    """
    A material design circular progress indicator, which spins to indicate that the
    application is busy.

    A control that shows progress along a circle.

    ```python
    ft.ProgressRing(value=0.4, padding=ft.Padding.all(10))
    ```

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

    stroke_width: Optional[Number] = None
    """
    The width of the line used to draw the circle.
    """

    color: Optional[ColorValue] = None
    """
    The progress indicator's color.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Color of the circular track being filled
    by the circular indicator.
    """

    stroke_align: Optional[Number] = None
    """
    The relative position of the stroke.

    Value typically ranges be `-1.0` (inside stroke) and `1.0` (outside stroke).

    A value of 0 (center stroke) will center the border on the edge of the control.

    If [`ProgressRing.year_2023`][flet.] is `True`, then the
    default value is `0`. Otherwise, the default value is `-1`.
    """

    stroke_cap: Optional[StrokeCap] = None
    """
    The progress indicator's line ending.
    """

    semantics_label: Optional[str] = None
    """
    Used to identify the purpose of this progress bar for screen reading software.
    """

    semantics_value: Optional[Number] = None
    """
    Used for determinate progress indicators to indicate how much progress has been
    made.
    """

    track_gap: Optional[Number] = None
    """
    The gap between the active indicator and the background track.

    If [`year_2023`][(c).] is `True` or `Theme.use_material3` is
    `False`, then no track gap will be drawn.

    Set `track_gap` to `0` to hide this track gap.

    If `None`,
    [`ProgressIndicatorTheme.track_gap`][flet.] is used.

    If that's is also `None`, defaults to `4.0`.
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    Defines the minimum and maximum size of the progress indicator.

    If `None`,
    [`ProgressIndicatorTheme.size_constraints`][flet.]
    is used.

    If that's is also `None`, defaults to a minimum width and height of `36`.
    """

    padding: Optional[PaddingValue] = None
    """
    The padding around the indicator track.

    If `None`,
    [`ProgressIndicatorTheme.circular_track_padding`][flet.]
    is used.

    If that's is also `None` and [`year_2023`][(c).] is `False`,
    defaults to `Padding.all(4.0)`.

    Otherwise, defaults to `Padding.all(0.0)`.
    """

    year_2023: Optional[bool] = None
    """
    If this is set to `False`, the `ProgressRing` will use the latest Material Design 3
    appearance, which was introduced in December 2023.

    When `True`, the `ProgressRing` will use the 2023 Material Design 3 appearance.

    If not set, then the
    [`ProgressIndicatorTheme.year_2023`][flet.] will be
    used, which is `False` by default.

    If [`Theme.use_material3`][flet.] is `False`, then this property
    is ignored.
    """
