from typing import Optional

import flet as ft
from flet_fluent_ui.types import ExpanderDirection

__all__ = ["Expander"]


@ft.control("FluentExpander")
class Expander(ft.LayoutControl):
    """
    A Fluent expander: a header that shows or hides its :attr:`content` when
    clicked.

    Example:
    ```python
    fluent.Expander(
        header="Advanced options",
        content=fluent.Checkbox(label="Enable logging"),
    )
    ```
    """

    header: ft.StrOrControl
    """
    The always-visible header.
    """

    content: ft.Control
    """
    The control shown below (or above) :attr:`header` while expanded.
    """

    leading: Optional[ft.IconDataOrControl] = None
    """
    An icon or control shown before :attr:`header`.
    """

    trailing: Optional[ft.Control] = None
    """
    A control shown at the end of the header, before the chevron.
    """

    expanded: bool = False
    """
    Whether :attr:`content` is shown.
    """

    direction: ExpanderDirection = ExpanderDirection.DOWN
    """
    The direction the content opens in.
    """

    content_padding: ft.PaddingValue = 16
    """
    The padding around :attr:`content`.
    """

    on_change: Optional[ft.ControlEventHandler["Expander"]] = None
    """
    Called when the expander opens or closes.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the new :attr:`expanded` value.
    """
