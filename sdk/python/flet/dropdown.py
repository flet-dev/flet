from typing import Optional

from beartype import beartype

from flet.control import Control, InputBorder, OptionalNumber
from flet.form_field_control import FormFieldControl
from flet.ref import Ref


class Dropdown(FormFieldControl):
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
        # FormField specific
        #
        label: str = None,
        icon: str = None,
        border: InputBorder = None,
        filled: bool = None,
        hint_text: str = None,
        helper_text: str = None,
        counter_text: str = None,
        error_text: str = None,
        prefix: Control = None,
        suffix: Control = None,
        #
        # DropDown Specific
        #
        value: str = None,
        on_change=None,
        options=None,
    ):
        FormFieldControl.__init__(
            self,
            ref=ref,
            width=width,
            height=height,
            expand=expand,
            opacity=opacity,
            visible=visible,
            disabled=disabled,
            data=data,
            #
            # FormField specific
            #
            label=label,
            icon=icon,
            border=border,
            filled=filled,
            hint_text=hint_text,
            helper_text=helper_text,
            counter_text=counter_text,
            error_text=error_text,
            prefix=prefix,
            suffix=suffix,
        )

        self.__options = []
        self.value = value
        self.options = options
        self.on_change = on_change

    def _get_control_name(self):
        return "dropdown"

    def _get_children(self):
        return FormFieldControl._get_children().extend(self.__options)

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

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)


class Option(Control):
    def __init__(self, key=None, text=None, disabled=None, ref=None):
        Control.__init__(self, ref=ref, disabled=disabled)
        assert key != None or text != None, "key or text must be specified"
        self.key = key
        self.text = text
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
