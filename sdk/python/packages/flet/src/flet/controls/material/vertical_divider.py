from typing import Annotated, Optional

from flet.controls._validation import V
from flet.controls.base_control import control
from flet.controls.border_radius import BorderRadiusValue
from flet.controls.control import Control
from flet.controls.types import ColorValue, Number

__all__ = ["VerticalDivider"]


@control("VerticalDivider")
class VerticalDivider(Control):
    """
    A thin vertical line, with padding on either side.

    In the material design language, this represents a divider.

    Example:
    ```python
    ft.Row(
        width=120,
        height=60,
        expand=True,
        spacing=0,
        controls=[
            ft.Container(
                bgcolor=ft.Colors.BLUE_GREY_200,
                alignment=ft.Alignment.CENTER,
                expand=True,
            ),
            ft.VerticalDivider(),
            ft.Container(
                bgcolor=ft.Colors.GREY_500,
                alignment=ft.Alignment.CENTER,
                expand=True,
            ),
        ],
    )
    ```

    """

    width: Annotated[
        Optional[Number],
        V.ge(0),
    ] = None
    """
    The divider's width. The divider itself is always drawn as a vertical line that is \
    centered within the width specified by this value.

    If `None`, [`DividerTheme.space`][flet.] is used.
    If that's is also `None`, defaults to `16.0`.

    Raises:
        ValueError: If it is not greater than or equal to `0`.
    """

    thickness: Annotated[
        Optional[Number],
        V.ge(0),
    ] = None
    """
    The thickness of this divider.

    Note:
        A divider with a thickness of `0.0` is always drawn as a line with a width of
        exactly one device pixel.

    If `None`, [`DividerTheme.thickness`][flet.] is used.
    If that's is also `None`, defaults to `0.0`.

    Raises:
        ValueError: If it is not greater than or equal to `0`.
    """

    color: Optional[ColorValue] = None
    """
    The color to use when painting the line.

    If `None`, [`DividerTheme.color`][flet.] is used.
    """

    leading_indent: Annotated[
        Optional[Number],
        V.ge(0),
    ] = None
    """
    The amount of empty space to the leading edge of the divider.

    If `None`, [`DividerTheme.leading_indent`][flet.] is used.
    If that's is also `None`, defaults to `0.0`.

    Raises:
        ValueError: If it is not greater than or equal to `0`.
    """

    trailing_indent: Annotated[
        Optional[Number],
        V.ge(0),
    ] = None
    """
    The amount of empty space to the trailing edge of the divider.

    If `None`, [`DividerTheme.trailing_indent`][flet.] is used.
    If that's is also `None`, defaults to `0.0`.

    Raises:
        ValueError: If it is not greater than or equal to `0`.
    """

    radius: Optional[BorderRadiusValue] = None
    """
    The border radius of the divider.
    """
