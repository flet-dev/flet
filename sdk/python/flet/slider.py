from typing import Optional, Union

from beartype import beartype

from flet.control import Control
from flet.ref import Ref


class Slider(Control):
    def __init__(
        self,
        id: str = None,
        ref: Ref = None,
        width: float = None,
        height: float = None,
        padding: float = None,
        margin: float = None,
        expand: int = None,
        opacity: float = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # Specific
        #
        value: float = None,
        min: float = None,
        max: float = None,
        divisions: int = None,
        on_change=None,
    ):
        Control.__init__(
            self,
            id=id,
            ref=ref,
            width=width,
            height=height,
            padding=padding,
            margin=margin,
            expand=expand,
            opacity=opacity,
            visible=visible,
            disabled=disabled,
            data=data,
        )
        self.value = value
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
    def value(self, value: Optional[float]):
        self._set_attr("value", value)

    # min
    @property
    def min(self):
        return self._get_attr("min")

    @min.setter
    @beartype
    def min(self, value: Optional[float]):
        self._set_attr("min", value)

    # max
    @property
    def max(self):
        return self._get_attr("max")

    @max.setter
    @beartype
    def max(self, value: Optional[float]):
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
