from typing import Optional

from beartype import beartype

from flet.control import Control, OptionalNumber
from flet.ref import Ref


class RadioGroup(Control):
    def __init__(
        self,
        content: Control = None,
        #
        # Control
        #
        ref: Ref = None,
        opacity: OptionalNumber = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # Specific
        #
        value: str = None,
        on_change=None,
    ):

        Control.__init__(
            self,
            ref=ref,
            opacity=opacity,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.content = content
        self.value = value
        self.on_change = on_change

    def _get_control_name(self):
        return "radiogroup"

    def _get_children(self):
        if self.__content == None:
            return []
        self.__content._set_attr_internal("n", "content")
        return [self.__content]

    # value
    @property
    def value(self):
        return self._get_attr("value")

    @value.setter
    def value(self, value):
        self._set_attr("value", value)

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    @beartype
    def content(self, value: Optional[Control]):
        self.__content = value

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)
