from typing import Optional

import flet as ft

__all__ = ["ProgressBar", "ProgressRing"]


@ft.control("FluentProgressBar")
class ProgressBar(ft.LayoutControl):
    """
    A Fluent progress bar.

    Example:
    ```python
    fluent.ProgressBar(value=60)
    fluent.ProgressBar()  # indeterminate
    ```
    """

    value: Optional[ft.Number] = None
    """
    The progress, from `0` to `100`.

    If `None`, the bar is indeterminate: it animates continuously to show
    that work is in progress without saying how much is done.
    """

    stroke_width: ft.Number = 4.5
    """
    The thickness of the bar.
    """

    color: Optional[ft.ColorValue] = None
    """
    The color of the filled part.

    If `None`, the accent color of the theme is used.
    """

    bgcolor: Optional[ft.ColorValue] = None
    """
    The color of the track behind the filled part.
    """


@ft.control("FluentProgressRing")
class ProgressRing(ft.LayoutControl):
    """
    A Fluent progress ring: a circular progress indicator.

    Example:
    ```python
    fluent.ProgressRing(value=60)
    fluent.ProgressRing()  # indeterminate
    ```
    """

    value: Optional[ft.Number] = None
    """
    The progress, from `0` to `100`.

    If `None`, the ring is indeterminate: it spins continuously to show that
    work is in progress without saying how much is done.
    """

    stroke_width: ft.Number = 4.5
    """
    The thickness of the ring.
    """

    color: Optional[ft.ColorValue] = None
    """
    The color of the filled part.

    If `None`, the accent color of the theme is used.
    """

    bgcolor: Optional[ft.ColorValue] = None
    """
    The color of the track behind the filled part.
    """
