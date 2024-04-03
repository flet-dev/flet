from enum import Enum
from typing import Any, List, Optional, Union

from flet_core.border import Border
from flet_core.control import Control, OptionalNumber
from flet_core.gradients import Gradient
from flet_core.ref import Ref
from flet_core.shadow import BoxShadow
from flet_core.text_style import TextStyle
from flet_core.textfield import InputFilter, KeyboardType, TextCapitalization, TextField
from flet_core.types import (
    AnimationValue,
    BlendMode,
    BorderRadiusValue,
    OffsetValue,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    TextAlign,
)


class VisibilityMode(Enum):
    NEVER = "never"
    EDITING = "editing"
    NOT_EDITING = "notEditing"
    ALWAYS = "always"


class CupertinoTextField(TextField):
    """
    An iOS-style text field.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinotextfield
    """

    def __init__(
        self,
        placeholder_text: Optional[str] = None,
        value: Optional[str] = None,
        placeholder_style: Optional[TextStyle] = None,
        gradient: Optional[Gradient] = None,
        blend_mode: Optional[BlendMode] = None,
        shadow: Union[None, BoxShadow, List[BoxShadow]] = None,
        prefix_visibility_mode: Optional[VisibilityMode] = None,
        suffix_visibility_mode: Optional[VisibilityMode] = None,
        clear_button_semantics_label: Optional[str] = None,
        #
        # TextField
        #
        keyboard_type: Optional[KeyboardType] = None,
        rtl: Optional[bool] = None,
        multiline: Optional[bool] = None,
        min_lines: Optional[int] = None,
        max_lines: Optional[int] = None,
        max_length: Optional[int] = None,
        password: Optional[bool] = None,
        can_reveal_password: Optional[bool] = None,
        read_only: Optional[bool] = None,
        shift_enter: Optional[bool] = None,
        text_align: Optional[TextAlign] = None,
        autofocus: Optional[bool] = None,
        capitalization: Optional[TextCapitalization] = None,
        autocorrect: Optional[bool] = None,
        enable_suggestions: Optional[bool] = None,
        smart_dashes_type: Optional[bool] = None,
        smart_quotes_type: Optional[bool] = None,
        cursor_color: Optional[str] = None,
        cursor_width: OptionalNumber = None,
        cursor_height: OptionalNumber = None,
        cursor_radius: OptionalNumber = None,
        show_cursor: Optional[bool] = None,
        selection_color: Optional[str] = None,
        input_filter: Optional[InputFilter] = None,
        on_change=None,
        on_submit=None,
        on_focus=None,
        on_blur=None,
        #
        # FormField
        #
        text_size: OptionalNumber = None,
        text_style: Optional[TextStyle] = None,
        border: Optional[Border] = None,
        color: Optional[str] = None,
        bgcolor: Optional[str] = None,
        border_radius: BorderRadiusValue = None,
        focused_color: Optional[str] = None,
        focused_bgcolor: Optional[str] = None,
        focused_border_width: OptionalNumber = None,
        focused_border_color: Optional[str] = None,
        content_padding: PaddingValue = None,
        dense: Optional[bool] = None,
        filled: Optional[bool] = None,
        prefix: Optional[Control] = None,
        suffix: Optional[Control] = None,
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
        on_animation_end=None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        TextField.__init__(
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
            # FormField
            #
            text_size=text_size,
            text_style=text_style,
            color=color,
            bgcolor=bgcolor,
            border_radius=border_radius,
            focused_color=focused_color,
            focused_bgcolor=focused_bgcolor,
            focused_border_width=focused_border_width,
            focused_border_color=focused_border_color,
            content_padding=content_padding,
            dense=dense,
            filled=filled,
            prefix=prefix,
            suffix=suffix,
            #
            # TextField
            #
            value=value,
            keyboard_type=keyboard_type,
            rtl=rtl,
            multiline=multiline,
            min_lines=min_lines,
            max_lines=max_lines,
            max_length=max_length,
            password=password,
            can_reveal_password=can_reveal_password,
            read_only=read_only,
            shift_enter=shift_enter,
            text_align=text_align,
            autofocus=autofocus,
            capitalization=capitalization,
            autocorrect=autocorrect,
            enable_suggestions=enable_suggestions,
            smart_dashes_type=smart_dashes_type,
            smart_quotes_type=smart_quotes_type,
            cursor_color=cursor_color,
            cursor_width=cursor_width,
            cursor_height=cursor_height,
            cursor_radius=cursor_radius,
            show_cursor=show_cursor,
            selection_color=selection_color,
            input_filter=input_filter,
            on_change=on_change,
            on_submit=on_submit,
            on_focus=on_focus,
            on_blur=on_blur,
        )

        self.placeholder_text = placeholder_text
        self.placeholder_style = placeholder_style
        self.gradient = gradient
        self.blend_mode = blend_mode
        self.shadow = shadow
        self.suffix_visibility_mode = suffix_visibility_mode
        self.prefix_visibility_mode = prefix_visibility_mode
        self.clear_button_semantics_label = clear_button_semantics_label
        self.border = border

    def _get_control_name(self):
        return "cupertinotextfield"

    def before_update(self):
        super().before_update()
        self._set_attr_json("gradient", self.__gradient)
        self._set_attr_json("shadow", self.__shadow if self.__shadow else None)
        self._set_attr_json("placeholderStyle", self.__placeholder_style)
        self._set_attr_json("border", self.__border)

    # placeholder_text
    @property
    def placeholder_text(self):
        return self._get_attr("placeholderText")

    @placeholder_text.setter
    def placeholder_text(self, value):
        self._set_attr("placeholderText", value)

    # placeholder_style
    @property
    def placeholder_style(self):
        return self.__placeholder_style

    @placeholder_style.setter
    def placeholder_style(self, value: Optional[TextStyle]):
        self.__placeholder_style = value

    # gradient
    @property
    def gradient(self) -> Optional[Gradient]:
        return self.__gradient

    @gradient.setter
    def gradient(self, value: Optional[Gradient]):
        self.__gradient = value

    # blend_mode
    @property
    def blend_mode(self) -> Optional[BlendMode]:
        return self.__blend_mode

    @blend_mode.setter
    def blend_mode(self, value: Optional[BlendMode]):
        self.__blend_mode = value
        self._set_attr(
            "blendMode", value.value if isinstance(value, BlendMode) else value
        )

    # shadow
    @property
    def shadow(self):
        return self.__shadow

    @shadow.setter
    def shadow(self, value: Union[None, BoxShadow, List[BoxShadow]]):
        self.__shadow = value if value is not None else []

    # suffix_visibility_mode
    @property
    def suffix_visibility_mode(self) -> Optional[VisibilityMode]:
        return self.__suffix_visibility_mode

    @suffix_visibility_mode.setter
    def suffix_visibility_mode(self, value: Optional[VisibilityMode]):
        self.__suffix_visibility_mode = value
        self._set_enum_attr("suffixVisibilityMode", value, VisibilityMode)

    # prefix_visibility_mode
    @property
    def prefix_visibility_mode(self) -> Optional[VisibilityMode]:
        return self.__prefix_visibility_mode

    @prefix_visibility_mode.setter
    def prefix_visibility_mode(self, value: Optional[VisibilityMode]):
        self.__prefix_visibility_mode = value
        self._set_attr(
            "prefixVisibilityMode",
            value.value if isinstance(value, VisibilityMode) else value,
        )

    # clear_button_semantics_label
    @property
    def clear_button_semantics_label(self):
        return self._get_attr("clearButtonSemanticsLabel")

    @clear_button_semantics_label.setter
    def clear_button_semantics_label(self, value):
        self._set_attr("clearButtonSemanticsLabel", value)

    # border
    @property
    def border(self) -> Optional[Border]:
        return self.__border

    @border.setter
    def border(self, value: Optional[Border]):
        self.__border = value
