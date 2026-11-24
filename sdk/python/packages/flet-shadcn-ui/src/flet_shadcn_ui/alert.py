from typing import Optional

import flet as ft
from flet_shadcn_ui.types import AlertVariant

__all__ = ["Alert"]


@ft.control("ShadAlert")
class Alert(ft.LayoutControl):
    """
    A Shadcn alert that calls attention to a short message.

    Example:
    ```python
    shad.Alert(
        icon=shad.LucideIcons.TERMINAL,
        title="Heads up!",
        description="You can add components to your app using the CLI.",
    )
    ```
    """

    title: Optional[ft.StrOrControl] = None
    """
    The title of this alert.
    """

    description: Optional[ft.StrOrControl] = None
    """
    The text shown below :attr:`title`.
    """

    icon: Optional[ft.IconDataOrControl] = None
    """
    An icon or control shown before :attr:`title` and :attr:`description`.
    """

    variant: AlertVariant = AlertVariant.PRIMARY
    """
    The visual variant of this alert.
    """

    icon_color: Optional[ft.ColorValue] = None
    """
    The color of :attr:`icon`.

    If `None`, the color is taken from :attr:`variant`.
    """
