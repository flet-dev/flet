from typing import Optional

from beartype import beartype

from flet.control import Control


class Expanded(Control):
    def __init__(
        self,
        control=None,
        id=None,
        ref=None,
        visible=None,
        disabled=None,
        data=None,
    ):
        Control.__init__(
            self,
            id=id,
            ref=ref,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.control = control

    def _get_control_name(self):
        return "expanded"

    # control
    @property
    def control(self):
        return self.__control

    @control.setter
    def control(self, value):
        self.__control = value

    def _get_children(self):
        return [self.__control]
