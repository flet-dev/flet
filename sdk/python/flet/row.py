from typing import List, Optional

from beartype import beartype

from flet.control import Control, CrossAxisAlignment, MainAxisAlignment
from flet.ref import Ref


class Row(Control):
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
        horizontal_alignment: MainAxisAlignment = None,
        vertical_alignment: CrossAxisAlignment = None,
        spacing: float = None,
        wrap: bool = None,
        run_spacing: float = None,
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
            horizontal_alignment=horizontal_alignment,
            vertical_alignment=vertical_alignment,
            spacing=spacing,
            wrap=wrap,
            run_spacing=run_spacing,
        )

        self.__controls = []
        if controls != None:
            for control in controls:
                self.__controls.append(control)

    def _get_control_name(self):
        return "row"

    # horizontal_alignment
    @property
    def horizontal_alignment(self):
        return self._get_attr("horizontalAlignment")

    @horizontal_alignment.setter
    @beartype
    def horizontal_alignment(self, value: MainAxisAlignment):
        self._set_attr("horizontalAlignment", value)

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
        self.__controls = value

    def _get_children(self):
        return self.__controls
