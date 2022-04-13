from typing import List, Optional

from beartype import beartype

from flet.constrained_control import ConstrainedControl
from flet.control import Control, CrossAxisAlignment, MainAxisAlignment
from flet.ref import Ref


class Column(ConstrainedControl):
    def __init__(
        self,
        controls: List[Control] = None,
        ref: Ref = None,
        width: float = None,
        height: float = None,
        expand: int = None,
        opacity: float = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # Column specific
        #
        alignment: MainAxisAlignment = None,
        horizontal_alignment: CrossAxisAlignment = None,
        spacing: float = None,
        tight: bool = None,
        wrap: bool = None,
        run_spacing: float = None,
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

        self.__controls = []
        self.controls = controls
        self.horizontal_alignment = horizontal_alignment
        self.alignment = alignment
        self.spacing = spacing
        self.tight = tight
        self.wrap = wrap
        self.run_spacing = run_spacing

    def _get_control_name(self):
        return "column"

    # tight
    @property
    def tight(self):
        return self._get_attr("tight", data_type="bool", def_value=False)

    @tight.setter
    @beartype
    def tight(self, value: Optional[bool]):
        self._set_attr("tight", value)

    # alignment
    @property
    def alignment(self):
        return self._get_attr("alignment")

    @alignment.setter
    @beartype
    def alignment(self, value: MainAxisAlignment):
        self._set_attr("alignment", value)

    # horizontal_alignment
    @property
    def horizontal_alignment(self):
        return self._get_attr("horizontalAlignment")

    @horizontal_alignment.setter
    @beartype
    def horizontal_alignment(self, value: CrossAxisAlignment):
        self._set_attr("horizontalAlignment", value)

    # spacing
    @property
    def spacing(self):
        return self._get_attr("spacing")

    @spacing.setter
    @beartype
    def spacing(self, value: Optional[float]):
        self._set_attr("spacing", value)

    # wrap
    @property
    def wrap(self):
        return self._get_attr("wrap", data_type="bool", def_value=False)

    @wrap.setter
    @beartype
    def wrap(self, value: Optional[bool]):
        self._set_attr("wrap", value)

    # run_spacing
    @property
    def run_spacing(self):
        return self._get_attr("runSpacing")

    @run_spacing.setter
    @beartype
    def run_spacing(self, value: Optional[float]):
        self._set_attr("runSpacing", value)

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value):
        self.__controls = value or []

    def _get_children(self):
        return self.__controls
