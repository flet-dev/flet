from typing import List, Optional

from beartype import beartype

from flet.control import Control, MainAxisAlignment
from flet.ref import Ref

try:
    from typing import Literal
except:
    from typing_extensions import Literal


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
        title_padding: float = None,
        content: Control = None,
        content_padding: float = None,
        actions: List[Control] = None,
        actions_padding: float = None,
        actions_alignment: MainAxisAlignment = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.open = open
        self.modal = modal
        self.title = title
        self.title_padding = title_padding
        self.content = content
        self.content_padding = content_padding
        self.__actions = []
        self.actions = actions
        self.actions_padding = actions_padding
        self.actions_alignment = actions_alignment

    def _get_control_name(self):
        return "snackbar"

    def _get_children(self):
        return []

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
        return self._get_attr("titlePadding")

    @title_padding.setter
    def title_padding(self, value):
        self._set_attr("titlePadding", value)

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
        return self._get_attr("contentPadding")

    @content_padding.setter
    def content_padding(self, value):
        self._set_attr("contentPadding", value)

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
        return self._get_attr("actionsPadding")

    @actions_padding.setter
    def actions_padding(self, value):
        self._set_attr("actionsPadding", value)

    # actions_alignment
    @property
    def actions_alignment(self):
        return self._get_attr("actionsAlignment")

    @actions_alignment.setter
    @beartype
    def actions_alignment(self, value: MainAxisAlignment):
        self._set_attr("actionsAlignment", value)
