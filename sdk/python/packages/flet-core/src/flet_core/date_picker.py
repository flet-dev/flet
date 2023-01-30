from datetime import datetime, date
from enum import Enum
from typing import Any, Optional, Union

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.text_style import TextStyle
from flet_core.types import (
    ResponsiveNumber,
)
from flet_core.textfield import KeyboardType, KeyboardTypeString

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


DatePickerModeString = Literal[
    "day",
    "year"
]


class DatePickerMode(Enum):
    DAY = "day"
    YEAR = "year"


DatePickerEntryModeString = Literal[
    "calendar",
    "input",
    "calendarOnly",
    "inputOnly"
]


class DatePickerEntryMode(Enum):
    CALENDAR = "calendar"
    INPUT = "input"
    CALENDAR_ONLY = "calendarOnly"
    INPUT_ONLY = "inputOnly"


DatePickerState = Literal["pickDate", "initState"]


class DatePicker(Control):
    """
    A button lets the user select date on datepicker dialog.

    Example:
    ```
    import flet as ft
    from flet_core.date_picker import DatePickerMode, DatePickerEntryMode


    def main(page: ft.Page):
        def change_date(e):
            page.add(ft.Checkbox(label=f"Current date {date_picker.value}"))
            date_button.text = f"{date_picker.value}"
            page.update()

        date_picker = ft.DatePicker(
            on_change=change_date,
            date_picker_mode=DatePickerMode.YEAR,
            date_picker_entry_mode=DatePickerEntryMode.INPUT,
            hint_text="Say hello?",
        )

        page.overlay.append(date_picker)

        date_button = ft.ElevatedButton(
            "Pick date",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda _: date_picker.pick_date(),
        )

        page.add(date_button)


    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/date_picker
    """

    def __init__(
            self,
            ref: Optional[Ref] = None,
            expand: Optional[Union[bool, int]] = None,
            col: Optional[ResponsiveNumber] = None,
            opacity: OptionalNumber = None,
            tooltip: Optional[str] = None,
            visible: Optional[bool] = None,
            disabled: Optional[bool] = None,
            data: Any = None,

            value: Optional[datetime] = None,
            text_style: Optional[TextStyle] = None,
            first_date: Optional[datetime] = None,
            last_date: Optional[datetime] = None,
            keyboard_type: Optional[KeyboardType] = None,
            date_picker_mode: Optional[DatePickerMode] = None,
            date_picker_entry_mode: Optional[DatePickerEntryMode] = None,
            locale: Optional[str] = None,
            help_text: Optional[str] = None,
            cancel_text: Optional[str] = None,
            confirm_text: Optional[str] = None,
            hint_text: Optional[str] = None,
            on_change=None,
            on_submit=None,
    ):
        Control.__init__(
            self,
            ref=ref,
            expand=expand,
            col=col,
            opacity=opacity,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )
        self.value = value
        self.first_date = first_date
        self.last_date = last_date
        self.keyboard_type = keyboard_type
        self.locale = locale
        self.help_text = help_text
        self.cancel_text = cancel_text
        self.confirm_text = confirm_text
        self.date_picker_mode = date_picker_mode
        self.date_picker_entry_mode = date_picker_entry_mode
        self.text_style = text_style
        self.hint_text = hint_text
        self.on_change = on_change
        self.on_submit = on_submit
        self.state = "initState"

    def _get_control_name(self):
        return "datepicker"

    def _before_build_command(self):
        super()._before_build_command()

    def pick_date(self):
        self.state = "pickDate"
        self.update()

    async def pick_date_async(self):
        self.state = "pickDate"
        await self.update_async()

    # state
    @property
    def state(self) -> Optional[DatePickerState]:
        return self._get_attr("state")

    @state.setter
    def state(self, value: Optional[DatePickerState]):
        self._set_attr("state", value)

    # value
    @property
    def value(self) -> Optional[datetime]:
        value_string = self._get_attr("value", def_value=None)
        if value_string is None or value_string == '':
            return None
        else:
            return datetime.fromisoformat(value_string)

    @value.setter
    def value(self, value: Optional[Union[datetime, str]]):
        if isinstance(value, (date, datetime)):
            value = value.isoformat()
        self._set_attr("value", value)

    # first_date
    @property
    def first_date(self) -> Optional[datetime]:
        value_string = self._get_attr("firstDate", def_value=None)
        if value_string is None:
            return None
        else:
            return datetime.fromisoformat(value_string)

    @first_date.setter
    def first_date(self, value: Optional[Union[datetime, str]]):
        if isinstance(value, (date, datetime)):
            value = value.isoformat()
        self._set_attr("firstDate", value)

    # last_date
    @property
    def last_date(self) -> Optional[datetime]:
        value_string = self._get_attr("lastDate", def_value=None)
        if value_string is None:
            return None
        else:
            return datetime.fromisoformat(value_string)

    @last_date.setter
    def last_date(self, value: Optional[Union[datetime, str]]):
        if isinstance(value, (date, datetime)):
            value = value.isoformat()
        self._set_attr("lastDate", value)

    # locale
    @property
    def locale(self) -> Optional[str]:
        return self._get_attr("locale", def_value=None)

    @locale.setter
    def locale(self, value: Optional[str]):
        self._set_attr("locale", value)

    # help_text
    @property
    def help_text(self) -> Optional[str]:
        return self._get_attr("helpText", def_value=None)

    @help_text.setter
    def help_text(self, value: Optional[str]):
        self._set_attr("helpText", value)

    # cancel_text
    @property
    def cancel_text(self) -> Optional[str]:
        return self._get_attr("cancelText", def_value=None)

    @cancel_text.setter
    def cancel_text(self, value: Optional[str]):
        self._set_attr("cancelText", value)

    # confirm_text
    @property
    def confirm_text(self) -> Optional[str]:
        return self._get_attr("confirmText", def_value=None)

    @confirm_text.setter
    def confirm_text(self, value: Optional[str]):
        self._set_attr("confirmText", value)

    # keyboard_type
    @property
    def keyboard_type(self) -> Optional[KeyboardType]:
        return self.__keyboard_type

    @keyboard_type.setter
    def keyboard_type(self, value: Optional[KeyboardType]):
        self.__keyboard_type = value
        if isinstance(value, KeyboardType):
            self._set_attr("keyboardType", value.value)
        else:
            self.__set_keyboard_type(value)

    def __set_keyboard_type(self, value: KeyboardTypeString):
        self._set_attr("keyboardType", value)

    # date_picker_mode
    @property
    def date_picker_mode(self) -> DatePickerMode:
        return self.__date_picker_mode

    @date_picker_mode.setter
    def date_picker_mode(self, value: DatePickerMode):
        self.__date_picker_mode = value
        if isinstance(value, DatePickerMode):
            self._set_attr("datePickerMode", value.value)
        else:
            self.__set_date_picker_mode(value)

    def __set_date_picker_mode(self, value: DatePickerMode):
        self._set_attr("datePickerMode", value)

    # date_picker_entry_mode
    @property
    def date_picker_entry_mode(self) -> DatePickerEntryMode:
        return self.__date_picker_entry_mode

    @date_picker_entry_mode.setter
    def date_picker_entry_mode(self, value: DatePickerEntryMode):
        self.__date_picker_entry_mode = value
        if isinstance(value, DatePickerEntryMode):
            self._set_attr("datePickerEntryMode", value.value)
        else:
            self.__set_date_picker_entry_mode(value)

    def __set_date_picker_entry_mode(self, value: DatePickerEntryMode):
        self._set_attr("datePickerEntryMode", value)

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)
        if handler is not None:
            self._set_attr("onchange", True)
        else:
            self._set_attr("onchange", None)

    # on_submit
    @property
    def on_submit(self):
        return self._get_event_handler("submit")

    @on_submit.setter
    def on_submit(self, handler):
        self._add_event_handler("submit", handler)