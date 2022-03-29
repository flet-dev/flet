from typing import Optional

from beartype import beartype

from flet.control import Control


class Nav(Control):
    def __init__(
        self,
        id=None,
        ref=None,
        value=None,
        items=None,
        on_change=None,
        on_expand=None,
        on_collapse=None,
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
        )

        self.value = value
        self.on_change = on_change
        self.on_expand = on_expand
        self.on_collapse = on_collapse
        self.__items = []
        if items != None:
            for item in items:
                self.__items.append(item)

    def _get_control_name(self):
        return "nav"

    # items
    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, value):
        self.__items = value

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)

    # on_expand
    @property
    def on_expand(self):
        return self._get_event_handler("expand")

    @on_expand.setter
    def on_expand(self, handler):
        self._add_event_handler("expand", handler)

    # on_collapse
    @property
    def on_collapse(self):
        return self._get_event_handler("collapse")

    @on_collapse.setter
    def on_collapse(self, handler):
        self._add_event_handler("collapse", handler)

    # value
    @property
    def value(self):
        return self._get_attr("value")

    @value.setter
    def value(self, value):
        self._set_attr("value", value)

    def _get_children(self):
        return self.__items


class Item(Control):
    def __init__(
        self,
        id=None,
        ref=None,
        key=None,
        text=None,
        icon=None,
        icon_color=None,
        url=None,
        items=None,
        new_window=None,
        expanded=None,
        visible=None,
        disabled=None,
        data=None,
    ):
        Control.__init__(
            self, id=id, ref=ref, visible=visible, disabled=disabled, data=data
        )
        # key and text are optional for group item but key or text are required for level 2 and deeper items
        # assert key != None or text != None, "key or text must be specified"
        self.key = key
        self.text = text
        self.icon = icon
        self.icon_color = icon_color
        self.url = url
        self.new_window = new_window
        self.expanded = expanded
        self.__items = []
        if items != None:
            for item in items:
                self.__items.append(item)

    def _get_control_name(self):
        return "item"

    # items
    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, value):
        self.__items = value

    # key
    @property
    def key(self):
        return self._get_attr("key")

    @key.setter
    def key(self, value):
        self._set_attr("key", value)

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

    # expanded
    @property
    def expanded(self):
        return self._get_attr("expanded", data_type="bool", def_value=False)

    @expanded.setter
    @beartype
    def expanded(self, value: Optional[bool]):
        self._set_attr("expanded", value)

    def _get_children(self):
        return self.__items
