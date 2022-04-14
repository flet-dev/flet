from typing import List, Optional

from beartype import beartype

from flet.constrained_control import ConstrainedControl
from flet.control import Control, OptionalNumber, ScrollDirection
from flet.ref import Ref


class GridView(ConstrainedControl):
    def __init__(
        self,
        controls: List[Control] = None,
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
        scroll_direction: ScrollDirection = None,
        cross_axis_count: int = None,
        main_axis_spacing: OptionalNumber = None,
        cross_axis_spacing: OptionalNumber = None,
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

        self.__controls: List[Control] = []
        self.controls = controls
        self.scroll_direction = scroll_direction
        self.cross_axis_count = cross_axis_count
        self.main_axis_spacing = main_axis_spacing
        self.cross_axis_spacing = cross_axis_spacing

    def _get_control_name(self):
        return "gridview"

    def _get_children(self):
        return self.__controls

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
    def main_axis_spacing(self, value: OptionalNumber):
        self._set_attr("mainAxisSpacing", value)

    # cross_axis_spacing
    @property
    def cross_axis_spacing(self):
        return self._get_attr("crossAxisSpacing")

    @cross_axis_spacing.setter
    @beartype
    def cross_axis_spacing(self, value: OptionalNumber):
        self._set_attr("crossAxisSpacing", value)

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value):
        self.__controls = value or []
