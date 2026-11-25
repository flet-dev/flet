from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

import flet as ft
from flet_fluent_ui.types import CalendarDisplayMode, CalendarSelectionMode

__all__ = ["CalendarDatePicker", "CalendarView", "CalendarViewChangeEvent"]


@dataclass
class CalendarViewChangeEvent(ft.Event["CalendarView"]):
    """
    Event fired when the user changes the selection of a
    :class:`~flet_fluent_ui.CalendarView`.
    """

    selected_dates: list[datetime]
    """
    All selected dates, in order. In
    :attr:`~flet_fluent_ui.CalendarSelectionMode.RANGE` mode, these are the
    start and end of the range.

    Like :attr:`~flet_fluent_ui.CalendarView.value`, each is a `datetime` in
    UTC for midnight local time: use `astimezone()` to get the local date.
    """


@ft.control("FluentCalendarView")
class CalendarView(ft.LayoutControl):
    """
    A Fluent calendar that is always shown, for viewing and selecting dates.
    The user can switch between the days of a month, the months of a year and
    the years of a decade.

    Example:
    ```python
    fluent.CalendarView(value=date(2025, 5, 14), width=300)
    ```
    """

    value: Optional[ft.DateTimeValue] = None
    """
    The selected date, or the start of the selected range when
    :attr:`selection_mode` is :attr:`~flet_fluent_ui.CalendarSelectionMode.RANGE`.

    After the user picks a date, it holds a `datetime` in UTC for midnight
    local time: use `value.astimezone()` to get the local date.
    """

    end_value: Optional[ft.DateTimeValue] = None
    """
    The end of the selected range, when :attr:`selection_mode` is
    :attr:`~flet_fluent_ui.CalendarSelectionMode.RANGE`.
    """

    selection_mode: CalendarSelectionMode = CalendarSelectionMode.SINGLE
    """
    How many dates the user can select.

    In :attr:`~flet_fluent_ui.CalendarSelectionMode.MULTIPLE` mode,
    :attr:`value` and :attr:`end_value` hold the first and last selected
    dates, and preselect up to two dates when set.
    """

    first_date: Optional[ft.DateTimeValue] = None
    """
    The earliest date that can be selected. Earlier dates are shown greyed
    out.
    """

    last_date: Optional[ft.DateTimeValue] = None
    """
    The latest date that can be selected. Later dates are shown greyed out.
    """

    blackout_dates: list[ft.DateTimeValue] = field(default_factory=list)
    """
    Dates that can't be selected, such as holidays. They are shown struck
    through.
    """

    first_day_of_week: Optional[int] = None
    """
    The day the weeks start on: `1` for Monday through `7` for Sunday.

    If `None`, it depends on the locale.
    """

    highlight_today: bool = True
    """
    Whether today's date is highlighted.
    """

    selection_color: Optional[ft.ColorValue] = None
    """
    The color of selected dates.

    If `None`, the accent color of the theme is used.
    """

    display_mode: CalendarDisplayMode = CalendarDisplayMode.MONTH
    """
    What the calendar shows at first: the days of a month, the months of a
    year or the years of a decade.
    """

    on_change: Optional[ft.EventHandler[CalendarViewChangeEvent]] = None
    """
    Called when the user changes the selection.

    :attr:`value` and :attr:`end_value` hold the first and last selected
    dates, and the event's
    :attr:`~flet_fluent_ui.CalendarViewChangeEvent.selected_dates` all of
    them.
    """


@ft.control("FluentCalendarDatePicker")
class CalendarDatePicker(ft.LayoutControl):
    """
    A Fluent calendar date picker: a button showing the selected date, which
    opens a calendar to pick another.

    Example:
    ```python
    fluent.CalendarDatePicker(placeholder="Pick a date")
    ```
    """

    value: Optional[ft.DateTimeValue] = None
    """
    The selected date.

    After the user picks a date, it holds a `datetime` in UTC for midnight
    local time: use `value.astimezone()` to get the local date.
    """

    placeholder: Optional[str] = None
    """
    The text shown while no date is selected.

    If `None`, a localized "Pick a date" is shown.
    """

    first_date: Optional[ft.DateTimeValue] = None
    """
    The earliest date that can be selected. Earlier dates are shown greyed
    out.
    """

    last_date: Optional[ft.DateTimeValue] = None
    """
    The latest date that can be selected. Later dates are shown greyed out.
    """

    blackout_dates: list[ft.DateTimeValue] = field(default_factory=list)
    """
    Dates that can't be selected, such as holidays. They are shown struck
    through.
    """

    first_day_of_week: Optional[int] = None
    """
    The day the weeks start on: `1` for Monday through `7` for Sunday.

    If `None`, it depends on the locale.
    """

    highlight_today: bool = True
    """
    Whether today's date is highlighted.
    """

    selection_color: Optional[ft.ColorValue] = None
    """
    The color of selected dates.

    If `None`, the accent color of the theme is used.
    """

    close_on_selection: bool = True
    """
    Whether the calendar closes when the user picks a date.
    """

    on_change: Optional[ft.ControlEventHandler["CalendarDatePicker"]] = None
    """
    Called when the user picks a date.

    :attr:`value` holds the new date.
    """
