from datetime import time
from enum import Enum
from typing import Any, Optional, Union

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.text_style import TextStyle
from flet_core.textfield import KeyboardType, KeyboardTypeString
from flet_core.types import ResponsiveNumber


class TimePickerEntryMode(Enum):
    DIAL = "dial"
    INPUT = "input"
    DIAL_ONLY = "dialOnly"
    INPUT_ONLY = "inputOnly"


class TimePicker(Control):
    """
    A Material-style time picker dialog.

    It is added to [`page.overlay`](page#overlay) and called using its `pick_time()` method.

    Depending on the `time_picker_mode`, it will show either a Dial or an Input (TextField) for picking a time.

            Example:
            ```
            ```

            -----

            Online docs: https://flet.dev/docs/controls/time_picker
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
        open: bool = False,
        value: Optional[time] = None,
        text_style: Optional[TextStyle] = None,
        keyboard_type: Optional[KeyboardType] = None,
        time_picker_entry_mode: Optional[TimePickerEntryMode] = None,
        hour_label_text: Optional[str] = None,
        minute_label_text: Optional[str] = None,
        help_text: Optional[str] = None,
        cancel_text: Optional[str] = None,
        confirm_text: Optional[str] = None,
        error_format_text: Optional[str] = None,
        error_invalid_text: Optional[str] = None,
        field_hint_text: Optional[str] = None,
        field_label_text: Optional[str] = None,
        switch_to_calendar_icon: Optional[str] = None,
        switch_to_input_icon: Optional[str] = None,
        on_change=None,
        on_dismiss=None,
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
        self.keyboard_type = keyboard_type
        self.help_text = help_text
        self.cancel_text = cancel_text
        self.confirm_text = confirm_text
        self.error_format_text = error_format_text
        self.error_invalid_text = error_invalid_text
        self.hour_label_text = hour_label_text
        self.minute_label_text = minute_label_text
        self.time_picker_entry_mode = time_picker_entry_mode
        self.text_style = text_style
        self.field_hint_text = field_hint_text
        self.field_label_text = field_label_text
        self.switch_to_calendar_icon = switch_to_calendar_icon
        self.switch_to_input_icon = switch_to_input_icon
        self.on_change = on_change
        self.on_dismiss = on_dismiss
        self.open = open

    def _get_control_name(self):
        return "timepicker"

    def _before_build_command(self):
        super()._before_build_command()

    def pick_time(self):
        self.open = True
        self.update()

    async def pick_time_async(self):
        self.open = True
        await self.update_async()

    # open
    @property
    def open(self) -> Optional[bool]:
        return self._get_attr("open", data_type="bool", def_value=False)

    @open.setter
    def open(self, value: Optional[bool]):
        self._set_attr("open", value)

    # value
    @property
    def value(self) -> Optional[time]:
        value_string = self._get_attr(
            "value", def_value=None
        )  # value_string in comes in format 'HH:MM'
        splitted = value_string.split(":")
        return (
            time(hour=int(splitted[0]), minute=int(splitted[1]))
            if value_string
            else None
        )

    @value.setter
    def value(self, value: Optional[Union[time, str]]):
        if isinstance(value, (time)):
            value = value.strftime("%H:%M")
        self._set_attr("value", value)

    # hour_label_text
    @property
    def hour_label_text(self) -> Optional[str]:
        return self._get_attr("hourLabelText", def_value=None)

    @hour_label_text.setter
    def hour_label_text(self, value: Optional[str]):
        self._set_attr("hourLabelText", value)

    # minute_label_text
    @property
    def minute_label_text(self) -> Optional[str]:
        return self._get_attr("minuteLabelText", def_value=None)

    @minute_label_text.setter
    def minute_label_text(self, value: Optional[str]):
        self._set_attr("minuteLabelText", value)

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

    # time_picker_entry_mode
    @property
    def time_picker_entry_mode(self) -> Optional[TimePickerEntryMode]:
        return self.__time_picker_entry_mode

    @time_picker_entry_mode.setter
    def time_picker_entry_mode(self, value: Optional[TimePickerEntryMode]):
        self.__time_picker_entry_mode = value
        self._set_attr(
            "timePickerEntryMode", value.value if value is not None else None
        )

    # switch_to_calendar_icon
    @property
    def switch_to_calendar_icon(self):
        return self._get_attr("switchToCalendarEntryModeIcon")

    @switch_to_calendar_icon.setter
    def switch_to_calendar_icon(self, value):
        self._set_attr("switchToCalendarEntryModeIcon", value)

    # switch_to_input_icon
    @property
    def switch_to_input_icon(self):
        return self._get_attr("switchToInputEntryModeIcon")

    @switch_to_input_icon.setter
    def switch_to_input_icon(self, value):
        self._set_attr("switchToInputEntryModeIcon", value)

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
