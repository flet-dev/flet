from typing import Any, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    BlendMode,
    BlendModeString,
    BorderRadiusValue,
    ImageFit,
    ImageFitString,
    ImageRepeat,
    ImageRepeatString,
    OffsetValue,
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
        ref: Optional[Ref] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
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
        #
        # Specific
        #
        src_base64: Optional[str] = None,
        repeat: Optional[ImageRepeat] = None,
        fit: Optional[ImageFit] = None,
        border_radius: BorderRadiusValue = None,
        color: Optional[str] = None,
        color_blend_mode: BlendMode = BlendMode.NONE,
        gapless_playback: Optional[bool] = None,
        semantics_label: Optional[str] = None,
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

        self.src = src
        self.src_base64 = src_base64
        self.fit = fit
        self.repeat = repeat
        self.border_radius = border_radius
        self.color = color
        self.color_blend_mode = color_blend_mode
        self.gapless_playback = gapless_playback
        self.semantics_label = semantics_label

    def _get_control_name(self):
        return "image"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("borderRadius", self.__border_radius)

    # src
    @property
    def src(self):
        return self._get_attr("src")

    @src.setter
    def src(self, value):
        self._set_attr("src", value)

    # src_base64
    @property
    def src_base64(self):
        return self._get_attr("srcBase64")

    @src_base64.setter
    def src_base64(self, value):
        self._set_attr("srcBase64", value)

    # fit
    @property
    def fit(self) -> Optional[ImageFit]:
        return self.__fit

    @fit.setter
    def fit(self, value: Optional[ImageFit]):
        self.__fit = value
        if isinstance(value, ImageFit):
            self._set_attr("fit", value.value)
        else:
            self.__set_fit(value)

    def __set_fit(self, value: ImageFitString):
        self._set_attr("fit", value)

    # repeat
    @property
    def repeat(self) -> Optional[ImageRepeat]:
        return self.__repeat

    @repeat.setter
    def repeat(self, value: Optional[ImageRepeat]):
        self.__repeat = value
        if isinstance(value, ImageRepeat):
            self._set_attr("repeat", value.value)
        else:
            self.__set_repeat(value)

    def __set_repeat(self, value: ImageRepeatString):
        self._set_attr("repeat", value)

    # border_radius
    @property
    def border_radius(self) -> BorderRadiusValue:
        return self.__border_radius

    @border_radius.setter
    def border_radius(self, value: BorderRadiusValue):
        self.__border_radius = value

    # color
    @property
    def color(self):
        return self._get_attr("color")

    @color.setter
    def color(self, value):
        self._set_attr("color", value)

    # color_blend_mode
    @property
    def color_blend_mode(self) -> BlendMode:
        return self.__blend_mode

    @color_blend_mode.setter
    def color_blend_mode(self, value: BlendMode):
        self.__blend_mode = value
        if isinstance(value, BlendMode):
            self._set_attr("colorBlendMode", value.value)
        else:
            self.__set_blend_mode(value)

    def __set_blend_mode(self, value: BlendModeString):
        self._set_attr("colorBlendMode", value)

    # gapless_playback
    @property
    def gapless_playback(self) -> Optional[bool]:
        return self._get_attr("gaplessPlayback", data_type="bool", def_value=False)

    @gapless_playback.setter
    def gapless_playback(self, value: Optional[bool]):
        self._set_attr("gaplessPlayback", value)

    # semantics_label
    @property
    def semantics_label(self):
        return self._get_attr("semanticsLabel")

    @semantics_label.setter
    def semantics_label(self, value):
        self._set_attr("semanticsLabel", value)
