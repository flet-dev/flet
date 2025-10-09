from typing import Optional

import flet as ft

__all__ = ["Lottie"]


@ft.control("Lottie")
class Lottie(ft.LayoutControl):
    """
    Displays lottie animations.
    """

    src: Optional[str] = None
    """
    The source of the Lottie file.

    Can be a URL or a local [asset file](https://flet.dev/docs/cookbook/assets).

    Note:
        If both `src` and [`src_base64`][..] are provided,
        `src_base64` will be prioritized/used.

    Raises:
        AssertionError: If neither [`src`][(c).] nor
            [`src_base64`][(c).] is provided.
    """

    src_base64: Optional[str] = None
    """
    The base64 encoded string of the Lottie file.

    Note:
        If both `src_base64` and [`src`][..] are provided,
        `src_base64` will be prioritized/used.

    Raises:
        AssertionError: If neither [`src`][(c).] nor
            [`src_base64`][(c).] is provided.
    """

    repeat: bool = True
    """
    Whether the animation should repeat in a loop.

    Note:
        Has no effect if [`animate`][..] is `False`.
    """

    reverse: bool = False
    """
    Whether the animation should be played in reverse
    (from start to end and then continuously from end to start).

    Note:
        Has no effect if [`animate`][..] or [`repeat`][..] is `False`.
    """

    animate: bool = True
    """
    Whether the animation should be played automatically.
    """

    enable_merge_paths: bool = False
    """
    Whether to enable merge path support.
    """

    enable_layers_opacity: bool = False
    """
    Whether to enable layer-level opacity.
    """

    background_loading: Optional[bool] = None
    """
    Whether the animation should be loaded in the background.
    """

    filter_quality: ft.FilterQuality = ft.FilterQuality.LOW
    """
    The quality of the image layer.
    """

    fit: Optional[ft.BoxFit] = None
    """
    Defines how to inscribe the Lottie composition
    into the space allocated during layout.
    """

    headers: Optional[dict[str, str]] = None
    """
    Headers for network requests.
    """

    error_content: Optional[ft.Control] = None
    """
    A control to display when an error occurs
    while loading the Lottie animation.

    For more information on the error, see [`on_error`][..].
    """

    on_error: Optional[ft.ControlEventHandler["Lottie"]] = None
    """
    Fires when an error occurs while loading the Lottie animation.

    The [`data`][flet.Event.data] property of the event handler argument
    contains information on the error.
    """

    def before_update(self):
        super().before_update()
        assert self.src or self.src_base64, (
            "at least one of src and src_base64 must be provided"
        )
