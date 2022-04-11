from typing import Optional

from beartype import beartype

from flet.control import Control


class GridView(Control):
    def __init__(
        self,
        controls=None,
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

        self.__controls = []
        if controls != None:
            for control in controls:
                self.__controls.append(control)

    def _get_control_name(self):
        return "gridview"

    def clean(self):
        Control.clean(self)
        self.__controls.clear()

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value):
        self.__controls = value

    def _get_children(self):
        return self.__controls
