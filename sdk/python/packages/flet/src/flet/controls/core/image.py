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

    src: OptionalString = None
    src_base64: OptionalString = None
    src_bytes: Optional[bytes] = None
    error_content: OptionalControl = None
    repeat: Optional[ImageRepeat] = None
    fit: Optional[BoxFit] = None
    border_radius: OptionalBorderRadiusValue = None
    color: OptionalColorValue = None
    color_blend_mode: Optional[BlendMode] = None
    gapless_playback: OptionalBool = None
    semantics_label: OptionalString = None
    exclude_from_semantics: OptionalBool = None
    filter_quality: Optional[FilterQuality] = None
    cache_width: OptionalInt = None
    cache_height: OptionalInt = None
    anti_alias: OptionalBool = None
