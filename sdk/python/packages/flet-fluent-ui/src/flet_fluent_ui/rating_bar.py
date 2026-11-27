from typing import Optional

import flet as ft

__all__ = ["RatingBar"]


@ft.control("FluentRatingBar")
class RatingBar(ft.LayoutControl):
    """
    A Fluent rating bar: a row of stars to show or pick a rating.

    Example:
    ```python
    fluent.RatingBar(value=3)
    fluent.RatingBar(value=4.5, read_only=True)
    ```
    """

    value: ft.Number = 0
    """
    The rating, from `0` to :attr:`max`. Fractional ratings fill stars
    partially.
    """

    max: int = 5
    """
    The number of stars.
    """

    icon_size: ft.Number = 20
    """
    The size of each star.
    """

    spacing: ft.Number = 8
    """
    The space between stars.
    """

    color: Optional[ft.ColorValue] = None
    """
    The color of rated stars.

    If `None`, the accent color of the theme is used.
    """

    unrated_color: Optional[ft.ColorValue] = None
    """
    The color of unrated stars.
    """

    read_only: bool = False
    """
    Whether the rating is only shown and can't be changed.
    """

    autofocus: bool = False
    """
    Whether this rating bar should be focused on initial display.
    """

    on_change: Optional[ft.ControlEventHandler["RatingBar"]] = None
    """
    Called when the user changes the rating.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the new rating.
    """
