from datetime import datetime
from enum import Enum
from typing import Any, Optional, Union

from flet.core.animation import AnimationValue
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import OptionalNumber
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    ColorEnums,
    ColorValue,
    DateTimeValue,
    OffsetValue,
    OptionalControlEventCallable,
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
        value: DateTimeValue = datetime.now(),
        first_date: Optional[DateTimeValue] = None,
        last_date: Optional[DateTimeValue] = None,
        bgcolor: Optional[ColorValue] = None,
        minute_interval: Optional[int] = None,
        minimum_year: Optional[int] = None,
        maximum_year: Optional[int] = None,
        item_extent: OptionalNumber = None,
        use_24h_format: Optional[bool] = None,
        date_picker_mode: Optional[CupertinoDatePickerMode] = None,
        date_order: Optional[CupertinoDatePickerDateOrder] = None,
        on_change: OptionalControlEventCallable = None,
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
        rotate: Optional[RotateValue] = None,
        scale: Optional[ScaleValue] = None,
        offset: Optional[OffsetValue] = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: Optional[AnimationValue] = None,
        animate_size: Optional[AnimationValue] = None,
        animate_position: Optional[AnimationValue] = None,
        animate_rotation: Optional[AnimationValue] = None,
        animate_scale: Optional[AnimationValue] = None,
        animate_offset: Optional[AnimationValue] = None,
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: Optional[TooltipValue] = None,
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
    def value(self) -> datetime:
        v = self._get_attr("value")
        return datetime.fromisoformat(v) if v else None

    @value.setter
    def value(self, value: DateTimeValue):
        self._set_attr("value", value.isoformat())

    # first_date
    @property
    def first_date(self) -> Optional[datetime]:
        v = self._get_attr("firstDate")
        return datetime.fromisoformat(v) if v is not None else None

    @first_date.setter
    def first_date(self, value: Optional[DateTimeValue]):
        self.__first_date = value
        self._set_attr("firstDate", value if value is None else value.isoformat())

    # last_date
    @property
    def last_date(self) -> Optional[datetime]:
        v = self._get_attr("lastDate")
        return datetime.fromisoformat(v) if v is not None else None

    @last_date.setter
    def last_date(self, value: Optional[DateTimeValue]):
        self._set_attr("lastDate", value if value is None else value.isoformat())

    # bgcolor
    @property
    def bgcolor(self) -> Optional[ColorValue]:
        return self.__bgcolor

    @bgcolor.setter
    def bgcolor(self, value: Optional[ColorValue]):
        self.__bgcolor = value
        self._set_enum_attr("bgcolor", value, ColorEnums)

    # item_extent
    @property
    def item_extent(self) -> float:
        return self._get_attr("itemExtent", data_type="float", def_value=32.0)

    @item_extent.setter
    def item_extent(self, value: OptionalNumber):
        assert value is None or value > 0, "item_extent must be greater than 0"
        self._set_attr("itemExtent", value)

    # min_year
    @property
    def min_year(self) -> int:
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
    def minute_interval(self) -> int:
        return self._get_attr("minuteInterval", data_type="int", def_value=1)

    @minute_interval.setter
    def minute_interval(self, value: Optional[int]):
        assert value is None or (
            value > 0 and 60 % value == 0
        ), "minute_interval must be a positive integer factor of 60"
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
        self._set_enum_attr("datePickerMode", value, CupertinoDatePickerMode)

    # date_order
    @property
    def date_order(self) -> Optional[CupertinoDatePickerDateOrder]:
        return self.__date_order

    @date_order.setter
    def date_order(self, value: Optional[CupertinoDatePickerDateOrder]):
        self.__date_order = value
        self._set_enum_attr("dateOrder", value, CupertinoDatePickerDateOrder)

    # on_change
    @property
    def on_change(self) -> OptionalControlEventCallable:
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler: OptionalControlEventCallable):
        self._add_event_handler("change", handler)
