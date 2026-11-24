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

    label: Optional[ft.StrOrControl] = None
    """
    The label shown above this picker.

    It turns red while :attr:`error_text` is set.
    """

    description: Optional[ft.StrOrControl] = None
    """
    Helper text shown below this picker.
    """

    error_text: Optional[str] = None
    """
    An error message shown in red below this picker. The field borders turn red too.

    Set it after validating the value, and set it back to `None` (or an empty
    string) to clear the error.
    """

    on_change: Optional[ft.ControlEventHandler["TimePicker"]] = None
    """
    Called when the user changes the time.
    """
