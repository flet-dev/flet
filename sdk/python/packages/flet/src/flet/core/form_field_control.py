from enum import Enum
from typing import Any, Optional, Union

from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.box import BoxConstraints
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, OptionalNumber
from flet.core.ref import Ref
from flet.core.text_style import TextStyle
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    BorderRadiusValue,
    ColorEnums,
    ColorValue,
    DurationValue,
    IconEnums,
    IconValueOrControl,
    OffsetValue,
    OptionalControlEventCallable,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    VerticalAlignment,
)

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class InputBorder(Enum):
    NONE = "none"
    OUTLINE = "outline"
    UNDERLINE = "underline"


class FormFieldControl(ConstrainedControl):
    def __init__(
        self,
        text_size: OptionalNumber = None,
        text_style: Optional[TextStyle] = None,
        text_vertical_align: Union[VerticalAlignment, OptionalNumber] = None,
        label: Optional[Union[str, Control]] = None,
        label_style: Optional[TextStyle] = None,
        icon: Optional[IconValueOrControl] = None,
        border: Optional[InputBorder] = None,
        color: Optional[ColorValue] = None,
        bgcolor: Optional[ColorValue] = None,
        border_radius: Optional[BorderRadiusValue] = None,
        border_width: OptionalNumber = None,
        border_color: Optional[ColorValue] = None,
        focused_color: Optional[ColorValue] = None,
        focused_bgcolor: Optional[ColorValue] = None,
        focused_border_width: OptionalNumber = None,
        focused_border_color: Optional[ColorValue] = None,
        content_padding: Optional[PaddingValue] = None,
        dense: Optional[bool] = None,
        filled: Optional[bool] = None,
        fill_color: Optional[ColorValue] = None,
        focus_color: Optional[ColorValue] = None,
        align_label_with_hint: Optional[bool] = None,
        hover_color: Optional[ColorValue] = None,
        hint_text: Optional[str] = None,
        hint_style: Optional[TextStyle] = None,
        hint_fade_duration: Optional[DurationValue] = None,
        hint_max_lines: Optional[int] = None,
        helper: Optional[Control] = None,
        helper_text: Optional[str] = None,
        helper_style: Optional[TextStyle] = None,
        helper_max_lines: Optional[int] = None,
        counter: Optional[Control] = None,
        counter_text: Optional[str] = None,
        counter_style: Optional[TextStyle] = None,
        error: Optional[Control] = None,
        error_text: Optional[str] = None,
        error_style: Optional[TextStyle] = None,
        error_max_lines: Optional[int] = None,
        prefix: Optional[Control] = None,
        prefix_icon: Optional[IconValueOrControl] = None,
        prefix_icon_size_constraints: Optional[BoxConstraints] = None,
        prefix_text: Optional[str] = None,
        prefix_style: Optional[TextStyle] = None,
        suffix: Optional[Control] = None,
        suffix_icon: Optional[IconValueOrControl] = None,
        suffix_icon_size_constraints: Optional[BoxConstraints] = None,
        size_constraints: Optional[BoxConstraints] = None,
        collapsed: Optional[bool] = None,
        fit_parent_size: Optional[bool] = None,
        suffix_text: Optional[str] = None,
        suffix_style: Optional[TextStyle] = None,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: Optional[RotateValue] = None,
        scale: Optional[ScaleValue] = None,
        offset: Optional[OffsetValue] = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: Optional[AnimationValue] = None,
        animate_size: Optional[AnimationValue] = None,
        animate_position: Optional[AnimationValue] = None,
        animate_rotation: Optional[AnimationValue] = None,
        animate_scale: Optional[AnimationValue] = None,
        animate_offset: Optional[AnimationValue] = None,
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: Optional[TooltipValue] = None,
        badge: Optional[BadgeValue] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        rtl: Optional[bool] = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
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
            badge=badge,
            visible=visible,
            disabled=disabled,
            data=data,
            rtl=rtl,
        )

        self.text_size = text_size
        self.text_style = text_style
        self.text_vertical_align = text_vertical_align
        self.label = label
        self.label_style = label_style
        self.icon = icon
        self.border = border
        self.color = color
        self.bgcolor = bgcolor
        self.border_radius = border_radius
        self.border_width = border_width
        self.border_color = border_color
        self.focused_color = focused_color
        self.focused_bgcolor = focused_bgcolor
        self.focused_border_width = focused_border_width
        self.focused_border_color = focused_border_color
        self.content_padding = content_padding
        self.filled = filled
        self.dense = dense
        self.hint_text = hint_text
        self.hint_style = hint_style
        self.helper = helper
        self.helper_text = helper_text
        self.helper_style = helper_style
        self.counter = counter
        self.counter_text = counter_text
        self.counter_style = counter_style
        self.error = error
        self.error_text = error_text
        self.error_style = error_style
        self.prefix = prefix
        self.prefix_icon = prefix_icon
        self.prefix_text = prefix_text
        self.prefix_style = prefix_style
        self.suffix = suffix
        self.suffix_icon = suffix_icon
        self.suffix_text = suffix_text
        self.suffix_style = suffix_style
        self.hover_color = hover_color
        self.fill_color = fill_color
        self.focus_color = focus_color
        self.align_label_with_hint = align_label_with_hint
        self.hint_fade_duration = hint_fade_duration
        self.hint_max_lines = hint_max_lines
        self.helper_max_lines = helper_max_lines
        self.error_max_lines = error_max_lines
        self.prefix_icon_size_constraints = prefix_icon_size_constraints
        self.suffix_icon_size_constraints = suffix_icon_size_constraints
        self.size_constraints = size_constraints
        self.collapsed = collapsed
        self.fit_parent_size = fit_parent_size

    def before_update(self):
        super().before_update()
        self._set_attr_json("borderRadius", self.__border_radius)
        self._set_attr_json("contentPadding", self.__content_padding)
        self._set_attr_json("textStyle", self.__text_style)
        self._set_attr_json("labelStyle", self.__label_style)
        self._set_attr_json("hintStyle", self.__hint_style)
        self._set_attr_json("helperStyle", self.__helper_style)
        self._set_attr_json("counterStyle", self.__counter_style)
        self._set_attr_json("errorStyle", self.__error_style)
        self._set_attr_json("prefixStyle", self.__prefix_style)
        self._set_attr_json("suffixStyle", self.__suffix_style)
        self._set_attr_json("hintFadeDuration", self.__hint_fade_duration)
        self._set_attr_json(
            "prefixIconSizeConstraints", self.__prefix_icon_size_constraints
        )
        self._set_attr_json(
            "suffixIconSizeConstraints", self.__suffix_icon_size_constraints
        )
        self._set_attr_json("sizeConstraints", self.__size_constraints)
        if isinstance(self.__suffix_icon, str):
            self._set_attr("suffixIcon", self.__suffix_icon)
        if isinstance(self.__prefix_icon, str):
            self._set_attr("prefixIcon", self.__prefix_icon)
        if isinstance(self.__icon, str):
            self._set_attr("icon", self.__icon)
        if isinstance(self.__label, str):
            self._set_attr("label", self.__label)

    def _get_children(self):
        children = []
        for control, name in [
            (self.__prefix, "prefix"),
            (self.__suffix, "suffix"),
            (self.__suffix_icon, "suffix_icon"),
            (self.__prefix_icon, "prefix_icon"),
            (self.__icon, "icon"),
            (self.__counter, "counter"),
            (self.__error, "error"),
            (self.__helper, "helper"),
            (self.__label, "label"),
        ]:
            if isinstance(control, Control):
                control._set_attr_internal("n", name)
                children.append(control)
        return children

    # text_size
    @property
    def text_size(self) -> OptionalNumber:
        return self._get_attr("textSize")

    @text_size.setter
    def text_size(self, value: OptionalNumber):
        self._set_attr("textSize", value)

    # text_style
    @property
    def text_style(self) -> Optional[TextStyle]:
        return self.__text_style

    @text_style.setter
    def text_style(self, value: Optional[TextStyle]):
        self.__text_style = value

    # label
    @property
    def label(self) -> Optional[Union[str, Control]]:
        return self.__label

    @label.setter
    def label(self, value: Optional[Union[str, Control]]):
        self.__label = value

    # label_style
    @property
    def label_style(self) -> Optional[TextStyle]:
        return self.__label_style

    @label_style.setter
    def label_style(self, value: Optional[TextStyle]):
        self.__label_style = value

    # icon
    @property
    def icon(self) -> Optional[IconValueOrControl]:
        return self.__icon

    @icon.setter
    def icon(self, value: Optional[IconValueOrControl]):
        self.__icon = value
        if not isinstance(value, Control):
            self._set_enum_attr("icon", value, IconEnums)

    # border
    @property
    def border(self) -> Optional[InputBorder]:
        return self.__border

    @border.setter
    def border(self, value: Optional[InputBorder]):
        self.__border = value
        self._set_enum_attr("border", value, InputBorder)

    # color
    @property
    def color(self) -> Optional[ColorValue]:
        return self.__color

    @color.setter
    def color(self, value: Optional[ColorValue]):
        self.__color = value
        self._set_enum_attr("color", value, ColorEnums)

    # focus_color
    @property
    def focus_color(self) -> Optional[str]:
        return self._get_attr("focusColor")

    @focus_color.setter
    def focus_color(self, value: Optional[str]):
        self._set_attr("focusColor", value)

    # align_label_with_hint
    @property
    def align_label_with_hint(self) -> Optional[bool]:
        return self._get_attr("alignLabelWithHint", data_type="bool")

    @align_label_with_hint.setter
    def align_label_with_hint(self, value: Optional[bool]):
        self._set_attr("alignLabelWithHint", value)

    # fit_parent_size
    @property
    def fit_parent_size(self) -> Optional[bool]:
        return self._get_attr("fitParentSize", data_type="bool", def_value=False)

    @fit_parent_size.setter
    def fit_parent_size(self, value: Optional[bool]):
        self._set_attr("fitParentSize", value)

    # hint_fade_duration
    @property
    def hint_fade_duration(self) -> Optional[DurationValue]:
        return self.__hint_fade_duration

    @hint_fade_duration.setter
    def hint_fade_duration(self, value: Optional[DurationValue]):
        self.__hint_fade_duration = value

    # hint_max_lines
    @property
    def hint_max_lines(self) -> Optional[int]:
        return self._get_attr("hintMaxLines", data_type="int")

    @hint_max_lines.setter
    def hint_max_lines(self, value: Optional[int]):
        self._set_attr("hintMaxLines", value)

    # helper_max_lines
    @property
    def helper_max_lines(self) -> Optional[int]:
        return self._get_attr("helperMaxLines", data_type="int")

    @helper_max_lines.setter
    def helper_max_lines(self, value: Optional[int]):
        self._set_attr("helperMaxLines", value)

    # error_max_lines
    @property
    def error_max_lines(self) -> Optional[int]:
        return self._get_attr("errorMaxLines", data_type="int")

    @error_max_lines.setter
    def error_max_lines(self, value: Optional[int]):
        self._set_attr("errorMaxLines", value)

    # prefix_icon_size_constraints
    @property
    def prefix_icon_size_constraints(self) -> Optional[BoxConstraints]:
        return self.__prefix_icon_size_constraints

    @prefix_icon_size_constraints.setter
    def prefix_icon_size_constraints(self, value: Optional[BoxConstraints]):
        self.__prefix_icon_size_constraints = value

    # suffix_icon_size_constraints
    @property
    def suffix_icon_size_constraints(self) -> Optional[BoxConstraints]:
        return self.__suffix_icon_size_constraints

    @suffix_icon_size_constraints.setter
    def suffix_icon_size_constraints(self, value: Optional[BoxConstraints]):
        self.__suffix_icon_size_constraints = value

    # size_constraints
    @property
    def size_constraints(self) -> Optional[BoxConstraints]:
        return self.__size_constraints

    @size_constraints.setter
    def size_constraints(self, value: Optional[BoxConstraints]):
        self.__size_constraints = value

    # collapsed
    @property
    def collapsed(self) -> Optional[bool]:
        return self._get_attr("collapsed", data_type="bool")

    @collapsed.setter
    def collapsed(self, value: Optional[bool]):
        self._set_attr("collapsed", value)

    # bgcolor
    @property
    def bgcolor(self) -> Optional[ColorValue]:
        return self.__bgcolor

    @bgcolor.setter
    def bgcolor(self, value: Optional[ColorValue]):
        self.__bgcolor = value
        self._set_enum_attr("bgcolor", value, ColorEnums)

    # border_radius
    @property
    def border_radius(self) -> Optional[BorderRadiusValue]:
        return self.__border_radius

    @border_radius.setter
    def border_radius(self, value: Optional[BorderRadiusValue]):
        self.__border_radius = value

    # border_width
    @property
    def border_width(self) -> OptionalNumber:
        return self._get_attr("borderWidth")

    @border_width.setter
    def border_width(self, value: OptionalNumber):
        self._set_attr("borderWidth", value)

    # border_color
    @property
    def border_color(self) -> Optional[ColorValue]:
        return self.__border_color

    @border_color.setter
    def border_color(self, value: Optional[ColorValue]):
        self.__border_color = value
        self._set_enum_attr("borderColor", value, ColorEnums)

    # text_vertical_align
    @property
    def text_vertical_align(self) -> Union[VerticalAlignment, OptionalNumber]:
        return self._get_attr("textVerticalAlign")

    @text_vertical_align.setter
    def text_vertical_align(self, value: Union[VerticalAlignment, OptionalNumber]):
        v = value.value if isinstance(value, VerticalAlignment) else value
        if v is not None:
            v = max(-1.0, min(v, 1.0))  # make sure 0.0 <= value <= 1.0
        self._set_attr("textVerticalAlign", v)

    # focused_color
    @property
    def focused_color(self) -> Optional[ColorValue]:
        return self.__focused_color

    @focused_color.setter
    def focused_color(self, value: Optional[ColorValue]):
        self.__focused_color = value
        self._set_enum_attr("focusedColor", value, ColorEnums)

    # focused_bgcolor
    @property
    def focused_bgcolor(self) -> Optional[str]:
        return self.__focused_bgcolor

    @focused_bgcolor.setter
    def focused_bgcolor(self, value: Optional[str]):
        self.__focused_bgcolor = value
        self._set_enum_attr("focusedBgcolor", value, ColorEnums)

    # focused_border_width
    @property
    def focused_border_width(self) -> OptionalNumber:
        return self._get_attr("focusedBorderWidth")

    @focused_border_width.setter
    def focused_border_width(self, value: OptionalNumber):
        self._set_attr("focusedBorderWidth", value)

    # focused_border_color
    @property
    def focused_border_color(self) -> Optional[ColorValue]:
        return self.__focused_border_color

    @focused_border_color.setter
    def focused_border_color(self, value: Optional[ColorValue]):
        self.__focused_border_color = value
        self._set_enum_attr("focusedBorderColor", value, ColorEnums)

    # content_padding
    @property
    def content_padding(self) -> Optional[PaddingValue]:
        return self.__content_padding

    @content_padding.setter
    def content_padding(self, value: Optional[PaddingValue]):
        self.__content_padding = value

    # dense
    @property
    def dense(self) -> bool:
        return self._get_attr("dense", data_type="bool", def_value=False)

    @dense.setter
    def dense(self, value: Optional[bool]):
        self._set_attr("dense", value)

    # filled
    @property
    def filled(self) -> Optional[bool]:
        return self._get_attr("filled", data_type="bool")

    @filled.setter
    def filled(self, value: Optional[bool]):
        self._set_attr("filled", value)

    # hint_text
    @property
    def hint_text(self) -> Optional[str]:
        return self._get_attr("hintText")

    @hint_text.setter
    def hint_text(self, value: Optional[str]):
        self._set_attr("hintText", value)

    # hint_style
    @property
    def hint_style(self) -> Optional[TextStyle]:
        return self.__hint_style

    @hint_style.setter
    def hint_style(self, value: Optional[TextStyle]):
        self.__hint_style = value

    # helper_text
    @property
    def helper_text(self) -> Optional[str]:
        return self._get_attr("helperText")

    @helper_text.setter
    def helper_text(self, value: Optional[str]):
        self._set_attr("helperText", value)

    # helper_style
    @property
    def helper_style(self) -> Optional[TextStyle]:
        return self.__helper_style

    @helper_style.setter
    def helper_style(self, value: Optional[TextStyle]):
        self.__helper_style = value

    # counter_text
    @property
    def counter_text(self) -> Optional[str]:
        return self._get_attr("counterText")

    @counter_text.setter
    def counter_text(self, value: Optional[str]):
        self._set_attr("counterText", value)

    # counter_style
    @property
    def counter_style(self) -> Optional[TextStyle]:
        return self.__counter_style

    @counter_style.setter
    def counter_style(self, value: Optional[TextStyle]):
        self.__counter_style = value

    # error_text
    @property
    def error_text(self) -> Optional[str]:
        return self._get_attr("errorText")

    @error_text.setter
    def error_text(self, value: Optional[str]):
        self._set_attr("errorText", value)

    # error_style
    @property
    def error_style(self) -> Optional[TextStyle]:
        return self.__error_style

    @error_style.setter
    def error_style(self, value: Optional[TextStyle]):
        self.__error_style = value

    # prefix
    @property
    def prefix(self) -> Optional[Control]:
        return self.__prefix

    @prefix.setter
    def prefix(self, value: Optional[Control]):
        self.__prefix = value

    # error
    @property
    def error(self) -> Optional[Control]:
        return self.__error

    @error.setter
    def error(self, value: Optional[Control]):
        self.__error = value

    # helper
    @property
    def helper(self) -> Optional[Control]:
        return self.__helper

    @helper.setter
    def helper(self, value: Optional[Control]):
        self.__helper = value

    # counter
    @property
    def counter(self) -> Optional[Control]:
        return self.__counter

    @counter.setter
    def counter(self, value: Optional[Control]):
        self.__counter = value

    # prefix_icon
    @property
    def prefix_icon(self) -> Optional[IconValueOrControl]:
        return self.__prefix_icon

    @prefix_icon.setter
    def prefix_icon(self, value: Optional[IconValueOrControl]):
        self.__prefix_icon = value
        if not isinstance(value, Control):
            self._set_enum_attr("prefixIcon", value, IconEnums)

    # prefix_text
    @property
    def prefix_text(self) -> Optional[str]:
        return self._get_attr("prefixText")

    @prefix_text.setter
    def prefix_text(self, value: Optional[str]):
        self._set_attr("prefixText", value)

    # prefix_style
    @property
    def prefix_style(self) -> Optional[TextStyle]:
        return self.__prefix_style

    @prefix_style.setter
    def prefix_style(self, value: Optional[TextStyle]):
        self.__prefix_style = value

    # suffix
    @property
    def suffix(self) -> Optional[Control]:
        return self.__suffix

    @suffix.setter
    def suffix(self, value: Optional[Control]):
        self.__suffix = value

    # suffix_icon
    @property
    def suffix_icon(self) -> Optional[IconValueOrControl]:
        return self.__suffix_icon

    @suffix_icon.setter
    def suffix_icon(self, value: Optional[IconValueOrControl]):
        self.__suffix_icon = value
        if not isinstance(value, Control):
            self._set_enum_attr("suffixIcon", value, IconEnums)

    # suffix_text
    @property
    def suffix_text(self) -> Optional[str]:
        return self._get_attr("suffixText")

    @suffix_text.setter
    def suffix_text(self, value: Optional[str]):
        self._set_attr("suffixText", value)

    # suffix_style
    @property
    def suffix_style(self) -> Optional[TextStyle]:
        return self.__suffix_style

    @suffix_style.setter
    def suffix_style(self, value: Optional[TextStyle]):
        self.__suffix_style = value

    # fill_color
    @property
    def fill_color(self) -> Optional[ColorValue]:
        return self.__fill_color

    @fill_color.setter
    def fill_color(self, value: Optional[ColorValue]):
        self.__fill_color = value
        self._set_enum_attr("fillColor", value, ColorEnums)

    # hover_color
    @property
    def hover_color(self) -> Optional[ColorValue]:
        return self.__hover_color

    @hover_color.setter
    def hover_color(self, value: Optional[ColorValue]):
        self.__hover_color = value
        self._set_enum_attr("hoverColor", value, ColorEnums)
