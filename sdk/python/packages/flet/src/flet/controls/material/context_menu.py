from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import Event, EventHandler
from flet.controls.layout_control import LayoutControl
from flet.controls.material.popup_menu_button import PopupMenuItem
from flet.controls.transform import Offset, OffsetValue

__all__ = [
    "ContextMenu",
    "ContextMenuDismissEvent",
    "ContextMenuSelectEvent",
    "ContextMenuTrigger",
]


class ContextMenuTrigger(Enum):
    """Defines how a menu is shown for a specific mouse button."""

    DOWN = "down"
    """
    Represents a trigger mode where the menu is shown
    when the mouse button is pressed down.
    """

    LONG_PRESS = "longPress"
    """
    Represents a trigger mode where the menu is shown
    after a long press of the mouse button.
    """


@dataclass(kw_only=True)
class ContextMenuDismissEvent(Event["ContextMenu"]):
    """Event fired when a [`ContextMenu`][flet.] is dismissed."""

    global_position: Offset = field(metadata={"data_field": "g"})
    """
    Global pointer position in logical pixels.
    """

    local_position: Optional[Offset] = field(default=None, metadata={"data_field": "l"})
    """
    Local pointer position relative to the wrapped control.
    """

    button: Optional[str] = field(default=None, metadata={"data_field": "b"})
    """
    Mouse button that triggered the menu.

    If a string, can be one of:
    `"primary"` (linked to [`ContextMenu.primary_items`][flet.]),
    `"secondary"` (linked to [`ContextMenu.secondary_items`][flet.]),
    or `"tertiary"` (linked to [`ContextMenu.tertiary_items`][flet.]).
    """

    trigger: Optional[ContextMenuTrigger] = field(
        default=None, metadata={"data_field": "tr"}
    )
    """
    The trigger mode that opened the menu.
    """

    item_count: Optional[int] = field(default=None, metadata={"data_field": "ic"})
    """
    Total number of entries displayed in the corresponding context menu.
    """


@dataclass(kw_only=True)
class ContextMenuSelectEvent(ContextMenuDismissEvent):
    """Event fired when a [`ContextMenu`][flet.] item is selected."""

    item_id: Optional[int] = field(default=None, metadata={"data_field": "id"})
    """
    Internal numeric identifier of the selected menu item.
    """

    item_index: Optional[int] = field(default=None, metadata={"data_field": "idx"})
    """
    Index of the selected menu entry within the rendered list.
    """

    @property
    def item(self) -> Optional[PopupMenuItem]:
        """The selected menu item."""
        return self.page.get_control(self.item_id)


@control("ContextMenu")
class ContextMenu(LayoutControl):
    """
    Wraps its [`content`][(c).] and displays contextual
    menus for specific mouse events.

    Tip:
        On web, call [`disable()`][flet.BrowserContextMenu.disable] method of
        [`Page.browser_context_menu`][flet.] to suppress the default browser
        context menu before relying on custom menus.
    """

    content: Control
    """
    The child control that listens for mouse interaction.

    Raises:
        ValueError: If not visible.
    """

    items: list[PopupMenuItem] = field(default_factory=list)
    """
    A list of menu items to display in the context menu,
    when [`open()`][(c).open] is called.
    """

    primary_items: list[PopupMenuItem] = field(default_factory=list)
    """
    A list of menu items to display in the context menu,
    for primary (usually left) mouse button actions.

    These items are displayed when the corresponding
    [`primary_trigger`][(c).] is activated.
    """

    secondary_items: list[PopupMenuItem] = field(default_factory=list)
    """
    A list of menu items to display in the context menu
    for secondary (usually right) mouse button actions.

    These items are displayed when the corresponding
    [`secondary_trigger`][(c).] is activated.
    """

    tertiary_items: list[PopupMenuItem] = field(default_factory=list)
    """
    A list of menu items to display in the context menu
    for tertiary (usually middle) mouse button actions.

    These items are displayed when the corresponding
    [`tertiary_trigger`][(c).] is activated.
    """

    primary_trigger: Optional[ContextMenuTrigger] = None
    """
    Defines a trigger mode for the display of [`primary_items`][(c).].

    If set to `None`, the trigger is disabled.
    """

    secondary_trigger: Optional[ContextMenuTrigger] = ContextMenuTrigger.DOWN
    """
    Defines a trigger mode for the display of [`secondary_items`][(c).].

    If set to `None`, the trigger is disabled.
    """

    tertiary_trigger: Optional[ContextMenuTrigger] = ContextMenuTrigger.DOWN
    """
    Defines a trigger mode for the display of [`tertiary_items`][(c).].

    If set to `None`, the trigger is disabled.
    """

    on_select: Optional[EventHandler[ContextMenuSelectEvent]] = None
    """
    Fires when a context menu item is selected.
    """

    on_dismiss: Optional[EventHandler[ContextMenuDismissEvent]] = None
    """
    Fires when the menu is dismissed without a selection,
    or when an attempt is made to open the menu but no items are available.
    """

    async def open(
        self,
        global_position: Optional[OffsetValue] = None,
        local_position: Optional[OffsetValue] = None,
    ) -> None:
        """
        Opens the context menu programmatically, and displays [`items`][(c).].

        Args:
            global_position: A global coordinate describing where the menu
                should appear. If omitted, `local_position` or the center of the
                [`content`][(c).] is used.
            local_position: A local coordinate relative to the [`content`][(c).].
                When provided without `global_position`, the coordinate is translated
                to global space automatically.
        """
        await self._invoke_method(
            "open",
            {
                "global_position": global_position,
                "local_position": local_position,
            },
        )

    def before_update(self):
        super().before_update()
        if not self.content.visible:
            raise ValueError("content must be visible")
