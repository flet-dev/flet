from dataclasses import field
from typing import Optional

import flet as ft
from flet_fluent_ui.types import FlyoutPlacementMode

__all__ = ["Flyout", "TeachingTip"]


@ft.control("FluentFlyout")
class Flyout(ft.LayoutControl):
    """
    A Fluent flyout: a light popup attached to :attr:`content`, opened and
    closed with :attr:`open`.

    Example:
    ```python
    def toggle(e):
        flyout.open = not flyout.open


    flyout = fluent.Flyout(
        content=fluent.Button("Empty cart", on_click=toggle),
        flyout=ft.Text("All items will be removed. Do you want to continue?"),
    )
    ```
    """

    content: ft.Control
    """
    The control the flyout is attached to.
    """

    flyout: ft.Control
    """
    The control shown in the popup.
    """

    open: bool = False
    """
    Whether the flyout is shown.

    Resizing the window closes the flyout, which calls :attr:`on_dismiss`.
    """

    placement: FlyoutPlacementMode = FlyoutPlacementMode.AUTO
    """
    Where the flyout opens relative to :attr:`content`.
    """

    dismissible: bool = True
    """
    Whether clicking outside the flyout, or pressing Escape, closes it.
    """

    dismiss_on_pointer_move_away: bool = False
    """
    Whether the flyout closes when the mouse pointer leaves both the flyout
    and :attr:`content`.
    """

    on_dismiss: Optional[ft.ControlEventHandler["Flyout"]] = None
    """
    Called when the flyout is closed other than by setting :attr:`open` to
    `False`: by the user, or by resizing the window.

    :attr:`open` is set to `False` before this is called.
    """


@ft.control("FluentTeachingTip")
class TeachingTip(ft.LayoutControl):
    """
    A Fluent teaching tip: a callout that points at :attr:`content` to tell
    the user about a feature, opened and closed with :attr:`open`.

    Example:
    ```python
    tip = fluent.TeachingTip(
        content=fluent.Button("Save"),
        title="Save automatically",
        subtitle="Changes are saved as you type, so you can close this page "
        "at any time.",
        open=True,
    )
    ```
    """

    content: ft.Control
    """
    The control the tip points at.
    """

    title: ft.StrOrControl
    """
    The title of the tip, shown in bold.
    """

    subtitle: Optional[ft.StrOrControl] = None
    """
    The text of the tip, below :attr:`title`.
    """

    leading: Optional[ft.IconDataOrControl] = None
    """
    An icon or control shown before :attr:`title`.
    """

    buttons: list[ft.Control] = field(default_factory=list)
    """
    Buttons shown in a row at the bottom of the tip, sharing its width.
    """

    media: Optional[ft.Control] = None
    """
    An image or other control shown at the edge of the tip, opposite the
    control it points at.

    It is not shown when the tip has :attr:`buttons`.
    """

    open: bool = False
    """
    Whether the tip is shown.

    Resizing the window closes the tip, which calls :attr:`on_dismiss`.
    """

    placement: FlyoutPlacementMode = FlyoutPlacementMode.AUTO
    """
    Where the tip opens relative to :attr:`content`.
    """

    show_close_button: bool = True
    """
    Whether the tip has a close button in its corner.
    """

    dismissible: bool = True
    """
    Whether clicking outside the tip, or pressing Escape, closes it.
    """

    on_dismiss: Optional[ft.ControlEventHandler["TeachingTip"]] = None
    """
    Called when the tip is closed other than by setting :attr:`open` to
    `False`: by the user, or by resizing the window.

    :attr:`open` is set to `False` before this is called.
    """
