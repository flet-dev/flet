from typing import Any, Optional, Union

from beartype import beartype

from flet.control import Control, OptionalNumber
from flet.ref import Ref


class Icon(Control):
    def __init__(
        self,
        name: Optional[str] = None,
        ref: Optional[Ref] = None,
        expand: Union[None, bool, int] = None,
        opacity: OptionalNumber = None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        color: Optional[str] = None,
        size: OptionalNumber = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            expand=expand,
            opacity=opacity,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.name = name
        self.color = color
        self.size = size

    def _get_control_name(self):
        return "icon"

    # name
    @property
    def name(self):
        return self._get_attr("name")

    @name.setter
    def name(self, value):
        self._set_attr("name", value)

    # color
    @property
    def color(self):
        return self._get_attr("color")

    @color.setter
    def color(self, value):
        self._set_attr("color", value)

    # size
    @property
    def size(self) -> OptionalNumber:
        return self._get_attr("size")

    @size.setter
    @beartype
    def size(self, value: OptionalNumber):
        self._set_attr("size", value)
