from typing import Optional

import flet as ft

__all__ = ["Slider"]


@ft.control("FluentSlider")
class Slider(ft.LayoutControl):
    """
    A Fluent slider, for choosing a value from a range.

    Example:
    ```python
    fluent.Slider(value=40, on_change=lambda e: print(e.data))
    ```
    """

    value: ft.Number = 0
    """
    The current value.

    It must be between :attr:`min` and :attr:`max`.
    """

    min: ft.Number = 0
    """
    The minimum value.
    """

    max: ft.Number = 100
    """
    The maximum value.
    """

    divisions: Optional[int] = None
    """
    The number of discrete steps between :attr:`min` and :attr:`max`.

    If `None`, the slider is continuous.
    """

    label: Optional[str] = None
    """
    The text shown in a tooltip above the thumb while it is dragged.

    If `None`, no tooltip is shown.
    """

    vertical: bool = False
    """
    Whether the slider is vertical instead of horizontal.
    """

    autofocus: bool = False
    """
    Whether this slider should be focused on initial display.
    """

    on_change: Optional[ft.ControlEventHandler["Slider"]] = None
    """
    Called while the value changes.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the new value.
    """

    on_change_start: Optional[ft.ControlEventHandler["Slider"]] = None
    """
    Called when the user starts changing the value.
    """

    on_change_end: Optional[ft.ControlEventHandler["Slider"]] = None
    """
    Called when the user stops changing the value.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the final value.
    """
