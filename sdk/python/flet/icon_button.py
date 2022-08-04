from typing import Optional, Union

from beartype import beartype

from flet.buttons import ButtonStyle
from flet.constrained_control import ConstrainedControl
from flet.control import Control, OptionalNumber
from flet.ref import Ref


class IconButton(ConstrainedControl):
    def __init__(
        self,
        icon: str = None,
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
        icon_size: OptionalNumber = None,
        icon_color: str = None,
        selected_icon: str = None,
        selected_icon_color: str = None,
        selected: bool = None,
        bgcolor: str = None,
        style: ButtonStyle = None,
        content: Control = None,
        autofocus: bool = None,
        on_click=None,
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

        self.icon = icon
        self.icon_size = icon_size
        self.icon_color = icon_color
        self.selected_icon = selected_icon
        self.selected_icon_color = selected_icon_color
        self.selected = selected
        self.bgcolor = bgcolor
        self.style = style
        self.content = content
        self.autofocus = autofocus
        self.on_click = on_click

    def _get_control_name(self):
        return "iconbutton"

    def _before_build_command(self):
        self._set_attr_json("style", self.__style)

    def _get_children(self):
        if self.__content == None:
            return []
        self.__content._set_attr_internal("n", "content")
        return [self.__content]

    # icon
    @property
    def icon(self):
        return self._get_attr("icon")

    @icon.setter
    def icon(self, value):
        self._set_attr("icon", value)

    # selected_icon
    @property
    def selected_icon(self):
        return self._get_attr("selectedIcon")

    @selected_icon.setter
    def selected_icon(self, value):
        self._set_attr("selectedIcon", value)

    # icon_size
    @property
    def icon_size(self):
        return self._get_attr("iconSize")

    @icon_size.setter
    def icon_size(self, value):
        self._set_attr("iconSize", value)

    # icon_color
    @property
    def icon_color(self):
        return self._get_attr("iconColor")

    @icon_color.setter
    def icon_color(self, value):
        self._set_attr("iconColor", value)

    # selected_icon_color
    @property
    def selected_icon_color(self):
        return self._get_attr("selectedIconColor")

    @selected_icon_color.setter
    def selected_icon_color(self, value):
        self._set_attr("selectedIconColor", value)

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgcolor", value)

    # selected
    @property
    def selected(self):
        return self._get_attr("selected", data_type="bool", def_value=False)

    @selected.setter
    @beartype
    def selected(self, value: Optional[bool]):
        self._set_attr("selected", value)

    # style
    @property
    def style(self):
        return self.__style

    @style.setter
    @beartype
    def style(self, value: Optional[ButtonStyle]):
        self.__style = value

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

    # autofocus
    @property
    def autofocus(self):
        return self._get_attr("autofocus", data_type="bool", def_value=False)

    @autofocus.setter
    @beartype
    def autofocus(self, value: Optional[bool]):
        self._set_attr("autofocus", value)
