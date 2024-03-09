from datetime import date, datetime
from enum import Enum
from typing import Any, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


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

    def __init__(
        self,
        value: Optional[datetime] = None,
        first_date: Optional[datetime] = None,
        last_date: Optional[datetime] = None,
        bgcolor: Optional[str] = None,
        minute_interval: Optional[int] = None,
        minimum_year: Optional[int] = None,
        maximum_year: Optional[int] = None,
        item_extent: OptionalNumber = None,
        use_24h_format: Optional[bool] = None,
        date_picker_mode: Optional[CupertinoDatePickerMode] = None,
        date_order: Optional[CupertinoDatePickerDateOrder] = None,
        on_change=None,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        on_animation_end=None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
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
        self.date_picker_mode = date_picker_mode
        self.date_order = date_order
        self.on_change = on_change

    def _get_control_name(self):
        return "cupertinodatepicker"

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
        if value is not None and value < 0:
            raise ValueError("item_extent must be greater than 0")
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
        if value is not None and (value < 0 or 60 % value != 0):
            raise ValueError("minute_interval must be a positive integer factor of 60")
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
