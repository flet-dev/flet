from typing import Optional

import flet as ft

__all__ = ["Popover"]


@ft.control("ShadPopover")
class Popover(ft.LayoutControl):
    """
    A Shadcn popover: a floating panel attached to :attr:`content`, opened and
    closed with :attr:`open`.

    Example:
    ```python
    def toggle(e):
        popover.open = not popover.open


    popover = shad.Popover(
        content=shad.Button("Open popover", on_click=toggle),
        popover=ft.Text("Place content for the popover here."),
    )
    ```
    """

    content: ft.Control
    """
    The control the popover is attached to.
    """

    popover: ft.Control
    """
    The control shown in the floating panel.
    """

    open: bool = False
    """
    Whether the popover is shown.
    """

    close_on_tap_outside: bool = True
    """
    Whether tapping outside the popover closes it.
    """

    on_dismiss: Optional[ft.ControlEventHandler["Popover"]] = None
    """
    Called when the popover is closed by tapping outside it.

    :attr:`open` is set to `False` before this is called.
    """
