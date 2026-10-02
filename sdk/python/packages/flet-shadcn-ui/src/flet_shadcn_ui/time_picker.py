import datetime
from typing import Optional

import flet as ft

__all__ = ["TimePicker"]


@ft.control("ShadTimePicker")
class TimePicker(ft.LayoutControl):
    """
    A Shadcn time picker with hour and minute fields.

    Example:
    ```python
    shad.TimePicker(on_change=lambda e: print(e.control.value))
    ```
    """

    value: Optional[datetime.time] = None
    """
    The selected time. Only hours and minutes are used.

    If `None`, the fields are empty.
    """

    period: bool = False
    """
    Whether to use a 12-hour clock with an AM/PM selector.

    :attr:`value` is always in 24-hour time.
    """

    hour_label: Optional[ft.StrOrControl] = None
    """
    The label above the hour field.

    If `None`, "Hours" is shown.
    """

    minute_label: Optional[ft.StrOrControl] = None
    """
    The label above the minute field.

    If `None`, "Minutes" is shown.
    """

    on_change: Optional[ft.ControlEventHandler["TimePicker"]] = None
    """
    Called when the user changes the time.
    """
