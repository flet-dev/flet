from datetime import time
from typing import Optional

import flet as ft

__all__ = ["DatePicker", "TimePicker"]


@ft.control("FluentDatePicker")
class DatePicker(ft.LayoutControl):
    """
    A Fluent date picker: a field showing the month, day and year, which opens
    scrolling lists to pick each of them.

    Example:
    ```python
    fluent.DatePicker(header="Birthday", value=date(1990, 4, 12))
    ```
    """

    value: Optional[ft.DateTimeValue] = None
    """
    The selected date.

    If `None`, the field shows placeholders and the lists open at today's
    date.

    After the user picks a date, it holds a `datetime` in UTC for midnight
    local time: use `value.astimezone()` to get the local date.
    """

    header: Optional[str] = None
    """
    A label shown above the field.
    """

    first_date: Optional[ft.DateTimeValue] = None
    """
    The earliest date that can be picked.

    If `None`, it is 100 years before today.
    """

    last_date: Optional[ft.DateTimeValue] = None
    """
    The latest date that can be picked.

    If `None`, it is 25 years after today.
    """

    show_day: bool = True
    """
    Whether the field shows the day.
    """

    show_month: bool = True
    """
    Whether the field shows the month.
    """

    show_year: bool = True
    """
    Whether the field shows the year.
    """

    autofocus: bool = False
    """
    Whether this picker should be focused on initial display.
    """

    on_change: Optional[ft.ControlEventHandler["DatePicker"]] = None
    """
    Called when the user picks a date and confirms it.

    :attr:`value` holds the new date.
    """


@ft.control("FluentTimePicker")
class TimePicker(ft.LayoutControl):
    """
    A Fluent time picker: a field showing the hour and minute, which opens
    scrolling lists to pick each of them.

    Example:
    ```python
    fluent.TimePicker(header="Alarm", value=time(7, 30))
    ```
    """

    value: Optional[time] = None
    """
    The selected time.

    If `None`, the field shows placeholders and the lists open at the current
    time.
    """

    header: Optional[str] = None
    """
    A label shown above the field.
    """

    use_24_hour: bool = False
    """
    Whether hours go from `00` to `23`, instead of from `1` to `12` with an
    AM/PM field.
    """

    minute_increment: int = 1
    """
    The step between the minutes offered: for example, `15` offers `00`, `15`,
    `30` and `45`.
    """

    autofocus: bool = False
    """
    Whether this picker should be focused on initial display.
    """

    on_change: Optional[ft.ControlEventHandler["TimePicker"]] = None
    """
    Called when the user picks a time and confirms it.

    :attr:`value` holds the new time.
    """
