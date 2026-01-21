from typing import Optional, Union

from flet.controls.animation import Animation
from flet.controls.base_control import control
from flet.controls.border_radius import BorderRadiusValue
from flet.controls.box import BoxFit, FilterQuality
from flet.controls.control import Control
from flet.controls.layout_control import LayoutControl
from flet.controls.types import (
    BlendMode,
    ColorValue,
    ImageRepeat,
)

__all__ = ["Image"]


@control("Image")
class Image(LayoutControl):
    """
    Displays an image.

    The following popular formats are supported: JPEG, PNG, SVG,
    GIF, Animated GIF, WebP, Animated WebP, BMP, and WBMP.

    Example:
    ```python
    ft.Image(
        src="https://flet.dev/img/logo.svg",
        width=100,
        height=100,
    )
    ```
    """

    src: Union[str, bytes]
    """
    The image source.

    It can be one of the following:
    - A URL or local [asset file](https://flet.dev/docs/cookbook/assets) path;
    - A base64 string;
    - Raw bytes.
    """

    error_content: Optional[Control] = None
    """
    Fallback control to display if the image cannot be loaded
    from the provided source.
    """

    repeat: ImageRepeat = ImageRepeat.NO_REPEAT
    """
    How to paint any portions of the layout bounds not covered by this image.
    """

    fit: Optional[BoxFit] = None
    """
    Defines how to inscribe this image into the space allocated during layout.
    """

    border_radius: Optional[BorderRadiusValue] = None
    """
    Clips this image to have rounded corners.
    """

    color: Optional[ColorValue] = None
    """
    If set, this color is blended with each
    image pixel using [`color_blend_mode`][(c).].
    """

    color_blend_mode: Optional[BlendMode] = None
    """
    Used to combine [`color`][(c).] with the image.

    In terms of the blend mode, color is the source and this image is the destination.
    """

    gapless_playback: bool = False
    """
    Whether to continue showing the old image (`True`), or briefly show nothing
    (`False`), when the image provider changes.

    Has no effect on svg images.
    """

    semantics_label: Optional[str] = None
    """
    A semantic description of this image.

    Used to provide a description of the image to TalkBack on Android, and VoiceOver
    on iOS.
    """

    exclude_from_semantics: bool = False
    """
    Whether to exclude this image from semantics.
    """

    filter_quality: FilterQuality = FilterQuality.MEDIUM
    """
    The rendering quality of the image.
    """

    placeholder_src: Optional[Union[str, bytes]] = None
    """
    A placeholder displayed while the image is loading.

    It can be one of the following:
    - A URL or local [asset file](https://flet.dev/docs/cookbook/assets) path;
    - A base64 string;
    - Raw bytes.

    If `None`, no placeholder is shown while loading; the [`src`][(c).]
    simply appears (or fades in if [`placeholder_src`][(c).] or
    [`placeholder_fade_out_animation`][(c).] is not `None`).

    Note:
        SVG sources are currently not supported as placeholders. If provided,
        this property will be ignored and the [`src`][(c).] will be
        displayed directly instead.
    """

    placeholder_fit: Optional[BoxFit] = None
    """
    Defines how to inscribe the placeholder into its space.

    If `None`, default to [`fit`][(c).].
    """

    fade_in_animation: Optional[Animation] = None
    """
    Fade-in animation of the [`src`][(c).] image as it appears after loading,
    replacing the [`placeholder_src`][(c).].

    If `None`, defaults to
    `Animation(Duration(milliseconds=250), AnimationCurve.EASE_IN_OUT)`,
    if [`placeholder_src`][(c).] or [`placeholder_fade_out_animation`][(c).]
    is not `None`.
    """

    placeholder_fade_out_animation: Optional[Animation] = None
    """
    Fade-out animation for the [`placeholder_src`][(c).], after the [`src`][(c).] loads.

    If `None`, defaults to
    `Animation(Duration(milliseconds=150), AnimationCurve.EASE_OUT)`,
    if [`placeholder_src`][(c).] or [`fade_in_animation`][(c).] is not `None`.
    """

    cache_width: Optional[int] = None
    """
    The size at which this image should be decoded.

    The image will, however, be rendered to the constraints of the layout regardless
    of this parameter.
    """

    cache_height: Optional[int] = None
    """
    The size at which this image should be decoded.

    The image will, however, be rendered to the constraints of the layout regardless
    of this parameter.
    """

    anti_alias: bool = False
    """
    Whether to paint the image with anti-aliasing.

    Anti-aliasing alleviates the sawtooth artifact when this image is rotated.
    """

    def init(self):
        super().init()
        self._internals["skip_properties"] = ["width", "height"]
