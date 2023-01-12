from typing import Any, Optional, Union

from flet_core.alignment import Alignment
from flet_core.control import Control, OptionalNumber
from flet_core.focus import FocusData
from flet_core.form_field_control import FormFieldControl, InputBorder
from flet_core.ref import Ref
from flet_core.text_style import TextStyle
from flet_core.types import (
    AnimationValue,
    BorderRadiusValue,
    OffsetValue,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class Dropdown(FormFieldControl):
    """
    A dropdown lets the user select from a number of items. The dropdown shows the currently selected item as well as an arrow that opens a menu for selecting another item.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        def button_clicked(e):
            t.value = f"Dropdown value is:  {dd.value}"
            page.update()

        t = ft.Text()
        b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
        dd = ft.Dropdown(
            width=200,
            options=[
                ft.dropdown.Option("Red"),
                ft.dropdown.Option("Green"),
                ft.dropdown.Option("Blue"),
            ],
        )
        page.add(dd, b, t)

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/dropdown
    """

    def __init__(
        self,
        ref: Optional[Ref] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        aspect_ratio: OptionalNumber = None,
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
        text_style: Optional[TextStyle] = None,
        label: Optional[str] = None,
        label_style: Optional[TextStyle] = None,
        icon: Optional[str] = None,
        border: Optional[InputBorder] = None,
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
        dense: Optional[bool] = None,
        filled: Optional[bool] = None,
        hint_text: Optional[str] = None,
        hint_style: Optional[TextStyle] = None,
        helper_text: Optional[str] = None,
        helper_style: Optional[TextStyle] = None,
        counter_text: Optional[str] = None,
        counter_style: Optional[TextStyle] = None,
        error_text: Optional[str] = None,
        error_style: Optional[TextStyle] = None,
        prefix: Optional[Control] = None,
        prefix_icon: Optional[str] = None,
        prefix_text: Optional[str] = None,
        prefix_style: Optional[TextStyle] = None,
        suffix: Optional[Control] = None,
        suffix_icon: Optional[str] = None,
        suffix_text: Optional[str] = None,
        suffix_style: Optional[TextStyle] = None,
        #
        # DropDown Specific
        #
        value: Optional[str] = None,
        autofocus: Optional[bool] = None,
        options=None,
        alignment: Optional[Alignment] = None,
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
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
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
            text_style=text_style,
            label=label,
            label_style=label_style,
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
            dense=dense,
            filled=filled,
            hint_text=hint_text,
            hint_style=hint_style,
            helper_text=helper_text,
            helper_style=helper_style,
            counter_text=counter_text,
            counter_style=counter_style,
            error_text=error_text,
            error_style=error_style,
            prefix=prefix,
            prefix_icon=prefix_icon,
            prefix_text=prefix_text,
            prefix_style=prefix_style,
            suffix=suffix,
            suffix_icon=suffix_icon,
            suffix_text=suffix_text,
            suffix_style=suffix_style,
        )

        self.__options = []
        self.value = value
        self.autofocus = autofocus
        self.options = options
        self.alignment = alignment
        self.on_focus = on_focus
        self.on_blur = on_blur
        self.on_change = on_change

    def _get_control_name(self):
        return "dropdown"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("alignment", self.__alignment)

    def _get_children(self):
        result = FormFieldControl._get_children(self)
        result.extend(self.__options)
        return result

    def focus(self):
        self._set_attr_json("focus", FocusData())
        self.update()

    async def focus_async(self):
        self._set_attr_json("focus", FocusData())
        await self.update_async()

    # options
    @property
    def options(self):
        return self.__options

    @options.setter
    def options(self, value):
        self.__options = value if value is not None else []

    # value
    @property
    def value(self) -> Optional[str]:
        return self._get_attr("value")

    @value.setter
    def value(self, value: Optional[str]):
        self._set_attr("value", value)

    # autofocus
    @property
    def autofocus(self) -> Optional[bool]:
        return self._get_attr("autofocus", data_type="bool", def_value=False)

    @autofocus.setter
    def autofocus(self, value: Optional[bool]):
        self._set_attr("autofocus", value)

    # alignment
    @property
    def alignment(self) -> Optional[Alignment]:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value

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
