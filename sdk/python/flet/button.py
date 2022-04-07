from typing import Optional

from beartype import beartype

from flet.control import Control


class Button(Control):
    def __init__(
        self,
        text=None,
        id=None,
        ref=None,
        primary=None,
        compound=None,
        action=None,
        toolbar=None,
        split=None,
        secondary_text=None,
        url=None,
        new_window=None,
        title=None,
        icon=None,
        icon_color=None,
        focused=None,
        data=None,
        on_click=None,
        on_focus=None,
        on_blur=None,
        menu_items=None,
        width=None,
        height=None,
        padding=None,
        margin=None,
        visible=None,
        disabled=None,
    ):
        Control.__init__(
            self,
            id=id,
            ref=ref,
            width=width,
            height=height,
            padding=padding,
            margin=margin,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.primary = primary
        self.compound = compound
        self.action = action
        self.toolbar = toolbar
        self.split = split
        self.text = text
        self.secondary_text = secondary_text
        self.url = url
        self.new_window = new_window
        self.title = title
        self.icon = icon
        self.icon_color = icon_color
        self.focused = focused
        self.on_click = on_click
        self.on_focus = on_focus
        self.on_blur = on_blur
        self.__menu_items = []
        if menu_items != None:
            for item in menu_items:
                self.__menu_items.append(item)

    def _get_control_name(self):
        return "button"

    # menu_items
    @property
    def menu_items(self):
        return self.__menu_items

    @menu_items.setter
    def menu_items(self, value):
        self.__menu_items = value

    # on_click
    @property
    def on_click(self):
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler):
        self._add_event_handler("click", handler)

    # primary
    @property
    def primary(self):
        return self._get_attr("primary", data_type="bool", def_value=False)

    @primary.setter
    @beartype
    def primary(self, value: Optional[bool]):
        self._set_attr("primary", value)

    # compound
    @property
    def compound(self):
        return self._get_attr("compound", data_type="bool", def_value=False)

    @compound.setter
    @beartype
    def compound(self, value: Optional[bool]):
        self._set_attr("compound", value)

    # action
    @property
    def action(self):
        return self._get_attr("action", data_type="bool", def_value=False)

    @action.setter
    @beartype
    def action(self, value: Optional[bool]):
        self._set_attr("action", value)

    # toolbar
    @property
    def toolbar(self):
        return self._get_attr("toolbar", data_type="bool", def_value=False)

    @toolbar.setter
    @beartype
    def toolbar(self, value: Optional[bool]):
        self._set_attr("toolbar", value)

    # split
    @property
    def split(self):
        return self._get_attr("split", data_type="bool", def_value=False)

    @split.setter
    @beartype
    def split(self, value: Optional[bool]):
        self._set_attr("split", value)

    # text
    @property
    def text(self):
        return self._get_attr("text")

    @text.setter
    def text(self, value):
        self._set_attr("text", value)

    # secondary_text
    @property
    def secondary_text(self):
        return self._get_attr("secondaryText")

    @secondary_text.setter
    def secondary_text(self, value):
        self._set_attr("secondaryText", value)

    # url
    @property
    def url(self):
        return self._get_attr("url")

    @url.setter
    def url(self, value):
        self._set_attr("url", value)

    # new_window
    @property
    def new_window(self):
        return self._get_attr("newWindow", data_type="bool", def_value=False)

    @new_window.setter
    @beartype
    def new_window(self, value: Optional[bool]):
        self._set_attr("newWindow", value)

    # title
    @property
    def title(self):
        return self._get_attr("title")

    @title.setter
    def title(self, value):
        self._set_attr("title", value)

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

    def _get_children(self):
        return self.__menu_items

    # focused
    @property
    def focused(self):
        return self._get_attr("focused", data_type="bool", def_value=False)

    @focused.setter
    @beartype
    def focused(self, value: Optional[bool]):
        self._set_attr("focused", value)

    # on_focus
    @property
    def on_focus(self):
        return self._get_event_handler("focus")

    @on_focus.setter
    def on_focus(self, handler):
        self._add_event_handler("focus", handler)

    # on_blur
    @property
    def on_blur(self):
        return self._get_event_handler("blur")

    @on_blur.setter
    def on_blur(self, handler):
        self._add_event_handler("blur", handler)


class MenuItem(Control):
    def __init__(
        self,
        text=None,
        id=None,
        ref=None,
        secondary_text=None,
        url=None,
        new_window=None,
        icon=None,
        icon_color=None,
        icon_only=None,
        split=None,
        divider=None,
        on_click=None,
        sub_menu_items=None,
        width=None,
        height=None,
        padding=None,
        margin=None,
        visible=None,
        disabled=None,
        data=None,
    ):
        Control.__init__(
            self,
            id=id,
            ref=ref,
            width=width,
            height=height,
            padding=padding,
            margin=margin,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.text = text
        self.secondary_text = secondary_text
        self.url = url
        self.new_window = new_window
        self.icon = icon
        self.icon_color = icon_color
        self.icon_only = icon_only
        self.split = split
        self.divider = divider
        self.on_click = on_click
        self.__sub_menu_items = []
        if sub_menu_items != None:
            for item in sub_menu_items:
                self.__sub_menu_items.append(item)

    def _get_control_name(self):
        return "item"

    # on_click
    @property
    def on_click(self):
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler):
        self._add_event_handler("click", handler)

    # sub_menu_items
    @property
    def sub_menu_items(self):
        return self.__sub_menu_items

    @sub_menu_items.setter
    def sub_menu_items(self, value):
        self.__sub_menu_items = value

    # text
    @property
    def text(self):
        return self._get_attr("text")

    @text.setter
    def text(self, value):
        self._set_attr("text", value)

    # secondary_text
    @property
    def secondary_text(self):
        return self._get_attr("secondaryText")

    @secondary_text.setter
    def secondary_text(self, value):
        self._set_attr("secondaryText", value)

    # url
    @property
    def url(self):
        return self._get_attr("url")

    @url.setter
    def url(self, value):
        self._set_attr("url", value)

    # new_window
    @property
    def new_window(self):
        return self._get_attr("newWindow", data_type="bool", def_value=False)

    @new_window.setter
    @beartype
    def new_window(self, value: Optional[bool]):
        self._set_attr("newWindow", value)

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

    # icon_only
    @property
    def icon_only(self):
        return self._get_attr("iconOnly", data_type="bool", def_value=False)

    @icon_only.setter
    @beartype
    def icon_only(self, value: Optional[bool]):
        self._set_attr("iconOnly", value)

    # split
    @property
    def split(self):
        return self._get_attr("split", data_type="bool", def_value=False)

    @split.setter
    @beartype
    def split(self, value: Optional[bool]):
        self._set_attr("split", value)

    # divider
    @property
    def divider(self):
        return self._get_attr("divider", data_type="bool", def_value=False)

    @divider.setter
    @beartype
    def divider(self, value: Optional[bool]):
        self._set_attr("divider", value)

    def _get_children(self):
        return self.__sub_menu_items
