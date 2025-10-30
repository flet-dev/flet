from typing import Optional

from flet.controls.base_control import control
from flet.controls.border_radius import BorderRadiusValue
from flet.controls.control import Control
from flet.controls.layout_control import LayoutControl
from flet.controls.padding import PaddingValue
from flet.controls.types import (
    ClipBehavior,
    ColorValue,
    NotchShape,
    Number,
)

__all__ = ["BottomAppBar"]


@control("BottomAppBar")
class BottomAppBar(LayoutControl):
    """
    A material design bottom app bar.

    ```python
    ft.BottomAppBar(
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.IconButton(ft.Icons.MENU),
                ft.IconButton(ft.Icons.SEARCH),
                ft.IconButton(ft.Icons.SETTINGS),
            ],
        ),
    )
    ```
    """

    content: Optional[Control] = None
    """
    The content of this bottom app bar.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The fill color to use for this app bar.

    If `None`, [`BottomAppBarTheme.bgcolor`][flet.] is used;
    if that is also `None`, then defaults to [`ColorScheme.surface`][flet.].
    """

    shadow_color: Optional[ColorValue] = None
    """
    The color of the shadow below this app bar.

    If `None`, [`BottomAppBarTheme.shadow_color`][flet.] is used;
    if that is also `None`, then defaults to [`Colors.TRANSPARENT`][flet.].
    """

    padding: Optional[PaddingValue] = None
    """
    Empty space to inscribe inside a container decoration (background, border).

    If `None`, [`BottomAppBarTheme.padding`][flet.] is used;
    if that is also `None`, then defaults to
    `Padding.symmetric(vertical=12.0, horizontal=16.0)`.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    Defines how the [`content`][(c).] of this app bar should be clipped.

    If `None`, defaults to:
    - [`ClipBehavior.ANTI_ALIAS`][flet.] if [`border_radius`][(c).]
        is set and not equal to [`BorderRadius.all(0)`][flet.BorderRadius.all];
    - Else [`ClipBehavior.NONE`][flet.].
    """

    shape: Optional[NotchShape] = None
    """
    The notch that is made for the floating action button.

    If `None`, [`BottomAppBarTheme.shape`][flet.] is used;
    if that is also `None`, then the shape will be rectangular with no notch.
    """

    notch_margin: Number = 4.0
    """
    The margin between the [`FloatingActionButton`][flet.] and this
    app bar's notch.

    Note:
        Has effect only if [`shape`][(c).] is not `None`.
    """

    elevation: Optional[Number] = None
    """
    The z-coordinate at which to place this bottom app bar relative to its
    parent. It controls the size of the shadow below this app bar.

    If `None`, [`BottomAppBarTheme.elevation`][flet.] is used;
    if that is also `None`, then defaults to `3`.

    Raises:
        ValueError: If it is less than `0`.
    """

    border_radius: Optional[BorderRadiusValue] = None
    """
    The border radius to apply when clipping and painting this app bar.
    """

    def before_update(self):
        super().before_update()
        if self.elevation is not None and self.elevation < 0:
            raise ValueError(
                f"elevation must be greater than or equal to 0, got {self.elevation}"
            )
