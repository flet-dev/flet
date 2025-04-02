from typing import Optional

from flet.core.box import FilterQuality
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.types import (
    BlendMode,
    BorderRadiusValue,
    ColorValue,
    ImageFit,
    ImageRepeat,
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

    src: Optional[str] = None
    src_base64: Optional[str] = None
    error_content: Optional[Control] = None
    repeat: Optional[ImageRepeat] = None
    fit: Optional[ImageFit] = None
    border_radius: Optional[BorderRadiusValue] = None
    color: Optional[ColorValue] = None
    color_blend_mode: Optional[BlendMode] = None
    gapless_playback: Optional[bool] = None
    semantics_label: Optional[str] = None
    exclude_from_semantics: Optional[bool] = None
    filter_quality: Optional[FilterQuality] = None
    cache_width: Optional[int] = None
    cache_height: Optional[int] = None
    anti_alias: Optional[bool] = None
