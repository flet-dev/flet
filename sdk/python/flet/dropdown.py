from typing import Optional, Union

from beartype import beartype

from flet.control import Control, InputBorder, OptionalNumber, PaddingValue
from flet.focus import FocusData
from flet.form_field_control import FormFieldControl
from flet.ref import Ref


class Dropdown(FormFieldControl):
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
        # FormField specific
        #
        label: str = None,
        icon: str = None,
        border: InputBorder = None,
        content_padding: PaddingValue = None,
        filled: bool = None,
        hint_text: str = None,
        helper_text: str = None,
        counter_text: str = None,
        error_text: str = None,
        prefix: Control = None,
        prefix_icon: str = None,
        prefix_text: str = None,
        suffix: Control = None,
        suffix_icon: str = None,
        suffix_text: str = None,
        #
        # DropDown Specific
        #
        value: str = None,
        autofocus: bool = None,
        options=None,
        on_change=None,
        on_focus=None,
        on_blur=None,
    ):
        FormFieldControl.__init__(
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
            #
            # FormField specific
            #
            label=label,
            icon=icon,
            border=border,
            content_padding=content_padding,
            filled=filled,
            hint_text=hint_text,
            helper_text=helper_text,
            counter_text=counter_text,
            error_text=error_text,
            prefix=prefix,
            prefix_icon=prefix_icon,
            prefix_text=prefix_text,
            suffix=suffix,
            suffix_icon=suffix_icon,
            suffix_text=suffix_text,
        )

        self.__options = []
        self.value = value
        self.autofocus = autofocus
        self.options = options
        self.on_focus = on_focus
        self.on_blur = on_blur
        self.on_change = on_change

    def _get_control_name(self):
        return "dropdown"

    def _get_children(self):
        result = FormFieldControl._get_children(self)
        result.extend(self.__options)
        return result

    def focus(self):
        self._set_attr_json("focus", FocusData())
        self.update()

    # options
    @property
    def options(self):
        return self.__options

    @options.setter
    def options(self, value):
        self.__options = value or []

    # value
    @property
    def value(self):
        return self._get_attr("value")

    @value.setter
    def value(self, value):
        self._set_attr("value", value)

    # autofocus
    @property
    def autofocus(self):
        return self._get_attr("autofocus", data_type="bool", def_value=False)

    @autofocus.setter
    @beartype
    def autofocus(self, value: Optional[bool]):
        self._set_attr("autofocus", value)

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)

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
    def __init__(self, key=None, text=None, disabled=None, ref=None):
        Control.__init__(self, ref=ref, disabled=disabled)
        assert key != None or text != None, "key or text must be specified"
        self.key = key
        self.text = text
        self.disabled = disabled

    def _get_control_name(self):
        return "dropdownoption"

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
