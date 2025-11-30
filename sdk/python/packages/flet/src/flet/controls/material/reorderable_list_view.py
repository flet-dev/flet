from dataclasses import dataclass, field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import (
    Event,
    EventHandler,
)
from flet.controls.core.list_view import ListView
from flet.controls.padding import PaddingValue
from flet.controls.types import (
    ClipBehavior,
    MouseCursor,
    Number,
)


@dataclass
class OnReorderEvent(Event["ReorderableListView"]):
    """
    Represents an event triggered during the reordering of items in a
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

    horizontal: bool = False
    """
    Whether the [`controls`][(c).] should be laid out horizontally.
    """

    reverse: bool = False
    """
    Whether the scroll view scrolls in the reading direction.

    For example, if the reading direction is left-to-right and [`horizontal`][(c).]
    is `True`, then the scroll view scrolls from left to right when `reverse` is `False`
    and from right to left when `reverse` is `True`.

    Similarly, if [`horizontal`][(c).] is `False`, then the scroll view scrolls from top
    to bottom when `reverse` is `False` and from bottom to top when `reverse` is `True`.
    """

    item_extent: Optional[Number] = None
    """
    Defines the extent that the [`controls`][(c).] should have in the scroll direction.

    Specifying an `item_extent` is more efficient than letting the [`controls`][(c).]
    determine their own extent because the scrolling machinery can make use of the
    foreknowledge of the `controls` extent to save work, for example when the scroll
    position changes drastically.
    """

    first_item_prototype: bool = False
    """
    Whether the dimensions of the first item should be used as a "prototype"
    for all other items.

    If `True`, their height or width will be the same as the first item.
    """

    padding: Optional[PaddingValue] = None
    """
    The amount of space by which to inset the [`controls`][(c).].
    """

    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    """
    The content will be clipped (or not) according to this option.
    """

    cache_extent: Optional[Number] = None
    """
    The viewport has an area before and after the visible area to cache items that are
    about to become visible when the user scrolls.

    Items that fall in this cache area are laid out even though they are not (yet)
    visible on screen. The `cache_extent` describes how many pixels the cache area
    extends before the leading edge and after the trailing edge of the viewport.

    The total extent, which the viewport will try to cover with children, is
    `cache_extent` before the leading edge + extent of the main axis + `cache_extent`
    after the trailing edge.

    The cache area is also used to implement implicit accessibility scrolling on iOS:
    When the accessibility focus moves from an item in the visible viewport to an
    invisible item in the cache area, the framework will bring that item into view
    with an (implicit) scroll action.
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

    build_controls_on_demand: bool = True
    """
    Whether the [`controls`][(c).] should be built lazily/on-demand,
    i.e. only when they are about to become visible.

    This is particularly useful when dealing with a large number of controls.
    """

    show_default_drag_handles: bool = True
    """
    Whether to show default drag handles for each [`controls`][(c).] item.

    If `True`: on desktop platforms, a drag handle is stacked over the
    center of each item's trailing edge; on mobile platforms, a long
    press anywhere on the item starts a drag.

    The default desktop drag handle is just an [`Icons.DRAG_HANDLE`][flet.]
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
    Called when a [`controls`][(c).] item has been dragged to a new location/position
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
