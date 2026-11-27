from typing import Optional

import flet as ft

__all__ = [
    "Button",
    "FilledButton",
    "HyperlinkButton",
    "IconButton",
    "OutlinedButton",
]


@ft.control("FluentButton")
class Button(ft.LayoutControl):
    """
    A Fluent button: the standard button for most actions.

    See also :class:`~flet_fluent_ui.FilledButton` for the main action,
    :class:`~flet_fluent_ui.OutlinedButton`,
    :class:`~flet_fluent_ui.HyperlinkButton` and
    :class:`~flet_fluent_ui.IconButton`.

    Example:
    ```python
    fluent.Button("Save", on_click=lambda e: print("saved"))
    fluent.Button("Save", disabled=True)
    ```
    """

    content: Optional[ft.StrOrControl] = None
    """
    The button's label.

    If a string is provided, it is wrapped in a :class:`~flet.Text` control.
    """

    autofocus: bool = False
    """
    Whether this button should be focused on initial display.
    """

    on_click: Optional[ft.ControlEventHandler["Button"]] = None
    """
    Called when this button is clicked.
    """

    on_long_press: Optional[ft.ControlEventHandler["Button"]] = None
    """
    Called when this button is long-pressed.
    """

    on_focus: Optional[ft.ControlEventHandler["Button"]] = None
    """
    Called when this button receives focus.
    """

    on_blur: Optional[ft.ControlEventHandler["Button"]] = None
    """
    Called when this button loses focus.
    """

    async def focus(self):
        """
        Requests focus for this button.
        """
        await self._invoke_method("focus")


@ft.control("FluentFilledButton")
class FilledButton(Button):
    """
    A Fluent button filled with the accent color, for the main action of a
    page or dialog.

    Example:
    ```python
    fluent.FilledButton("Continue", on_click=lambda e: print("continue"))
    fluent.FilledButton("Continue", disabled=True)
    ```
    """


@ft.control("FluentOutlinedButton")
class OutlinedButton(Button):
    """
    A Fluent button with a border and no fill.

    Example:
    ```python
    fluent.OutlinedButton("Cancel")
    fluent.OutlinedButton("Cancel", disabled=True)
    ```
    """


@ft.control("FluentHyperlinkButton")
class HyperlinkButton(Button):
    """
    A Fluent button that looks like a hyperlink: accent-colored text with no
    border or fill.

    Example:
    ```python
    async def open_docs(e: ft.Event[fluent.HyperlinkButton]):
        await ft.UrlLauncher().launch_url("https://flet.dev")


    fluent.HyperlinkButton("Open docs", on_click=open_docs)
    fluent.HyperlinkButton("Open docs", disabled=True)
    ```
    """


@ft.control("FluentIconButton")
class IconButton(ft.LayoutControl):
    """
    A Fluent button that shows only an icon.

    Example:
    ```python
    fluent.IconButton(fluent.FluentIcons.SETTINGS, tooltip="Settings")
    fluent.IconButton(fluent.FluentIcons.SETTINGS, disabled=True)
    ```
    """

    icon: ft.IconDataOrControl
    """
    The icon to show.
    """

    icon_size: Optional[ft.Number] = None
    """
    The size of :attr:`icon` when it is an :class:`~flet.IconData`.

    If `None`, the theme's icon size for buttons is used.
    """

    autofocus: bool = False
    """
    Whether this button should be focused on initial display.
    """

    on_click: Optional[ft.ControlEventHandler["IconButton"]] = None
    """
    Called when this button is clicked.
    """

    on_long_press: Optional[ft.ControlEventHandler["IconButton"]] = None
    """
    Called when this button is long-pressed.
    """

    on_focus: Optional[ft.ControlEventHandler["IconButton"]] = None
    """
    Called when this button receives focus.
    """

    on_blur: Optional[ft.ControlEventHandler["IconButton"]] = None
    """
    Called when this button loses focus.
    """

    async def focus(self):
        """
        Requests focus for this button.
        """
        await self._invoke_method("focus")
