from typing import List, Optional, Union

from beartype import beartype

from flet.constrained_control import ConstrainedControl
from flet.control import (
    Control,
    CrossAxisAlignment,
    MainAxisAlignment,
    OptionalNumber,
    ScrollMode,
)
from flet.ref import Ref


class Row(ConstrainedControl):
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
        # Row specific
        #
        alignment: MainAxisAlignment = None,
        vertical_alignment: CrossAxisAlignment = None,
        spacing: OptionalNumber = None,
        tight: bool = None,
        wrap: bool = None,
        run_spacing: OptionalNumber = None,
        scroll: ScrollMode = None,
        auto_scroll: bool = None,
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
        self.alignment = alignment
        self.vertical_alignment = vertical_alignment
        self.spacing = spacing
        self.tight = tight
        self.wrap = wrap
        self.run_spacing = run_spacing
        self.__scroll = False
        self.scroll = scroll
        self.auto_scroll = auto_scroll

    def _get_control_name(self):
        return "row"

    def _get_children(self):
        return self.__controls

    def clean(self):
        Control.clean(self)
        self.__controls.clear()

    # tight
    @property
    def tight(self):
        return self._get_attr("tight", data_type="bool", def_value=False)

    @tight.setter
    @beartype
    def tight(self, value: Optional[bool]):
        self._set_attr("tight", value)

    # horizontal_alignment
    @property
    def alignment(self):
        return self._get_attr("alignment")

    @alignment.setter
    @beartype
    def alignment(self, value: MainAxisAlignment):
        self._set_attr("alignment", value)

    # vertical_alignment
    @property
    def vertical_alignment(self):
        return self._get_attr("verticalAlignment")

    @vertical_alignment.setter
    @beartype
    def vertical_alignment(self, value: CrossAxisAlignment):
        self._set_attr("verticalAlignment", value)

    # spacing
    @property
    def spacing(self):
        return self._get_attr("spacing")

    @spacing.setter
    @beartype
    def spacing(self, value: OptionalNumber):
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
    def run_spacing(self, value: OptionalNumber):
        self._set_attr("runSpacing", value)

    # scroll
    @property
    def scroll(self):
        return self.__scroll

    @scroll.setter
    @beartype
    def scroll(self, value: ScrollMode):
        self.__scroll = value
        if value == True:
            value = "auto"
        elif value == False:
            value = "none"
        self._set_attr("scroll", value)

    # auto_scroll
    @property
    def auto_scroll(self):
        return self._get_attr("autoScroll")

    @auto_scroll.setter
    @beartype
    def auto_scroll(self, value: Optional[bool]):
        self._set_attr("autoScroll", value)

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value):
        self.__controls = value or []
