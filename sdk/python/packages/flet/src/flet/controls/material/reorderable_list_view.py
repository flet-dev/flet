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
    new_index: Optional[int]
    old_index: Optional[int]


@control("ReorderableListView")
class ReorderableListView(ListView):
    """
    A scrollable list of controls that can be reordered.
    """

    controls: list[Control] = field(default_factory=list)
    """
    The controls to be reordered.
    """

    horizontal: bool = False
    """
    Whether the `controls` should be laid out horizontally.
    """

    reverse: bool = False
    """
    Whether the scroll view scrolls in the reading direction.

    For example, if the reading direction is left-to-right and `horizontal` is `True`,
    then the scroll view scrolls from left to right when `reverse` is `False`
    and from right to left when `reverse` is `True`.

    Similarly, if `horizontal` is `False`, then the scroll view scrolls from top
    to bottom when `reverse` is `False` and from bottom to top when `reverse` is `True`.
    """

    item_extent: Optional[Number] = None
    """
    If non-null, forces the children to have the given extent in the scroll direction.

    Specifying an `item_extent` is more efficient than letting the children determine
    their own extent because the scrolling machinery can make use of the foreknowledge
    of the children's extent to save work, for example when the scroll position
    changes drastically.
    """

    first_item_prototype: bool = False
    """
    `True` if the dimensions of the first item should be used as a "prototype" for all
    other items, i.e. their height or width will be the same as the first item.
    """

    padding: Optional[PaddingValue] = None
    """
    The amount of space by which to inset the `controls`.
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
    The velocity scalar per pixel over scroll. It represents how the velocity scale
    with the over scroll distance. The auto-scroll velocity = (distance of overscroll)
    * velocity scalar.
    """

    header: Optional[Control] = None
    """
    A non-reorderable header item to show before the `controls`.
    """

    footer: Optional[Control] = None
    """
    A non-reorderable footer item to show after the `controls`.
    """

    build_controls_on_demand: bool = True
    """
    Whether the `controls` should be built lazily/on-demand, i.e. only when they are
    about to become visible.

    This is particularly useful when dealing with a large number of controls.
    """

    show_default_drag_handles: bool = True
    """
    TBD
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    TBD
    """

    on_reorder: Optional[EventHandler[OnReorderEvent]] = None
    """
    Called when a child control has been dragged to a new location in the list and the
    application should update the order of the items.
    """

    on_reorder_start: Optional[EventHandler[OnReorderEvent]] = None
    """
    Called when an item drag has started.
    """

    on_reorder_end: Optional[EventHandler[OnReorderEvent]] = None
    """
    Called when the dragged item is dropped.
    """
