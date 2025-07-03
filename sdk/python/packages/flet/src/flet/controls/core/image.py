from typing import Optional

from flet.controls.base_control import control
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.box import BoxFit, FilterQuality
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import OptionalControl
from flet.controls.types import (
    BlendMode,
    ImageRepeat,
    OptionalBool,
    OptionalColorValue,
    OptionalInt,
    OptionalString,
)

__all__ = ["Image"]


@control("Image")
class Image(ConstrainedControl):
    """
    A control that displays an image.

    The source can be specified through one of the following properties (in order of precedence):

    - [`src_bytes`][(c).]
    - [`src_base64`][(c).]
    - [`src`][(c).]
    """

    src: OptionalString = None
    """
    The image source.

    This could be an external URL or a local
    [asset file](https://flet.dev/docs/cookbook/assets).
    """

    src_base64: OptionalString = None
    """
    A string representing an image encoded in Base64 format.
    
    [Here](https://github.com/flet-dev/examples/blob/main/python/controls/information-displays/image/image-base64.py) 
    is an example.
    
    /// details | Tip
        type: tip

    - Use `base64` command (on Linux, macOS or WSL) to convert file to Base64 format:
        ```bash
        base64 -i <image.png> -o <image-base64.txt>
        ```

    - On Windows you can use PowerShell to encode string into Base64 format:
        ```posh
        [convert]::ToBase64String((Get-Content -path "your_file_path" -Encoding byte))
        ```
    ///
    """

    src_bytes: Optional[bytes] = None
    """
    A byte array representing an image.
    """

    error_content: OptionalControl = None
    """
    Fallback control to display if the image cannot be loaded 
    from the provided sources (`src` or `src_base64`).
    """

    repeat: ImageRepeat = ImageRepeat.NO_REPEAT
    """
    How to paint any portions of the layout bounds not covered by the image.

    Type: [`ImageRepeat`][flet.ImageRepeat]
    """

    fit: Optional[BoxFit] = None
    """
    How to inscribe the image into the space allocated during layout.

    Type: [`BoxFit`][flet.BoxFit]
    """

    border_radius: OptionalBorderRadiusValue = None
    """
    Clip image to have rounded corners.
    """

    color: OptionalColorValue = None
    """
    If set, this [color](https://flet.dev/docs/reference/colors) is blended with each
    image pixel using [`color_blend_mode`][flet.Image.color_blend_mode].
    """

    color_blend_mode: Optional[BlendMode] = None
    """
    Used to combine `color` with the image.

    In terms of the blend mode, color is the source and this image is the destination.

    Type: [`BlendMode`][flet.BlendMode]
    """

    gapless_playback: bool = False
    """
    Whether to continue showing the old image (`True`), or briefly show nothing 
    (`False`), when the image provider changes.

    Has no effect on svg images.
    """

    semantics_label: OptionalString = None
    """
    A semantic description of the image.

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

    Type: [`FilterQuality`][flet.FilterQuality]
    """

    cache_width: OptionalInt = None
    """
    The size at which the image should be decoded.

    The image will, however, be rendered to the constraints of the layout regardless
    of this parameter.
    """

    cache_height: OptionalInt = None
    """
    The size at which the image should be decoded.

    The image will, however, be rendered to the constraints of the layout regardless
    of this parameter.
    """

    anti_alias: bool = False
    """
    Whether to paint the image with anti-aliasing.

    Anti-aliasing alleviates the sawtooth artifact when the image is rotated.
    """

