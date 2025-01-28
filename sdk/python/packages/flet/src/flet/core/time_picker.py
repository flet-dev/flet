from datetime import datetime, time
from enum import Enum
from typing import Any, Optional, Union

from flet.core.control import Control, OptionalNumber
from flet.core.control_event import ControlEvent
from flet.core.event_handler import EventHandler
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    ColorEnums,
    ColorValue,
    OptionalControlEventCallable,
    OptionalEventCallable,
    Orientation,
    ResponsiveNumber,
)


class TimePickerEntryMode(Enum):
    DIAL = "dial"
    INPUT = "input"
    DIAL_ONLY = "dialOnly"
    INPUT_ONLY = "inputOnly"


class TimePickerEntryModeChangeEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        self.entry_mode: Optional[TimePickerEntryMode] = TimePickerEntryMode(e.data)


class TimePicker(Control):
    """
    A Material-style time picker dialog.

    It is added to [`page.overlay`](page#overlay) and can be opened by setting `open=True` or by calling `Page.open()` method.

    Depending on the `time_picker_entry_mode`, it will show either a Dial or an Input (hour and minute text fields) for picking a time.

    Example:
    ```
    import flet as ft


    def main(page: ft.Page):
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        def handle_change(e):
            page.add(ft.Text(f"TimePicker change: {time_picker.value}"))

        def handle_dismissal(e):
            page.add(ft.Text(f"TimePicker dismissed: {time_picker.value}"))

        def handle_entry_mode_change(e):
            page.add(ft.Text(f"TimePicker Entry mode changed to {e.entry_mode}"))

        time_picker = ft.TimePicker(
            confirm_text="Confirm",
            error_invalid_text="Time out of range",
            help_text="Pick your time slot",
            on_change=handle_change,
            on_dismiss=handle_dismissal,
            on_entry_mode_change=handle_entry_mode_change,
        )

        page.add(
            ft.ElevatedButton(
                "Pick time",
                icon=ft.icons.TIME_TO_LEAVE,
                on_click=lambda _: page.open(time_picker),
            )
        )


    ft.app(main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/time_picker
    """

    def __init__(
        self,
        value: Optional[time] = datetime.now().time(),
        open: bool = False,
        time_picker_entry_mode: Optional[TimePickerEntryMode] = None,
        hour_label_text: Optional[str] = None,
        minute_label_text: Optional[str] = None,
        help_text: Optional[str] = None,
        cancel_text: Optional[str] = None,
        confirm_text: Optional[str] = None,
        error_invalid_text: Optional[str] = None,
        orientation: Optional[Orientation] = None,
        barrier_color: Optional[ColorValue] = None,
        on_change: OptionalControlEventCallable = None,
        on_dismiss: OptionalControlEventCallable = None,
        on_entry_mode_change: OptionalEventCallable[
            TimePickerEntryModeChangeEvent
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
            lambda e: TimePickerEntryModeChangeEvent(e)
        )
        self._add_event_handler(
            "entryModeChange", self.__on_entry_mode_change.get_handler()
        )

        self.value = value
        self.help_text = help_text
        self.cancel_text = cancel_text
        self.confirm_text = confirm_text
        self.error_invalid_text = error_invalid_text
        self.hour_label_text = hour_label_text
        self.minute_label_text = minute_label_text
        self.time_picker_entry_mode = time_picker_entry_mode
        self.orientation = orientation
        self.on_change = on_change
        self.on_dismiss = on_dismiss
        self.open = open
        self.on_entry_mode_change = on_entry_mode_change
        self.barrier_color = barrier_color

    def _get_control_name(self):
        return "timepicker"

    # open
    @property
    def open(self) -> bool:
        return self._get_attr("open", data_type="bool", def_value=False)

    @open.setter
    def open(self, value: Optional[bool]):
        self._set_attr("open", value)

    # value
    @property
    def value(self) -> time:
        v = self._get_attr("value")  # format HH:MM
        return time(*map(int, v.split(":")))

    @value.setter
    def value(self, value: time):
        self._set_attr("value", value.strftime("%H:%M"))

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
        self._set_enum_attr("timePickerEntryMode", value, TimePickerEntryMode)

    # orientation
    @property
    def orientation(self) -> Optional[Orientation]:
        return self.__orientation

    @orientation.setter
    def orientation(self, value: Optional[Orientation]):
        self.__orientation = value
        self._set_enum_attr("orientation", value, Orientation)

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
    ) -> OptionalEventCallable[TimePickerEntryModeChangeEvent]:
        return self.__on_entry_mode_change.handler

    @on_entry_mode_change.setter
    def on_entry_mode_change(
        self, handler: OptionalEventCallable[TimePickerEntryModeChangeEvent]
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
