from typing import Optional

from beartype import beartype
from flet.constrained_control import ConstrainedControl

from flet.control import Control
from flet.ref import Ref


class ElevatedButton(ConstrainedControl):
    def __init__(
        self,
        text: str = None,
        ref: Ref = None,
        width: float = None,
        height: float = None,
        expand: int = None,
        opacity: float = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # Specific
        #
        icon: str = None,
        icon_color: str = None,
        content: Control = None,
        on_click=None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            width=width,
            height=height,
            expand=expand,
            opacity=opacity,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.text = text
        self.icon = icon
        self.icon_color = icon_color
        self.content = content
        self.on_click = on_click

    def _get_control_name(self):
        return "elevatedbutton"

    # text
    @property
    def text(self):
        return self._get_attr("text")

    @text.setter
    def text(self, value):
        self._set_attr("text", value)

    # icon
    @property
    def icon(self):
        return self._get_attr("icon")

    @icon.setter
    def icon(self, value):
        self._set_attr("icon", value)

    # icon_color
    @property
    def icon_color(self):
        return self._get_attr("iconColor")

    @icon_color.setter
    def icon_color(self, value):
        self._set_attr("iconColor", value)

    # on_click
    @property
    def on_click(self):
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler):
        self._add_event_handler("click", handler)

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    @beartype
    def content(self, value: Optional[Control]):
        self.__content = value

    def _get_children(self):
        if self.__content == None:
            return []
        return [self.__content]
