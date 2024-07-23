from enum import Enum
from typing import Any, Optional, Union

from flet_core.alignment import Alignment
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    OptionalEventCallable,
)


class CupertinoTimerPickerMode(Enum):
    HOUR_MINUTE = "hm"
    HOUR_MINUTE_SECONDS = "hms"
    MINUTE_SECONDS = "ms"


class CupertinoTimerPicker(ConstrainedControl):
    """
    A countdown timer picker in iOS style.

    It can show a countdown duration with hour, minute and second spinners. The duration is bound between 0 and 23 hours 59 minutes 59 seconds.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinotimerpicker
    """

    def __init__(
        self,
        value: Optional[int] = None,
        alignment: Optional[Alignment] = None,
        second_interval: OptionalNumber = None,
        minute_interval: OptionalNumber = None,
        mode: Optional[CupertinoTimerPickerMode] = None,
        bgcolor: Optional[str] = None,
        item_extent: OptionalNumber = None,
        on_change: OptionalEventCallable = None,
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
        on_animation_end: OptionalEventCallable = None,
        tooltip: Optional[str] = None,
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
        self.alignment = alignment
        self.mode = mode
        self.bgcolor = bgcolor
        self.on_change = on_change
        self.second_interval = second_interval
        self.minute_interval = minute_interval
        self.item_extent = item_extent

    def _get_control_name(self):
        return "cupertinotimerpicker"

    def before_update(self):
        super().before_update()
        self._set_attr_json("alignment", self.__alignment)

    # value
    @property
    def value(self) -> Optional[int]:
        return self._get_attr("value", data_type="int", def_value=0)

    @value.setter
    def value(self, value: Optional[int]):
        self._set_attr("value", value)

    # alignment
    @property
    def alignment(self) -> Optional[Alignment]:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value

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

    # item_extent
    @property
    def item_extent(self) -> OptionalNumber:
        return self._get_attr("itemExtent", data_type="float", def_value=32.0)

    @item_extent.setter
    def item_extent(self, value: OptionalNumber):
        self._set_attr("itemExtent", value)

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
        self._set_enum_attr("mode", value, CupertinoTimerPickerMode)

    # on_change
    @property
    def on_change(self) -> OptionalEventCallable:
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler: OptionalEventCallable):
        self._add_event_handler("change", handler)
