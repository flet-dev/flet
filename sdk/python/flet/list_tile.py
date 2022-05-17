from typing import Optional, Union

from beartype import beartype

from flet import padding
from flet.constrained_control import ConstrainedControl
from flet.control import Control, OptionalNumber, PaddingValue
from flet.ref import Ref


class ListTile(ConstrainedControl):
    def __init__(
        self,
        text: str = None,
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
        # Specific
        #
        content_padding: PaddingValue = None,
        leading: Control = None,
        title: Control = None,
        subtitle: Control = None,
        trailing: Control = None,
        is_three_line: bool = None,
        selected: bool = None,
        dense: bool = None,
        autofocus: bool = None,
        on_click=None,
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

        self.content_padding = content_padding
        self.leading = leading
        self.title = title
        self.subtitle = subtitle
        self.trailing = trailing
        self.is_three_line = is_three_line
        self.selected = selected
        self.dense = dense
        self.autofocus = autofocus
        self.on_click = on_click

    def _get_control_name(self):
        return "listtile"

    def _get_children(self):
        children = []
        if self.__leading:
            self.__leading._set_attr_internal("n", "leading")
            children.append(self.__leading)
        if self.__title:
            self.__title._set_attr_internal("n", "title")
            children.append(self.__title)
        if self.__subtitle:
            self.__subtitle._set_attr_internal("n", "subtitle")
            children.append(self.__subtitle)
        if self.__trailing:
            self.__trailing._set_attr_internal("n", "trailing")
            children.append(self.__trailing)
        return children

    # content_padding
    @property
    def content_padding(self):
        return self.__content_padding

    @content_padding.setter
    @beartype
    def content_padding(self, value: PaddingValue):
        self.__content_padding = value
        if value and isinstance(value, (int, float)):
            value = padding.all(value)
        self._set_attr_json("contentPadding", value)

    # leading
    @property
    def leading(self):
        return self.__leading

    @leading.setter
    @beartype
    def leading(self, value: Optional[Control]):
        self.__leading = value

    # title
    @property
    def title(self):
        return self.__title

    @title.setter
    @beartype
    def title(self, value: Optional[Control]):
        self.__title = value

    # subtitle
    @property
    def subtitle(self):
        return self.__subtitle

    @subtitle.setter
    @beartype
    def subtitle(self, value: Optional[Control]):
        self.__subtitle = value

    # trailing
    @property
    def trailing(self):
        return self.__trailing

    @trailing.setter
    @beartype
    def trailing(self, value: Optional[Control]):
        self.__trailing = value

    # is_three_line
    @property
    def is_three_line(self):
        return self._get_attr("isThreeLine", data_type="bool", def_value=False)

    @is_three_line.setter
    @beartype
    def is_three_line(self, value: Optional[bool]):
        self._set_attr("isThreeLine", value)

    # selected
    @property
    def selected(self):
        return self._get_attr("selected", data_type="bool", def_value=False)

    @selected.setter
    @beartype
    def selected(self, value: Optional[bool]):
        self._set_attr("selected", value)

    # dense
    @property
    def dense(self):
        return self._get_attr("dense", data_type="bool", def_value=False)

    @dense.setter
    @beartype
    def dense(self, value: Optional[bool]):
        self._set_attr("dense", value)

    # autofocus
    @property
    def autofocus(self):
        return self._get_attr("autofocus", data_type="bool", def_value=False)

    @autofocus.setter
    @beartype
    def autofocus(self, value: Optional[bool]):
        self._set_attr("autofocus", value)

    # on_click
    @property
    def on_click(self):
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler):
        self._add_event_handler("click", handler)
        if handler != None:
            self._set_attr("onclick", True)
        else:
            self._set_attr("onclick", None)
