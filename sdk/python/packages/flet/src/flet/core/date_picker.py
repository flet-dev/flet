from datetime import datetime
from enum import Enum
from typing import Any, Optional, Union

from flet.core.control import Control, OptionalNumber
from flet.core.control_event import ControlEvent
from flet.core.event_handler import EventHandler
from flet.core.ref import Ref
from flet.core.textfield import KeyboardType
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    ColorEnums,
    ColorValue,
    DateTimeValue,
    IconEnums,
    IconValue,
    OptionalControlEventCallable,
    OptionalEventCallable,
    ResponsiveNumber,
)

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
        value: Optional[DateTimeValue] = None,
        first_date: DateTimeValue = datetime(year=1900, month=1, day=1),
        last_date: DateTimeValue = datetime(year=2050, month=1, day=1),
        current_date: DateTimeValue = datetime.now(),
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
        switch_to_calendar_icon: Optional[IconValue] = None,
        switch_to_input_icon: Optional[IconValue] = None,
        barrier_color: Optional[ColorValue] = None,
        on_change: OptionalControlEventCallable = None,
        on_dismiss: OptionalControlEventCallable = None,
        on_entry_mode_change: OptionalEventCallable[
            "DatePickerEntryModeChangeEvent"
        ] = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        expand: Optional[Union[bool, int]] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        tooltip: Optional[TooltipValue] = None,
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
            lambda e: DatePickerEntryModeChangeEvent(e)
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
        self.barrier_color = barrier_color

    def _get_control_name(self):
        return "datepicker"

    # open
    @property
    def open(self) -> bool:
        return self._get_attr("open", data_type="bool", def_value=False)

    @open.setter
    def open(self, value: Optional[bool]):
        self._set_attr("open", value)

    # value
    @property
    def value(self) -> Optional[DateTimeValue]:
        v = self._get_attr("value")
        return datetime.fromisoformat(v) if v else None

    @value.setter
    def value(self, value: Optional[DateTimeValue]):
        self.__value = value
        self._set_attr("value", value if value is None else value.isoformat())

    @property
    def first_date(self) -> DateTimeValue:
        return self.__first_date

    @first_date.setter
    def first_date(self, value: DateTimeValue):
        self.__first_date = value
        self._set_attr("firstDate", value.isoformat())

    # last_date
    @property
    def last_date(self) -> DateTimeValue:
        return self.__last_date

    @last_date.setter
    def last_date(self, value: DateTimeValue):
        self.__last_date = value
        self._set_attr("lastDate", value.isoformat())

    # current_date
    @property
    def current_date(self) -> DateTimeValue:
        return self.__current_date

    @current_date.setter
    def current_date(self, value: DateTimeValue):
        self.__current_date = value
        self._set_attr("currentDate", value.isoformat())

    # field_hint_text
    @property
    def field_hint_text(self) -> Optional[str]:
        return self._get_attr("fieldHintText")

    @field_hint_text.setter
    def field_hint_text(self, value: Optional[str]):
        self._set_attr("fieldHintText", value)

    # field_label_text
    @property
    def field_label_text(self) -> Optional[str]:
        return self._get_attr("fieldLabelText")

    @field_label_text.setter
    def field_label_text(self, value: Optional[str]):
        self._set_attr("fieldLabelText", value)

    # help_text
    @property
    def help_text(self) -> Optional[str]:
        return self._get_attr("helpText")

    @help_text.setter
    def help_text(self, value: Optional[str]):
        self._set_attr("helpText", value)

    # cancel_text
    @property
    def cancel_text(self) -> Optional[str]:
        return self._get_attr("cancelText")

    @cancel_text.setter
    def cancel_text(self, value: Optional[str]):
        self._set_attr("cancelText", value)

    # confirm_text
    @property
    def confirm_text(self) -> Optional[str]:
        return self._get_attr("confirmText")

    @confirm_text.setter
    def confirm_text(self, value: Optional[str]):
        self._set_attr("confirmText", value)

    # error_format_text
    @property
    def error_format_text(self) -> Optional[str]:
        return self._get_attr("errorFormatText")

    @error_format_text.setter
    def error_format_text(self, value: Optional[str]):
        self._set_attr("errorFormatText", value)

    # error_invalid_text
    @property
    def error_invalid_text(self) -> Optional[str]:
        return self._get_attr("errorInvalidText")

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
    def switch_to_calendar_icon(self) -> Optional[IconValue]:
        return self.__switch_to_calendar_icon

    @switch_to_calendar_icon.setter
    def switch_to_calendar_icon(self, value: Optional[IconValue]):
        self.__switch_to_calendar_icon = value
        self._set_enum_attr("switchToCalendarEntryModeIcon", value, IconEnums)

    # switch_to_input_icon
    @property
    def switch_to_input_icon(self) -> Optional[IconValue]:
        return self.__switch_to_input_icon

    @switch_to_input_icon.setter
    def switch_to_input_icon(self, value: Optional[IconValue]):
        self.__switch_to_input_icon = value
        self._set_enum_attr("switchToInputEntryModeIcon", value, IconEnums)

    # on_change
    @property
    def on_change(self) -> OptionalControlEventCallable:
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler: OptionalControlEventCallable):
        self._add_event_handler("change", handler)

    # on_dismiss
    @property
    def on_dismiss(self) -> OptionalControlEventCallable:
        return self._get_event_handler("dismiss")

    @on_dismiss.setter
    def on_dismiss(self, handler: OptionalControlEventCallable):
        self._add_event_handler("dismiss", handler)

    # on_entry_mode_change
    @property
    def on_entry_mode_change(
        self,
    ) -> OptionalEventCallable[DatePickerEntryModeChangeEvent]:
        return self.__on_entry_mode_change.handler

    @on_entry_mode_change.setter
    def on_entry_mode_change(
        self, handler: OptionalEventCallable[DatePickerEntryModeChangeEvent]
    ):
        self.__on_entry_mode_change.handler = handler

    # barrier_color
    @property
    def barrier_color(self) -> Optional[ColorValue]:
        return self.__barrier_color

    @barrier_color.setter
    def barrier_color(self, value: Optional[ColorValue]):
        self.__barrier_color = value
        self._set_enum_attr("barrierColor", value, ColorEnums)
