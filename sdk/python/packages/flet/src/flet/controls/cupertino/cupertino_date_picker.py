from dataclasses import field
from datetime import datetime
from enum import Enum
from typing import Optional

from flet.controls.constrained_control import ConstrainedControl
from flet.controls.types import (
    DateTimeValue,
    Number,
    OptionalColorValue,
    OptionalControlEventCallable,
)

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


class CupertinoDatePicker(ConstrainedControl):
    """
    An iOS-styled date picker.

    -----

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
    date_picker_mode: Optional[CupertinoDatePickerMode] = None
    date_order: Optional[CupertinoDatePickerDateOrder] = None
    on_change: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert self.item_extent > 0, "item_extent must be greater than 0"

    # # value
    # @property
    # def value(self) -> datetime:
    #     v = self._get_attr("value")
    #     return datetime.fromisoformat(v) if v else None
    #
    # @value.setter
    # def value(self, value: DateTimeValue):
    #     self._set_attr("value", value.isoformat())
    #
    # # first_date
    # @property
    # def first_date(self) -> Optional[datetime]:
    #     v = self._get_attr("firstDate")
    #     return datetime.fromisoformat(v) if v is not None else None
    #
    # @first_date.setter
    # def first_date(self, value: Optional[DateTimeValue]):
    #     self.__first_date = value
    #     self._set_attr("firstDate", value if value is None else value.isoformat())
    #
    # # last_date
    # @property
    # def last_date(self) -> Optional[datetime]:
    #     v = self._get_attr("lastDate")
    #     return datetime.fromisoformat(v) if v is not None else None
    #
    # @last_date.setter
    # def last_date(self, value: Optional[DateTimeValue]):
    #     self._set_attr("lastDate", value if value is None else value.isoformat())
