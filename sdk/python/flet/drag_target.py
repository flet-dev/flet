from beartype import beartype

from flet.control import Control
from flet.ref import Ref


class DragTarget(Control):
    def __init__(
        self,
        ref: Ref = None,
        disabled: bool = None,
        visible: bool = None,
        data: any = None,
        #
        # Specific
        #
        group: str = None,
        content: Control = None,
        on_will_accept=None,
        on_accept=None,
        on_leave=None,
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.__content: Control = None

        self.group = group
        self.content = content
        self.on_will_accept = on_will_accept
        self.on_accept = on_accept
        self.on_leave = on_leave

    def _get_control_name(self):
        return "dragtarget"

    def _get_children(self):
        children = []
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
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

    # on_will_accept
    @property
    def on_will_accept(self):
        return self._get_event_handler("will_accept")

    @on_will_accept.setter
    def on_will_accept(self, handler):
        self._add_event_handler("will_accept", handler)

    # on_accept
    @property
    def on_accept(self):
        return self._get_event_handler("accept")

    @on_accept.setter
    def on_accept(self, handler):
        self._add_event_handler("accept", handler)

    # on_leave
    @property
    def on_leave(self):
        return self._get_event_handler("leave")

    @on_leave.setter
    def on_leave(self, handler):
        self._add_event_handler("leave", handler)
