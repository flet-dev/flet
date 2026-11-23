from typing import Optional

import flet as ft
from flet_fluent_ui.types import InfoBarSeverity

__all__ = ["InfoBar"]


@ft.control("FluentInfoBar")
class InfoBar(ft.LayoutControl):
    """
    A Fluent info bar: an inline message about the state of the app, colored
    by its :attr:`severity`.

    Example:
    ```python
    fluent.InfoBar(
        title="Update available",
        content="Restart the app to install it.",
        severity=fluent.InfoBarSeverity.WARNING,
    )
    ```
    """

    title: ft.StrOrControl
    """
    The title of the message.
    """

    content: Optional[ft.StrOrControl] = None
    """
    The text shown after :attr:`title`.
    """

    action: Optional[ft.Control] = None
    """
    A control shown after :attr:`content`, usually a
    :class:`~flet_fluent_ui.Button`.
    """

    severity: InfoBarSeverity = InfoBarSeverity.INFO
    """
    The severity of the message, which sets the color and icon.
    """

    long: bool = False
    """
    Whether :attr:`content` and :attr:`action` are shown below :attr:`title`
    instead of on the same line, for longer messages.
    """

    icon_visible: bool = True
    """
    Whether the severity icon is shown.
    """

    on_close: Optional[ft.ControlEventHandler["InfoBar"]] = None
    """
    Called when the close button is clicked.

    The close button is only shown when this handler is set. The info bar is
    not hidden automatically: hide or remove it in the handler.
    """
