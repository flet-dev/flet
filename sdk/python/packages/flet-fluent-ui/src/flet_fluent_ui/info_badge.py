from typing import Optional

import flet as ft
from flet_fluent_ui.types import InfoBarSeverity

__all__ = ["InfoBadge"]


@ft.control("FluentInfoBadge")
class InfoBadge(ft.LayoutControl):
    """
    A Fluent info badge: a small colored dot or count that draws attention to
    something, such as new items.

    Example:
    ```python
    fluent.InfoBadge("5")
    fluent.InfoBadge(severity=fluent.InfoBarSeverity.ERROR)  # a dot
    ```
    """

    content: Optional[ft.StrOrControl] = None
    """
    The text or control in the badge, usually a count.

    If `None`, the badge is a small dot.
    """

    severity: InfoBarSeverity = InfoBarSeverity.INFO
    """
    The color of the badge: the accent color for
    :attr:`~flet_fluent_ui.InfoBarSeverity.INFO`, or the attention, success or
    critical color.
    """

    bgcolor: Optional[ft.ColorValue] = None
    """
    The color of the badge, overriding :attr:`severity`.
    """

    color: Optional[ft.ColorValue] = None
    """
    The color of :attr:`content`.
    """
