from typing import List, Optional

from beartype import beartype

from flet import padding
from flet.control import Control, MainAxisAlignment, PaddingValue
from flet.ref import Ref


class AlertDialog(Control):
    def __init__(
        self,
        ref: Ref = None,
        disabled: bool = None,
        visible: bool = None,
        data: any = None,
        #
        # Specific
        #
        open: bool = False,
        modal: bool = False,
        title: Control = None,
        title_padding: PaddingValue = None,
        content: Control = None,
        content_padding: PaddingValue = None,
        actions: List[Control] = None,
        actions_padding: PaddingValue = None,
        actions_alignment: MainAxisAlignment = None,
        on_dismiss=None,
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.__title: Control = None
        self.__content: Control = None
        self.__actions: List[Control] = []

        self.open = open
        self.modal = modal
        self.title = title
        self.title_padding = title_padding
        self.content = content
        self.content_padding = content_padding
        self.actions = actions
        self.actions_padding = actions_padding
        self.actions_alignment = actions_alignment
        self.on_dismiss = on_dismiss

    def _get_control_name(self):
        return "alertdialog"

    def _get_children(self):
        children = []
        if self.__title:
            self.__title._set_attr_internal("n", "title")
            children.append(self.__title)
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        for action in self.__actions:
            action._set_attr_internal("n", "action")
            children.append(action)
        return children

    # open
    @property
    def open(self):
        return self._get_attr("open", data_type="bool", def_value=False)

    @open.setter
    @beartype
    def open(self, value: Optional[bool]):
        self._set_attr("open", value)

    # modal
    @property
    def modal(self):
        return self._get_attr("modal", data_type="bool", def_value=False)

    @modal.setter
    @beartype
    def modal(self, value: Optional[bool]):
        self._set_attr("modal", value)

    # title
    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    # title_padding
    @property
    def title_padding(self):
        return self.__title_padding

    @title_padding.setter
    @beartype
    def title_padding(self, value: PaddingValue):
        self.__title_padding = value
        if value and isinstance(value, (int, float)):
            value = padding.all(value)
        self._set_attr_json("titlePadding", value)

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    # content_padding
    @property
    def content_padding(self):
        return self.__content_padding

    @content_padding.setter
    @beartype
    def content_padding(self, value: PaddingValue):
        self.__content_padding = value
        if value and isinstance(value, (int, float)):
            value = padding.all(value)
        self._set_attr_json("contentPadding", value)

    # actions
    @property
    def actions(self):
        return self.__actions

    @actions.setter
    def actions(self, value):
        self.__actions = value or []

    # actions_padding
    @property
    def actions_padding(self):
        return self.__actions_padding

    @actions_padding.setter
    @beartype
    def actions_padding(self, value: PaddingValue):
        self.__actions_padding = value
        if value and isinstance(value, (int, float)):
            value = padding.all(value)
        self._set_attr_json("actionsPadding", value)

    # actions_alignment
    @property
    def actions_alignment(self):
        return self._get_attr("actionsAlignment")

    @actions_alignment.setter
    @beartype
    def actions_alignment(self, value: MainAxisAlignment):
        self._set_attr("actionsAlignment", value)

    # on_dismiss
    @property
    def on_dismiss(self):
        return self._get_event_handler("dismiss")

    @on_dismiss.setter
    def on_dismiss(self, handler):
        self._add_event_handler("dismiss", handler)
