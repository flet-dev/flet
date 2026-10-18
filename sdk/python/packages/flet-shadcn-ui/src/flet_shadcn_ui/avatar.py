from typing import Optional

import flet as ft

__all__ = ["Avatar"]


@ft.control("ShadAvatar")
class Avatar(ft.LayoutControl):
    """
    A Shadcn avatar: a round image with a fallback for when it can't be shown.

    Example:
    ```python
    shad.Avatar(src="https://github.com/shadcn.png", placeholder="CN")
    ```
    """

    src: Optional[str] = None
    """
    The image to show: a URL, or a path relative to the app's assets directory.

    If `None`, or if the image fails to load, :attr:`placeholder` is shown.
    """

    placeholder: Optional[ft.StrOrControl] = None
    """
    The content shown when there is no image, typically the person's initials.
    """

    size: Optional[ft.Number] = None
    """
    The width and height of this avatar.

    If `None`, defaults to `40`.
    """

    bgcolor: Optional[ft.ColorValue] = None
    """
    The background color behind :attr:`placeholder`.

    If `None`, the muted color of the theme is used.
    """
