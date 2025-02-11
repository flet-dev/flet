import warnings
from typing import Any, List, Optional, Union

from flet.core.animation import AnimationValue
from flet.core.buttons import ButtonStyle
from flet.core.control import Control, OptionalNumber
from flet.core.dropdown import Option
from flet.core.form_field_control import FormFieldControl, InputBorder
from flet.core.menu_bar import MenuStyle
from flet.core.ref import Ref
from flet.core.text_style import TextStyle
from flet.core.textfield import InputFilter, TextCapitalization
from flet.core.types import (
    BorderRadiusValue,
    ColorValue,
    IconEnums,
    IconValueOrControl,
    OffsetValue,
    OptionalEventCallable,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
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
        editable: Optional[bool] = None,
        max_menu_height: OptionalNumber = None,
        expanded_insets: PaddingValue = None,
        menu_style: Optional[MenuStyle] = None,
        selected_suffix: Optional[Control] = None,
        input_filter: Optional[InputFilter] = None,
        capitalization: Optional[TextCapitalization] = None,
        selected_suffix_icon: Optional[str] = None,
        trailing_icon: Optional[IconValueOrControl] = None,
        select_icon: Optional[IconValueOrControl] = None,
        selected_trailing_icon: Optional[IconValueOrControl] = None,
        on_change: OptionalEventCallable = None,
        on_focus: OptionalEventCallable = None,
        on_blur: OptionalEventCallable = None,
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
        error_style: Optional[TextStyle] = None,  # to be deprecated
        error_text: Optional[str] = None,
        text_size: OptionalNumber = None,
        text_style: Optional[TextStyle] = None,
        label: Optional[str] = None,
        label_style: Optional[TextStyle] = None,
        icon: Optional[IconValueOrControl] = None,
        border: Optional[InputBorder] = None,
        color: Optional[str] = None,
        focused_color: Optional[str] = None,  # to be deprecated
        focused_bgcolor: Optional[str] = None,
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
        prefix: Optional[Control] = None,
        prefix_text: Optional[str] = None,
        prefix_style: Optional[TextStyle] = None,
        prefix_icon: Optional[str] = None,
        suffix: Optional[Control] = None,
        suffix_icon: Optional[IconValueOrControl] = None,
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
            # focused_color=focused_color,
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
            error_text=error_text,
            error_style=error_style,
            # prefix=prefix,
            icon=icon,
            prefix_icon=prefix_icon,
            # suffix=suffix,
            # suffix_icon=suffix_icon,
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
            "bgcolor",
            "hint_content",
            "prefix_text",
            "prefix_style",
            "prefix",
            "focused_color",
        ]

        for item in deprecated_properties_list:
            if eval(item) is not None:
                warnings.warn(
                    f"{item} is deprecated since version 0.26.0 "
                    f"and will be removed in version 0.29.0.",
                    category=DeprecationWarning,
                    stacklevel=2,
                )

        self.options = options
        self.selected_suffix = selected_suffix
        self.input_filter = input_filter
        self.enable_filter = enable_filter
        self.enable_search = enable_search
        self.editable = editable
        self.max_menu_height = max_menu_height
        self.expanded_insets = expanded_insets
        self.menu_style = menu_style
        self.capitalization = capitalization
        self.label_content = label_content
        self.selected_suffix_icon = selected_suffix_icon
        self.trailing_icon = trailing_icon
        self.selected_trailing_icon = selected_trailing_icon
        self.select_icon = select_icon
        self.on_change = on_change
        self.on_focus = on_focus
        self.on_blur = on_blur
        self.value = value

    def _get_control_name(self):
        return "dropdownmenu"

    def before_update(self):
        super().before_update()
        ##self._set_attr_json("inputFilter", self.__input_filter)
        ##self._set_attr_json("expandInsets", self.__expanded_insets)
        # 3self._set_attr_json("menuStyle", self.__menu_style)
        self.expand_loose = self.expand  # to fix a display issue

    # def _get_children(self):
    #     children = FormFieldControl._get_children(self) + self.__options
    #     if isinstance(self.__selected_suffix, Control):
    #         self.__selected_suffix._set_attr_internal("n", "selectedSuffix")
    #         children.append(self.__selected_suffix)

    #     if isinstance(self.__label_content, Control):
    #         self.__label_content._set_attr_internal("n", "label")
    #         children.append(self.__label_content)
    #     return children
    def _get_children(self):
        children = FormFieldControl._get_children(self) + self.__options
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

    # max_menu_height
    @property
    def max_menu_height(self) -> OptionalNumber:
        return self._get_attr("maxMenuHeight", data_type="float")

    @max_menu_height.setter
    def max_menu_height(self, value: OptionalNumber):
        self._set_attr("maxMenuHeight", value)

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
            f"select_icon is deprecated since version 0.26.0 "
            f"and will be removed in version 0.29.0. Use trailing_icon instead.",
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
                f"select_icon is deprecated since version 0.26.0 "
                f"and will be removed in version 0.29.0. Use trailing_icon instead.",
                category=DeprecationWarning,
                stacklevel=2,
            )

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
