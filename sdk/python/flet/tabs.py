from typing import Optional

from beartype import beartype

from flet.control import Control


class Tabs(Control):
    def __init__(
        self,
        tabs=None,
        id=None,
        ref=None,
        value=None,
        solid=None,
        on_change=None,
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

        self.solid = solid
        self.on_change = on_change
        self.__tabs = []
        self.tabs = tabs
        if value:
            self.value = value

    def _get_control_name(self):
        return "tabs"

    def clean(self):
        Control.clean(self)
        self.__tabs.clear()
        self.value = None

    # tabs
    @property
    def tabs(self):
        return self.__tabs

    @tabs.setter
    def tabs(self, value):
        value = value or []
        self.__tabs = value
        self.value = value and (value[0].key or value[0].text) or ""

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)

    # value
    @property
    def value(self):
        return self._get_attr("value")

    @value.setter
    @beartype
    def value(self, value: str):
        if not value:
            assert (
                not self.tabs
            ), "Setting an empty value is only allowed if you have no tabs"
        else:
            assert any(
                value in keys for keys in [(tab.key, tab.text) for tab in self.tabs]
            ), f"'{value}' is not a key for any tab"
        self._set_attr("value", value or "")

    # solid
    @property
    def solid(self):
        return self._get_attr("solid", data_type="bool", def_value=False)

    @solid.setter
    @beartype
    def solid(self, value: Optional[bool]):
        self._set_attr("solid", value)

    def _get_children(self):
        return self.__tabs


class Tab(Control):
    def __init__(
        self, text, controls=None, id=None, ref=None, key=None, icon=None, count=None
    ):
        Control.__init__(self, id=id, ref=ref)
        assert key or text, "key or text must be specified"
        self.key = key
        self.text = text
        self.icon = icon
        self.count = count
        self.__controls = []
        self.controls = controls

    def _get_control_name(self):
        return "tab"

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

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value):
        self.__controls = value or []

    # count
    @property
    def count(self):
        return self._get_attr("count")

    @count.setter
    def count(self, value):
        self._set_attr("count", value)

    def _get_children(self):
        return self.__controls
