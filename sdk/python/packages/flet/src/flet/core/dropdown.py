import time
import warnings
from typing import Any, Dict, List, Optional, Union

from flet.core.alignment import Alignment
from flet.core.animation import AnimationValue
from flet.core.buttons import ButtonStyle
from flet.core.control import Control, OptionalNumber
from flet.core.form_field_control import FormFieldControl, InputBorder
from flet.core.menu_bar import MenuStyle
from flet.core.ref import Ref
from flet.core.text_style import TextStyle
from flet.core.textfield import InputFilter, TextCapitalization
from flet.core.types import (
    BorderRadiusValue,
    ColorValue,
    ControlState,
    ControlStateValue,
    IconEnums,
    IconValueOrControl,
    Number,
    OffsetValue,
    OptionalControlEventCallable,
    OptionalEventCallable,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    TextAlign,
)


class Option(Control):
    def __init__(
        self,
        key: Optional[str] = None,
        text: Optional[str] = None,
        content: Optional[Control] = None,
        leading_icon: Optional[IconValueOrControl] = None,
        trailing_icon: Optional[IconValueOrControl] = None,
        style: Optional[ButtonStyle] = None,
        alignment: Optional[Alignment] = None,  # to be deprecated
        text_style: Optional[TextStyle] = None,  # to be deprecated
        on_click: OptionalControlEventCallable = None,  # to be deprecated
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
        self.leading_icon = leading_icon
        self.trailing_icon = trailing_icon
        self.style = style

        deprecated_properties_list = ["text_style", "on_click", "alignment"]

        for item in deprecated_properties_list:
            if eval(item) is not None:
                warnings.warn(
                    f"{item} is deprecated since version 0.27.0 "
                    f"and will be removed in version 0.30.0.",
                    category=DeprecationWarning,
                    stacklevel=2,
                )

    def _get_control_name(self):
        return "dropdownoption"

    def _get_children(self):
        children = super()._get_children()
        if isinstance(self.__leading_icon, Control):
            self.__leading_icon._set_attr_internal("n", "leadingIcon")
            children.append(self.__leading_icon)
        if isinstance(self.__trailing_icon, Control):
            self.__trailing_icon._set_attr_internal("n", "trailing_icon")
            children.append(self.__trailing_icon)
        if isinstance(self.__content, Control):
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    def before_update(self):
        super().before_update()
        assert (
            self.key is not None or self.text is not None
        ), "key or text must be specified"
        self._set_attr_json("style", self.__style)

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

    # style
    @property
    def style(self) -> Optional[ButtonStyle]:
        return self.__style

    @style.setter
    def style(self, value: Optional[ButtonStyle]):
        self.__style = value

    # leading_icon
    @property
    def leading_icon(self) -> Optional[IconValueOrControl]:
        return self.__leading_icon

    @leading_icon.setter
    def leading_icon(self, value: Optional[IconValueOrControl]):
        self.__leading_icon = value
        if not isinstance(value, Control):
            self._set_enum_attr("leadingIcon", value, IconEnums)

    # trailing_icon
    @property
    def trailing_icon(self) -> Optional[IconValueOrControl]:
        return self.__trailing_icon

    @trailing_icon.setter
    def trailing_icon(self, value: Optional[IconValueOrControl]):
        self.__trailing_icon = value
        if not isinstance(value, Control):
            self._set_enum_attr("trailingIcon", value, IconEnums)


class DropdownOption(Option):
    """Alias for Option"""


class Dropdown(FormFieldControl):
    """
    A dropdown control that allows users to select a single option from a list of options.
    -----
    Online docs: https://flet.dev/docs/controls/dropdown
    """

    def __init__(
        self,
        value: Optional[str] = None,
        autofocus: Optional[bool] = None,
        text_align: Optional[TextAlign] = None,
        elevation: ControlStateValue[OptionalNumber] = None,
        options: Optional[List[Option]] = None,
        label_content: Optional[str] = None,
        enable_filter: Optional[bool] = None,
        enable_search: Optional[bool] = None,
        editable: Optional[bool] = None,
        max_menu_height: OptionalNumber = None,  # to be discontinued
        menu_height: OptionalNumber = None,
        menu_width: OptionalNumber = None,
        expanded_insets: PaddingValue = None,
        selected_suffix: Optional[Control] = None,
        input_filter: Optional[InputFilter] = None,
        capitalization: Optional[TextCapitalization] = None,
        options_fill_horizontally: Optional[bool] = None,  # to be deprecated
        padding: Optional[PaddingValue] = None,  # to be deprecated
        trailing_icon: Optional[IconValueOrControl] = None,
        leading_icon: Optional[IconValueOrControl] = None,
        select_icon: Optional[IconValueOrControl] = None,  # to be deprecated
        selected_trailing_icon: Optional[IconValueOrControl] = None,
        on_change: OptionalEventCallable = None,
        on_focus: OptionalEventCallable = None,
        on_blur: OptionalEventCallable = None,
        enable_feedback: Optional[bool] = None,  # to be deprecated
        item_height: OptionalNumber = None,  # to be deprecated
        alignment: Optional[Alignment] = None,  # to be deprecated
        hint_content: Optional[Control] = None,  # to be deprecated
        icon_content: Optional[Control] = None,  # to be deprecated
        select_icon_size: OptionalNumber = None,  # to be deprecated
        icon_size: OptionalNumber = None,  # to be deprecated
        select_icon_enabled_color: Optional[ColorValue] = None,  # to be deprecated
        icon_enabled_color: Optional[ColorValue] = None,  # to be deprecated
        select_icon_disabled_color: Optional[ColorValue] = None,  # to be deprecated
        icon_disabled_color: Optional[ColorValue] = None,  # to be deprecated
        #
        # FormField specific
        #
        bgcolor: Optional[ColorValue] = None,
        error_style: Optional[TextStyle] = None,
        error_text: Optional[str] = None,
        text_size: OptionalNumber = None,
        text_style: Optional[TextStyle] = None,
        label: Optional[str] = None,
        label_style: Optional[TextStyle] = None,
        icon: Optional[IconValueOrControl] = None,  # to deprecated
        border: Optional[InputBorder] = None,
        color: Optional[str] = None,
        focused_color: Optional[str] = None,  # to be deprecated
        focused_bgcolor: Optional[str] = None,  # to be deprecated
        border_width: OptionalNumber = None,
        border_color: Optional[str] = None,
        border_radius: Optional[BorderRadiusValue] = None,
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
        prefix: Optional[Control] = None,  # to be deprecated
        prefix_text: Optional[str] = None,  # to be deprecated
        prefix_style: Optional[TextStyle] = None,  # to be deprecated
        prefix_icon: Optional[str] = None,  # to be deprecated
        disabled_hint_content: Optional[Control] = None,  # to be deprecated
        suffix: Optional[Control] = None,  # to be deprecated
        suffix_icon: Optional[IconValueOrControl] = None,  # to be deprecated
        suffix_text: Optional[str] = None,  # to be deprecated
        suffix_style: Optional[TextStyle] = None,  # to be deprecated
        counter: Optional[Control] = None,  # to be deprecated
        counter_text: Optional[str] = None,  # to be deprecated
        counter_style: Optional[TextStyle] = None,  # to be deprecated
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
            border_radius=border_radius,
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
            error_text=error_text,
            error_style=error_style,
            prefix_icon=prefix_icon,
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

        deprecated_properties_list = [
            "select_icon_size",
            "select_icon_enabled_color",
            "select_icon_disabled_color",
            "suffix",
            "suffix_icon",
            "suffix_style",
            "suffix_text",
            "icon_content",
            "icon_enabled_color",
            "icon_disabled_color",
            "icon_size",
            "icon",
            "hint_content",
            "prefix_text",
            "prefix_style",
            "prefix",
            "prefix_icon",
            "focused_color",
            "disabled_hint_content",
            "alignment",
            "focused_bgcolor",
            "item_height",
            "enable_feedback",
            "options_fill_horizontally",
            "padding",
            "max_menu_height",
        ]

        for item in deprecated_properties_list:
            if eval(item) is not None:
                warnings.warn(
                    f"{item} is deprecated since version 0.27.0 "
                    f"and will be removed in version 0.30.0.",
                    category=DeprecationWarning,
                    stacklevel=2,
                )

        self.options = options
        self.selected_suffix = selected_suffix
        self.input_filter = input_filter
        self.enable_filter = enable_filter
        self.enable_search = enable_search
        self.editable = editable
        self.menu_height = menu_height
        self.menu_width = menu_width
        self.expanded_insets = expanded_insets
        self.capitalization = capitalization
        self.label_content = label_content
        self.leading_icon = leading_icon
        self.trailing_icon = trailing_icon
        self.selected_trailing_icon = selected_trailing_icon
        self.select_icon = select_icon
        self.on_change = on_change
        self.on_focus = on_focus
        self.on_blur = on_blur
        self.value = value
        self.bgcolor = bgcolor
        self.elevation = elevation
        self.text_align = text_align
        self.autofocus = autofocus

    def _get_control_name(self):
        return "dropdown"

    def before_update(self):
        super().before_update()
        self._set_attr_json("bgcolor", self.__bgcolor, wrap_attr_dict=True)
        self._set_attr_json("elevation", self.__elevation, wrap_attr_dict=True)
        ##self._set_attr_json("inputFilter", self.__input_filter)
        ##self._set_attr_json("expandInsets", self.__expanded_insets)
        self.expand_loose = self.expand  # to fix a display issue

    def _get_children(self):
        children = FormFieldControl._get_children(self) + self.__options
        if isinstance(self.__leading_icon, Control):
            self.__leading_icon._set_attr_internal("n", "leading_icon")
            children.append(self.__leading_icon)
        if isinstance(self.__select_icon, Control):
            self.__select_icon._set_attr_internal("n", "select_icon")
            children.append(self.__select_icon)
        if isinstance(self.__trailing_icon, Control):
            self.__trailing_icon._set_attr_internal("n", "trailing_icon")
            children.append(self.__trailing_icon)
        if isinstance(self.__selected_trailing_icon, Control):
            self.__selected_trailing_icon._set_attr_internal(
                "n", "selected_trailing_icon"
            )
            children.append(self.__selected_trailing_icon)
        return children

    def __contains__(self, item):
        return item in self.__options

    def focus(self):
        self._set_attr_json("focus", str(time.time()))
        self.update()

    # value
    @property
    def value(self) -> Optional[str]:
        return self._get_attr("value")

    @value.setter
    def value(self, value: Optional[str]):
        self._set_attr("value", value)

    # options
    @property
    def options(self) -> Optional[List[Option]]:
        return self.__options

    @options.setter
    def options(self, value: Optional[List[Option]]):
        self.__options = value if value is not None else []

    # menu_height
    @property
    def menu_height(self) -> OptionalNumber:
        return self._get_attr("menuHeight", data_type="float")

    @menu_height.setter
    def menu_height(self, value: OptionalNumber):
        self._set_attr("menuHeight", value)

    # menu_width
    @property
    def menu_width(self) -> OptionalNumber:
        return self._get_attr("menuWidth", data_type="float")

    @menu_width.setter
    def menu_width(self, value: OptionalNumber):
        self._set_attr("menuWidth", value)

    # editable
    @property
    def editable(self) -> bool:
        return self._get_attr("editable", data_type="bool", def_value=False)

    @editable.setter
    def editable(self, value: Optional[bool]):
        self._set_attr("editable", value)

    # select_icon
    @property
    def select_icon(self) -> Optional[IconValueOrControl]:
        warnings.warn(
            f"select_icon is deprecated since version 0.27.0 "
            f"and will be removed in version 0.30.0. Use trailing_icon instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return self.__select_icon

    @select_icon.setter
    def select_icon(self, value: Optional[IconValueOrControl]):
        self.__select_icon = value

        if not isinstance(value, Control):
            self._set_enum_attr("selectIcon", value, IconEnums)

        if value is not None:
            warnings.warn(
                f"select_icon is deprecated since version 0.27.0 "
                f"and will be removed in version 0.30.0. Use trailing_icon instead.",
                category=DeprecationWarning,
                stacklevel=2,
            )

    # leading_icon
    @property
    def leading_icon(self) -> Optional[IconValueOrControl]:
        return self.__leading_icon

    @leading_icon.setter
    def leading_icon(self, value: Optional[IconValueOrControl]):
        self.__leading_icon = value
        if not isinstance(value, Control):
            self._set_enum_attr("leadingIcon", value, IconEnums)

    # trailing_icon
    @property
    def trailing_icon(self) -> Optional[IconValueOrControl]:
        return self.__trailing_icon

    @trailing_icon.setter
    def trailing_icon(self, value: Optional[IconValueOrControl]):
        self.__trailing_icon = value
        if not isinstance(value, Control):
            self._set_enum_attr("trailingIcon", value, IconEnums)

    # selected_trailing_icon
    @property
    def selected_trailing_icon(self) -> Optional[IconValueOrControl]:
        return self.__selected_trailing_icon

    @selected_trailing_icon.setter
    def selected_trailing_icon(self, value: Optional[IconValueOrControl]):
        self.__selected_trailing_icon = value
        if not isinstance(value, Control):
            self._set_enum_attr("selectedTrailingIcon", value, IconEnums)

    # bgcolor
    @property
    def bgcolor(self) -> ControlStateValue[ColorValue]:
        return self.__bgcolor

    @bgcolor.setter
    def bgcolor(self, value: ControlStateValue[ColorValue]):
        self.__bgcolor = value

    # text_align
    @property
    def text_align(self) -> Optional[TextAlign]:
        return self.__text_align

    @text_align.setter
    def text_align(self, value: Optional[TextAlign]):
        self.__text_align = value
        self._set_enum_attr("textAlign", value, TextAlign)

    # elevation
    @property
    def elevation(self) -> Union[OptionalNumber, Dict[ControlState, Number]]:
        return self.__elevation

    @elevation.setter
    def elevation(self, value: Union[OptionalNumber, Dict[ControlState, Number]]):
        self.__elevation = value

    # enable_filter
    @property
    def enable_filter(self) -> bool:
        return self._get_attr("enableFilter", data_type="bool", def_value=False)

    @enable_filter.setter
    def enable_filter(self, value: Optional[bool]):
        self._set_attr("enableFilter", value)

    # enable_search
    @property
    def enable_search(self) -> bool:
        return self._get_attr("enableSearch", data_type="bool", def_value=True)

    @enable_search.setter
    def enable_search(self, value: Optional[bool]):
        self._set_attr("enableSearch", value)

    # autofocus
    @property
    def autofocus(self) -> bool:
        return self._get_attr("autofocus", data_type="bool", def_value=False)

    @autofocus.setter
    def autofocus(self, value: Optional[bool]):
        self._set_attr("autofocus", value)

    # on_change
    @property
    def on_change(self) -> OptionalControlEventCallable:
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler: OptionalControlEventCallable):
        self._add_event_handler("change", handler)

    # on_focus
    @property
    def on_focus(self) -> OptionalControlEventCallable:
        return self._get_event_handler("focus")

    @on_focus.setter
    def on_focus(self, handler: OptionalControlEventCallable):
        self._add_event_handler("focus", handler)

    # on_blur
    @property
    def on_blur(self) -> OptionalControlEventCallable:
        return self._get_event_handler("blur")

    @on_blur.setter
    def on_blur(self, handler: OptionalControlEventCallable):
        self._add_event_handler("blur", handler)
