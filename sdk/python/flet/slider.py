from typing import Optional, Union

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
        expand: Union[bool, int] = None,
        opacity: OptionalNumber = None,
        tooltip: str = None,
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
        autofocus: bool = None,
        on_change=None,
        on_focus=None,
        on_blur=None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            width=width,
            height=height,
            expand=expand,
            opacity=opacity,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )
        self.value = value
        self.label = label
        self.min = min
        self.max = max
        self.divisions = divisions
        self.autofocus = autofocus
        self.on_change = on_change
        self.on_focus = on_focus
        self.on_blur = on_blur

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

    # autofocus
    @property
    def autofocus(self):
        return self._get_attr("autofocus", data_type="bool", def_value=False)

    @autofocus.setter
    @beartype
    def autofocus(self, value: Optional[bool]):
        self._set_attr("autofocus", value)

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)

    # on_focus
    @property
    def on_focus(self):
        return self._get_event_handler("focus")

    @on_focus.setter
    def on_focus(self, handler):
        self._add_event_handler("focus", handler)

    # on_blur
    @property
    def on_blur(self):
        return self._get_event_handler("blur")

    @on_blur.setter
    def on_blur(self, handler):
        self._add_event_handler("blur", handler)
