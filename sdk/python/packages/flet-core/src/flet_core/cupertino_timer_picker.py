from enum import Enum
from typing import Any, Optional, Union

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class CupertinoTimerPickerMode(Enum):
    HOUR_MINUTE = "hm"
    HOUR_MINUTE_SECONDS = "hms"
    MINUTE_SECONDS = "ms"


class CupertinoTimerPicker(Control):
    """
    A countdown timer picker in iOS style.

    It can show a countdown duration with hour, minute and second spinners. The duration is bound between 0 and 23 hours 59 minutes 59 seconds.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinotimerpicker
    """

    def __init__(
        self,
        value: Optional[int] = None,
        second_interval: OptionalNumber = None,
        minute_interval: OptionalNumber = None,
        mode: Optional[CupertinoTimerPickerMode] = None,
        bgcolor: Optional[str] = None,
        modal: bool = False,
        open: bool = False,
        on_change=None,
        on_dismiss=None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )
        self.value = value
        self.mode = mode
        self.bgcolor = bgcolor
        self.on_change = on_change
        self.second_interval = second_interval
        self.minute_interval = minute_interval
        self.modal = modal
        self.open = open
        self.on_dismiss = on_dismiss

    def _get_control_name(self):
        return "cupertinotimerpicker"

    # value
    @property
    def value(self) -> Optional[int]:
        return self._get_attr("value", data_type="int", def_value=0)

    @value.setter
    def value(self, value: Optional[int]):
        self._set_attr("value", value)

    # bgcolor
    @property
    def bgcolor(self) -> Optional[str]:
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value: Optional[str]):
        self._set_attr("bgcolor", value)

    # second_interval
    @property
    def second_interval(self) -> OptionalNumber:
        return self._get_attr("secondInterval", data_type="int", def_value=1)

    @second_interval.setter
    def second_interval(self, value: OptionalNumber):
        self._set_attr("secondInterval", value)

    # minute_interval
    @property
    def minute_interval(self) -> OptionalNumber:
        return self._get_attr("minuteInterval", data_type="int", def_value=1)

    @minute_interval.setter
    def minute_interval(self, value: OptionalNumber):
        self._set_attr("minuteInterval", value)

    # mode
    @property
    def mode(self) -> Optional[CupertinoTimerPickerMode]:
        return self.__mode

    @mode.setter
    def mode(self, value: Optional[CupertinoTimerPickerMode]):
        self.__mode = value
        self._set_attr("mode", value.value if value is not None else None)

    # open
    @property
    def open(self) -> Optional[bool]:
        return self._get_attr("open", data_type="bool", def_value=False)

    @open.setter
    def open(self, value: Optional[bool]):
        self._set_attr("open", value)

    # modal
    @property
    def modal(self) -> Optional[bool]:
        return self._get_attr("modal", data_type="bool", def_value=False)

    @modal.setter
    def modal(self, value: Optional[bool]):
        self._set_attr("modal", value)

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
