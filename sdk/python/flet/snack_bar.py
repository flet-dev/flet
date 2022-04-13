from typing import Optional

from beartype import beartype

from flet.control import Control
from flet.ref import Ref

try:
    from typing import Literal
except:
    from typing_extensions import Literal


class SnackBarAction(Control):
    def __init__(
        self,
        ref: Ref = None,
        disabled: bool = None,
        visible: bool = None,
        data: any = None,
        #
        # Specific
        #
        label: str = False,
        on_click=None,
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.label = label
        self.on_click = on_click

    def _get_control_name(self):
        return "snackbaraction"

    # label
    @property
    def label(self):
        return self._get_attr("label")

    @label.setter
    def label(self, value):
        self._set_attr("label", value)

    # on_click
    @property
    def on_click(self):
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler):
        self._add_event_handler("click", handler)


class SnackBar(Control):
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
        content: str = None,
        action: SnackBarAction = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.open = open
        self.content = content
        self.action = action

    def _get_control_name(self):
        return "snackbar"

    def _get_children(self):
        if self.__content == None:
            return []
        return [self.__content]

    # open
    @property
    def open(self):
        return self._get_attr("open", data_type="bool", def_value=False)

    @open.setter
    @beartype
    def open(self, value: Optional[bool]):
        self._set_attr("open", value)

    # content
    @property
    def content(self):
        return self._get_attr("content")

    @content.setter
    def content(self, value):
        self._set_attr("content", value)

    # action
    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, value):
        self.__action = value
