from typing import Optional

from beartype import beartype

from flet.control import Control

try:
    from typing import Literal
except:
    from typing_extensions import Literal


BoxSide = Literal[None, "start", "end"]


class Checkbox(Control):
    def __init__(
        self,
        label=None,
        id=None,
        ref=None,
        value=None,
        value_field=None,
        box_side: BoxSide = None,
        focused=None,
        data=None,
        width=None,
        height=None,
        padding=None,
        margin=None,
        on_change=None,
        visible=None,
        disabled=None,
    ):
        Control.__init__(
            self,
            id=id,
            ref=ref,
            width=width,
            height=height,
            padding=padding,
            margin=margin,
            visible=visible,
            disabled=disabled,
            data=data,
        )
        self.value = value
        self.value_field = value_field
        self.label = label
        self.box_side = box_side
        self.focused = focused
        self.on_change = on_change

    def _get_control_name(self):
        return "checkbox"

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)

    # value
    @property
    def value(self):
        return self._get_attr("value", data_type="bool", def_value=False)

    @value.setter
    @beartype
    def value(self, value: Optional[bool]):
        self._set_attr("value", value)

    # value_field
    @property
    def value_field(self):
        return self._get_attr("value")

    @value_field.setter
    def value_field(self, value):
        if value != None:
            self._set_attr("value", f"{{{value}}}")

    # label
    @property
    def label(self):
        return self._get_attr("label")

    @label.setter
    def label(self, value):
        self._set_attr("label", value)

    # box_side
    @property
    def box_side(self):
        return self._get_attr("boxSide")

    @box_side.setter
    @beartype
    def box_side(self, value: BoxSide):
        self._set_attr("boxSide", value)

    # focused
    @property
    def focused(self):
        return self._get_attr("focused", data_type="bool", def_value=False)

    @focused.setter
    @beartype
    def focused(self, value: Optional[bool]):
        self._set_attr("focused", value)
