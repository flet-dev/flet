from typing import Optional, Union

from beartype import beartype

from flet.buttons import ButtonStyle
from flet.constrained_control import ConstrainedControl
from flet.control import Control, OptionalNumber
from flet.ref import Ref


class ElevatedButton(ConstrainedControl):
    def __init__(
        self,
        text: str = None,
        ref: Ref = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[bool, int] = None,
        opacity: OptionalNumber = None,
        tooltip: str = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # Specific
        #
        color: str = None,
        bgcolor: str = None,
        elevation: OptionalNumber = None,
        style: ButtonStyle = None,
        icon: str = None,
        icon_color: str = None,
        content: Control = None,
        autofocus: bool = None,
        on_click=None,
        on_long_press=None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            opacity=opacity,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.__color = None
        self.__bgcolor = None
        self.__elevation = None

        self.text = text
        self.color = color
        self.bgcolor = bgcolor
        self.elevation = elevation
        self.style = style
        self.icon = icon
        self.icon_color = icon_color
        self.content = content
        self.autofocus = autofocus
        self.on_click = on_click
        self.on_long_press = on_long_press

    def _get_control_name(self):
        return "elevatedbutton"

    def _before_build_command(self):
        if self.__color != None or self.__bgcolor != None or self.__elevation != None:
            if self.__style == None:
                self.__style = ButtonStyle()
            if self.__style.color == None:
                self.__style.color = self.__color
            if self.__style.bgcolor == None:
                self.__style.bgcolor = self.__bgcolor
            if self.__style.elevation == None:
                self.__style.elevation = self.__elevation
        self._set_attr_json("style", self.__style)

    def _get_children(self):
        if self.__content == None:
            return []
        self.__content._set_attr_internal("n", "content")
        return [self.__content]

    # text
    @property
    def text(self):
        return self._get_attr("text")

    @text.setter
    def text(self, value):
        self._set_attr("text", value)

    # color
    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        self.__color = value

    # bgcolor
    @property
    def bgcolor(self):
        return self.__bgcolor

    @bgcolor.setter
    def bgcolor(self, value):
        self.__bgcolor = value

    # elevation
    @property
    def elevation(self) -> OptionalNumber:
        return self.__elevation

    @elevation.setter
    @beartype
    def elevation(self, value: OptionalNumber):
        self.__elevation = value

    # style
    @property
    def style(self):
        return self.__style

    @style.setter
    @beartype
    def style(self, value: Optional[ButtonStyle]):
        self.__style = value

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

    # on_long_press
    @property
    def on_long_press(self):
        return self._get_event_handler("long_press")

    @on_long_press.setter
    def on_long_press(self, handler):
        self._add_event_handler("long_press", handler)

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    @beartype
    def content(self, value: Optional[Control]):
        self.__content = value

    # autofocus
    @property
    def autofocus(self):
        return self._get_attr("autofocus", data_type="bool", def_value=False)

    @autofocus.setter
    @beartype
    def autofocus(self, value: Optional[bool]):
        self._set_attr("autofocus", value)
