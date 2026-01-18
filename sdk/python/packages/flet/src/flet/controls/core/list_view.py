from dataclasses import field
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.layout_control import LayoutControl
from flet.controls.padding import PaddingValue
from flet.controls.scrollable_control import ScrollableControl
from flet.controls.types import ClipBehavior, Number

__all__ = ["ListView"]


@control("ListView")
class ListView(LayoutControl, ScrollableControl, AdaptiveControl):
    """
    A scrollable list of controls arranged linearly.

    ListView is the most commonly used scrolling control. It displays its children one
    after another in the scroll direction. In the cross axis, the children are required
    to fill the ListView.

    ```python
    ft.ListView(
        controls=[ft.Text(f"Item {i}") for i in range(1, 6)],
    )
    ```

    """

    controls: list[Control] = field(default_factory=list)
    """
    A list of `Control`s to display inside ListView.
    """

    horizontal: bool = False
    """
    Whether to layout the [`controls`][(c).] horizontally.
    """

    reverse: bool = False
    """
    Whether the scroll view scrolls in the reading direction.

    For example, if the reading direction is left-to-right and
    [`horizontal`][(c).] is `True`,
    then the scroll view scrolls from left to right when `reverse` is `False`
    and from right to left when `reverse` is `True`.

    Similarly, if `horizontal` is `False`, then the scroll view scrolls from top
    to bottom when `reverse` is `False` and from bottom to top when `reverse` is `True`.
    """

    spacing: Number = 0
    """
    The height of divider between the [`controls`][(c).].
    """

    item_extent: Optional[Number] = None
    """
    A fixed height or width (when [`horizontal`][(c).] is `True`)
    of an item to optimize rendering.

    Note:
        This property has effect only when [`build_controls_on_demand`][(c).]
        is `True` or [`spacing`][(c).] is `0`.
    """

    first_item_prototype: bool = False
    """
    Whether the dimensions of the first item of [`controls`][(c).]
    should be used as a "prototype" for all other items,
    i.e. their `height` or `width` will be the same as the first item.
    """

    prototype_item: Optional[Control] = None
    """
    A control to be used as a "prototype" for all items,
    i.e. their `height` or `width` will be the same as the `prototype_item`.

    Note:
        This property has effect only when [`build_controls_on_demand`][(c).]
        is `True` or [`spacing`][(c).] is `0`.
    """

    divider_thickness: Number = 0
    """
    If greater than `0` then `Divider` is used as a spacing between list view items.
    """

    padding: Optional[PaddingValue] = None
    """
    The amount of space by which to inset the children.
    """

    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    """
    How to clip the [`controls`][(c).]
    """

    semantic_child_count: Optional[int] = None
    """
    The number of children that will contribute semantic information.
    """

    cache_extent: Optional[Number] = None
    """
    Items that fall in the cache area (before or after the visible area that are about
    to become visible when the user scrolls) are laid out even though they are not
    yet visible on screen.

    The `cache_extent` describes how many pixels the cache area extends before the
    leading edge and after the trailing edge of the viewport.

    The total extent covered is:
    `cache_extent` before + main axis extent + `cache_extent` after.
    """

    build_controls_on_demand: bool = True
    """
    Whether the [`controls`][(c).] should be built lazily/on-demand.

    This is particularly useful when dealing with a large number of controls.
    """
