from dataclasses import field
from datetime import date, datetime
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import ControlEventHandler
from flet.controls.duration import DateTimeValue
from flet.controls.layout_control import LayoutControl
from flet.controls.types import ColorValue, Locale, Number

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
    The initial date and/or time of the picker.

    It must conform to the intervals set in [`first_date`][(c).], [`last_date`][(c).],
    [`minimum_year`][(c).], and [`maximum_year`][(c).],
    else a `ValueError` will be raised.

    Defaults to the present date and time.

    Raises:
        ValueError: If [`value`][(c).] is before [`first_date`][(c).] or
            after [`last_date`][(c).].
        ValueError: If [`value`][(c).] year is less than [`minimum_year`][(c).] or
            greater than [`maximum_year`][(c).].
        ValueError: If [`value`][(c).] minute is not divisible by
            [`minute_interval`][(c).].
    """

    locale: Optional[Locale] = None
    """
    The locale for this date picker. It is intended for rare cases where this
    control should be localized differently from the rest of the page.

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
        `first_date`, with the exception that the [`on_change`][(c).] will not be
        called. Once let go, the picker will scroll back to `first_date`.

    Note:
        In [`CupertinoDatePickerMode.TIME`][flet.] mode, a time becomes unselectable
        if the datetime produced by combining that particular time and the date part of
        [`value`][(c).] is earlier than `last_date`. So typically, `first_date` needs
        to be set to a datetime that is on the same date as [`value`][(c).].
    """

    last_date: Optional[DateTimeValue] = None
    """
    The latest allowable date that the user can select.

    - If set to `None` (the default), there is no upper date limit.
    - When not `None`, one can still scroll the picker to dates later than
        `last_date`, with the exception that the [`on_change`][(c).] will not be called.
        Once let go, the picker will scroll back to `last_date`.

    Note:
        In [`CupertinoDatePickerMode.TIME`][flet.] mode, a time becomes unselectable
        if the datetime produced by combining that particular time and the date part
        of [`value`][(c).] is later than `last_date`. So typically, `last_date` needs
        to be set to a datetime that is on the same date as [`value`][(c).].
    """

    bgcolor: Optional[ColorValue] = None
    """
    The background color of this date picker.
    """

    minute_interval: int = 1
    """
    The granularity of the minutes spinner, if it is shown in the current
    [`date_picker_mode`][(c).].

    Note:
        Must be an integer factor of `60`.

    Raises:
        ValueError: If [`minute_interval`][(c).] is not a positive integer factor of
            `60`.
    """

    minimum_year: int = 1
    """
    Minimum year to which the picker can be scrolled when in
    [`CupertinoDatePickerMode.DATE`][flet.] mode.

    Raises:
        ValueError: If [`value`][(c).] year is less than [`minimum_year`][(c).].
    """

    maximum_year: Optional[int] = None
    """
    Maximum year to which the picker can be scrolled when in
    [`CupertinoDatePickerMode.DATE`][flet.] mode.

    Defaults to `None` - no limit.

    Raises:
        ValueError: If [`value`][(c).] year is greater than [`maximum_year`][(c).].
    """

    item_extent: Number = 32.0
    """
    The uniform height of all children.

    Raises:
        ValueError: If [`item_extent`][(c).] is not strictly greater than `0`.
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
        ValueError: If [`show_day_of_week`][(c).] is set when
            [`date_picker_mode`][(c).] is not
            [`CupertinoDatePickerMode.DATE`][flet.].
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
        the [`date_picker_mode`][(c).]. For example, if `date_picker_mode` is
        [`CupertinoDatePickerMode.MONTH_YEAR`][flet.]
        both [`CupertinoDatePickerDateOrder.DAY_MONTH_YEAR`][flet.] and
        [`CupertinoDatePickerDateOrder.MONTH_DAY_YEAR`][flet.] will result
        in the `month|year` order.
    """

    on_change: Optional[ControlEventHandler["CupertinoDatePicker"]] = None
    """
    Called when the selected date and/or time changes.

    Will not be called if the new selected value is not valid,
    or is not in the range of [`first_date`][(c).] and [`last_date`][(c).].
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
        if not (self.minute_interval > 0 and 60 % self.minute_interval == 0):
            raise ValueError(
                f"minute_interval must be a positive integer factor of 60, "
                f"got {self.minute_interval}"
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

        if value.minute % self.minute_interval != 0:
            raise ValueError(
                f"value.minute ({value.minute}) must be divisible by minute_interval "
                f"({self.minute_interval})"
            )
