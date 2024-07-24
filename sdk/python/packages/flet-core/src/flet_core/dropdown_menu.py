from typing import Any, List, Optional, Union

from flet_core.border import BorderSide
from flet_core.buttons import ButtonStyle
from flet_core.control import Control, OptionalNumber
from flet_core.dropdown import Option
from flet_core.form_field_control import FormFieldControl, InputBorder
from flet_core.menu_bar import MenuStyle
from flet_core.ref import Ref
from flet_core.text_style import TextStyle
from flet_core.textfield import InputFilter, TextCapitalization
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    OptionalEventCallable,
    DurationValue,
)


class DropdownMenuOption(Option):
    def __init__(
        self,
        key: Optional[str] = None,
        text: Optional[str] = None,
        content: Optional[Control] = None,
        prefix: Optional[Control] = None,
        prefix_icon: Optional[str] = None,
        suffix: Optional[Control] = None,
        suffix_icon: Optional[str] = None,
        style: Optional[ButtonStyle] = None,
        #
        # Control
        #
        ref=None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
    ):
        Option.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
            key=key,
            text=text,
            content=content,
        )
        self.prefix = prefix
        self.suffix = suffix
        self.prefix_icon = prefix_icon
        self.suffix_icon = suffix_icon
        self.style = style

    def _get_control_name(self):
        return "dropdownmenuoption"

    def _get_children(self):
        children = super()._get_children()
        if self.__suffix is not None:
            self.__suffix._set_attr_internal("n", "suffix")
            children.append(self.__suffix)
        if self.__prefix is not None:
            self.__prefix._set_attr_internal("n", "prefix")
            children.append(self.__prefix)
        return children

    def before_update(self):
        super().before_update()
        assert (
            self.key is not None or self.text is not None
        ), "key or text must be specified"
        self._set_attr_json("style", self.__style)

    # prefix
    @property
    def prefix(self) -> Optional[Control]:
        return self.prefix

    @prefix.setter
    def prefix(self, value: Optional[Control]):
        self.__prefix = value

    # suffix
    @property
    def suffix(self) -> Optional[Control]:
        return self.__suffix

    @suffix.setter
    def suffix(self, value: Optional[Control]):
        self.__suffix = value

    # style
    @property
    def style(self) -> Optional[ButtonStyle]:
        return self.__style

    @style.setter
    def style(self, value: Optional[ButtonStyle]):
        self.__style = value

    # prefix_icon
    @property
    def prefix_icon(self) -> Optional[str]:
        return self.__prefix_icon

    @prefix_icon.setter
    def prefix_icon(self, value: Optional[str]):
        self.__prefix_icon = value

    # suffix_icon
    @property
    def suffix_icon(self) -> Optional[str]:
        return self.__suffix_icon

    @suffix_icon.setter
    def suffix_icon(self, value: Optional[str]):
        self.__suffix_icon = value


