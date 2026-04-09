from dataclasses import field
from datetime import date, datetime
from enum import Enum
from typing import Annotated, Optional

from flet.controls.base_control import control
from flet.controls.control_event import ControlEventHandler
from flet.controls.duration import DateTimeValue
from flet.controls.layout_control import LayoutControl
from flet.controls.types import ColorValue, Locale, Number
from flet.utils.validation import V

__all__ = [
    "CupertinoDatePicker",
    "CupertinoDatePickerDateOrder",
    "CupertinoDatePickerMode",
]


class CupertinoDatePickerMode(Enum):
    """
    Different display modes of :class:`~flet.CupertinoDatePicker`.
    """

    TIME = "time"
    """
    Mode that shows the date in hour, minute, and (optional) an AM/PM designation.
    The AM/PM designation is shown only if `CupertinoDatePicker` does not use 24h
    format, i.e. if :attr:`~flet.CupertinoDatePicker.use_24h_format` is `False`.
    Column order is subject to internationalization.

    Example: `4 | 14 | PM`
    """

    DATE = "date"
    """
    Mode that shows the date in month, day of month, and year.
    Name of month is spelled in full.
    Column order is subject to internationalization.

    Example: `July | 13 | 2012`
    """

    DATE_AND_TIME = "dateAndTime"
    """
    Mode that shows the date as day of the week, month, day of month and
    the time in hour, minute, and (optional) an AM/PM designation.
    The AM/PM designation is shown only if `CupertinoDatePicker` does not use 24h
    format, i.e. if :attr:`~flet.CupertinoDatePicker.use_24h_format` is `False`.
    Column order is subject to internationalization.

    Example: `Fri Jul 13 | 4 | 14 | PM`
    """

    MONTH_YEAR = "monthYear"
    """
    Mode that shows the date in month and year.
    Name of month is spelled in full.
    Column order is subject to internationalization.

    Example: `July | 2012`
    """


class CupertinoDatePickerDateOrder(Enum):
    """
    Determines the order of the columns inside
    :class:`~flet.CupertinoDatePicker` in date mode.
    """

    DAY_MONTH_YEAR = "dmy"
    """
    Order of the columns, from left to right: day, month, year.

    Example: `12 | March | 1996`
    """

    MONTH_DAY_YEAR = "mdy"
    """
    Order of the columns, from left to right: month, day, year.

    Example: `March | 12 | 1996`
    """

    YEAR_MONTH_DAY = "ymd"
    """
    Order of the columns, from left to right: year, month, day.

    Example: `1996 | March | 12`
    """

    YEAR_DAY_MONTH = "ydm"
    """
    Order of the columns, from left to right: year, day, month.

    Example: `1996 | 12 | March`
    """


