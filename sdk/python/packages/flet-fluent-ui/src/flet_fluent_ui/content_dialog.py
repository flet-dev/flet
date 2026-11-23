from dataclasses import field
from typing import Optional

import flet as ft

__all__ = ["ContentDialog"]


@ft.control("FluentContentDialog")
class ContentDialog(ft.DialogControl):
    """
    A Fluent dialog: a window over the page that the user must deal with
    before going back to it.

    Open it with :meth:`flet.Page.show_dialog` and close it with
    :meth:`flet.Page.pop_dialog`, like :class:`~flet.AlertDialog`.

    Example:
    ```python
    page.show_dialog(
        fluent.ContentDialog(
            title="Delete file?",
            content="The file will be deleted permanently.",
            actions=[
                fluent.FilledButton("Delete", on_click=delete),
                fluent.Button("Cancel", on_click=lambda e: page.pop_dialog()),
            ],
        )
    )
    ```
    """

    title: Optional[ft.StrOrControl] = None
    """
    The title of this dialog.
    """

    content: Optional[ft.StrOrControl] = None
    """
    The main content of this dialog.
    """

    actions: list[ft.Control] = field(default_factory=list)
    """
    The buttons shown at the bottom, usually :class:`~flet_fluent_ui.Button`
    and :class:`~flet_fluent_ui.FilledButton` controls. They share the width
    of the dialog equally.
    """

    modal: bool = True
    """
    Whether the dialog stays open when the user clicks outside it.

    The dialog can be closed with `Esc` either way.
    """
