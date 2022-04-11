from typing import List, Optional

from beartype import beartype

from flet.control import Control, ScrollDirection
from flet.ref import Ref


class GridView(Control):
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
        cross_axis_count: int = None,
        main_axis_spacing: float = None,
        cross_axis_spacing: float = None,
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
            cross_axis_count=cross_axis_count,
            main_axis_spacing=main_axis_spacing,
            cross_axis_spacing=cross_axis_spacing,
        )

        self.__controls = []
        if controls != None:
            for control in controls:
                self.__controls.append(control)

    def _get_control_name(self):
        return "gridview"

    # scroll_direction
    @property
    def scroll_direction(self):
        return self._get_attr("scrollDirection")

    @scroll_direction.setter
    @beartype
    def scroll_direction(self, value: ScrollDirection):
        self._set_attr("scrollDirection", value)

    # cross_axis_count
    @property
    def cross_axis_count(self):
        return self._get_attr("crossAxisCount")

    @cross_axis_count.setter
    @beartype
    def cross_axis_count(self, value: Optional[int]):
        self._set_attr("crossAxisCount", value)

    # main_axis_spacing
    @property
    def main_axis_spacing(self):
        return self._get_attr("mainAxisSpacing")

    @main_axis_spacing.setter
    @beartype
    def main_axis_spacing(self, value: Optional[float]):
        self._set_attr("mainAxisSpacing", value)

    # cross_axis_spacing
    @property
    def cross_axis_spacing(self):
        return self._get_attr("crossAxisSpacing")

    @cross_axis_spacing.setter
    @beartype
    def cross_axis_spacing(self, value: Optional[float]):
        self._set_attr("crossAxisSpacing", value)

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value):
        self.__controls = value

    def _get_children(self):
        return self.__controls
