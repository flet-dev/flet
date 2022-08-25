from typing import Any, Optional

from beartype import beartype

from flet.control import Control
from flet.ref import Ref


class WindowDragArea(Control):
    def __init__(
        self,
        content: Optional[Control] = None,
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.__content: Optional[Control] = None

        self.content = content

    def _get_control_name(self):
        return "windowDragArea"

    def _get_children(self):
        children = []
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value
