from typing import Optional

import flet as ft

__all__ = ["Tooltip"]


@ft.control("FluentTooltip")
class Tooltip(ft.LayoutControl):
    """
    Shows a Fluent tooltip with a :attr:`message` when the pointer hovers over
    its :attr:`content`, or when it is long-pressed.

    Example:
    ```python
    fluent.Tooltip(
        message="Save the document",
        content=fluent.IconButton(fluent.FluentIcons.SAVE),
    )
    ```
    """

    message: str
    """
    The text of the tooltip.
    """

    content: ft.Control
    """
    The control that shows the tooltip.
    """

    show_below: bool = True
    """
    Whether the tooltip is shown below :attr:`content` instead of above it,
    when there is room.
    """

    wait_duration: Optional[ft.DurationValue] = None
    """
    How long the pointer must hover before the tooltip is shown.

    If `None`, the theme's default is used.
    """

    show_duration: Optional[ft.DurationValue] = None
    """
    How long the tooltip stays visible after the pointer leaves or the
    long-press ends.

    If `None`, the theme's default is used.
    """
