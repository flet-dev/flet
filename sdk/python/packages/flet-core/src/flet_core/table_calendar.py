from datetime import datetime, date
from enum import Enum
from typing import Any, Optional, Union, Literal

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)

CalendarFormatString = Literal[
    "month",
    "twoWeeks",
    "week",
]


class CalendarFormat(Enum):
    MONTH = "month"
    TWO_WEEKS = "twoWeeks"
    WEEK = "week"


RangeSelectionModeString = Literal[
    "disabled",
    "toggledOff",
    "toggledOn",
    "enforced"
]


class CalendarRangeSelectionMode(Enum):
    DISABLED = "disabled"
    TOGGLE_OFF = "toggledOff"
    TOGGLE_ON = "toggledOn"
    ENFORCED = "enforced"


class TableCalendar(ConstrainedControl):
    """
    TODO: write docs.
    TODO: write examples.
    """

    def __init__(
            self,
            ref: Optional[Ref] = None,
            width: OptionalNumber = None,
            height: OptionalNumber = None,
            expand: Union[None, bool, int] = None,
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
            #
            # TableCalendar Specific
            #
            focused_day: Optional[datetime] = None,
            first_day: Optional[datetime] = None,
            last_day: Optional[datetime] = None,
            current_day: Optional[datetime] = None,
            locale: Optional[str] = None,
            calendar_format: Optional[CalendarFormat] = None,
            range_selection_mode: Optional[CalendarRangeSelectionMode] = None,
            on_day_selected: Optional = None,
            on_range_selected: Optional = None,
            on_format_changed: Optional = None,
            on_page_changed: Optional = None,
            events=None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            width=width,
            height=height,
            expand=expand,
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
            data=data
        )

        self.__events = [],
        self.focused_day = focused_day,
        self.first_day = first_day,
        self.last_day = last_day,
        self.current_day = current_day,
        self.locale = locale,
        self.calendar_format = calendar_format,
        self.range_selection_mode = range_selection_mode,
        self.on_day_selected = on_day_selected,
        self.on_range_selected = on_range_selected,
        self.on_format_changed = on_format_changed,
        self.on_page_changed = on_page_changed,
        self.events = events

    def _get_control_name(self):
        return "tablecalendar"

    def _before_build_command(self):
        super()._before_build_command()

    def _get_children(self):
        result = ConstrainedControl._get_children(self)
        result.extend(self.__events)
        return result

    # focused_day
    @property
    def focused_day(self) -> Optional[datetime]:
        value_string = self._get_attr("focusedDay", def_value=None)
        return datetime.fromisoformat(value_string) if value_string else None

    @focused_day.setter
    def focused_day(self, value: Optional[Union[datetime, str]]):
        if isinstance(value, (date, datetime)):
            value = value.isoformat()
        self._set_attr("focusedDay", value)

    # first_date
    @property
    def first_day(self) -> Optional[datetime]:
        value_string = self._get_attr("firstDay", def_value=None)
        return datetime.fromisoformat(value_string) if value_string else None

    @first_day.setter
    def first_day(self, value: Optional[Union[datetime, str]]):
        if isinstance(value, (date, datetime)):
            value = value.isoformat()
        self._set_attr("firstDay", value)

    # last_date
    @property
    def last_day(self) -> Optional[datetime]:
        value_string = self._get_attr("lastDay", def_value=None)
        return datetime.fromisoformat(value_string) if value_string else None

    @last_day.setter
    def last_day(self, value: Optional[Union[datetime, str]]):
        if isinstance(value, (date, datetime)):
            value = value.isoformat()
        self._set_attr("lastDay", value)

    # current_day
    @property
    def current_day(self) -> Optional[datetime]:
        value_string = self._get_attr("currentDay", def_value=None)
        return datetime.fromisoformat(value_string) if value_string else None

    @current_day.setter
    def current_day(self, value: Optional[Union[datetime, str]]):
        if isinstance(value, (date, datetime)):
            value = value.isoformat()
        self._set_attr("currentDay", value)

    # locale
    @property
    def locale(self) -> Optional[str]:
        return self._get_attr("locale", def_value=None)

    @locale.setter
    def locale(self, value: Optional[str]):
        self._set_attr("locale", value)

    # events
    @property
    def events(self):
        return self.__events

    @events.setter
    def events(self, value):
        self.__events = value if value is not None else []

    # date_picker_mode
    @property
    def calendar_format(self) -> CalendarFormat:
        return self.__date_calendar_format

    @calendar_format.setter
    def calendar_format(self, value: CalendarFormat):
        self.__date_calendar_format = value
        if isinstance(value, CalendarFormat):
            self._set_attr("calendarFormat", value.value)
        else:
            self.__set_calendar_format(value)

    def __set_calendar_format(self, value: CalendarFormat):
        self._set_attr("calendarFormat", value)

    # date_picker_entry_mode
    @property
    def date_range_selection_mode(self) -> CalendarRangeSelectionMode:
        return self.__date_range_selection_mode

    @date_range_selection_mode.setter
    def date_range_selection_mode(self, value: CalendarRangeSelectionMode):
        self.__date_range_selection_mode = value
        if isinstance(value, CalendarRangeSelectionMode):
            self._set_attr("rangeSelectionMode", value.value)
        else:
            self.__set_range_selection_mode(value)

    def __set_range_selection_mode(self, value: CalendarRangeSelectionMode):
        self._set_attr("rangeSelectionMode", value)

    # on_day_selected
    @property
    def on_day_selected(self):
        return self._get_event_handler("daySelected")

    @on_day_selected.setter
    def on_day_selected(self, handler):
        self._add_event_handler("daySelected", handler)

    # on_range_selected
    @property
    def on_range_selected(self):
        return self._get_event_handler("rangeSelected")

    @on_range_selected.setter
    def on_range_selected(self, handler):
        self._add_event_handler("rangeSelected", handler)

    # on_format_changed
    @property
    def on_format_changed(self):
        return self._get_event_handler("formatChange")

    @on_format_changed.setter
    def on_format_changed(self, handler):
        self._add_event_handler("formatChange", handler)

    # on_format_changed
    @property
    def on_page_changed(self):
        return self._get_event_handler("pageChanged")

    @on_page_changed.setter
    def on_page_changed(self, handler):
        self._add_event_handler("pageChanged", handler)


class CalendarEvent(Control):
    def __init__(
            self,
            key: Optional[str] = None,
            label: Optional[str] = None,
            date: Optional[str] = None,
            disabled: Optional[str] = None,
            ref: Optional[Ref] = None
    ):
        Control.__init__(self, ref=ref, disabled=disabled)
        assert key is not None or label is not None, "key or text must be specified"
        self.key = key
        self.label = label
        self.date = date
        self.disabled = disabled

    def _get_control_name(self):
        return "calendarevent"

    # key
    @property
    def key(self):
        return self._get_attr("key")

    @key.setter
    def key(self, value):
        self._set_attr("key", value)

    # label
    @property
    def label(self):
        return self._get_attr("label")

    @label.setter
    def label(self, value):
        self._set_attr("label", value)

    # date
    @property
    def date(self) -> Optional[datetime]:
        value_string = self._get_attr("date", def_value=None)
        return datetime.fromisoformat(value_string) if value_string else None

    @date.setter
    def date(self, value: Optional[Union[datetime, str]]):
        if isinstance(value, (date, datetime)):
            value = value.isoformat()
        self._set_attr("date", value)
