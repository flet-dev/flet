from typing import List, Optional, Union

from beartype import beartype

from flet import padding
from flet.constrained_control import ConstrainedControl
from flet.control import Control, OptionalNumber, PaddingValue
from flet.ref import Ref


class GridView(ConstrainedControl):
    def __init__(
        self,
        controls: List[Control] = None,
        ref: Ref = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        expand: Union[bool, int] = None,
        opacity: OptionalNumber = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # Specific
        #
        horizontal: bool = None,
        runs_count: int = None,
        max_extent: int = None,
        spacing: OptionalNumber = None,
        run_spacing: OptionalNumber = None,
        child_aspect_ratio: OptionalNumber = None,
        padding: PaddingValue = None,
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
        self.horizontal = horizontal
        self.runs_count = runs_count
        self.max_extent = max_extent
        self.spacing = spacing
        self.run_spacing = run_spacing
        self.child_aspect_ratio = child_aspect_ratio
        self.padding = padding

    def _get_control_name(self):
        return "gridview"

    def _get_children(self):
        return self.__controls

    def clean(self):
        Control.clean(self)
        self.__controls.clear()

    # horizontal
    @property
    def horizontal(self):
        return self._get_attr("horizontal")

    @horizontal.setter
    @beartype
    def horizontal(self, value: Optional[bool]):
        self._set_attr("horizontal", value)

    # runs_count
    @property
    def runs_count(self):
        return self._get_attr("runsCount")

    @runs_count.setter
    @beartype
    def runs_count(self, value: Optional[int]):
        self._set_attr("runsCount", value)

    # max_extent
    @property
    def max_extent(self):
        return self._get_attr("maxExtent")

    @max_extent.setter
    @beartype
    def max_extent(self, value: OptionalNumber):
        self._set_attr("maxExtent", value)

    # spacing
    @property
    def spacing(self):
        return self._get_attr("spacing")

    @spacing.setter
    @beartype
    def spacing(self, value: OptionalNumber):
        self._set_attr("spacing", value)

    # run_spacing
    @property
    def run_spacing(self):
        return self._get_attr("runSpacing")

    @run_spacing.setter
    @beartype
    def run_spacing(self, value: OptionalNumber):
        self._set_attr("runSpacing", value)

    # child_aspect_ratio
    @property
    def child_aspect_ratio(self):
        return self._get_attr("childAspectRatio")

    @child_aspect_ratio.setter
    @beartype
    def child_aspect_ratio(self, value: OptionalNumber):
        self._set_attr("childAspectRatio", value)

    # padding
    @property
    def padding(self):
        return self.__padding

    @padding.setter
    @beartype
    def padding(self, value: PaddingValue):
        self.__padding = value
        if value and isinstance(value, (int, float)):
            value = padding.all(value)
        self._set_attr_json("padding", value)

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value):
        self.__controls = value or []
