from typing import Optional

from flet.controls.base_control import control
from flet.controls.layout_control import LayoutControl
from flet.controls.types import ColorValue, Number

__all__ = ["CupertinoActivityIndicator"]


@control("CupertinoActivityIndicator")
class CupertinoActivityIndicator(LayoutControl):
    """
    An iOS-style activity indicator that spins clockwise.

    ```python
    ft.CupertinoActivityIndicator(
        radius=30,
        color=ft.CupertinoColors.DARK_BACKGROUND_GRAY,
    )
    ```
    """

    radius: Number = 10
    """
    The radius of this indicator.

    Raises:
        ValueError: If it is not strictly greater than `0`.
    """

    color: Optional[ColorValue] = None
    """
    Defines the color of this indicator.
    """

    animating: bool = True
    """
    Whether this indicator is running its animation.

    Note:
        Has no effect if [`progress`][(c).] is not `None`.
    """

    progress: Optional[Number] = None
    """
    Determines the percentage of spinner ticks that will be shown.

    Typical usage would display all ticks, however, this allows for more fine-grained
    control such as during pull-to-refresh when the drag-down action shows one tick at
    a time as the user continues to drag down.

    Note:
        If not `None`, then [`animating`][(c).] will be ignored.

    Raises:
        ValueError: If it is not between `0.0` and `1.0`, inclusive.
    """

    def before_update(self):
        super().before_update()
        if self.radius <= 0.0:
            raise ValueError(
                f"radius must be strictly greater than 0.0, got {self.radius}"
            )
        if self.progress is not None and not 0.0 <= self.progress <= 1.0:
            raise ValueError(
                f"progress must be between 0.0 and 1.0 inclusive, got {self.progress}"
            )
