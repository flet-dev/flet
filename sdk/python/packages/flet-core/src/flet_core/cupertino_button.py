import warnings
from typing import Any, Optional, Union

from flet_core.alignment import Alignment
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.tooltip import TooltipValue
from flet_core.types import (
    AnimationValue,
    BorderRadiusValue,
    OffsetValue,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    UrlTarget,
    OptionalControlEventCallable,
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
        icon: Optional[str] = None,
        icon_color: Optional[str] = None,
        content: Optional[Control] = None,
        bgcolor: Optional[str] = None,
        color: Optional[str] = None,
        disabled_color: Optional[str] = None,
        disabled_bgcolor: Optional[str] = None,
        opacity_on_click: OptionalNumber = None,
        min_size: OptionalNumber = None,
        padding: PaddingValue = None,
        alignment: Optional[Alignment] = None,
        border_radius: BorderRadiusValue = None,
        url: Optional[str] = None,
        url_target: Optional[UrlTarget] = None,
        on_click: OptionalControlEventCallable = None,
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
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: TooltipValue = None,
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
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.disabled_color = disabled_color
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
        return self._get_attr("icon")

    @icon.setter
    def icon(self, value):
        self._set_attr("icon", value)

    # icon_color
    @property
    def icon_color(self):
        return self._get_attr("iconColor")

    @icon_color.setter
    def icon_color(self, value):
        self._set_attr("iconColor", value)

    # alignment
    @property
    def alignment(self) -> Optional[Alignment]:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value

    # disabled_color
    @property
    def disabled_color(self) -> Optional[str]:
        warnings.warn(
            f"disabled_color is deprecated since version 0.24.0 "
            f"and will be removed in version 0.27.0. Use disabled_bgcolor instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return self._get_attr("disabledColor")

    @disabled_color.setter
    def disabled_color(self, value: Optional[str]):
        self._set_attr("disabledColor", value)
        if value is not None:
            warnings.warn(
                f"disabled_color is deprecated since version 0.24.0 "
                f"and will be removed in version 0.27.0. Use disabled_bgcolor instead.",
                category=DeprecationWarning,
                stacklevel=2,
            )

    # disabled_bgcolor
    @property
    def disabled_bgcolor(self) -> Optional[str]:
        return self._get_attr("disabledBgcolor")

    @disabled_bgcolor.setter
    def disabled_bgcolor(self, value: Optional[str]):
        self._set_attr("disabledBgcolor", value)

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
    def border_radius(self) -> BorderRadiusValue:
        return self.__border_radius

    @border_radius.setter
    def border_radius(self, value: BorderRadiusValue):
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
    def padding(self) -> PaddingValue:
        return self.__padding

    @padding.setter
    def padding(self, value: PaddingValue):
        self.__padding = value

    # bgcolor
    @property
    def bgcolor(self) -> Optional[str]:
        return self._get_attr("bgColor")

    @bgcolor.setter
    def bgcolor(self, value: Optional[str]):
        self._set_attr("bgColor", value)

    # color
    @property
    def color(self) -> Optional[str]:
        return self._get_attr("color")

    @color.setter
    def color(self, value: Optional[str]):
        self._set_attr("color", value)

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
