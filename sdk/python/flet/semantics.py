from typing import Any, Optional

from beartype import beartype

from flet.control import Control, OptionalNumber
from flet.ref import Ref


class Semantics(Control):
    def __init__(
        self,
        content: Optional[Control] = None,
        ref: Optional[Ref] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        label: Optional[str] = None,
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
        if self.__content is not None:
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
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    @beartype
    def content(self, value: Optional[Control]):
        self.__content = value
