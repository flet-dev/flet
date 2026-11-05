from typing import Annotated, Optional

import flet as ft
from flet.utils.validation import V

__all__ = ["DatePicker", "DateRangePicker"]


@ft.control("ShadDatePicker")
class DatePicker(ft.LayoutControl):
    """
    A Shadcn date picker: a button that opens a calendar in a popover.

    When the user picks a day, :attr:`value` is set to a `datetime` at
    midnight UTC of that day, so `value.date()` gives the picked date in any
    time zone. A `date` can be assigned as well.

    Example:
    ```python
    shad.DatePicker(on_change=lambda e: print(e.control.value))
    ```
    """

    value: Optional[ft.DateTimeValue] = None
    """
    The selected day.

    If `None`, :attr:`placeholder` is shown.
    """

    placeholder: Optional[ft.StrOrControl] = None
    """
    The content shown while no day is selected.

    If `None`, "Select date" is shown.
    """

    min_date: Annotated[
        Optional[ft.DateTimeValue],
        V.le_field("max_date"),
    ] = None
    """
    The earliest day that can be picked.

    Raises:
        ValueError: If it is not less than or equal to :attr:`max_date`,
            when :attr:`max_date` is set.
    """

    max_date: Annotated[
        Optional[ft.DateTimeValue],
        V.ge_field("min_date"),
    ] = None
    """
    The latest day that can be picked.

    Raises:
        ValueError: If it is not greater than or equal to :attr:`min_date`,
            when :attr:`min_date` is set.
    """

    close_on_select: bool = True
    """
    Whether the calendar closes as soon as a day is picked.
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
    An error message shown in red below this picker. The button border turns red too.

    Set it after validating the value, and set it back to `None` (or an empty
    string) to clear the error.
    """

    on_change: Optional[ft.ControlEventHandler["DatePicker"]] = None
    """
    Called when the user picks or clears a day.
    """


@ft.control("ShadDateRangePicker")
class DateRangePicker(ft.LayoutControl):
    """
    A Shadcn date range picker: a button that opens a two-month calendar in a
    popover for picking a start and an end day.

    The first click picks the start day and the second click the end day.
    Clicking again after a range is complete starts a new range on the
    clicked day. Before the end is picked, clicking a day earlier than the
    start moves the start.

    Picked days are set to a `datetime` at midnight UTC of that day, so
    `.date()` gives the picked date in any time zone. A `date` can be assigned
    as well.

    Example:
    ```python
    shad.DateRangePicker(
        on_change=lambda e: print(e.control.start_value, e.control.end_value)
    )
    ```
    """

    start_value: Optional[ft.DateTimeValue] = None
    """
    The first day of the selected range.
    """

    end_value: Optional[ft.DateTimeValue] = None
    """
    The last day of the selected range.

    `None` while the user has picked only the start day.
    """

    placeholder: Optional[ft.StrOrControl] = None
    """
    The content shown while no range is selected.

    If `None`, "Select date" is shown.
    """

    min_date: Annotated[
        Optional[ft.DateTimeValue],
        V.le_field("max_date"),
    ] = None
    """
    The earliest day that can be picked.

    Raises:
        ValueError: If it is not less than or equal to :attr:`max_date`,
            when :attr:`max_date` is set.
    """

    max_date: Annotated[
        Optional[ft.DateTimeValue],
        V.ge_field("min_date"),
    ] = None
    """
    The latest day that can be picked.

    Raises:
        ValueError: If it is not greater than or equal to :attr:`min_date`,
            when :attr:`min_date` is set.
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
    An error message shown in red below this picker. The button border turns red too.

    Set it after validating the value, and set it back to `None` (or an empty
    string) to clear the error.
    """

    on_change: Optional[ft.ControlEventHandler["DateRangePicker"]] = None
    """
    Called when the user changes the range.
    """
