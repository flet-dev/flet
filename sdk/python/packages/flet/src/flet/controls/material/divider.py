from typing import Annotated, Optional

from flet.controls.base_control import control
from flet.controls.border_radius import BorderRadiusValue
from flet.controls.control import Control
from flet.controls.types import ColorValue, Number
from flet.utils.validation import V

__all__ = ["Divider"]


@control("Divider")
class Divider(Control):
    """
    A thin horizontal line (divider), with padding on either side.

    ```python
    ft.Column(
        width=240,
        spacing=10,
        controls=[
            ft.Text("Section A", weight=ft.FontWeight.W_600),
            ft.Divider(),
            ft.Text("Section B"),
        ],
    )
    ```
    """

    color: Optional[ColorValue] = None
    """
    The color to use when painting the line.

    If `None`, :attr:`flet.DividerTheme.color` is used.
    """

    height: Annotated[
        Optional[Number],
        V.ge(0),
    ] = None
    """
    The divider's height extent. The divider itself is always drawn as a horizontal \
    line that is centered within the height specified by this value.

    If `None`, :attr:`flet.DividerTheme.space` is used.
    If that's is also `None`, defaults to `16.0`.

    Raises:
        ValueError: If :attr:`height` is negative.
    """

    leading_indent: Annotated[
        Optional[Number],
        V.ge(0),
    ] = None
    """
    The amount of empty space to the leading edge of the divider.

    If `None`, :attr:`flet.DividerTheme.leading_indent` is used.
    If that's is also `None`, defaults to `0.0`.

    Raises:
        ValueError: If it is not greater than or equal to `0`.
    """

    thickness: Annotated[
        Optional[Number],
        V.ge(0),
    ] = None
    """
    The thickness of the line drawn within the divider.

    A divider with a thickness of `0.0` is always drawn as a line with a
    height of exactly one device pixel.

    If `None`, :attr:`flet.DividerTheme.thickness` is used.
    If that is also `None`, defaults to `0.0`.

    Raises:
        ValueError: If :attr:`thickness` is negative.
    """

    trailing_indent: Annotated[
        Optional[Number],
        V.ge(0),
    ] = None
    """
    The amount of empty space to the trailing edge of the divider.

    If `None`, :attr:`flet.DividerTheme.trailing_indent` is used.
    If that is also `None`, defaults to `0.0`.

    Raises:
        ValueError: If it is not greater than or equal to `0`.
    """

    radius: Optional[BorderRadiusValue] = None
    """
    The border radius of the divider.
    """
