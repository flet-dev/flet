from typing import Optional

from beartype import beartype

from flet.control import Control
from flet.ref import Ref

try:
    from typing import Literal
except:
    from typing_extensions import Literal


LabelPosition = Literal[None, "right", "left"]


class Checkbox(Control):
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
        label: str = None,
        label_position: LabelPosition = None,
        value: bool = None,
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
        self.label = label
        self.label_position = label_position
        self.on_change = on_change

    def _get_control_name(self):
        return "checkbox"

    # value
    @property
    def value(self):
        return self._get_attr("value", data_type="bool", def_value=False)

    @value.setter
    @beartype
    def value(self, value: Optional[bool]):
        self._set_attr("value", value)

    # label
    @property
    def label(self):
        return self._get_attr("label")

    @label.setter
    def label(self, value):
        self._set_attr("label", value)

    # label_position
    @property
    def label_position(self):
        return self._get_attr("labelPosition")

    @label_position.setter
    @beartype
    def label_position(self, value: LabelPosition):
        self._set_attr("labelPosition", value)

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)
