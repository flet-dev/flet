import datetime as dt
import flet as ft
import calendar

from typing import Any, Optional, Union, Iterable, Callable

from beartype.typing import List

from flet.control import Control, OptionalNumber
from flet.ref import Ref
from flet.types import (
    AnimationValue,
    CrossAxisAlignment,
    MainAxisAlignment,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    ScrollMode,
)

    
class DatetimeField(ft.Row):
    date_controls_dict = dict()
    months_ = list(calendar.month_name)[1:]
    dt_format = "%Y,%B,%d,%H,%M"
    options = ['_years','_months','_days','_hours','_minutes']

    def __init__(self, page: ft.Page, on_change: Callable = None, controls: Optional[List[Control]] = None, ref: Optional[Ref] = None, width: OptionalNumber = None, height: OptionalNumber = None, left: OptionalNumber = None, top: OptionalNumber = None, right: OptionalNumber = None, bottom: OptionalNumber = None, expand: Union[None, bool, int] = None, col: Optional[ResponsiveNumber] = None, opacity: OptionalNumber = None, rotate: RotateValue = None, scale: ScaleValue = None, offset: OffsetValue = None, aspect_ratio: OptionalNumber = None, animate_opacity: AnimationValue = None, animate_size: AnimationValue = None, animate_position: AnimationValue = None, animate_rotation: AnimationValue = None, animate_scale: AnimationValue = None, animate_offset: AnimationValue = None, on_animation_end=None, visible: Optional[bool] = None, disabled: Optional[bool] = None, data: Any = None, alignment: MainAxisAlignment = MainAxisAlignment.NONE, vertical_alignment: CrossAxisAlignment = CrossAxisAlignment.NONE, spacing: OptionalNumber = None, tight: Optional[bool] = None, wrap: Optional[bool] = None, run_spacing: OptionalNumber = None, scroll: Optional[ScrollMode] = None, auto_scroll: Optional[bool] = None) -> None:
        """
        Needs page element for update days.
        """
        super().__init__(controls, ref, width, height, left, top, right, bottom, expand, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, alignment, vertical_alignment, spacing, tight, wrap, run_spacing, scroll, auto_scroll)    
        self.page = page
        self.on_change = on_change or (lambda x : None)

        # Create all components and equal controls property
        for attr in self.options: getattr(self, attr)()
        self.controls = list(self.date_controls_dict.values())

    def _years(self) -> None:
        year = dt.date.today().year
        years = list(map(lambda x : str(x), range(year, year-10, -1)))
        self._dropdown('years', years, on_change=self._on_change, width = 110, hint_text='Year')

    def _months(self) -> None:
        self._dropdown('months', self.months_, on_change=self._on_change, width = 120, hint_text='Month')

    def _days(self, year:int=dt.date.today().year, month:int=1) -> None:
        """
        Get month days by choosen month and year.
        """
        day = calendar.monthrange(year, month)[1]
        days = range(1, day+1)
        self._dropdown('days', days, on_change=self._on_change_wrapper, width = 110, hint_text='Day')

    def _hours(self) -> None:
        hours = range(24)
        self._dropdown('hours', hours, on_change=self._on_change_wrapper, width = 110, hint_text='Hour')

    def _minutes(self) -> None:
        minutes = range(60)
        self._dropdown('minutes', minutes , on_change=self._on_change_wrapper, width = 110, hint_text='Minute')

    def _on_change(self, e) -> None:
        """
        The method then checks if both the year and month dropdown menus 
        have valid values, and if so, it calls the days() method to update 
        the days dropdown menu.
        """
        self.on_change(self.value)

        year = self.date_controls_dict['years'].value
        month = self.date_controls_dict['months'].value
        valid = year != '' and year != None and month != '' and month != None

        if valid:
            year, month =int(year), self.months_.index(month) + 1
            elements = range(1, calendar.monthrange(year, month)[1] + 1)
            dropdown_option = lambda x : ft.dropdown.Option(x)
            self.date_controls_dict['days'].options = list(map(dropdown_option, elements))
            self.page.update()

    def _on_change_wrapper(self, e):
        self.on_change(self.value)

    def _dropdown(self, name: str, elements: Iterable, **kwargs) -> None:
        """
        Transform list to "ft.dropdown.Option" 
        list and add my components list.
        """
        dropdown_option = lambda x : ft.dropdown.Option(x)
        self.date_controls_dict[name] = ft.Dropdown(options=list(map(dropdown_option, elements)), **kwargs)
    
    @property
    def value(self) -> Union[list, dt.datetime]:
        controls = list(map(lambda x : x.value, self.controls))
        if None not in controls:
            str_dt = ",".join(controls)
            try:
                return dt.datetime.strptime(str_dt, self.dt_format)
            except:
                return controls
        return controls
    
    @value.setter
    def value(self, values: Union[list, dict]) -> None:
        if isinstance(values, list):
            assert len(values) == len(self.controls), f'elements lenght not matching : {len(values)} != {self.controls}'
            for control, value in zip(self.controls, values): 
                control.value = value

        elif isinstance(values, dict):
            for key, value in values.items():
                assert key in self.date_controls_dict[key], f'{key} not in {self.options}'
                self.date_controls_dict[key].value = value
                
