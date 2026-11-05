from dataclasses import field
from typing import Optional

import flet as ft
from flet_shadcn_ui.types import DialogVariant, SheetSide, ToastVariant

__all__ = ["Dialog", "Sheet", "Sonner", "Toast"]


@ft.control("ShadDialog")
class Dialog(ft.DialogControl):
    """
    A Shadcn dialog: a window over the page that the user must deal with
    before going back to it.

    Open it with :meth:`flet.Page.show_dialog` and close it with
    :meth:`flet.Page.pop_dialog`, like :class:`~flet.AlertDialog`.

    Example:
    ```python
    page.show_dialog(
        shad.Dialog(
            title="Edit profile",
            description="Make changes to your profile here.",
            content=shad.Input(value="Pedro Duarte"),
            actions=[shad.Button("Save changes", on_click=save)],
        )
    )
    ```
    """

    title: Optional[ft.StrOrControl] = None
    """
    The title of this dialog.
    """

    description: Optional[ft.StrOrControl] = None
    """
    The text shown below :attr:`title`.
    """

    content: Optional[ft.Control] = None
    """
    The main content of this dialog.
    """

    actions: list[ft.Control] = field(default_factory=list)
    """
    The buttons shown at the bottom, usually :class:`~flet_shadcn_ui.Button`
    controls.
    """

    variant: DialogVariant = DialogVariant.PRIMARY
    """
    The visual variant of this dialog.
    """

    modal: bool = False
    """
    Whether the dialog stays open when the user clicks outside it.
    """


@ft.control("ShadSheet")
class Sheet(ft.DialogControl):
    """
    A Shadcn sheet: a panel that slides in from an edge of the screen.

    Open it with :meth:`flet.Page.show_dialog` and close it with
    :meth:`flet.Page.pop_dialog`.

    Example:
    ```python
    page.show_dialog(
        shad.Sheet(
            side=shad.SheetSide.RIGHT,
            title="Settings",
            content=shad.Switch(label="Notifications"),
        )
    )
    ```
    """

    side: SheetSide = SheetSide.BOTTOM
    """
    The edge of the screen the sheet slides in from.
    """

    title: Optional[ft.StrOrControl] = None
    """
    The title of this sheet.
    """

    description: Optional[ft.StrOrControl] = None
    """
    The text shown below :attr:`title`.
    """

    content: Optional[ft.Control] = None
    """
    The main content of this sheet.
    """

    actions: list[ft.Control] = field(default_factory=list)
    """
    The buttons shown at the bottom, usually :class:`~flet_shadcn_ui.Button`
    controls.
    """

    modal: bool = False
    """
    Whether the sheet stays open when the user clicks outside it.
    """


@ft.control("ShadToast")
class Toast(ft.DialogControl):
    """
    A Shadcn toast: a short notification in a corner of the screen that
    disappears after :attr:`duration`.

    Only one toast is visible at a time: showing another one replaces it.
    For notifications that stack, use :class:`~flet_shadcn_ui.Sonner`.

    Open it with :meth:`flet.Page.show_dialog`, like :class:`~flet.SnackBar`.
    :attr:`~flet.DialogControl.on_dismiss` is called when it disappears,
    whether it timed out, was closed by the user or was replaced.

    Example:
    ```python
    page.show_dialog(
        shad.Toast(
            title="Scheduled: Catch up",
            description="Friday, February 10, 2023 at 5:57 PM",
        )
    )
    ```
    """

    title: Optional[ft.StrOrControl] = None
    """
    The title of this toast.
    """

    description: Optional[ft.StrOrControl] = None
    """
    The text shown below :attr:`title`.
    """

    action: Optional[ft.Control] = None
    """
    A control shown next to the text, usually a small
    :class:`~flet_shadcn_ui.Button` such as "Undo".
    """

    variant: ToastVariant = ToastVariant.PRIMARY
    """
    The visual variant of this toast.
    """

    duration: ft.DurationValue = field(default_factory=lambda: ft.Duration(seconds=5))
    """
    How long the toast stays visible.
    """


@ft.control("ShadSonner")
class Sonner(ft.DialogControl):
    """
    A Shadcn Sonner toast: a notification in the bottom-right corner that
    stacks with other Sonner toasts and disappears after :attr:`duration`.

    Hovering the stack expands it to show every toast.

    Open it with :meth:`flet.Page.show_dialog`.
    :attr:`~flet.DialogControl.on_dismiss` is called when it disappears,
    whether it timed out or was closed by the user.

    Example:
    ```python
    page.show_dialog(
        shad.Sonner(
            title="Event has been created",
            description="Sunday, December 03, 2023 at 9:00 AM",
        )
    )
    ```
    """

    title: Optional[ft.StrOrControl] = None
    """
    The title of this toast.
    """

    description: Optional[ft.StrOrControl] = None
    """
    The text shown below :attr:`title`.
    """

    action: Optional[ft.Control] = None
    """
    A control shown next to the text, usually a small
    :class:`~flet_shadcn_ui.Button` such as "Undo".
    """

    variant: ToastVariant = ToastVariant.PRIMARY
    """
    The visual variant of this toast.
    """

    duration: ft.DurationValue = field(default_factory=lambda: ft.Duration(seconds=5))
    """
    How long the toast stays visible.
    """
