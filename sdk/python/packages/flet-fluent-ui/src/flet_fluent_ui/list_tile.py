from typing import Optional

import flet as ft
from flet_fluent_ui.types import ListTileSelectionMode

__all__ = ["ListTile"]


@ft.control("FluentListTile")
class ListTile(ft.LayoutControl):
    """
    A Fluent list tile: one row of a list, with a title and optional subtitle,
    leading icon and trailing control.

    With a :attr:`selection_mode`, the tile can be selected: a selected tile
    shows an accent bar, or a checked checkbox in
    :attr:`~flet_fluent_ui.ListTileSelectionMode.MULTIPLE` mode.

    Example:
    ```python
    fluent.ListTile(
        title="Inbox",
        subtitle="3 unread messages",
        leading=fluent.FluentIcons.MAIL,
        selection_mode=fluent.ListTileSelectionMode.SINGLE,
        selected=True,
    )
    ```
    """

    title: Optional[ft.StrOrControl] = None
    """
    The main text of this tile.
    """

    subtitle: Optional[ft.StrOrControl] = None
    """
    Secondary text shown below :attr:`title`. It needs a :attr:`title`.
    """

    leading: Optional[ft.IconDataOrControl] = None
    """
    An icon or control shown before :attr:`title`.
    """

    trailing: Optional[ft.Control] = None
    """
    A control shown at the end of this tile.
    """

    selection_mode: ListTileSelectionMode = ListTileSelectionMode.NONE
    """
    Whether and how this tile can be selected.
    """

    selected: bool = False
    """
    Whether this tile is selected. Only used when :attr:`selection_mode` is not
    :attr:`~flet_fluent_ui.ListTileSelectionMode.NONE`.

    In :attr:`~flet_fluent_ui.ListTileSelectionMode.SINGLE` mode, deselect the
    other tiles of the list in :attr:`on_selection_change`.
    """

    autofocus: bool = False
    """
    Whether this tile should be focused on initial display.
    """

    on_click: Optional[ft.ControlEventHandler["ListTile"]] = None
    """
    Called when this tile is clicked.
    """

    on_selection_change: Optional[ft.ControlEventHandler["ListTile"]] = None
    """
    Called when the user selects or deselects this tile.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the new :attr:`selected` value.
    """
