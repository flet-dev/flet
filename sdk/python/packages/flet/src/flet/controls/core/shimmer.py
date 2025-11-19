from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.duration import DurationValue
from flet.controls.gradients import Gradient
from flet.controls.layout_control import LayoutControl
from flet.controls.types import (
    ColorValue,
)

__all__ = ["Shimmer", "ShimmerDirection"]


class ShimmerDirection(Enum):
    """
    Direction of the shimmering gradient animation.
    """

    LTR = "ltr"
    """
    The shimmer moves from left to right.
    """

    RTL = "rtl"
    """
    The shimmer moves from right to left.
    """

    TTB = "ttb"
    """
    The shimmer moves from top to bottom.
    """

    BTT = "btt"
    """
    The shimmer moves from bottom to top.
    """


@control("Shimmer")
class Shimmer(LayoutControl):
    """
    Applies an animated shimmering effect to its [`content`][(c).].

    Use it to create lightweight loading placeholders or to add motion to
    otherwise static layouts.

    ```python
    ft.Shimmer(
        base_color=ft.Colors.with_opacity(0.3, ft.Colors.GREY_400),
        highlight_color=ft.Colors.WHITE,
        content=ft.Column(
            controls=[
                ft.Container(height=80, bgcolor=ft.Colors.GREY_300),
                ft.Container(height=80, bgcolor=ft.Colors.GREY_300),
                ft.Container(height=80, bgcolor=ft.Colors.GREY_300),
            ],
        ),
    )
    ```
    """

    content: Control
    """
    The control to render with the shimmer effect.
    """

    gradient: Optional[Gradient] = None
    """
    Custom gradient that defines the shimmer colors.
    """

    base_color: Optional[ColorValue] = None
    """
    Base color used when no [`gradient`][(c).] is provided.
    """

    highlight_color: Optional[ColorValue] = None
    """
    Highlight color used when no [`gradient`][(c).] is provided.
    """

    period: DurationValue = 1500
    """
    Duration of a shimmer cycle in milliseconds.
    """

    direction: ShimmerDirection = ShimmerDirection.LTR
    """
    Direction of the shimmering animation.
    """

    loop: int = 0
    """
    Number of times the animation should repeat. `0` means infinite.
    """

    def before_update(self):
        super().before_update()
        if self.content is None:
            raise ValueError("content must be provided.")
        if self.gradient is None and (
            self.base_color is None or self.highlight_color is None
        ):
            raise ValueError("Either gradient or both base_color and highlight_color must be provided.")
        if self.loop is not None and self.loop < 0:
            raise ValueError("loop must be a non-negative integer (greater than or equal to 0).")
