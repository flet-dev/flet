from dataclasses import dataclass, field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import (
    Event,
    EventHandler,
)
from flet.controls.core.list_view import ListView
from flet.controls.types import MouseCursor, Number


@dataclass
class OnReorderEvent(Event["ReorderableListView"]):
    """
    Represents an event triggered during the reordering of items in a \
    [`ReorderableListView`][flet.].
    """

    new_index: Optional[int]
    """The new position of the item after reordering."""

    old_index: Optional[int]
    """The original/previous position of the item before reordering."""


@control("ReorderableListView")
class ReorderableListView(ListView):
    """
    A scrollable list of controls that can be reordered.

    Tip:
        By default, each child control (from [`controls`][(c).]) is draggable using an
        automatically created drag handle (see [`show_default_drag_handles`][(c).]).
        To customize the draggable area, use the [`ReorderableDragHandle`][flet.] to
        define your own drag handle or region.

    Example:
    ```python
    ft.ReorderableListView(
        controls=[
            ft.ListTile(
                title=ft.Text(f"Item {i}"),
                bgcolor=ft.Colors.BLUE_GREY_300,
            )
            for i in range(1, 6)
        ],
    )
    ```

    """

    controls: list[Control] = field(default_factory=list)
    """
    The controls to be reordered.
    """

    anchor: Number = 0.0
    """
    The relative position of the zero scroll offset.
    """

    auto_scroller_velocity_scalar: Optional[Number] = None
    """
    The velocity scalar per pixel over scroll.

    It represents how the velocity scale with the over scroll distance.
    The auto-scroll velocity = (distance of overscroll) * velocity scalar.
    """

    header: Optional[Control] = None
    """
    A non-reorderable header item to show before the [`controls`][(c).].
    """

    footer: Optional[Control] = None
    """
    A non-reorderable footer item to show after the [`controls`][(c).].
    """

    show_default_drag_handles: bool = True
    """
    Whether to show default drag handles for each [`controls`][(c).] item.

    If `True`: on desktop platforms, a drag handle is stacked over the
    center of each item's trailing edge; on mobile platforms, a long
    press anywhere on the item starts a drag.

    The default desktop drag handle is just an `Icons.DRAG_HANDLE`
    wrapped by a [`ReorderableDragHandle`][flet.]. On mobile platforms, the entire
    item is wrapped with a [`ReorderableDelayedDragStartListener`].

    To customize the appearance or layout of drag handles, wrap each
    [`controls`][(c).] item, or a control within each of them, with a
    [`ReorderableDragHandle`][flet.], [`ReorderableDelayedDragStartListener`],
    or your own subclass of [`ReorderableDragHandle`][flet.]. For full control
    over the drag handles, you might want to set `show_default_drag_handles` to `False`.

    Example:
        ```python
        ft.ReorderableListView(
            show_default_drag_handles=False,
            controls=[
                ft.ListTile(
                    title=ft.Text(f"Draggable Item {i}", color=ft.Colors.BLACK),
                    leading=ft.ReorderableDragHandle(
                        content=ft.Icon(ft.Icons.DRAG_INDICATOR, color=ft.Colors.RED),
                        mouse_cursor=ft.MouseCursor.GRAB,
                    ),
                )
                for i in range(10)
            ],
        )
        ```
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    The cursor for a mouse pointer when it enters or is hovering over the drag handle.
    """

    on_reorder: Optional[EventHandler[OnReorderEvent]] = None
    """
    Called when a [`controls`][(c).] item has been dragged to a new location/position \
    and the order of the items gets updated.
    """

    on_reorder_start: Optional[EventHandler[OnReorderEvent]] = None
    """
    Called when a [`controls`][(c).] item drag has started.
    """

    on_reorder_end: Optional[EventHandler[OnReorderEvent]] = None
    """
    Called when the dragged [`controls`][(c).] item is dropped.
    """
