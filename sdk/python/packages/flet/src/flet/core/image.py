from typing import Any, Optional, Union

from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.box import FilterQuality
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, OptionalNumber
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    BlendMode,
    BorderRadiusValue,
    ColorEnums,
    ColorValue,
    ImageFit,
    ImageRepeat,
    OffsetValue,
    OptionalControlEventCallable,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class Image(ConstrainedControl):
    """
    A control that displays an image.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "Image Example"

        img = ft.Image(
            src=f"/icons/icon-512.png",
            width=100,
            height=100,
            fit=ft.ImageFit.CONTAIN,
        )

        page.add(img)

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/image
    """

    def __init__(
        self,
        src: Optional[str] = None,
        src_base64: Optional[str] = None,
        error_content: Optional[Control] = None,
        repeat: Optional[ImageRepeat] = None,
        fit: Optional[ImageFit] = None,
        border_radius: Optional[BorderRadiusValue] = None,
        color: Optional[ColorValue] = None,
        color_blend_mode: Optional[BlendMode] = None,
        gapless_playback: Optional[bool] = None,
        semantics_label: Optional[str] = None,
        exclude_from_semantics: Optional[bool] = None,
        filter_quality: Optional[FilterQuality] = None,
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

        self.src = src
        self.src_base64 = src_base64
        self.error_content = error_content
        self.fit = fit
        self.repeat = repeat
        self.border_radius = border_radius
        self.color = color
        self.color_blend_mode = color_blend_mode
        self.gapless_playback = gapless_playback
        self.semantics_label = semantics_label
        self.exclude_from_semantics = exclude_from_semantics
        self.filter_quality = filter_quality

    def _get_control_name(self):
        return "image"

    def _get_children(self):
        if self.__error_content is not None:
            self.__error_content._set_attr_internal("n", "error_content")
            return [self.__error_content]
        return []

    def before_update(self):
        super().before_update()
        self._set_attr_json("borderRadius", self.__border_radius)

    # src
    @property
    def src(self):
        return self._get_attr("src")

    @src.setter
    def src(self, value: Optional[str]):
        self._set_attr("src", value)

    # src_base64
    @property
    def src_base64(self):
        return self._get_attr("srcBase64")

    @src_base64.setter
    def src_base64(self, value: Optional[str]):
        self._set_attr("srcBase64", value)

    # fit
    @property
    def fit(self) -> Optional[ImageFit]:
        return self.__fit

    @fit.setter
    def fit(self, value: Optional[ImageFit]):
        self.__fit = value
        self._set_attr("fit", value.value if isinstance(value, ImageFit) else value)

    # filter_quality
    @property
    def filter_quality(self) -> Optional[FilterQuality]:
        return self.__filter_quality

    @filter_quality.setter
    def filter_quality(self, value: Optional[FilterQuality]):
        self.__filter_quality = value
        self._set_attr(
            "filterQuality", value.value if isinstance(value, FilterQuality) else value
        )

    # repeat
    @property
    def repeat(self) -> Optional[ImageRepeat]:
        return self.__repeat

    @repeat.setter
    def repeat(self, value: Optional[ImageRepeat]):
        self.__repeat = value
        self._set_enum_attr("repeat", value, ImageRepeat)

    # border_radius
    @property
    def border_radius(self) -> Optional[BorderRadiusValue]:
        return self.__border_radius

    @border_radius.setter
    def border_radius(self, value: Optional[BorderRadiusValue]):
        self.__border_radius = value

    # color
    @property
    def color(self) -> Optional[ColorValue]:
        return self.__color

    @color.setter
    def color(self, value: Optional[ColorValue]):
        self.__color = value
        self._set_enum_attr("color", value, ColorEnums)

    # color_blend_mode
    @property
    def color_blend_mode(self) -> Optional[BlendMode]:
        return self.__blend_mode

    @color_blend_mode.setter
    def color_blend_mode(self, value: Optional[BlendMode]):
        self.__blend_mode = value
        self._set_enum_attr("colorBlendMode", value, BlendMode)

    # gapless_playback
    @property
    def gapless_playback(self) -> bool:
        return self._get_attr("gaplessPlayback", data_type="bool", def_value=False)

    @gapless_playback.setter
    def gapless_playback(self, value: Optional[bool]):
        self._set_attr("gaplessPlayback", value)

    # exclude_from_semantics
    @property
    def exclude_from_semantics(self) -> bool:
        return self._get_attr("excludeFromSemantics", data_type="bool", def_value=False)

    @exclude_from_semantics.setter
    def exclude_from_semantics(self, value: Optional[bool]):
        self._set_attr("excludeFromSemantics", value)

    # semantics_label
    @property
    def semantics_label(self) -> Optional[str]:
        return self._get_attr("semanticsLabel")

    @semantics_label.setter
    def semantics_label(self, value: Optional[str]):
        self._set_attr("semanticsLabel", value)

    # error_content
    @property
    def error_content(self) -> Optional[Control]:
        return self.__error_content

    @error_content.setter
    def error_content(self, value: Optional[Control]):
        self.__error_content = value
