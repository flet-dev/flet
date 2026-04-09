from typing import Annotated, Optional

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
from flet.utils.validation import V

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

    If `None`, :attr:`flet.BottomAppBarTheme.bgcolor` is used;
    if that is also `None`, then defaults to :attr:`flet.ColorScheme.surface`.
    """

    shadow_color: Optional[ColorValue] = None
    """
    The color of the shadow below this app bar.

    If `None`, :attr:`flet.BottomAppBarTheme.shadow_color` is used;
    if that is also `None`, then defaults to :attr:`flet.Colors.TRANSPARENT`.
    """

    padding: Optional[PaddingValue] = None
    """
    Empty space to inscribe inside a container decoration (background, border).

    If `None`, :attr:`flet.BottomAppBarTheme.padding` is used;
    if that is also `None`, then defaults to
    `Padding.symmetric(vertical=12.0, horizontal=16.0)`.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    Defines how the :attr:`content` of this app bar should be clipped.

    If `None`, defaults to:
    - :attr:`flet.ClipBehavior.ANTI_ALIAS` if :attr:`border_radius`
        is set and not equal to :meth:`flet.BorderRadius.all`;
    - Else :attr:`flet.ClipBehavior.NONE`.
    """

    shape: Optional[NotchShape] = None
    """
    The notch that is made for the floating action button.

    If `None`, :attr:`flet.BottomAppBarTheme.shape` is used;
    if that is also `None`, then the shape will be rectangular with no notch.
    """

    notch_margin: Number = 4.0
    """
    The margin between the :class:`~flet.FloatingActionButton` and this app bar's notch.

    Note:
        Has effect only if :attr:`shape` is not `None`.
    """

    elevation: Annotated[
        Optional[Number],
        V.ge(0),
    ] = None
    """
    The z-coordinate at which to place this bottom app bar relative to its parent. It \
    controls the size of the shadow below this app bar.

    If `None`, :attr:`flet.BottomAppBarTheme.elevation` is used;
    if that is also `None`, then defaults to `3`.

    Raises:
        ValueError: If it is not greater than or equal to `0`.
    """

    border_radius: Optional[BorderRadiusValue] = None
    """
    The border radius to apply when clipping and painting this app bar.
    """
