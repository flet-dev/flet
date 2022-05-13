from typing import Optional, Union

from beartype import beartype
from beartype.typing import List

from flet.constrained_control import ConstrainedControl
from flet.control import Control, OptionalNumber
from flet.ref import Ref


class PopupMenuItem(Control):
    def __init__(
        self,
        ref: Ref = None,
        checked: bool = None,
        icon: str = None,
        text: str = None,
        content: Control = None,
        on_click=None,
    ):
        Control.__init__(self, ref=ref)

        self.checked = checked
        self.icon = icon
        self.text = text
        self.__content: Control = None
        self.content = content
        self.on_click = on_click

    def _get_control_name(self):
        return "popupmenuitem"

    def _get_children(self):
        children = []
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # checked
    @property
    def checked(self):
        return self._get_attr("checked", data_type="bool")

    @checked.setter
    @beartype
    def checked(self, value: Optional[bool]):
        self._set_attr("checked", value)

    # icon
    @property
    def icon(self):
        return self._get_attr("icon")

    @icon.setter
    def icon(self, value):
        self._set_attr("icon", value)

    # text
    @property
    def text(self):
        return self._get_attr("text")

    @text.setter
    def text(self, value):
        self._set_attr("text", value)

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    # on_click
    @property
    def on_click(self):
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler):
        self._add_event_handler("click", handler)


class PopupMenuButton(ConstrainedControl):
    def __init__(
        self,
        ref: Ref = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        expand: Union[bool, int] = None,
        opacity: OptionalNumber = None,
        tooltip: str = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # PopupMenuButton-specific
        items: List[PopupMenuItem] = None,
        icon: str = None,
        on_cancelled=None,
    ):

        ConstrainedControl.__init__(
            self,
            ref=ref,
            width=width,
            height=height,
            expand=expand,
            opacity=opacity,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.items = items
        self.icon = icon
        self.on_cancelled = on_cancelled

    def _get_control_name(self):
        return "popupmenubutton"

    def _get_children(self):
        return self.__items

    # items
    @property
    def items(self):
        return self.__items

    @items.setter
    @beartype
    def items(self, value: Optional[List[PopupMenuItem]]):
        value = value or []
        self.__items = value

    # on_cancelled
    @property
    def on_cancelled(self):
        return self._get_event_handler("cancelled")

    @on_cancelled.setter
    def on_cancelled(self, handler):
        self._add_event_handler("cancelled", handler)

    # icon
    @property
    def icon(self):
        return self._get_attr("icon")

    @icon.setter
    def icon(self, value):
        self._set_attr("icon", value)
