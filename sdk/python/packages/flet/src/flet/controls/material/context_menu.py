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
    "ContextMenuEvent",
    "ContextMenuSelectEvent",
    "ContextMenuTrigger",
]


class ContextMenuTrigger(str, Enum):
    """Defines how a menu is shown for a specific mouse button."""

    DISABLED = "disabled"
    DOWN = "down"
    LONG_PRESS = "longPress"


@dataclass(kw_only=True)
class ContextMenuEvent(Event["ContextMenu"]):
    """Event fired when a context menu is shown or dismissed."""

    button: str = field(metadata={"data_field": "b"})
    """Mouse button that triggered the menu."""

    global_position: Offset = field(metadata={"data_field": "g"})
    """Global pointer position in logical pixels."""

    local_position: Optional[Offset] = field(default=None, metadata={"data_field": "l"})
    """Local pointer position relative to the wrapped control."""

    trigger: Optional[str] = field(default=None, metadata={"data_field": "tr"})
    """Trigger mode that opened the menu."""

    item_count: Optional[int] = field(default=None, metadata={"data_field": "ic"})
    """Total number of entries displayed in the context menu."""


@dataclass(kw_only=True)
class ContextMenuSelectEvent(ContextMenuEvent):
    """Event fired when a context menu item is selected."""

    item_id: Optional[int] = field(default=None, metadata={"data_field": "id"})
    """Internal numeric identifier of the selected menu item."""

    item_index: Optional[int] = field(default=None, metadata={"data_field": "idx"})
    """Index of the selected menu entry within the rendered list."""

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
        On the web, call [`disable()`][`flet.BrowserContextMenu.disable`] method of
        [`Page.browser_context_menu`][`flet.`] to suppress the default browser menu
        before relying on custom menus.
    """

    content: Control
    """
    The child control that listens for mouse interaction.

    Raises:
        ValueError: If not visible.
    """

    items: list[PopupMenuItem] = field(default_factory=list)
    """
    A default menu definition used when button-specific items are not supplied.
    """

    primary_items: list[PopupMenuItem] = field(default_factory=list)
    """
    The menu displayed for primary (usually left) mouse button actions.
    """

    secondary_items: list[PopupMenuItem] = field(default_factory=list)
    """
    The menu displayed for secondary (usually right) mouse button actions.
    """

    tertiary_items: list[PopupMenuItem] = field(default_factory=list)
    """
    The menu displayed for tertiary (usually middle) mouse button actions.
    """

    primary_trigger: ContextMenuTrigger = ContextMenuTrigger.DISABLED
    """
    How the menu for the primary button is invoked.
    """

    secondary_trigger: ContextMenuTrigger = ContextMenuTrigger.DOWN
    """
    How the menu for the secondary button is invoked.
    """

    tertiary_trigger: ContextMenuTrigger = ContextMenuTrigger.DOWN
    """
    How the menu for the tertiary button is invoked.
    """

    on_open: Optional[EventHandler[ContextMenuEvent]] = None
    """
    Fires immediately after the menu is shown.
    """

    on_select: Optional[EventHandler[ContextMenuSelectEvent]] = None
    """
    Fires when a `PopupMenuItem` is selected.
    """

    on_dismiss: Optional[EventHandler[ContextMenuEvent]] = None
    """
    Fires when the menu is dismissed without a selection, or when an attempt is made
    to open the menu but no items are available.
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
                wrapped control is used.
            local_position: A local coordinate relative to the wrapped control.
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
