from typing import Optional, Union

from beartype import beartype

from flet import margin
from flet.constrained_control import ConstrainedControl
from flet.control import Control, MarginValue, OptionalNumber
from flet.ref import Ref


class Card(ConstrainedControl):
    def __init__(
        self,
        ref: Ref = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        expand: Union[bool, int] = None,
        opacity: OptionalNumber = None,
        tooltip: str = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # Specific
        #
        content: Control = None,
        margin: MarginValue = None,
        elevation: OptionalNumber = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            width=width,
            height=height,
            expand=expand,
            opacity=opacity,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.content = content
        self.margin = margin
        self.elevation = elevation

    def _get_control_name(self):
        return "card"

    def _get_children(self):
        children = []
        if self.__content != None:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # margin
    @property
    def margin(self):
        return self.__margin

    @margin.setter
    @beartype
    def margin(self, value: MarginValue):
        self.__margin = value
        if value and isinstance(value, (int, float)):
            value = margin.all(value)
        self._set_attr_json("margin", value)

    # elevation
    @property
    def elevation(self) -> OptionalNumber:
        return self._get_attr("elevation")

    @elevation.setter
    @beartype
    def elevation(self, value: OptionalNumber):
        self._set_attr("elevation", value)

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    @beartype
    def content(self, value: Optional[Control]):
        self.__content = value
