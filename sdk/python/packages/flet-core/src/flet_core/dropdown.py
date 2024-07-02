import time
from typing import Any, List, Optional, Union

from flet_core.alignment import Alignment
from flet_core.control import Control, OptionalNumber
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
    OptionalEventCallable,
)
from flet_core.utils import deprecated


class Option(Control):
    def __init__(
        self,
        key: Optional[str] = None,
        text: Optional[str] = None,
        content: Optional[Control] = None,
        alignment: Optional[Alignment] = None,
        text_style: Optional[TextStyle] = None,
        on_click: OptionalEventCallable = None,
        #
        # Control
        #
        ref=None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
    ):
        Control.__init__(self, ref=ref, disabled=disabled, visible=visible, data=data)
        self.key = key
        self.text = text
        self.content = content
        self.on_click = on_click
        self.alignment = alignment
        self.text_style = text_style

    def _get_control_name(self):
        return "dropdownoption"

    def _get_children(self):
        children = []
        if self.__content is not None:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    def before_update(self):
        super().before_update()
        assert (
            self.key is not None or self.text is not None
        ), "key or text must be specified"
        self._set_attr_json("alignment", self.__alignment)
        if isinstance(self.__text_style, TextStyle):
            self._set_attr_json("textStyle", self.__text_style)

    # key
    @property
    def key(self) -> Optional[str]:
        return self._get_attr("key")

    @key.setter
    def key(self, value: Optional[str]):
        self._set_attr("key", value)

    # text
    @property
    def text(self) -> Optional[str]:
        return self._get_attr("text")

    @text.setter
    def text(self, value: Optional[str]):
        self._set_attr("text", value)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # alignment
    @property
    def alignment(self) -> Optional[Alignment]:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value

    # text_style
    @property
    def text_style(self) -> Optional[TextStyle]:
        return self.__text_style

    @text_style.setter
    def text_style(self, value: Optional[TextStyle]):
        self.__text_style = value

    # on_click
    @property
    def on_click(self) -> OptionalEventCallable:
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler: OptionalEventCallable):
        self._add_event_handler("click", handler)


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
        value: Optional[str] = None,
        options: Optional[List[Option]] = None,
        alignment: Optional[Alignment] = None,
        autofocus: Optional[bool] = None,
        hint_content: Optional[Control] = None,
        icon_content: Optional[Control] = None,
        elevation: OptionalNumber = None,
        item_height: OptionalNumber = None,
        max_menu_height: OptionalNumber = None,
        icon_size: OptionalNumber = None,
        enable_feedback: Optional[bool] = None,
        padding: PaddingValue = None,
        icon_enabled_color: Optional[str] = None,
        icon_disabled_color: Optional[str] = None,
        on_change: OptionalEventCallable = None,
        on_focus: OptionalEventCallable = None,
        on_blur: OptionalEventCallable = None,
        on_click: OptionalEventCallable = None,
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
        fill_color: Optional[str] = None,
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
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
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
        on_animation_end: OptionalEventCallable = None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        FormFieldControl.__init__(
            self,
            ref=ref,
            key=key,
            width=width,
            height=height,
            expand=expand,
            expand_loose=expand_loose,
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
            fill_color=fill_color,
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
        self.elevation = elevation
        self.hint_content = hint_content
        self.icon_content = icon_content
        self.padding = padding
        self.enable_feedback = enable_feedback
        self.on_focus = on_focus
        self.on_blur = on_blur
        self.on_change = on_change
        self.item_height = item_height
        self.max_menu_height = max_menu_height
        self.icon_size = icon_size
        self.icon_enabled_color = icon_enabled_color
        self.icon_disabled_color = icon_disabled_color
        self.on_click = on_click

    def _get_control_name(self):
        return "dropdown"

    def before_update(self):
        super().before_update()
        self._set_attr_json("padding", self.__padding)
        self._set_attr_json("alignment", self.__alignment)
        if (
            (
                self.bgcolor is not None
                or self.fill_color is not None
                or self.focused_bgcolor is not None
            )
        ) and self.filled is None:
            self.filled = True  # required to display any of the above colors

    def _get_children(self):
        children = FormFieldControl._get_children(self) + self.__options
        if isinstance(self.__hint_content, Control):
            self.__hint_content._set_attr_internal("n", "hint")
            children.append(self.__hint_content)
        if isinstance(self.__icon_content, Control):
            self.__icon_content._set_attr_internal("n", "icon")
            children.append(self.__icon_content)
        return children

    def focus(self):
        self._set_attr_json("focus", str(time.time()))
        self.update()

    @deprecated(
        reason="Use focus() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def focus_async(self):
        self.focus()

    # options
    @property
    def options(self):
        return self.__options

    @options.setter
    def options(self, value):
        self.__options = value if value is not None else []

    # icon_content
    @property
    def icon_content(self) -> Optional[Control]:
        return self.__icon_content

    @icon_content.setter
    def icon_content(self, value: Optional[Control]):
        self.__icon_content = value

    # hint_content
    @property
    def hint_content(self) -> Optional[Control]:
        return self.__hint_content

    @hint_content.setter
    def hint_content(self, value: Optional[Control]):
        self.__hint_content = value

    # value
    @property
    def value(self) -> Optional[str]:
        return self._get_attr("value")

    @value.setter
    def value(self, value: Optional[str]):
        self._set_attr("value", value)

    # icon_enabled_color
    @property
    def icon_enabled_color(self) -> Optional[str]:
        return self._get_attr("iconEnabledColor")

    @icon_enabled_color.setter
    def icon_enabled_color(self, value: Optional[str]):
        self._set_attr("iconEnabledColor", value)

    # icon_disabled_color
    @property
    def icon_disabled_color(self) -> Optional[str]:
        return self._get_attr("iconDisabledColor")

    @icon_disabled_color.setter
    def icon_disabled_color(self, value: Optional[str]):
        self._set_attr("iconDisabledColor", value)

    # item_height
    @property
    def item_height(self) -> OptionalNumber:
        return self._get_attr("itemHeight", data_type="float")

    @item_height.setter
    def item_height(self, value: OptionalNumber):
        assert (
            value is None or value >= 48.0
        ), "item_height must be greater than or equal to 48.0"
        self._set_attr("itemHeight", value)

    # menu_max_height
    @property
    def menu_max_height(self) -> OptionalNumber:
        return self._get_attr("menuMaxHeight", data_type="float")

    @menu_max_height.setter
    def menu_max_height(self, value: OptionalNumber):
        self._set_attr("menuMaxHeight", value)

    # icon_size
    @property
    def icon_size(self) -> OptionalNumber:
        return self._get_attr("iconSize", data_type="float", def_value=24.0)

    @icon_size.setter
    def icon_size(self, value: OptionalNumber):
        self._set_attr("iconSize", value)

    # padding
    @property
    def padding(self) -> PaddingValue:
        return self.__padding

    @padding.setter
    def padding(self, value: PaddingValue):
        self.__padding = value

    # autofocus
    @property
    def autofocus(self) -> Optional[bool]:
        return self._get_attr("autofocus", data_type="bool", def_value=False)

    @autofocus.setter
    def autofocus(self, value: Optional[bool]):
        self._set_attr("autofocus", value)

    # enable_feedback
    @property
    def enable_feedback(self) -> Optional[bool]:
        return self._get_attr("enableFeedback", data_type="bool", def_value=True)

    @enable_feedback.setter
    def enable_feedback(self, value: Optional[bool]):
        self._set_attr("enableFeedback", value)

    # elevation
    @property
    def elevation(self) -> OptionalNumber:
        return self._get_attr("elevation", data_type="float", def_value=8)

    @elevation.setter
    def elevation(self, value: OptionalNumber):
        self._set_attr("elevation", value)

    # alignment
    @property
    def alignment(self) -> Optional[Alignment]:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value

    # on_change
    @property
    def on_change(self) -> OptionalEventCallable:
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler: OptionalEventCallable):
        self._add_event_handler("change", handler)

    # on_focus
    @property
    def on_focus(self) -> OptionalEventCallable:
        return self._get_event_handler("focus")

    @on_focus.setter
    def on_focus(self, handler: OptionalEventCallable):
        self._add_event_handler("focus", handler)

    # on_blur
    @property
    def on_blur(self) -> OptionalEventCallable:
        return self._get_event_handler("blur")

    @on_blur.setter
    def on_blur(self, handler: OptionalEventCallable):
        self._add_event_handler("blur", handler)

    # on_click
    @property
    def on_click(self) -> OptionalEventCallable:
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler: OptionalEventCallable):
        self._add_event_handler("click", handler)
