from typing import List, Optional

from beartype import beartype

from flet.constrained_control import ConstrainedControl
from flet.control import Control, OptionalNumber
from flet.ref import Ref


class ListView(ConstrainedControl):
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
        horizontal: bool = None,
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

    def _get_control_name(self):
        return "listview"

    def _get_children(self):
        return self.__controls

    # horizontal
    @property
    def horizontal(self):
        return self._get_attr("horizontal")

    @horizontal.setter
    @beartype
    def horizontal(self, value: Optional[bool]):
        self._set_attr("horizontal", value)

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value):
        self.__controls = value or []
