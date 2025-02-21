import warnings
from typing import Any, Optional, Union

from flet.core.alignment import Alignment
from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, OptionalNumber
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    BorderRadiusValue,
    ColorEnums,
    ColorValue,
    IconEnums,
    IconValue,
    OffsetValue,
    OptionalControlEventCallable,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    UrlTarget,
)


class CupertinoButton(ConstrainedControl):
    """
    An iOS-style button.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinobutton
    """

    def __init__(
        self,
        text: Optional[str] = None,
        icon: Optional[IconValue] = None,
        icon_color: Optional[ColorValue] = None,
        content: Optional[Control] = None,
        bgcolor: Optional[ColorValue] = None,
        color: Optional[ColorValue] = None,
        disabled_bgcolor: Optional[ColorValue] = None,
        opacity_on_click: OptionalNumber = None,
        min_size: OptionalNumber = None,
        padding: Optional[PaddingValue] = None,
        alignment: Optional[Alignment] = None,
        border_radius: Optional[BorderRadiusValue] = None,
        url: Optional[str] = None,
        url_target: Optional[UrlTarget] = None,
        on_click: OptionalControlEventCallable = None,
        on_long_press: OptionalControlEventCallable = None,
        on_focus: OptionalControlEventCallable = None,
        on_blur: OptionalControlEventCallable = None,
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
        )

        self.disabled_bgcolor = disabled_bgcolor
        self.text = text
        self.icon = icon
        self.icon_color = icon_color
        self.bgcolor = bgcolor
        self.color = color
        self.border_radius = border_radius
        self.min_size = min_size
        self.opacity_on_click = opacity_on_click
        self.padding = padding
        self.alignment = alignment
        self.content = content
        self.url = url
        self.url_target = url_target
        self.on_click = on_click
        self.on_long_press = on_long_press
        self.on_focus = on_focus
        self.on_blur = on_blur

    def _get_control_name(self):
        return "cupertinobutton"

    def before_update(self):
        super().before_update()
        assert (
            self.text or self.icon or (self.__content and self.__content.visible)
        ), "at minimum, text, icon or a visible content must be provided"
        self._set_attr_json("padding", self.__padding)
        self._set_attr_json("borderRadius", self.__border_radius)
        self._set_attr_json("alignment", self.__alignment)

    def _get_children(self):
        if self.__content is None:
            return []
        self.__content._set_attr_internal("n", "content")
        return [self.__content]

    # text
    @property
    def text(self):
        return self._get_attr("text")

    @text.setter
    def text(self, value):
        self._set_attr("text", value)

    # icon
    @property
    def icon(self):
        return self.__icon

    @icon.setter
    def icon(self, value):
        self.__icon = value
        self._set_enum_attr("icon", value, IconEnums)

    # icon_color
    @property
    def icon_color(self):
        return self.__icon_color

    @icon_color.setter
    def icon_color(self, value):
        self.__icon_color = value
        self._set_enum_attr("iconColor", value, ColorEnums)

    # alignment
    @property
    def alignment(self) -> Optional[Alignment]:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value

    # disabled_bgcolor
    @property
    def disabled_bgcolor(self) -> Optional[str]:
        return self.__disabled_bgcolor

    @disabled_bgcolor.setter
    def disabled_bgcolor(self, value: Optional[str]):
        self.__disabled_bgcolor = value
        self._set_enum_attr("disabledBgcolor", value, ColorEnums)

    # opacity_on_click
    @property
    def opacity_on_click(self) -> float:
        return self._get_attr("opacityOnClick", data_type="float", def_value=0.4)

    @opacity_on_click.setter
    def opacity_on_click(self, value: OptionalNumber):
        if value is not None:
            value = max(0.0, min(value, 1.0))  # make sure 0.0 <= value <= 1.0
        self._set_attr("opacityOnClick", value)

    # border_radius
    @property
    def border_radius(self) -> Optional[BorderRadiusValue]:
        return self.__border_radius

    @border_radius.setter
    def border_radius(self, value: Optional[BorderRadiusValue]):
        self.__border_radius = value

    # min_size
    @property
    def min_size(self) -> float:
        return self._get_attr("minSize", data_type="float", def_value=44.0)

    @min_size.setter
    def min_size(self, value: OptionalNumber):
        self._set_attr("minSize", value)

    # padding
    @property
    def padding(self) -> Optional[PaddingValue]:
        return self.__padding

    @padding.setter
    def padding(self, value: Optional[PaddingValue]):
        self.__padding = value

    # bgcolor
    @property
    def bgcolor(self) -> Optional[ColorValue]:
        return self.__bgcolor

    @bgcolor.setter
    def bgcolor(self, value: Optional[ColorValue]):
        self.__bgcolor = value
        self._set_enum_attr("bgColor", value, ColorEnums)

    # color
    @property
    def color(self) -> Optional[ColorValue]:
        return self.__color

    @color.setter
    def color(self, value: Optional[ColorValue]):
        self.__color = value
        self._set_enum_attr("color", value, ColorEnums)

    # url
    @property
    def url(self):
        return self._get_attr("url")

    @url.setter
    def url(self, value):
        self._set_attr("url", value)

    # url_target
    @property
    def url_target(self) -> Optional[UrlTarget]:
        return self.__url_target

    @url_target.setter
    def url_target(self, value: Optional[UrlTarget]):
        self.__url_target = value
        self._set_enum_attr("urlTarget", value, UrlTarget)

    # on_click
    @property
    def on_click(self) -> OptionalControlEventCallable:
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler: OptionalControlEventCallable):
        self._add_event_handler("click", handler)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # on_long_press
    @property
    def on_long_press(self) -> OptionalControlEventCallable:
        return self._get_event_handler("longPress")

    @on_long_press.setter
    def on_long_press(self, handler: OptionalControlEventCallable):
        self._add_event_handler("longPress", handler)

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
