from typing import Any, Optional

from flet.core.control import Control
from flet.core.ref import Ref


class MergeSemantics(Control):
    """
    A control that merges the semantics of its descendants.

    Causes all the semantics of the subtree rooted at this node to be merged into one node in the semantics tree.

    Used by accessibility tools, search engines, and other semantic analysis software to determine the meaning of the application.

    -----

    Online docs: https://flet.dev/docs/controls/mergesemantics
    """

    def __init__(
        self,
        content: Optional[Control] = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.content = content

    def _get_control_name(self):
        return "mergesemantics"

    def _get_children(self):
        children = []
        if isinstance(self.__content, Control):
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value
