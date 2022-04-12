from typing import List

from beartype import beartype

from flet.control import Control, ScrollDirection
from flet.ref import Ref


class ListView(Control):
    def __init__(
        self,
        controls: List[Control] = None,
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
        scroll_direction: ScrollDirection = None,
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
            scroll_direction=scroll_direction,
        )

        self.__controls = []
        if controls != None:
            for control in controls:
                self.__controls.append(control)

    def _get_control_name(self):
        return "listview"

    # scroll_direction
    @property
    def scroll_direction(self):
        return self._get_attr("scrollDirection")

    @scroll_direction.setter
    @beartype
    def scroll_direction(self, value: ScrollDirection):
        self._set_attr("scrollDirection", value)

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value):
        self.__controls = value

    def _get_children(self):
        return self.__controls
