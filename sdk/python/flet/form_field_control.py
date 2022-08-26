from typing import Any, Optional, Union

from beartype import beartype

from flet.constrained_control import ConstrainedControl
from flet.control import Control, InputBorder, OptionalNumber
from flet.ref import Ref
from flet.types import (
    AnimationValue,
    BorderRadiusValue,
    OffsetValue,
    PaddingValue,
    RotateValue,
    ScaleValue,
)


class FormFieldControl(ConstrainedControl):
    def __init__(
        self,
        ref: Optional[Ref] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
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
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
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
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.__prefix: Optional[Control] = None
        self.__suffix: Optional[Control] = None

        self.text_size = text_size
        self.label = label
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
        self.hint_text = hint_text
        self.helper_text = helper_text
        self.counter_text = counter_text
        self.error_text = error_text
        self.prefix = prefix
        self.prefix_icon = prefix_icon
        self.prefix_text = prefix_text
        self.suffix = suffix
        self.suffix_icon = suffix_icon
        self.suffix_text = suffix_text

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("borderRadius", self.__border_radius)
        self._set_attr_json("contentPadding", self.__content_padding)

    def _get_children(self):
        children = []
        if self.__prefix:
            self.__prefix._set_attr_internal("n", "prefix")
            children.append(self.__prefix)
        if self.__suffix:
            self.__suffix._set_attr_internal("n", "suffix")
            children.append(self.__suffix)
        return children

    # text_size
    @property
    def text_size(self) -> OptionalNumber:
        return self._get_attr("textSize")

    @text_size.setter
    @beartype
    def text_size(self, value: OptionalNumber):
        self._set_attr("textSize", value)

    # label
    @property
    def label(self):
        return self._get_attr("label")

    @label.setter
    def label(self, value):
        self._set_attr("label", value)

    # icon
    @property
    def icon(self):
        return self._get_attr("icon")

    @icon.setter
    def icon(self, value):
        self._set_attr("icon", value)

    # border
    @property
    def border(self) -> InputBorder:
        return self._get_attr("border")

    @border.setter
    @beartype
    def border(self, value: InputBorder):
        self._set_attr("border", value)

    # color
    @property
    def color(self):
        return self._get_attr("color")

    @color.setter
    def color(self, value):
        self._set_attr("color", value)

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgcolor", value)

    # border_radius
    @property
    def border_radius(self) -> BorderRadiusValue:
        return self.__border_radius

    @border_radius.setter
    @beartype
    def border_radius(self, value: BorderRadiusValue):
        self.__border_radius = value

    # border_width
    @property
    def border_width(self) -> OptionalNumber:
        return self._get_attr("borderWidth")

    @border_width.setter
    @beartype
    def border_width(self, value: OptionalNumber):
        self._set_attr("borderWidth", value)

    # border_color
    @property
    def border_color(self):
        return self._get_attr("borderColor")

    @border_color.setter
    def border_color(self, value):
        self._set_attr("borderColor", value)

    # focused_color
    @property
    def focused_color(self):
        return self._get_attr("focusedColor")

    @focused_color.setter
    def focused_color(self, value):
        self._set_attr("focusedColor", value)

    # focused_bgcolor
    @property
    def focused_bgcolor(self):
        return self._get_attr("focusedBgcolor")

    @focused_bgcolor.setter
    def focused_bgcolor(self, value):
        self._set_attr("focusedBgcolor", value)

    # focused_border_width
    @property
    def focused_border_width(self) -> OptionalNumber:
        return self._get_attr("focusedBorderWidth")

    @focused_border_width.setter
    @beartype
    def focused_border_width(self, value: OptionalNumber):
        self._set_attr("focusedBorderWidth", value)

    # focused_border_color
    @property
    def focused_border_color(self):
        return self._get_attr("focusedBorderColor")

    @focused_border_color.setter
    def focused_border_color(self, value):
        self._set_attr("focusedBorderColor", value)

    # content_padding
    @property
    def content_padding(self) -> PaddingValue:
        return self.__content_padding

    @content_padding.setter
    @beartype
    def content_padding(self, value: PaddingValue):
        self.__content_padding = value

    # filled
    @property
    def filled(self) -> Optional[bool]:
        return self._get_attr("filled")

    @filled.setter
    def filled(self, value: Optional[bool]):
        self._set_attr("filled", value)

    # hint_text
    @property
    def hint_text(self):
        return self._get_attr("hintText")

    @hint_text.setter
    def hint_text(self, value):
        self._set_attr("hintText", value)

    # helper_text
    @property
    def helper_text(self):
        return self._get_attr("helperText")

    @helper_text.setter
    def helper_text(self, value):
        self._set_attr("helperText", value)

    # counter_text
    @property
    def counter_text(self):
        return self._get_attr("counterText")

    @counter_text.setter
    def counter_text(self, value):
        self._set_attr("counterText", value)

    # error_text
    @property
    def error_text(self):
        return self._get_attr("errorText")

    @error_text.setter
    def error_text(self, value):
        self._set_attr("errorText", value)

    # prefix
    @property
    def prefix(self):
        return self.__prefix

    @prefix.setter
    def prefix(self, value):
        self.__prefix = value

    # prefix_icon
    @property
    def prefix_icon(self):
        return self._get_attr("prefixIcon")

    @prefix_icon.setter
    def prefix_icon(self, value):
        self._set_attr("prefixIcon", value)

    # prefix_text
    @property
    def prefix_text(self):
        return self._get_attr("prefixText")

    @prefix_text.setter
    def prefix_text(self, value):
        self._set_attr("prefixText", value)

    # suffix
    @property
    def suffix(self):
        return self.__suffix

    @suffix.setter
    def suffix(self, value):
        self.__suffix = value

    # suffix_icon
    @property
    def suffix_icon(self):
        return self._get_attr("suffixIcon")

    @suffix_icon.setter
    def suffix_icon(self, value):
        self._set_attr("suffixIcon", value)

    # suffix_text
    @property
    def suffix_text(self):
        return self._get_attr("suffixText")

    @suffix_text.setter
    def suffix_text(self, value):
        self._set_attr("suffixText", value)
