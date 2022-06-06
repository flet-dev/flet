from typing import Optional

from beartype import beartype

from flet.control import Control
from flet.ref import Ref


class SnackBar(Control):
    def __init__(
        self,
        content: Control = None,
        ref: Ref = None,
        disabled: bool = None,
        visible: bool = None,
        data: any = None,
        #
        # Specific
        #
        open: bool = False,
        # remove_current_snackbar: bool = False,
        action: str = None,
        on_action=None,
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.open = open
        # self.remove_current_snackbar = remove_current_snackbar
        self.content = content
        self.action = action
        self.on_action = on_action

    def _get_control_name(self):
        return "snackbar"

    def _get_children(self):
        children = []
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # open
    @property
    def open(self):
        return self._get_attr("open", data_type="bool", def_value=False)

    @open.setter
    @beartype
    def open(self, value: Optional[bool]):
        self._set_attr("open", value)

    # # remove_current_snackbar
    # @property
    # def remove_current_snackbar(self):
    #     return self._get_attr(
    #         "removeCurrentSnackBar", data_type="bool", def_value=False
    #     )

    # @remove_current_snackbar.setter
    # @beartype
    # def remove_current_snackbar(self, value: Optional[bool]):
    #     self._set_attr("removeCurrentSnackBar", value)

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    @beartype
    def content(self, value: Control):
        self.__content = value

    # action
    @property
    def action(self):
        return self._get_attr("action")

    @action.setter
    def action(self, value):
        self._set_attr("action", value)

    # on_action
    @property
    def on_action(self):
        return self._get_event_handler("action")

    @on_action.setter
    def on_action(self, handler):
        self._add_event_handler("action", handler)
