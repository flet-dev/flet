from dataclasses import field
from datetime import date, datetime
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import ControlEventHandler
from flet.controls.duration import DateTimeValue
from flet.controls.layout_control import LayoutControl
from flet.controls.types import ColorValue, Number

__all__ = [
    "CupertinoDatePicker",
    "CupertinoDatePickerDateOrder",
    "CupertinoDatePickerMode",
]


class CupertinoDatePickerMode(Enum):
    TIME = "time"
    DATE = "date"
    DATE_AND_TIME = "dateAndTime"
    MONTH_YEAR = "monthYear"


class CupertinoDatePickerDateOrder(Enum):
    DAY_MONTH_YEAR = "dmy"
    MONTH_DAY_YEAR = "mdy"
    YEAR_MONTH_DAY = "ymd"
    YEAR_DAY_MONTH = "ydm"


@control("CupertinoDatePicker")
class CupertinoDatePicker(LayoutControl):
    """
    An iOS-styled date picker.
    """

    value: DateTimeValue = field(default_factory=lambda: datetime.now())
    """
    The initial date and/or time of the picker. It must conform to the intervals
    set in `first_date`, `last_date`, `min_year`, and `max_year` else an error
    will be `ValueError` will be raised.

    Defaults to the present date and time.
    """

    first_date: Optional[DateTimeValue] = None
    """
    The earliest allowable date that the user can select.

    Defaults to `None` - no limit.

    When not `None` (no limit), one can still scroll the picker to dates earlier than
    `first_date`, with the exception that the
    [`on_change`][flet.CupertinoDatePicker.on_change] will not be called.
    Once let go, the picker will scroll back to `first_date`.

    In `CupertinoDatePickerMode.TIME` mode, a time becomes unselectable if the
    datetime produced by combining that particular time and the date part of
    initialDateTime is earlier than `last_date`. So typically `first_date` needs
    to be set to a datetime that is on the same date as initialDateTime.
    """

    last_date: Optional[DateTimeValue] = None
    """
    The latest allowable date that the user can select.

    When not `None`, one can still scroll the picker to dates later than
    `last_date`, with the exception that the `on_change` will not be called.
    Once let go, the picker will scroll back to `last_date`.

    In [`CupertinoDatePickerMode.TIME`][flet.CupertinoDatePickerMode.TIME] mode,
    a time becomes unselectable if the
    datetime produced by combining that particular time and the date part of
    initialDateTime is later than `last_date`. So typically `last_date` needs to
    be set to a datetime that is on the same date as initialDateTime.

    Defaults to `None` - no limit.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The background color of the date picker.
    """

    minute_interval: int = 1
    """
    The granularity of the minutes spinner, if it is shown in the current
    [`date_picker_mode`][flet.CupertinoDatePicker.date_picker_mode].

    Note:
        Must be an integer factor of `60`.
    """

    minimum_year: int = 1
    """
    Minimum year to which the picker can be scrolled when in
    [`CupertinoDatePickerMode.DATE`][flet.CupertinoDatePickerMode.DATE] mode.
    """

    maximum_year: Optional[int] = None
    """
    Maximum year to which the picker can be scrolled when in
    [`CupertinoDatePickerMode.DATE`][flet.CupertinoDatePickerMode.DATE] mode.

    Defaults to `None` - no limit.
    """

    item_extent: Number = 32.0
    """
    The uniform height of all children.
    """

    use_24h_format: bool = False
    """
    Whether to use the 24-hour time format.

    If `False`, the 12-hour time format is used.
    """

    show_day_of_week: bool = False
    """
    Whether to show day of week alongside day.
    """

    date_picker_mode: CupertinoDatePickerMode = CupertinoDatePickerMode.DATE_AND_TIME
    """
    The mode of the date picker.
    """

    date_order: Optional[CupertinoDatePickerDateOrder] = None
    """
    The order in which the columns inside this picker are displayed.

    Note:
        The final order in which the columns are displayed is also influenced by
        the [`date_picker_mode`][flet.CupertinoDatePicker.date_picker_mode].
        For example,if `date_picker_mode` is
        [`CupertinoDatePickerMode.MONTH_YEAR`][flet.CupertinoDatePickerMode.MONTH_YEAR]
        both [`CupertinoDatePickerDateOrder.DAY_MONTH_YEAR`][flet.CupertinoDatePickerDateOrder.DAY_MONTH_YEAR] and
        [`CupertinoDatePickerDateOrder.MONTH_DAY_YEAR`][flet.CupertinoDatePickerDateOrder.MONTH_DAY_YEAR] will result in the month|year order.
    """  # noqa: E501

    on_change: Optional[ControlEventHandler["CupertinoDatePicker"]] = None
    """
    Called when the selected date and/or time changes.

    Will not fire if the new
    selected value is not valid, or is not in the range of
    [`first_date`][flet.CupertinoDatePicker.first_date] and
    [`last_date`][flet.CupertinoDatePicker.last_date].
    """

    def before_update(self):
        super().before_update()

        # Normalize value to datetime in case it's a date
        if isinstance(self.value, date) and not isinstance(self.value, datetime):
            value = datetime.combine(self.value, datetime.min.time())
        else:
            value = self.value

        assert self.item_extent > 0, (
            f"item_extent must be strictly greater than 0, got {self.item_extent}"
        )
        assert self.minute_interval > 0 and 60 % self.minute_interval == 0, (
            f"minute_interval must be a positive integer factor of 60, "
            f"got {self.minute_interval}"
        )

        if self.date_picker_mode == CupertinoDatePickerMode.DATE_AND_TIME:
            if self.first_date:
                assert value >= self.first_date, (
                    f"value ({value}) can't be before first_date ({self.first_date})"
                )
            if self.last_date:
                assert value <= self.last_date, (
                    f"value ({value}) can't be after last_date ({self.last_date})"
                )

        if self.date_picker_mode in [
            CupertinoDatePickerMode.DATE,
            CupertinoDatePickerMode.MONTH_YEAR,
        ]:
            assert 1 <= self.minimum_year <= value.year, (
                f"value.year ({value.year}) can't be less than minimum_year "
            )
            f"({self.minimum_year})"

            if self.maximum_year:
                assert value.year <= self.maximum_year, (
                    f"value.year ({value.year}) can't be greater than maximum_year "
                )
                f"({self.maximum_year})"

            if self.first_date:
                assert value >= self.first_date, (
                    f"value ({value}) can't be before first_date ({self.first_date})"
                )

            if self.last_date:
                assert value <= self.last_date, (
                    f"value ({value}) can't be after last_date ({self.last_date})"
                )

        if self.date_picker_mode != CupertinoDatePickerMode.DATE:
            assert not self.show_day_of_week, (
                "show_day_of_week is only supported when date_picker_mode is "
                "CupertinoDatePickerMode.DATE"
            )

        assert value.minute % self.minute_interval == 0, (
            f"value.minute ({value.minute}) must be divisible by minute_interval "
        )
        f"({self.minute_interval})"
