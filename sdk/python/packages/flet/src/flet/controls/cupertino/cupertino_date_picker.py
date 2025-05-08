from dataclasses import field
from datetime import date, datetime
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.duration import DateTimeValue
from flet.controls.types import Number, OptionalColorValue, OptionalControlEventCallable

__all__ = [
    "CupertinoDatePicker",
    "CupertinoDatePickerMode",
    "CupertinoDatePickerDateOrder",
]


class CupertinoDatePickerMode(Enum):
    TIME = "time"
    DATE = "date"
    DATE_AND_TIME = "dateAndTime"
    MONTH_YEAR = "monthYear"


class CupertinoDatePickerDateOrder(Enum):
    DAY_MONTH_YEAR = "dmy"
    MONTH_YEAR_DAY = "myd"
    YEAR_MONTH_DAY = "ymd"
    YEAR_DAY_MONTH = "ydm"


@control("CupertinoDatePicker")
class CupertinoDatePicker(ConstrainedControl):
    """
    An iOS-styled date picker.

    Online docs: https://flet.dev/docs/controls/cupertinodatepicker
    """

    value: DateTimeValue = field(default_factory=lambda: datetime.now())
    first_date: Optional[DateTimeValue] = None
    last_date: Optional[DateTimeValue] = None
    bgcolor: OptionalColorValue = None
    minute_interval: int = 1
    minimum_year: int = 1
    maximum_year: Optional[int] = None
    item_extent: Number = 32.0
    use_24h_format: bool = False
    show_day_of_week: bool = False
    date_picker_mode: CupertinoDatePickerMode = CupertinoDatePickerMode.DATE_AND_TIME
    date_order: Optional[CupertinoDatePickerDateOrder] = None
    on_change: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()

        # Normalize value to datetime in case it's a date
        if isinstance(self.value, date) and not isinstance(self.value, datetime):
            value = datetime.combine(self.value, datetime.min.time())
        else:
            value = self.value

        assert self.item_extent > 0, "item_extent must be strictly greater than 0"
        assert (
            self.minute_interval > 0 and 60 % self.minute_interval == 0
        ), "minute_interval must be a positive integer factor of 60"

        if self.date_picker_mode == CupertinoDatePickerMode.DATE_AND_TIME:
            if self.first_date:
                assert (
                    value >= self.first_date
                ), f"value ({value}) can't be before first_date ({self.first_date})"
            if self.last_date:
                assert (
                    value <= self.last_date
                ), f"value ({value}) can't be after last_date ({self.last_date})"

        if self.date_picker_mode in [
            CupertinoDatePickerMode.DATE,
            CupertinoDatePickerMode.MONTH_YEAR,
        ]:
            assert (
                1 <= self.minimum_year <= value.year
            ), f"value.year ({value.year}) can't be less than minimum_year "
            f"({self.minimum_year})"

            if self.maximum_year:
                assert (
                    value.year <= self.maximum_year
                ), f"value.year ({value.year}) can't be greater than maximum_year "
                f"({self.maximum_year})"

            if self.first_date:
                assert (
                    value >= self.first_date
                ), f"value ({value}) can't be before first_date ({self.first_date})"

            if self.last_date:
                assert (
                    value <= self.last_date
                ), f"value ({value}) can't be after last_date ({self.last_date})"

        if self.date_picker_mode != CupertinoDatePickerMode.DATE:
            assert (
                not self.show_day_of_week
            ), "show_day_of_week is only supported in CupertinoDatePickerMode.DATE mode"

        assert (
            value.minute % self.minute_interval == 0
        ), f"value.minute ({value.minute}) must be divisible by minute_interval "
        f"({self.minute_interval})"
