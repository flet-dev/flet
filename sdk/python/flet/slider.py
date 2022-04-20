from typing import Optional

from beartype import beartype

from flet.constrained_control import ConstrainedControl
from flet.control import Control, OptionalNumber
from flet.ref import Ref


class Slider(ConstrainedControl):
    def __init__(
        self,
        ref: Ref = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        expand: int = None,
        opacity: OptionalNumber = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # Specific
        #
        value: OptionalNumber = None,
        label: str = None,
        min: OptionalNumber = None,
        max: OptionalNumber = None,
        divisions: int = None,
        on_change=None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            width=width,
            height=height,
            expand=expand,
            opacity=opacity,
            visible=visible,
            disabled=disabled,
            data=data,
        )
        self.value = value
        self.label = label
        self.min = min
        self.max = max
        self.divisions = divisions
        self.on_change = on_change

    def _get_control_name(self):
        return "slider"

    # value
    @property
    def value(self):
        return self._get_attr("value", data_type="float")

    @value.setter
    @beartype
    def value(self, value: OptionalNumber):
        self._set_attr("value", value)

    # label
    @property
    def label(self):
        return self._get_attr("label")

    @label.setter
    def label(self, value):
        self._set_attr("label", value)

    # min
    @property
    def min(self):
        return self._get_attr("min")

    @min.setter
    @beartype
    def min(self, value: OptionalNumber):
        self._set_attr("min", value)

    # max
    @property
    def max(self):
        return self._get_attr("max")

    @max.setter
    @beartype
    def max(self, value: OptionalNumber):
        self._set_attr("max", value)

    # step
    @property
    def divisions(self):
        return self._get_attr("divisions")

    @divisions.setter
    @beartype
    def divisions(self, value: Optional[int]):
        self._set_attr("divisions", value)

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)
