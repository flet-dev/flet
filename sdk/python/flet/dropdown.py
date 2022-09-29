from typing import Any, Optional, Union

from beartype import beartype

from flet.control import Control, InputBorder, OptionalNumber
from flet.focus import FocusData
from flet.form_field_control import FormFieldControl
from flet.ref import Ref
from flet.types import (
    AnimationValue,
    BorderRadiusValue,
    OffsetValue,
    PaddingValue,
    RotateValue,
    ScaleValue,
)


class Dropdown(FormFieldControl):
    def __init__(
        self,
        ref: Optional[Ref] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        opacity: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        on_animation_end=None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # FormField specific
        #
        text_size: OptionalNumber = None,
        label: Optional[str] = None,
        icon: Optional[str] = None,
        border: InputBorder = None,
        color: Optional[str] = None,
        bgcolor: Optional[str] = None,
        border_radius: BorderRadiusValue = None,
        border_width: OptionalNumber = None,
        border_color: Optional[str] = None,
        focused_color: Optional[str] = None,
        focused_bgcolor: Optional[str] = None,
        focused_border_width: OptionalNumber = None,
        focused_border_color: Optional[str] = None,
        content_padding: PaddingValue = None,
        filled: Optional[bool] = None,
        hint_text: Optional[str] = None,
        helper_text: Optional[str] = None,
        counter_text: Optional[str] = None,
        error_text: Optional[str] = None,
        prefix: Optional[Control] = None,
        prefix_icon: Optional[str] = None,
        prefix_text: Optional[str] = None,
        suffix: Optional[Control] = None,
        suffix_icon: Optional[str] = None,
        suffix_text: Optional[str] = None,
        #
        # DropDown Specific
        #
        value: Optional[str] = None,
        autofocus: Optional[bool] = None,
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
            rotate=rotate,
            scale=scale,
            offset=offset,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
            #
            # FormField specific
            #
            text_size=text_size,
            label=label,
            icon=icon,
            border=border,
            color=color,
            bgcolor=bgcolor,
            border_radius=border_radius,
            border_width=border_width,
            border_color=border_color,
            focused_color=focused_color,
            focused_bgcolor=focused_bgcolor,
            focused_border_width=focused_border_width,
            focused_border_color=focused_border_color,
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
    def autofocus(self) -> Optional[bool]:
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
        assert key is not None or text is not None, "key or text must be specified"
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
