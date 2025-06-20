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

    Online docs: https://flet.dev/docs/controls/image
    """

    src: OptionalString = None
    """
    The image source.

    This could be an external URL or a local
    [asset file](https://flet.dev/docs/cookbook/assets).
    """

    src_base64: OptionalString = None
    """
    Displays an image from Base-64 encoded string, for example:

    https://github.com/flet-dev/examples/blob/main/python/controls/information-displays/image/image-base64.py

    Use `base64` command (Linux, macOS, WSL) to convert file to Base64 format:

    ```
    base64 -i <image.png> -o <image-base64.txt>
    ```

    On Windows you can use PowerShell to encode string into Base64 format:

    ```posh
    [convert]::ToBase64String((Get-Content -path "your_file_path" -Encoding byte))
    ```
    """

    src_bytes: Optional[bytes] = None
    """
    TBD
    """

    error_content: OptionalControl = None
    """
    Fallback `Control` to display if the image cannot be loaded from the source.
    """

    repeat: Optional[ImageRepeat] = None
    """
    How to paint any portions of the layout bounds not covered by the image.

    Values is of type
    [`ImageRepeat`](https://flet.dev/docs/reference/types/imagerepeat)
    and defaults to `ImageRepeat.NO_REPEAT`.
    """

    fit: Optional[BoxFit] = None
    """
    How to inscribe the image into the space allocated during layout.

    Value is of type
    [`ImageFit`](https://flet.dev/docs/reference/types/imagefit) and defaults to
    `ImageFit.NONE`.
    """

    border_radius: OptionalBorderRadiusValue = None
    """
    Clip image to have rounded corners.

    Value is of type
    [`BorderRadius`](https://flet.dev/docs/reference/types/borderradius).
    """

    color: OptionalColorValue = None
    """
    If set, this [color](https://flet.dev/docs/reference/colors) is blended with each
    image pixel using `color_blend_mode`.
    """

    color_blend_mode: Optional[BlendMode] = None
    """
    Used to combine `color` with the image.

    In terms of the blend mode, color is the source and this image is the destination.

    Value is of type
    [`BlendMode`](https://flet.dev/docs/reference/types/blendmode) and defaults to
    `BlendMode.COLOR`.
    """

    gapless_playback: OptionalBool = None
    """
    Whether to continue showing the old image (`True`), or briefly show nothing 
    (`False`), when the image provider changes.

    Defaults to `False`.
    """

    semantics_label: OptionalString = None
    """
    A semantic description of the image.

    Used to provide a description of the image to TalkBack on Android, and VoiceOver
    on iOS.
    """

    exclude_from_semantics: OptionalBool = None
    """
    Whether to exclude this image from semantics.

    Defaults to `False`.
    """

    filter_quality: Optional[FilterQuality] = None
    """
    The rendering quality of the image.

    Value is of type
    [`FilterQuality`](https://flet.dev/docs/reference/types/filterquality)
    and defaults to `FilterQuality.MEDIUM`.
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

    anti_alias: OptionalBool = None
    """
    Whether to paint the image with anti-aliasing.

    Anti-aliasing alleviates the sawtooth artifact when the image is rotated.
    """

