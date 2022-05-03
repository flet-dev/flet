from typing import Optional

from beartype import beartype
from beartype.typing import List

from flet.constrained_control import ConstrainedControl
from flet.control import Control, OptionalNumber
from flet.ref import Ref


class Tab(Control):
    def __init__(
        self,
        text: str = None,
        content: Control = None,
        tab_content: Control = None,
        ref: Ref = None,
        key: str = None,
        icon: str = None,
    ):
        Control.__init__(self, ref=ref)
        assert key or text, "key or text must be specified"
        self.key = key
        self.text = text
        self.icon = icon
        self.__content: Control = None
        self.content = content
        self.__tab_content: Control = None
        self.tab_content = tab_content

    def _get_control_name(self):
        return "tab"

    def _get_children(self):
        children = []
        if self.__tab_content:
            self.__tab_content._set_attr_internal("n", "tab_content")
            children.append(self.__tab_content)
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

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

    # tab_content
    @property
    def tab_content(self):
        return self.__tab_content

    @tab_content.setter
    def tab_content(self, value):
        self.__tab_content = value

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value


class Tabs(ConstrainedControl):
    def __init__(
        self,
        ref: Ref = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        expand: int = None,
        opacity: OptionalNumber = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # Tabs-specific
        tabs: List[Tab] = None,
        value: str = None,
        animation_duration: int = None,
        on_change=None,
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

        self.tabs = tabs
        self.value = value
        self.animation_duration = animation_duration
        self.on_change = on_change

    def _get_control_name(self):
        return "tabs"

    def _get_children(self):
        return self.__tabs

    # tabs
    @property
    def tabs(self):
        return self.__tabs

    @tabs.setter
    @beartype
    def tabs(self, value: Optional[List[Tab]]):
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
    def value(self, value: Optional[str]):
        if not value:
            assert (
                not self.tabs
            ), "Setting an empty value is only allowed if you have no tabs"
        else:
            assert any(
                value in keys for keys in [(tab.key, tab.text) for tab in self.tabs]
            ), f"'{value}' is not a key for any tab"
        self._set_attr("value", value or "")

    # animation_duration
    @property
    def animation_duration(self):
        return self._get_attr("animationDuration")

    @animation_duration.setter
    @beartype
    def animation_duration(self, value: Optional[int]):
        self._set_attr("animationDuration", value)
