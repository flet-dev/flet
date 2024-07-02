from datetime import date, datetime
from enum import Enum
from typing import Any, Optional, Union, Callable

from flet_core import ControlEvent
from flet_core.control import Control, OptionalNumber
from flet_core.event_handler import EventHandler
from flet_core.ref import Ref
from flet_core.textfield import KeyboardType
from flet_core.types import ResponsiveNumber, OptionalEventCallable
from flet_core.utils import deprecated

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class DatePickerMode(Enum):
    DAY = "day"
    YEAR = "year"


class DatePickerEntryMode(Enum):
    CALENDAR = "calendar"
    INPUT = "input"
    CALENDAR_ONLY = "calendarOnly"
    INPUT_ONLY = "inputOnly"


class DatePickerEntryModeChangeEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        self.entry_mode: Optional[DatePickerEntryMode] = DatePickerEntryMode(e.data)


class DatePicker(Control):
    """
    A Material-style date picker dialog.

    It is added to [`page.overlay`](page#overlay) and can be opened by setting `open=True` or by calling `Page.open()` method.

    Depending on the `date_picker_entry_mode`, it will show either a Calendar or an Input (TextField) for picking a date.

    Example:
    ```
    import flet as ft


    def main(page):
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        def handle_date_change(e: ft.ControlEvent):
            page.add(ft.Text(f"Date changed: {e.control.value.strftime('%Y-%m-%d %H:%M %p')}"))

        cupertino_date_picker = ft.CupertinoDatePicker(
            date_picker_mode=ft.CupertinoDatePickerMode.DATE_AND_TIME,
            on_change=handle_date_change,
        )
        page.add(
            ft.CupertinoFilledButton(
                "Open CupertinoDatePicker",
                on_click=lambda e: page.open(
                    ft.CupertinoBottomSheet(
                        cupertino_date_picker,
                        height=216,
                        padding=ft.padding.only(top=6),
                    )
                ),
            )
        )


    ft.app(main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/datepicker
    """

    def __init__(
        self,
        open: bool = False,
        value: Optional[datetime] = None,
        first_date: Optional[datetime] = None,
        last_date: Optional[datetime] = None,
        current_date: Optional[datetime] = None,
        keyboard_type: Optional[KeyboardType] = None,
        date_picker_mode: Optional[DatePickerMode] = None,
        date_picker_entry_mode: Optional[DatePickerEntryMode] = None,
        help_text: Optional[str] = None,
        cancel_text: Optional[str] = None,
        confirm_text: Optional[str] = None,
        error_format_text: Optional[str] = None,
        error_invalid_text: Optional[str] = None,
        field_hint_text: Optional[str] = None,
        field_label_text: Optional[str] = None,
        switch_to_calendar_icon: Optional[str] = None,
        switch_to_input_icon: Optional[str] = None,
        on_change: OptionalEventCallable = None,
        on_dismiss: OptionalEventCallable = None,
        on_entry_mode_change: Optional[
            Callable[[DatePickerEntryModeChangeEvent], None]
        ] = None,
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

        self.__on_entry_mode_change = EventHandler(
            lambda e: DatePickerEntryModeChangeEvent(e.data)
        )
        self._add_event_handler(
            "entryModeChange", self.__on_entry_mode_change.get_handler()
        )

        self.value = value
        self.first_date = first_date
        self.last_date = last_date
        self.current_date = current_date
        self.keyboard_type = keyboard_type
        self.help_text = help_text
        self.cancel_text = cancel_text
        self.confirm_text = confirm_text
        self.error_format_text = error_format_text
        self.error_invalid_text = error_invalid_text
        self.date_picker_mode = date_picker_mode
        self.date_picker_entry_mode = date_picker_entry_mode
        self.field_hint_text = field_hint_text
        self.field_label_text = field_label_text
        self.switch_to_calendar_icon = switch_to_calendar_icon
        self.switch_to_input_icon = switch_to_input_icon
        self.on_change = on_change
        self.on_dismiss = on_dismiss
        self.open = open
        self.on_entry_mode_change = on_entry_mode_change

    def _get_control_name(self):
        return "datepicker"

    def before_update(self):
        super().before_update()

    @deprecated(
        reason="Use Page.open() method instead.",
        version="0.23.0",
        delete_version="0.26.0",
    )
    def pick_date(self):
        self.open = True
        self.update()

    @deprecated(
        reason="Use Page.open() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def pick_date_async(self):
        self.pick_date()

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

    # field_hint_text
    @property
    def field_hint_text(self) -> Optional[str]:
        return self._get_attr("fieldHintText", def_value=None)

    @field_hint_text.setter
    def field_hint_text(self, value: Optional[str]):
        self._set_attr("fieldHintText", value)

    # field_label_text
    @property
    def field_label_text(self) -> Optional[str]:
        return self._get_attr("fieldLabelText", def_value=None)

    @field_label_text.setter
    def field_label_text(self, value: Optional[str]):
        self._set_attr("fieldLabelText", value)

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

    # error_format_text
    @property
    def error_format_text(self) -> Optional[str]:
        return self._get_attr("errorFormatText", def_value=None)

    @error_format_text.setter
    def error_format_text(self, value: Optional[str]):
        self._set_attr("errorFormatText", value)

    # error_invalid_text
    @property
    def error_invalid_text(self) -> Optional[str]:
        return self._get_attr("errorInvalidText", def_value=None)

    @error_invalid_text.setter
    def error_invalid_text(self, value: Optional[str]):
        self._set_attr("errorInvalidText", value)

    # keyboard_type
    @property
    def keyboard_type(self) -> Optional[KeyboardType]:
        return self.__keyboard_type

    @keyboard_type.setter
    def keyboard_type(self, value: Optional[KeyboardType]):
        self.__keyboard_type = value
        self._set_enum_attr("keyboardType", value, KeyboardType)

    # date_picker_mode
    @property
    def date_picker_mode(self) -> Optional[DatePickerMode]:
        return self.__date_picker_mode

    @date_picker_mode.setter
    def date_picker_mode(self, value: Optional[DatePickerMode]):
        self.__date_picker_mode = value
        self._set_enum_attr("datePickerMode", value, DatePickerMode)

    # date_picker_entry_mode
    @property
    def date_picker_entry_mode(self) -> Optional[DatePickerEntryMode]:
        return self.__date_picker_entry_mode

    @date_picker_entry_mode.setter
    def date_picker_entry_mode(self, value: Optional[DatePickerEntryMode]):
        self.__date_picker_entry_mode = value
        self._set_enum_attr("datePickerEntryMode", value, DatePickerEntryMode)

    # switch_to_calendar_icon
    @property
    def switch_to_calendar_icon(self) -> Optional[str]:
        return self._get_attr("switchToCalendarEntryModeIcon")

    @switch_to_calendar_icon.setter
    def switch_to_calendar_icon(self, value: Optional[str]):
        self._set_attr("switchToCalendarEntryModeIcon", value)

    # switch_to_input_icon
    @property
    def switch_to_input_icon(self) -> Optional[str]:
        return self._get_attr("switchToInputEntryModeIcon")

    @switch_to_input_icon.setter
    def switch_to_input_icon(self, value: Optional[str]):
        self._set_attr("switchToInputEntryModeIcon", value)

    # on_change
    @property
    def on_change(self) -> OptionalEventCallable:
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler: OptionalEventCallable):
        self._add_event_handler("change", handler)

    # on_dismiss
    @property
    def on_dismiss(self) -> OptionalEventCallable:
        return self._get_event_handler("dismiss")

    @on_dismiss.setter
    def on_dismiss(self, handler: OptionalEventCallable):
        self._add_event_handler("dismiss", handler)

    # on_entry_mode_change
    @property
    def on_entry_mode_change(self):
        return self.__on_entry_mode_change

    @on_entry_mode_change.setter
    def on_entry_mode_change(
        self, handler: Optional[Callable[[DatePickerEntryModeChangeEvent], None]]
    ):
        self.__on_entry_mode_change.subscribe(handler)