@control("CupertinoDatePicker")
class CupertinoDatePicker(LayoutControl):
    """
    An iOS-styled date picker.
    """

    value: DateTimeValue = field(default_factory=lambda: datetime.now())
    """
    The initial date and/or time of the picker.

    Defaults to the present date and time.

    Raises:
        ValueError: If it is not greater than or equal to :attr:`first_date`, when
            :attr:`first_date` is set.
        ValueError: If it is not less than or equal to :attr:`last_date`, when
            :attr:`last_date` is set.
        ValueError: If its year is not greater than or equal to
            :attr:`minimum_year`, when :attr:`date_picker_mode` is
            :attr:`flet.CupertinoDatePickerMode.DATE` or
            :attr:`flet.CupertinoDatePickerMode.MONTH_YEAR`.
        ValueError: If its year is not less than or equal to :attr:`maximum_year`,
            when :attr:`maximum_year` is set.
        ValueError: If its minute is not a multiple of :attr:`minute_interval`.
    """

    locale: Optional[Locale] = None
    """
    The locale for this date picker. It is intended for rare cases where this control \
    should be localized differently from the rest of the page.

    Notes:
        - The locale must be supported by Flutter's global localization delegates;
            otherwise the override is ignored and the control uses the page or system
            locale.
        - If `None` (the default), the page or system locale is used.
    """

    first_date: Optional[DateTimeValue] = None
    """
    The earliest allowable date that the user can select.

    - If set to `None` (the default), there is no lower date limit.
    - When not `None`, one can still scroll the picker to dates earlier than
        `first_date`, with the exception that the :attr:`on_change` will not be
        called. Once let go, the picker will scroll back to `first_date`.

    Note:
        In :attr:`flet.CupertinoDatePickerMode.TIME` mode, a time becomes unselectable
        if the datetime produced by combining that particular time and the date part of
        :attr:`value` is earlier than `last_date`. So typically, `first_date` needs
        to be set to a datetime that is on the same date as :attr:`value`.
    """

    last_date: Optional[DateTimeValue] = None
    """
    The latest allowable date that the user can select.

    - If set to `None` (the default), there is no upper date limit.
    - When not `None`, one can still scroll the picker to dates later than
        `last_date`, with the exception that the :attr:`on_change` will not be called.
        Once let go, the picker will scroll back to `last_date`.

    Note:
        In :attr:`flet.CupertinoDatePickerMode.TIME` mode, a time becomes unselectable
        if the datetime produced by combining that particular time and the date part
        of :attr:`value` is later than `last_date`. So typically, `last_date` needs
        to be set to a datetime that is on the same date as :attr:`value`.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The background color of this date picker.
    """

    minute_interval: Annotated[
        int,
        V.gt(0),
        V.factor_of(60),
    ] = 1
    """
    The granularity of the minutes spinner, if it is shown in the current \
    :attr:`date_picker_mode`.

    Raises:
        ValueError: If it is not strictly greater than `0`.
        ValueError: If it is not a factor of `60`.
    """

    minimum_year: int = 1
    """
    Minimum year to which the picker can be scrolled when in \
    :attr:`flet.CupertinoDatePickerMode.DATE` mode.

    Raises:
        ValueError: If it is greater than :attr:`value` year.
    """

    maximum_year: Optional[int] = None
    """
    Maximum year to which the picker can be scrolled when in \
    :attr:`flet.CupertinoDatePickerMode.DATE` mode.

    Defaults to `None` - no limit.

    Raises:
        ValueError: If it is less than :attr:`value` year.
    """

    item_extent: Number = 32.0
    """
    The uniform height of all children.

    Raises:
        ValueError: If it is not strictly greater than `0`.
    """

    use_24h_format: bool = False
    """
    Whether to use the 24-hour time format.

    If `False`, the 12-hour time format is used.
    """

    show_day_of_week: bool = False
    """
    Whether to show day of week alongside day.

    Raises:
        ValueError: If it is set when :attr:`date_picker_mode` is not
            :attr:`flet.CupertinoDatePickerMode.DATE`.
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
        the :attr:`date_picker_mode`. For example, if `date_picker_mode` is
        :attr:`flet.CupertinoDatePickerMode.MONTH_YEAR`
        both :attr:`flet.CupertinoDatePickerDateOrder.DAY_MONTH_YEAR` and
        :attr:`flet.CupertinoDatePickerDateOrder.MONTH_DAY_YEAR` will result
        in the `month|year` order.
    """

    on_change: Optional[ControlEventHandler["CupertinoDatePicker"]] = None
    """
    Called when the selected date and/or time changes.

    Will not be called if the new selected value is not valid,
    or is not in the range of :attr:`first_date` and :attr:`last_date`.
    """

    def before_update(self):
        super().before_update()

        # Normalize value to datetime in case it's a date
        if isinstance(self.value, date) and not isinstance(self.value, datetime):
            value = datetime.combine(self.value, datetime.min.time())
        else:
            value = self.value

        if self.item_extent <= 0:
            raise ValueError(
                f"item_extent must be strictly greater than 0, got {self.item_extent}"
            )
        if self.date_picker_mode == CupertinoDatePickerMode.DATE_AND_TIME:
            if self.first_date and value < self.first_date:
                raise ValueError(
                    f"value ({value}) can't be before first_date ({self.first_date})"
                )
            if self.last_date and value > self.last_date:
                raise ValueError(
                    f"value ({value}) can't be after last_date ({self.last_date})"
                )

        if self.date_picker_mode in [
            CupertinoDatePickerMode.DATE,
            CupertinoDatePickerMode.MONTH_YEAR,
        ]:
            if not (1 <= self.minimum_year <= value.year):
                raise ValueError(
                    f"value.year ({value.year}) can't be less than minimum_year "
                    f"({self.minimum_year})"
                )

            if self.maximum_year and value.year > self.maximum_year:
                raise ValueError(
                    f"value.year ({value.year}) can't be greater than maximum_year "
                    f"({self.maximum_year})"
                )

            if self.first_date and value < self.first_date:
                raise ValueError(
                    f"value ({value}) can't be before first_date ({self.first_date})"
                )

            if self.last_date and value > self.last_date:
                raise ValueError(
                    f"value ({value}) can't be after last_date ({self.last_date})"
                )

        if (
            self.date_picker_mode != CupertinoDatePickerMode.DATE
            and self.show_day_of_week
        ):
            raise ValueError(
                "show_day_of_week is only supported when date_picker_mode is "
                "CupertinoDatePickerMode.DATE"
            )

        if self.minute_interval > 0 and value.minute % self.minute_interval != 0:
            raise ValueError(
                f"value.minute ({value.minute}) must be a multiple of minute_interval "
                f"({self.minute_interval})"
            )
