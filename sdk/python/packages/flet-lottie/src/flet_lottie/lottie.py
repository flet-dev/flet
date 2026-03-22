from typing import Optional, Union

import flet as ft

__all__ = ["Lottie"]


@ft.control("Lottie")
class Lottie(ft.LayoutControl):
    """
    Displays lottie animations.

    Note:
        - Layer effects are currently not supported.
            See [airbnb/lottie-android#1964](https://github.com/airbnb/lottie-android/issues/1964)
            and [xvrh/lottie-flutter#189](https://github.com/xvrh/lottie-flutter/issues/189) for details.
    """  # noqa: E501

    src: Union[str, bytes]
    """
    The lottie animation source.

    It can be one of the following:
    - A URL or local [asset file](https://flet.dev/docs/cookbook/assets) path;
    - A base64 string;
    - Raw bytes.
    """

    repeat: bool = True
    """
    Whether the animation should repeat in a loop.

    Note:
        Has no effect if [`animate`][(c).] is `False`.
    """

    reverse: bool = False
    """
    Whether the animation should be played in reverse
    (from start to end and then continuously from end to start).

    Note:
        Has no effect if [`animate`][(c).] or [`repeat`][(c).] is `False`.
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

    For more information on the error, see [`on_error`][(c).].
    """

    on_error: Optional[ft.ControlEventHandler["Lottie"]] = None
    """
    Fires when an error occurs while loading the Lottie animation.

    The [`data`][flet.Event.data] property of the event handler argument
    contains information on the error.
    """
