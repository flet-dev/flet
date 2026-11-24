from dataclasses import field
from typing import Optional

import flet as ft

__all__ = ["Tooltip"]


@ft.control("ShadTooltip")
class Tooltip(ft.LayoutControl):
    """
    Shows a Shadcn-styled tooltip while the pointer hovers over :attr:`content`
    (or on long press on touch devices).

    Example:
    ```python
    shad.Tooltip(
        message="Add to library",
        content=shad.Button("Hover", variant=shad.ButtonVariant.OUTLINE),
    )
    ```
    """

    content: ft.Control
    """
    The control that shows the tooltip.
    """

    message: ft.StrOrControl
    """
    The text or control shown in the tooltip.
    """

    wait_duration: ft.DurationValue = field(
        default_factory=lambda: ft.Duration(milliseconds=0)
    )
    """
    How long the pointer must hover before the tooltip appears.
    """

    show_duration: Optional[ft.DurationValue] = None
    """
    How long the tooltip stays visible after the pointer leaves.

    If `None`, it hides right away.
    """
