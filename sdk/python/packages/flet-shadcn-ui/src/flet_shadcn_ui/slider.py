from typing import Annotated, Optional

import flet as ft
from flet.utils.validation import V

__all__ = ["Slider"]


@ft.control("ShadSlider")
class Slider(ft.LayoutControl):
    """
    A Shadcn slider for picking a number from a range.

    The slider needs a bounded width: inside a :class:`~flet.Row`, set
    :attr:`~flet.LayoutControl.width` or :attr:`~flet.Control.expand`.

    Example:
    ```python
    shad.Slider(value=0.33, width=300)
    shad.Slider(value=50, min=0, max=100, divisions=10)
    ```
    """

    value: Annotated[
        ft.Number,
        V.ge_field("min"),
        V.le_field("max"),
    ] = 0.0
    """
    The current value, between :attr:`min` and :attr:`max`.

    Raises:
        ValueError: If it is not greater than or equal to :attr:`min`.
        ValueError: If it is not less than or equal to :attr:`max`.
    """

    min: Annotated[
        ft.Number,
        V.lt_field("max"),
    ] = 0.0
    """
    The smallest value.

    Raises:
        ValueError: If it is not strictly less than :attr:`max`.
    """

    max: Annotated[
        ft.Number,
        V.gt_field("min"),
    ] = 1.0
    """
    The largest value.

    Raises:
        ValueError: If it is not strictly greater than :attr:`min`.
    """

    divisions: Annotated[
        Optional[int],
        V.gt(0),
    ] = None
    """
    The number of equal steps between :attr:`min` and :attr:`max`.

    If `None`, any value in the range can be picked.

    Raises:
        ValueError: If it is not strictly greater than `0`.
    """

    thumb_color: Optional[ft.ColorValue] = None
    """
    The fill color of the thumb.

    If `None`, the background color of the theme is used.
    """

    active_track_color: Optional[ft.ColorValue] = None
    """
    The color of the track between :attr:`min` and the thumb.

    If `None`, the primary color of the theme is used.
    """

    inactive_track_color: Optional[ft.ColorValue] = None
    """
    The color of the track between the thumb and :attr:`max`.

    If `None`, the secondary color of the theme is used.
    """

    on_change: Optional[ft.ControlEventHandler["Slider"]] = None
    """
    Called continuously while the user drags the thumb.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the new value.
    """

    on_change_start: Optional[ft.ControlEventHandler["Slider"]] = None
    """
    Called when the user starts dragging the thumb.
    """

    on_change_end: Optional[ft.ControlEventHandler["Slider"]] = None
    """
    Called when the user releases the thumb.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the final value.
    """
