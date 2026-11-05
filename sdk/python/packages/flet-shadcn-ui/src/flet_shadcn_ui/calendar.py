from typing import Annotated, Optional

import flet as ft
from flet.utils.validation import V

__all__ = ["Calendar"]


@ft.control("ShadCalendar")
class Calendar(ft.LayoutControl):
    """
    A Shadcn calendar for picking one day.

    When the user picks a day, :attr:`value` is set to a `datetime` at
    midnight UTC of that day, so `value.date()` gives the picked date in any
    time zone. A `date` can be assigned as well.

    Example:
    ```python
    shad.Calendar(value=date.today(), on_change=lambda e: print(e.control.value))
    ```
    """

    value: Optional[ft.DateTimeValue] = None
    """
    The selected day.

    If `None`, no day is selected.
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

    number_of_months: Annotated[
        int,
        V.gt(0),
    ] = 1
    """
    How many months to show side by side.

    Raises:
        ValueError: If it is not strictly greater than `0`.
    """

    show_outside_days: bool = True
    """
    Whether to show the days of the previous and next months that fill the
    first and last weeks.
    """

    show_week_numbers: bool = False
    """
    Whether to show the week number at the start of each week.
    """

    on_change: Optional[ft.ControlEventHandler["Calendar"]] = None
    """
    Called when the user picks or clears a day.
    """
