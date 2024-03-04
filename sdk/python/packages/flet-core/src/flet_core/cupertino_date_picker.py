from datetime import date, datetime
from enum import Enum
from typing import Any, Optional, Union

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import ResponsiveNumber

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class CupertinoDatePickerMode(Enum):
    TIME = "time"
    DATE = "date"
    DATE_AND_TIME = "dateAndTime"
    MONTH_YEAR = "monthYear"


class CupertinoDatePickerDateOrder(Enum):
    DAY_MONTH_YEAR = "dmy"
    MONTH_YEAR_DAY = "mdy"
    YEAR_MONTH_DAY = "ymd"
    YEAR_DAY_MONTH = "ydm"


class CupertinoDatePicker(Control):
    """


    -----

    Online docs: https://flet.dev/docs/controls/date_picker
    """

    def __init__(
        self,
        open: bool = False,
        value: Optional[datetime] = None,
        first_date: Optional[datetime] = None,
        last_date: Optional[datetime] = None,
        current_date: Optional[datetime] = None,
        bgcolor: Optional[str] = None,
        minute_interval: Optional[int] = None,
        minimum_year: Optional[int] = None,
        maximum_year: Optional[int] = None,
        item_extent: OptionalNumber = None,
        use_24h_format: Optional[bool] = None,
        date_picker_mode: Optional[CupertinoDatePickerMode] = None,
        date_order: Optional[CupertinoDatePickerDateOrder] = None,
        on_change=None,
        on_dismiss=None,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        expand: Optional[Union[bool, int]] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )
        self.value = value
        self.bgcolor = bgcolor
        self.minute_interval = minute_interval
        self.maximum_year = maximum_year
        self.minimum_year = minimum_year
        self.item_extent = item_extent
        self.first_date = first_date
        self.use_24h_format = use_24h_format
        self.last_date = last_date
        self.current_date = current_date
        self.date_picker_mode = date_picker_mode
        self.date_order = date_order
        self.on_change = on_change
        self.on_dismiss = on_dismiss
        self.open = open

    def _get_control_name(self):
        return "cupertinodatepicker"

    def before_update(self):
        super().before_update()

    def pick_date(self):
        self.open = True
        self.update()

    # open
    @property
    def open(self) -> Optional[bool]:
        return self._get_attr("open", data_type="bool", def_value=False)

    @open.setter
    def open(self, value: Optional[bool]):
        self._set_attr("open", value)

    # value
    @property
    def value(self) -> Optional[datetime]:
        value_string = self._get_attr("value", def_value=None)
        return datetime.fromisoformat(value_string) if value_string else None

    @value.setter
    def value(self, value: Optional[Union[datetime, str]]):
        if isinstance(value, (date, datetime)):
            value = value.isoformat()
        self._set_attr("value", value)

    # first_date
    @property
    def first_date(self) -> Optional[datetime]:
        value_string = self._get_attr("firstDate", def_value=None)
        return (
            datetime.fromisoformat(value_string) if value_string is not None else None
        )

    @first_date.setter
    def first_date(self, value: Optional[Union[datetime, str]]):
        if isinstance(value, (date, datetime)):
            value = value.isoformat()
        self._set_attr("firstDate", value)

    # last_date
    @property
    def last_date(self) -> Optional[datetime]:
        value_string = self._get_attr("lastDate", def_value=None)
        return (
            datetime.fromisoformat(value_string) if value_string is not None else None
        )

    @last_date.setter
    def last_date(self, value: Optional[Union[datetime, str]]):
        if isinstance(value, (date, datetime)):
            value = value.isoformat()
        self._set_attr("lastDate", value)

    # current_date
    @property
    def current_date(self) -> Optional[datetime]:
        value_string = self._get_attr("currentDate", def_value=None)
        return (
            datetime.fromisoformat(value_string) if value_string is not None else None
        )

    @current_date.setter
    def current_date(self, value: Optional[Union[datetime, str]]):
        if isinstance(value, (date, datetime)):
            value = value.isoformat()
        self._set_attr("currentDate", value)

    # bgcolor
    @property
    def bgcolor(self) -> Optional[str]:
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value: Optional[str]):
        self._set_attr("bgcolor", value)

    # item_extent
    @property
    def item_extent(self) -> OptionalNumber:
        return self._get_attr("itemExtent", data_type="float", def_value=32.0)

    @item_extent.setter
    def item_extent(self, value: OptionalNumber):
        self._set_attr("itemExtent", value)

    # min_year
    @property
    def min_year(self) -> Optional[int]:
        return self._get_attr("minYear", data_type="int", def_value=1)

    @min_year.setter
    def min_year(self, value: Optional[int]):
        self._set_attr("minYear", value)

    # max_year
    @property
    def max_year(self) -> Optional[int]:
        return self._get_attr("maxYear", data_type="int")

    @max_year.setter
    def max_year(self, value: Optional[int]):
        self._set_attr("maxYear", value)

    # minute_interval
    @property
    def minute_interval(self) -> Optional[int]:
        return self._get_attr("minuteInterval", data_type="int", def_value=1)

    @minute_interval.setter
    def minute_interval(self, value: Optional[int]):
        self._set_attr("minuteInterval", value)

    # use_24h_format
    @property
    def use_24h_format(self) -> Optional[int]:
        return self._get_attr("use24hFormat", data_type="bool", def_value=False)

    @use_24h_format.setter
    def use_24h_format(self, value: Optional[int]):
        self._set_attr("use24hFormat", value)

    # date_picker_mode
    @property
    def date_picker_mode(self) -> Optional[CupertinoDatePickerMode]:
        return self.__date_picker_mode

    @date_picker_mode.setter
    def date_picker_mode(self, value: Optional[CupertinoDatePickerMode]):
        self.__date_picker_mode = value
        self._set_attr(
            "datePickerMode",
            value.value if isinstance(value, CupertinoDatePickerMode) else value,
        )

    # date_order
    @property
    def date_order(self) -> Optional[CupertinoDatePickerDateOrder]:
        return self.__date_order

    @date_order.setter
    def date_order(self, value: Optional[CupertinoDatePickerDateOrder]):
        self.__date_order = value
        self._set_attr(
            "dateOrder",
            value.value if isinstance(value, CupertinoDatePickerDateOrder) else value,
        )

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)

    # on_dismiss
    @property
    def on_dismiss(self):
        return self._get_event_handler("dismiss")

    @on_dismiss.setter
    def on_dismiss(self, handler):
        self._add_event_handler("dismiss", handler)
