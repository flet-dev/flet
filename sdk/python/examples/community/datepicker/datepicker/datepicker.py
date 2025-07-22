import calendar
import locale as loc
from datetime import datetime, timedelta
from typing import Callable

from datepicker.selection_type import SelectionType
from flet import (
    BorderSide,
    ButtonStyle,
    Column,
    Container,
    ControlEvent,
    IconButton,
    MainAxisAlignment,
    MaterialState,
    RoundedRectangleBorder,
    Row,
    Text,
    TextButton,
    UserControl,
    VerticalDivider,
)
from flet_core import alignment, colors, icons


class DatePicker(UserControl):
    @property
    def selected_data(self):
        return self.selected

    PREV_MONTH = "PM"
    NEXT_MONTH = "NM"
    PREV_YEAR = "PY"
    NEXT_YEAR = "NY"

    PREV_HOUR = "PH"
    NEXT_HOUR = "NH"
    PREV_MINUTE = "PMIN"
    NEXT_MINUTE = "NMIN"

    EMPTY = ""
    WHITE_SPACE = " "

    DELTA_MONTH_WEEK = 5
    DELTA_YEAR_WEEK = 52
    DELTA_HOUR = 1
    DELTA_MINUTE = 1

    WEEKEND_DAYS = [5, 6]

    CELL_SIZE = 32
    LAYOUT_WIDTH = 340
    LAYOUT_MIN_HEIGHT = 280
    LAYOUT_MAX_HEIGHT = 320
    LAYOUT_DT_MIN_HEIGHT = 320
    LAYOUT_DT_MAX_HEIGHT = 360

    def __init__(
        self,
        hour_minute: bool = False,
        selected_date: list[datetime] | None = None,
        selection_type: SelectionType | int = SelectionType.SINGLE,
        disable_to: datetime = None,
        disable_from: datetime = None,
        holidays: list[datetime] = None,
        hide_prev_next_month_days: bool = False,
        first_weekday: int = 0,
        show_three_months: bool = False,
        locale: str = None,
        on_change: Callable = None,
    ):
        super().__init__()
        self.selected = selected_date if selected_date else []
        self.selection_type = (
            selection_type
            if not type(int)
            else SelectionType.from_value(selection_type)
        )
        self.hour_minute = hour_minute
        self.disable_to = disable_to
        self.disable_from = disable_from
        self.holidays = holidays
        self.hide_prev_next_month_days = hide_prev_next_month_days
        self.first_weekday = first_weekday
        self.show_three_months = show_three_months
        if locale:
            loc.setlocale(loc.LC_ALL, locale)
        self.on_change = on_change or (lambda x: None)

        self.now = datetime.now()
        self.yy = self.now.year
        self.mm = self.now.month
        self.dd = self.now.day
        self.hour = self.now.hour
        self.minute = self.now.minute
        self.cal = calendar.Calendar(first_weekday)

    def _on_change(self, e) -> None:
        self.on_change(e)

    def _get_current_month(self, year, month):
        return self.cal.monthdatescalendar(year, month)

    def _create_calendar(self, year, month, hour, minute, hide_ymhm=False):
        week_rows_controls = []
        week_rows_days_controls = []
        today = datetime.now()

        days = self._get_current_month(year, month)

        ym = self._year_month_selectors(year, month, hide_ymhm)
        week_rows_controls.append(Column([ym], alignment=MainAxisAlignment.START))

        labels = Row(self._row_labels(), spacing=18)
        week_rows_controls.append(Column([labels], alignment=MainAxisAlignment.START))

        weeks_rows_num = len(self._get_current_month(year, month))

        for w in range(0, weeks_rows_num):
            row = []

            for d in days[w]:
                d = (
                    datetime(d.year, d.month, d.day, self.hour, self.minute)
                    if self.hour_minute
                    else datetime(d.year, d.month, d.day)
                )

                month = d.month
                is_main_month = True if month == self.mm else False

                if self.hide_prev_next_month_days and not is_main_month:
                    row.append(
                        Text(
                            "",
                            width=self.CELL_SIZE,
                            height=self.CELL_SIZE,
                        )
                    )
                    continue

                dt_weekday = d.weekday()
                day = d.day
                is_weekend = False
                is_holiday = False

                is_day_disabled = False

                if self.disable_from and self._reset_time(d) > self._reset_time(
                    self.disable_from
                ):
                    is_day_disabled = True

                if self.disable_to and self._reset_time(d) < self._reset_time(
                    self.disable_to
                ):
                    is_day_disabled = True

                text_color = None
                border_side = None
                bg = None
                # week end bg color
                if dt_weekday in self.WEEKEND_DAYS:
                    text_color = colors.RED_500
                    is_weekend = True
                # holidays
                if self.holidays and d in self.holidays:
                    text_color = colors.RED_500
                    is_holiday = True

                # current day bg
                if (
                    is_main_month
                    and day == self.dd
                    and self.dd == today.day
                    and self.mm == today.month
                    and self.yy == today.year
                ):
                    border_side = BorderSide(2, colors.BLUE)
                elif (is_weekend or is_holiday) and (
                    not is_main_month or is_day_disabled
                ):
                    text_color = colors.RED_200
                    bg = None
                elif not is_main_month and is_day_disabled:
                    text_color = colors.BLACK38
                    bg = None
                elif not is_main_month:
                    text_color = colors.BLUE_200
                    bg = None
                else:
                    bg = None

                # selected days
                selected_numbers = len(self.selected)
                if self.selection_type != SelectionType.RANGE:
                    if selected_numbers > 0 and d in self.selected:
                        bg = colors.BLUE_400
                        text_color = colors.WHITE
                else:
                    if (
                        selected_numbers > 0
                        and selected_numbers < 3
                        and d in self.selected
                    ):
                        bg = colors.BLUE_400
                        text_color = colors.WHITE

                if self.selection_type == SelectionType.RANGE and selected_numbers > 1:
                    if d > self.selected[0] and d < self.selected[-1]:
                        bg = colors.BLUE_300
                        text_color = colors.WHITE

                row.append(
                    TextButton(
                        text=str(day),
                        data=d,
                        width=self.CELL_SIZE,
                        height=self.CELL_SIZE,
                        disabled=is_day_disabled,
                        style=ButtonStyle(
                            color=text_color,
                            bgcolor=bg,
                            padding=0,
                            shape={
                                MaterialState.DEFAULT: RoundedRectangleBorder(
                                    radius=20
                                ),
                            },
                            side=border_side,
                        ),
                        on_click=self._select_date,
                    )
                )

            week_rows_days_controls.append(Row(row, spacing=18))

        week_rows_controls.append(
            Column(
                week_rows_days_controls, alignment=MainAxisAlignment.START, spacing=0
            )
        )

        if self.hour_minute and not hide_ymhm:
            hm = self._hour_minute_selector(hour, minute)
            week_rows_controls.append(Row([hm], alignment=MainAxisAlignment.CENTER))

        return week_rows_controls

    def _year_month_selectors(self, year, month, hide_ymhm=False):
        prev_year = (
            IconButton(
                icon=icons.ARROW_BACK,
                data=self.PREV_YEAR,
                on_click=self._adjust_calendar,
            )
            if not hide_ymhm
            else Text(
                self.EMPTY,
                height=self.CELL_SIZE,
            )
        )
        next_year = (
            IconButton(
                icon=icons.ARROW_FORWARD,
                data=self.NEXT_YEAR,
                on_click=self._adjust_calendar,
            )
            if not hide_ymhm
            else Text(self.EMPTY)
        )
        prev_month = (
            IconButton(
                icon=icons.ARROW_BACK,
                data=self.PREV_MONTH,
                on_click=self._adjust_calendar,
            )
            if not hide_ymhm
            else Text(self.EMPTY)
        )
        next_month = (
            IconButton(
                icon=icons.ARROW_FORWARD,
                data=self.NEXT_MONTH,
                on_click=self._adjust_calendar,
            )
            if not hide_ymhm
            else Text(self.EMPTY)
        )
        ym = Row(
            [
                Row(
                    [
                        prev_year,
                        Text(year),
                        next_year,
                    ],
                    spacing=0,
                ),
                Row(
                    [
                        prev_month,
                        Text(calendar.month_name[month], text_align=alignment.center),
                        next_month,
                    ],
                    spacing=0,
                ),
            ],
            spacing=0,
            alignment=MainAxisAlignment.SPACE_BETWEEN,
        )

        return ym

    def _row_labels(self):
        label_row = []
        days_label = calendar.weekheader(2).split(self.WHITE_SPACE)
        for i in range(0, self.first_weekday):
            days_label.append(days_label.pop(0))
        for l in days_label:
            label_row.append(
                TextButton(
                    text=l,
                    width=self.CELL_SIZE,
                    height=self.CELL_SIZE,
                    disabled=True,
                    style=ButtonStyle(
                        padding=0,
                        color=colors.BLACK,
                        bgcolor=colors.GREY_300,
                        shape={
                            MaterialState.DEFAULT: RoundedRectangleBorder(radius=20),
                        },
                    ),
                )
            )

        return label_row

    def _hour_minute_selector(self, hour, minute):
        hm = Row(
            [
                Row(
                    [
                        IconButton(
                            icon=icons.ARROW_BACK,
                            data=self.PREV_HOUR,
                            on_click=self._adjust_hh_min,
                        ),
                        Text(hour),
                        IconButton(
                            icon=icons.ARROW_FORWARD,
                            data=self.NEXT_HOUR,
                            on_click=self._adjust_hh_min,
                        ),
                    ]
                ),
                Text(":"),
                Row(
                    [
                        IconButton(
                            icon=icons.ARROW_BACK,
                            data=self.PREV_MINUTE,
                            on_click=self._adjust_hh_min,
                        ),
                        Text(minute),
                        IconButton(
                            icon=icons.ARROW_FORWARD,
                            data=self.NEXT_MINUTE,
                            on_click=self._adjust_hh_min,
                        ),
                    ]
                ),
            ],
            spacing=48,
            alignment=MainAxisAlignment.SPACE_EVENLY,
        )

        return hm

    def build(self):
        rows = self._create_layout(self.yy, self.mm, self.hour, self.minute)

        cal_height = self._calculate_heigth(self.yy, self.mm)

        self.cal_container = Container(
            content=Row(rows),
            bgcolor=colors.WHITE,
            padding=12,
            height=self._cal_height(cal_height),
        )
        return self.cal_container

    def _calculate_heigth(self, year, month):
        if self.show_three_months:
            prev, next = self._prev_next_month(year, month)
            cal_height = max(
                len(self._get_current_month(year, month)),
                len(self._get_current_month(prev.year, prev.month)),
                len(self._get_current_month(next.year, next.month)),
            )
        else:
            cal_height = len(self._get_current_month(year, month))
        return cal_height

    def _create_layout(self, year, month, hour, minute):
        rows = []
        prev, next = self._prev_next_month(year, month)

        if self.show_three_months:
            week_rows_controls_prev = self._create_calendar(
                prev.year, prev.month, hour, minute, True
            )
            rows.append(
                Column(week_rows_controls_prev, width=self.LAYOUT_WIDTH, spacing=10)
            )
            rows.append(VerticalDivider())

        week_rows_controls = self._create_calendar(year, month, hour, minute)
        rows.append(Column(week_rows_controls, width=self.LAYOUT_WIDTH, spacing=10))

        if self.show_three_months:
            rows.append(VerticalDivider())
            week_rows_controls_next = self._create_calendar(
                next.year, next.month, hour, minute, True
            )
            rows.append(
                Column(week_rows_controls_next, width=self.LAYOUT_WIDTH, spacing=10)
            )

        return rows

    def _prev_next_month(self, year, month):
        delta = timedelta(weeks=self.DELTA_MONTH_WEEK)
        current = datetime(year, month, 15)
        prev = current - delta
        next = current + delta
        return prev, next

    def _select_date(self, e: ControlEvent):
        result: datetime = e.control.data

        if self.selection_type == SelectionType.RANGE:
            if len(self.selected) == 2:
                self.selected = []

            if len(self.selected) > 0:
                if self.selected[0] == result:
                    self.selected = []
                else:
                    if result > self.selected[0]:
                        if len(self.selected) == 1:
                            self.selected.append(result)
                        else:
                            return
                    else:
                        return
            else:
                self.selected.append(result)
        elif self.selection_type == SelectionType.MULTIPLE:
            if len(self.selected) > 0 and result in self.selected:
                self.selected.remove(result)
            else:
                if self.hour_minute:
                    result = datetime(
                        result.year, result.month, result.day, self.hour, self.minute
                    )
                self.selected.append(result)
        else:
            if len(self.selected) == 1 and result in self.selected:
                self.selected.remove(result)
            else:
                self.selected = []
                if self.hour_minute:
                    result = datetime(
                        result.year, result.month, result.day, self.hour, self.minute
                    )
                self.selected.append(result)
        self._on_change(self.selected)
        self._update_calendar()

    def _adjust_calendar(self, e: ControlEvent):
        if e.control.data == self.PREV_MONTH or e.control.data == self.NEXT_MONTH:
            delta = timedelta(weeks=self.DELTA_MONTH_WEEK)
        if e.control.data == self.PREV_YEAR or e.control.data == self.NEXT_YEAR:
            delta = timedelta(weeks=self.DELTA_YEAR_WEEK)

        if e.control.data == self.PREV_MONTH or e.control.data == self.PREV_YEAR:
            self.now = self.now - delta
        if e.control.data == self.NEXT_MONTH or e.control.data == self.NEXT_YEAR:
            self.now = self.now + delta

        self.mm = self.now.month
        self.yy = self.now.year
        self._update_calendar()

    def _adjust_hh_min(self, e: ControlEvent):
        if e.control.data == self.PREV_HOUR or e.control.data == self.NEXT_HOUR:
            delta = timedelta(hours=self.DELTA_HOUR)
        if e.control.data == self.PREV_MINUTE or e.control.data == self.NEXT_MINUTE:
            delta = timedelta(minutes=self.DELTA_MINUTE)

        if e.control.data == self.PREV_HOUR or e.control.data == self.PREV_MINUTE:
            self.now = self.now - delta
        if e.control.data == self.NEXT_HOUR or e.control.data == self.NEXT_MINUTE:
            self.now = self.now + delta

        self.hour = self.now.hour
        self.minute = self.now.minute
        self._update_calendar()

    def _update_calendar(self):
        self.cal_container.content = Row(
            self._create_layout(self.yy, self.mm, self.hour, self.minute)
        )
        cal_height = self._calculate_heigth(self.yy, self.mm)
        self.cal_container.height = self._cal_height(cal_height)
        self.update()

    def _cal_height(self, weeks_number):
        if self.hour_minute:
            return (
                self.LAYOUT_DT_MIN_HEIGHT
                if weeks_number == 5
                else self.LAYOUT_DT_MAX_HEIGHT
            )
        else:
            return (
                self.LAYOUT_MIN_HEIGHT if weeks_number == 5 else self.LAYOUT_MAX_HEIGHT
            )

    def _reset_time(self, date):
        return date.replace(hour=0, minute=0, second=0, microsecond=0)