class DropdownMenu(FormFieldControl):
    """
    A dropdown menu control that allows users to select a single option from a list of options.

    -----

    Online docs: https://flet.dev/docs/controls/dropdownmenu
    """

    def __init__(
        self,
        value: Optional[str] = None,
        options: Optional[List[DropdownMenuOption]] = None,
        label_content: Optional[str] = None,
        enable_filter: Optional[bool] = None,
        enable_search: Optional[bool] = None,
        request_focus_on_tap: Optional[bool] = None,
        menu_height: OptionalNumber = None,
        expanded_insets: PaddingValue = None,
        menu_style: Optional[MenuStyle] = None,
        selected_suffix: Optional[Control] = None,
        input_filter: Optional[InputFilter] = None,
        capitalization: Optional[TextCapitalization] = None,
        selected_suffix_icon: Optional[str] = None,
        on_change: OptionalEventCallable = None,
        on_focus: OptionalEventCallable = None,
        on_blur: OptionalEventCallable = None,
        #
        # FormField specific
        #
        text_size: OptionalNumber = None,
        text_style: Optional[TextStyle] = None,
        label: Optional[str] = None,
        label_style: Optional[TextStyle] = None,
        border: Optional[InputBorder] = None,
        color: Optional[str] = None,
        focused_color: Optional[str] = None,
        focused_bgcolor: Optional[str] = None,
        border_width: OptionalNumber = None,
        border_color: Optional[str] = None,
        focused_border_width: OptionalNumber = None,
        focused_border_color: Optional[str] = None,
        content_padding: PaddingValue = None,
        dense: Optional[bool] = None,
        filled: Optional[bool] = None,
        fill_color: Optional[str] = None,
        hover_color: Optional[str] = None,
        hint_text: Optional[str] = None,
        hint_style: Optional[TextStyle] = None,
        helper_text: Optional[str] = None,
        helper_style: Optional[TextStyle] = None,
        counter_style: Optional[TextStyle] = None,
        error_text: Optional[str] = None,
        error_text_style: Optional[TextStyle] = None,
        prefix: Optional[Control] = None,
        prefix_icon: Optional[str] = None,
        prefix_style: Optional[TextStyle] = None,
        suffix: Optional[Control] = None,
        suffix_icon: Optional[str] = None,
        suffix_style: Optional[TextStyle] = None,
        icon_color: Optional[str] = None,
        prefix_icon_color: Optional[str] = None,
        suffix_icon_color: Optional[str] = None,
        focus_color: Optional[str] = None,
        align_label_with_hint: Optional[bool] = None,
        floating_label_text_style: Optional[TextStyle] = None,
        active_indicator_border_side: Optional[BorderSide] = None,
        hint_fade_duration: DurationValue = None,
        error_max_lines: OptionalNumber = None,
        helper_max_lines: OptionalNumber = None,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
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
            text_size=text_size,
            text_style=text_style,
            label=label,
            label_style=label_style,
            border=border,
            color=color,
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
            hover_color=hover_color,
            hint_text=hint_text,
            hint_style=hint_style,
            helper_text=helper_text,
            helper_style=helper_style,
            counter_text_style=counter_style,
            error_text=error_text,
            error_text_style=error_text_style,
            prefix=prefix,
            prefix_icon=prefix_icon,
            prefix_text_style=prefix_style,
            suffix=suffix,
            suffix_icon=suffix_icon,
            suffix_text_style=suffix_style,
            icon_color=icon_color,
            prefix_icon_color=prefix_icon_color,
            suffix_icon_color=suffix_icon_color,
            focus_color=focus_color,
            align_label_with_hint=align_label_with_hint,
            floating_label_text_style=floating_label_text_style,
            active_indicator_border_side=active_indicator_border_side,
            hint_fade_duration=hint_fade_duration,
            error_max_lines=error_max_lines,
            helper_max_lines=helper_max_lines,
            ref=ref,
            key=key,
            width=width,
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
        )

        self.options = options
        self.selected_suffix = selected_suffix
        self.input_filter = input_filter
        self.enable_filter = enable_filter
        self.enable_search = enable_search
        self.request_focus_on_tap = request_focus_on_tap
        self.menu_height = menu_height
        self.expanded_insets = expanded_insets
        self.menu_style = menu_style
        self.capitalization = capitalization
        self.label_content = label_content
        self.selected_suffix_icon = selected_suffix_icon
        self.on_change = on_change
        self.on_focus = on_focus
        self.on_blur = on_blur
        self.value = value

    def _get_control_name(self):
        return "dropdownmenu"

    def before_update(self):
        super().before_update()
        self._set_attr_json("inputFilter", self.__input_filter)
        self._set_attr_json("expandInsets", self.__expanded_insets)
        self._set_attr_json("menuStyle", self.__menu_style)
        self.expand_loose = self.expand  # to fix a display issue

    def _get_children(self):
        children = FormFieldControl._get_children(self) + self.__options
        if isinstance(self.__selected_suffix, Control):
            self.__selected_suffix._set_attr_internal("n", "selectedSuffix")
            children.append(self.__selected_suffix)

        if isinstance(self.__label_content, Control):
            self.__label_content._set_attr_internal("n", "label")
            children.append(self.__label_content)
        return children

    # value
    @property
    def value(self) -> Optional[str]:
        return self._get_attr("value")

    @value.setter
    def value(self, value: Optional[str]):
        self._set_attr("value", value)

    # options
    @property
    def options(self) -> Optional[List[DropdownMenuOption]]:
        return self.__options

    @options.setter
    def options(self, value: Optional[List[DropdownMenuOption]]):
        self.__options = value if value is not None else []

    # selected_suffix
    @property
    def selected_suffix(self) -> Optional[Control]:
        return self.__selected_suffix

    @selected_suffix.setter
    def selected_suffix(self, value: Optional[Control]):
        self.__selected_suffix = value

    # label_content
    @property
    def label_content(self) -> Optional[Control]:
        return self.__label_content

    @label_content.setter
    def label_content(self, value: Optional[Control]):
        self.__label_content = value

    # input_filter
    @property
    def input_filter(self) -> Optional[InputFilter]:
        return self.__input_filter

    @input_filter.setter
    def input_filter(self, value: Optional[InputFilter]):
        self.__input_filter = value

    # capitalization
    @property
    def capitalization(self) -> Optional[TextCapitalization]:
        return self.__capitalization

    @capitalization.setter
    def capitalization(self, value: Optional[TextCapitalization]):
        self.__capitalization = value
        self._set_enum_attr("capitalization", value, TextCapitalization)

    # enable_filter
    @property
    def enable_filter(self) -> Optional[bool]:
        return self._get_attr("enableFilter", data_type="bool", def_value=False)

    @enable_filter.setter
    def enable_filter(self, value: Optional[bool]):
        self._set_attr("enableFilter", value)

    # enable_search
    @property
    def enable_search(self) -> Optional[bool]:
        return self._get_attr("enableSearch", data_type="bool", def_value=True)

    @enable_search.setter
    def enable_search(self, value: Optional[bool]):
        self._set_attr("enableSearch", value)

    # request_focus_on_tap
    @property
    def request_focus_on_tap(self) -> Optional[bool]:
        return self._get_attr("requestFocusOnTap", data_type="bool", def_value=True)

    @request_focus_on_tap.setter
    def request_focus_on_tap(self, value: Optional[bool]):
        self._set_attr("requestFocusOnTap", value)

    # selected_suffix_icon
    @property
    def selected_suffix_icon(self) -> Optional[str]:
        return self._get_attr("selectedSuffixIcon")

    @selected_suffix_icon.setter
    def selected_suffix_icon(self, value: Optional[str]):
        self._set_attr("selectedSuffixIcon", value)

    # menu_height
    @property
    def menu_height(self) -> OptionalNumber:
        return self._get_attr("menuHeight", data_type="float")

    @menu_height.setter
    def menu_height(self, value: OptionalNumber):
        self._set_attr("menuHeight", value)

    # expanded_insets
    @property
    def expanded_insets(self) -> PaddingValue:
        return self.__expanded_insets

    @expanded_insets.setter
    def expanded_insets(self, value: PaddingValue):
        self.__expanded_insets = value

    # menu_style
    @property
    def menu_style(self) -> Optional[MenuStyle]:
        return self.__menu_style

    @menu_style.setter
    def menu_style(self, value: Optional[MenuStyle]):
        self.__menu_style = value

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
