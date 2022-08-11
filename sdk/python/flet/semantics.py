from typing import Optional, Union

from beartype import beartype

from flet.control import Control, OptionalNumber
from flet.ref import Ref
from flet.types import AnimationValue, MarginValue, OffsetValue, RotateValue, ScaleValue


class Semantics(Control):
    def __init__(
        self,
        content: Control = None,
        ref: Ref = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # Specific
        #
        label: str = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.content = content
        self.label = label

    def _get_control_name(self):
        return "semantics"

    def _get_children(self):
        children = []
        if self.__content != None:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # label
    @property
    def label(self):
        return self._get_attr("label")

    @label.setter
    def label(self, value):
        self._set_attr("label", value)

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    @beartype
    def content(self, value: Optional[Control]):
        self.__content = value
