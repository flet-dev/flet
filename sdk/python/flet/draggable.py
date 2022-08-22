from typing import Any, Optional

from beartype import beartype

from flet.control import Control
from flet.ref import Ref


class Draggable(Control):
    def __init__(
        self,
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        group: Optional[str] = None,
        content: Optional[Control] = None,
        content_when_dragging: Optional[Control] = None,
        content_feedback: Optional[Control] = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.__content: Optional[Control] = None
        self.__content_when_dragging: Optional[Control] = None
        self.__content_feedback: Optional[Control] = None

        self.group = group
        self.content = content
        self.content_when_dragging = content_when_dragging
        self.content_feedback = content_feedback

    def _get_control_name(self):
        return "draggable"

    def _get_children(self):
        children = []
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        if self.__content_when_dragging:
            self.__content_when_dragging._set_attr_internal(
                "n", "content_when_dragging"
            )
            children.append(self.__content_when_dragging)
        if self.__content_feedback:
            self.__content_feedback._set_attr_internal("n", "content_feedback")
            children.append(self.__content_feedback)
        return children

    # group
    @property
    def group(self):
        return self._get_attr("group")

    @group.setter
    @beartype
    def group(self, value):
        self._set_attr("group", value)

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    # content_when_dragging
    @property
    def content_when_dragging(self):
        return self.__content_when_dragging

    @content_when_dragging.setter
    def content_when_dragging(self, value):
        self.__content_when_dragging = value

    # content_feedback
    @property
    def content_feedback(self):
        return self.__content_feedback

    @content_feedback.setter
    def content_feedback(self, value):
        self.__content_feedback = value
