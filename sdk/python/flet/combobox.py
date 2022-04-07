from beartype.typing import List, Optional, Union

from beartype import beartype

from flet.control import Control

try:
    from typing import Literal
except:
    from typing_extensions import Literal


ItemType = Literal[None, "normal", "divider", "header", "selectAll", "select_all"]
ComboBoxValue = Union[None, str, List[str]]


class ComboBox(Control):
    def __init__(
        self,
        label=None,
        id=None,
        ref=None,
        value: ComboBoxValue = None,
        placeholder=None,
        error_message=None,
        on_change=None,
        on_focus=None,
        on_blur=None,
        options=None,
        width=None,
        height=None,
        padding=None,
        margin=None,
        visible=None,
        disabled=None,
        focused=None,
        multi_select=None,
        allow_free_form=None,
        auto_complete=None,
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
        self.label = label
        self.value = value
        self.placeholder = placeholder
        self.error_message = error_message
        self.focused = focused
        self.multi_select = multi_select
        self.allow_free_form = allow_free_form
        self.auto_complete = auto_complete
        self.on_change = on_change
        self.on_focus = on_focus
        self.on_blur = on_blur
        self.__options = []
        if options != None:
            for option in options:
                self.__options.append(option)

    def _get_control_name(self):
        return "combobox"

    # options
    @property
    def options(self):
        return self.__options

    @options.setter
    def options(self, value):
        self.__options = value

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)

    # label
    @property
    def label(self):
        return self._get_attr("label")

    @label.setter
    def label(self, value):
        self._set_attr("label", value)

    # value
    @property
    def value(self):
        return self._get_value_or_list_attr("value", ",")

    @value.setter
    @beartype
    def value(self, value: ComboBoxValue):
        self._set_value_or_list_attr("value", value, ",")

    # placeholder
    @property
    def placeholder(self):
        return self._get_attr("placeholder")

    @placeholder.setter
    def placeholder(self, value):
        self._set_attr("placeholder", value)

    # error_message
    @property
    def error_message(self):
        return self._get_attr("errorMessage")

    @error_message.setter
    def error_message(self, value):
        self._set_attr("errorMessage", value)

    def _get_children(self):
        return self.__options

    # focused
    @property
    def focused(self):
        return self._get_attr("focused", data_type="bool", def_value=False)

    @focused.setter
    @beartype
    def focused(self, value: Optional[bool]):
        self._set_attr("focused", value)

    # multi_select
    @property
    def multi_select(self):
        return self._get_attr("multiselect", data_type="bool", def_value=False)

    @multi_select.setter
    @beartype
    def multi_select(self, value: Optional[bool]):
        self._set_attr("multiselect", value)

    # allow_free_form
    @property
    def allow_free_form(self):
        return self._get_attr("allowfreeform", data_type="bool", def_value=False)

    @allow_free_form.setter
    @beartype
    def allow_free_form(self, value: Optional[bool]):
        self._set_attr("allowfreeform", value)

    # auto_complete
    @property
    def auto_complete(self):
        return self._get_attr("autocomplete", data_type="bool", def_value=True)

    @auto_complete.setter
    @beartype
    def auto_complete(self, value: Optional[bool]):
        self._set_attr("autocomplete", value)

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


class Option(Control):
    def __init__(
        self, key=None, text=None, item_type: ItemType = None, disabled=None, ref=None
    ):
        Control.__init__(self, ref=ref, disabled=disabled)
        assert key != None or text != None, "key or text must be specified"
        self.key = key
        self.text = text
        self.item_type = item_type
        self.disabled = disabled

    def _get_control_name(self):
        return "option"

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

    # item_type
    @property
    def item_type(self):
        return self._get_attr("itemtype")

    @item_type.setter
    @beartype
    def item_type(self, value: ItemType):
        self._set_attr("itemtype", value)
