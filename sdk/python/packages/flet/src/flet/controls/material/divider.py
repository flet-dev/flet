from typing import Annotated, Optional

from flet.controls._validation import V
from flet.controls.base_control import control
from flet.controls.border_radius import BorderRadiusValue
from flet.controls.control import Control
from flet.controls.types import ColorValue, Number

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

    If `None`, [`DividerTheme.color`][flet.] is used.
    """

    height: Annotated[
        Optional[Number],
        V.ge(0),
    ] = None
    """
    The divider's height extent. The divider itself is always drawn as a horizontal \
    line that is centered within the height specified by this value.

    If `None`, [`DividerTheme.space`][flet.] is used.
    If that's is also `None`, defaults to `16.0`.

    Raises:
        ValueError: If [`height`][(c).] is negative.
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
        ValueError: If [`leading_indent`][(c).] is negative.
    """

    thickness: Annotated[
        Optional[Number],
        V.ge(0),
    ] = None
    """
    The thickness of the line drawn within the divider.

    A divider with a thickness of `0.0` is always drawn as a line with a
    height of exactly one device pixel.

    If `None`, [`DividerTheme.thickness`][flet.] is used.
    If that is also `None`, defaults to `0.0`.

    Raises:
        ValueError: If [`thickness`][(c).] is negative.
    """

    trailing_indent: Annotated[
        Optional[Number],
        V.ge(0),
    ] = None
    """
    The amount of empty space to the trailing edge of the divider.

    If `None`, [`DividerTheme.trailing_indent`][flet.] is used.
    If that is also `None`, defaults to `0.0`.

    Raises:
        ValueError: If [`trailing_indent`][(c).] is negative.
    """

    radius: Optional[BorderRadiusValue] = None
    """
    The border radius of the divider.
    """
