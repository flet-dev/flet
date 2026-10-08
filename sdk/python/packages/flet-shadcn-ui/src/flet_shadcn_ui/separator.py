from typing import Optional

import flet as ft

__all__ = ["Separator"]


@ft.control("ShadSeparator")
class Separator(ft.LayoutControl):
    """
    A Shadcn separator: a thin line that divides content.

    A horizontal separator fills the width of its parent. A vertical one, for
    example inside a :class:`~flet.Row`, fills the height of its parent, so give
    the row a fixed height or set its `intrinsic_height` to `True`.

    Example:
    ```python
    ft.Column([ft.Text("Account"), shad.Separator(), ft.Text("Billing")])
    ```
    """

    vertical: bool = False
    """
    Whether this separator is a vertical line instead of a horizontal one.
    """

    thickness: Optional[ft.Number] = None
    """
    The thickness of the line.

    If `None`, defaults to `1`.
    """

    color: Optional[ft.ColorValue] = None
    """
    The color of the line.

    If `None`, the border color of the theme is used.
    """

    margin: Optional[ft.MarginValue] = None
    """
    The space around the line.

    If `None`, defaults to `16` above and below a horizontal separator and
    `16` on each side of a vertical one.
    """
