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
    Payload for :class:`~flet.ReorderableListView` events related to item
    reordering.
    """

    new_index: Optional[int] = None
    """
    The new position of the item after the reordering, if available.

    Will be non-`None` only for the following events:
    :attr:`~flet.ReorderableListView.on_reorder`,
    :attr:`~flet.ReorderableListView.on_reorder_end`.
    """

    old_index: Optional[int] = None
    """
    The previous position of the item before the reordering, if available.

    Will be non-`None` only for the following events:
    :attr:`~flet.ReorderableListView.on_reorder`,
    :attr:`~flet.ReorderableListView.on_reorder_start`.
    """


@control("ReorderableListView")
class ReorderableListView(ListView):
    """
    A scrollable list of controls that can be reordered.

    Tip:
        By default, each child control (from :attr:`controls`) is draggable using an
        automatically created drag handle (see
        :attr:`show_default_drag_handles`). To customize the draggable area, use
        :class:`~flet.ReorderableDragHandle` to define your own drag handle or
        region.

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
    The controls displayed by this :class:`ReorderableListView`.

    Note:
        When an item of this list gets reordered, the :attr:`on_reorder` event gets
        fired, but it doesn't reorder the `controls` list automatically. So, to keep
        `controls` list in sync with the UI, reorder this list inside your
        :attr:`on_reorder` event handler. See :attr:`on_reorder` for an example.
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
    A non-reorderable header item to show before :attr:`controls`.
    """

    footer: Optional[Control] = None
    """
    A non-reorderable footer item to show after :attr:`controls`.
    """

    show_default_drag_handles: bool = True
    """
    Whether to show default drag handles for each :attr:`controls` item.

    If `True`: on desktop platforms, a drag handle is stacked over the
    center of each item's trailing edge; on mobile platforms, a long
    press anywhere on the item starts a drag.

    The default desktop drag handle is just an `Icons.DRAG_HANDLE`
    wrapped by a :class:`~flet.ReorderableDragHandle`. On mobile platforms, the
    entire item is wrapped with a :class:`~flet.ReorderableDragHandle`.

    To customize the appearance or layout of drag handles, wrap each
    :attr:`controls` item, or a control within each of them, with a
    :class:`~flet.ReorderableDragHandle`. For full control over the drag handles,
    you might want to set :attr:`show_default_drag_handles` to `False`.

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
    Called when a :attr:`controls` item has been dragged to a new location/position.

    Note:
        This event does not reorder :attr:`controls` automatically. So, to keep
        :attr:`controls` list in sync with the UI, reorder it accordingly inside
        your :attr:`on_reorder` event handler.

        Example:

        ```python
            def handle_reorder(e: ft.OnReorderEvent):
                rlv = e.control
                moved_item = rlv.controls.pop(e.old_index)  # Remove the reordered item from its old position
                rlv.controls.insert(e.new_index, moved_item)  # Insert the reordered item into its new position
                rlv.update()
        ```
    """  # noqa: E501

    on_reorder_start: Optional[EventHandler[OnReorderEvent]] = None
    """
    Called when a :attr:`controls` item drag has started.
    """

    on_reorder_end: Optional[EventHandler[OnReorderEvent]] = None
    """
    Called when the dragged :attr:`controls` item is dropped.
    """
