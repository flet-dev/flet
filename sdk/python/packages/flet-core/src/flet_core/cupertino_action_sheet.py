from typing import Any, List, Optional, Union

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref


class CupertinoActionSheet(Control):
    """
    An iOS-style action sheet.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinoactionsheet
    """

    def __init__(
        self,
        title: Optional[Control] = None,
        message: Optional[Control] = None,
        actions: Optional[List[Control]] = None,
        cancel: Optional[Control] = None,
        modal: bool = False,
        open: bool = False,
        on_dismiss=None,
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
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.cancel = cancel
        self.title = title
        self.message = message
        self.actions = actions
        self.modal = modal
        self.open = open
        self.on_dismiss = on_dismiss

    def _get_control_name(self):
        return "cupertinoactionsheet"

    def before_update(self):
        super().before_update()

    def _get_children(self):
        children = []
        if self.__cancel:
            self.__cancel._set_attr_internal("n", "cancel")
            children.append(self.__cancel)
        if self.__title:
            self.__title._set_attr_internal("n", "title")
            children.append(self.__title)
        if self.__message:
            self.__message._set_attr_internal("n", "message")
            children.append(self.__message)
        for action in self.__actions:
            action._set_attr_internal("n", "action")
            children.append(action)
        return children

    # cancel
    @property
    def cancel(self) -> Optional[Control]:
        return self.__cancel

    @cancel.setter
    def cancel(self, value: Optional[Control]):
        self.__cancel = value

    # title
    @property
    def title(self) -> Optional[Control]:
        return self.__title

    @title.setter
    def title(self, value: Optional[Control]):
        self.__title = value

    # message
    @property
    def message(self) -> Optional[Control]:
        return self.__message

    @message.setter
    def message(self, value: Optional[Control]):
        self.__message = value

    # actions
    @property
    def actions(self):
        return self.__actions

    @actions.setter
    def actions(self, value):
        self.__actions = value if value is not None else []

    # open
    @property
    def open(self) -> Optional[bool]:
        return self._get_attr("open", data_type="bool", def_value=False)

    @open.setter
    def open(self, value: Optional[bool]):
        self._set_attr("open", value)

    # modal
    @property
    def modal(self) -> Optional[bool]:
        return self._get_attr("modal", data_type="bool", def_value=False)

    @modal.setter
    def modal(self, value: Optional[bool]):
        self._set_attr("modal", value)

    # on_dismiss
    @property
    def on_dismiss(self):
        return self._get_event_handler("dismiss")

    @on_dismiss.setter
    def on_dismiss(self, handler):
        self._add_event_handler("dismiss", handler)
