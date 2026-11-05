from typing import Optional

import flet as ft

__all__ = ["Progress"]


@ft.control("ShadProgress")
class Progress(ft.LayoutControl):
    """
    A Shadcn progress bar.

    Example:
    ```python
    shad.Progress(value=0.6, width=300)
    ```
    """

    value: Optional[ft.Number] = None
    """
    The progress, from `0.0` (none) to `1.0` (complete).

    If `None`, the bar shows a continuous animation for an unknown amount of
    progress.
    """

    color: Optional[ft.ColorValue] = None
    """
    The color of the filled part.

    If `None`, the primary color of the theme is used.
    """

    bgcolor: Optional[ft.ColorValue] = None
    """
    The color of the track behind the filled part.

    If `None`, a translucent primary color is used.
    """

    bar_height: Optional[ft.Number] = None
    """
    The height of the bar.

    If `None`, defaults to `16`.
    """
