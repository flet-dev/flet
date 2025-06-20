from dataclasses import field
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.padding import OptionalPaddingValue
from flet.controls.scrollable_control import ScrollableControl
from flet.controls.types import ClipBehavior, Number, OptionalNumber

__all__ = ["ListView"]


@control("ListView")
class ListView(ConstrainedControl, ScrollableControl, AdaptiveControl):
    """
    A scrollable list of controls arranged linearly.

    ListView is the most commonly used scrolling control. It displays its children one
    after another in the scroll direction. In the cross axis, the children are required
    to fill the ListView.

    Online docs: https://flet.dev/docs/controls/listview
    """

    controls: list[Control] = field(default_factory=list)
    """
    A list of `Control`s to display inside ListView.
    """

    horizontal: bool = False
    """
    `True` to layout ListView items horizontally.
    """

    reverse: bool = False
    """
    Whether the scroll view scrolls in the reading direction.

    For example, if the reading direction is left-to-right and `horizontal` is `True`,
    then the scroll view scrolls from left to right when `reverse` is `False`
    and from right to left when `reverse` is `True`.

    Similarly, if `horizontal` is `False`, then the scroll view scrolls from top
    to bottom when `reverse` is `False` and from bottom to top when `reverse` is `True`.

    Defaults to `False`.
    """

    spacing: Number = 0
    """
    The height of Divider between ListView items.

    No spacing between items if not specified.
    """

    item_extent: OptionalNumber = None
    """
    A fixed height or width (for `horizontal` ListView) of an item to optimize 
    rendering.
    """

    first_item_prototype: bool = False
    """
    `True` if the dimensions of the first item should be used as a "prototype" for all
    other items, i.e. their height or width will be the same as the first item.

    Defaults to `False`.
    """

    divider_thickness: Number = 0
    """
    If greater than `0` then Divider is used as a spacing between list view items.
    """

    padding: OptionalPaddingValue = None
    """
    The amount of space by which to inset the children.

    Value is of type
    [`Padding`](https://flet.dev/docs/reference/types/padding).
    """

    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    """
    The content will be clipped (or not) according to this option.

    Value is of type
    [`ClipBehavior`](https://flet.dev/docs/reference/types/clipbehavior) and defaults
    to `ClipBehavior.HARD_EDGE`.
    """

    semantic_child_count: Optional[int] = None
    """
    The number of children that will contribute semantic information.
    """

    cache_extent: OptionalNumber = None
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
    Whether the `controls` should be built lazily/on-demand.

    This is particularly useful when dealing with a large number of controls.

    Defaults to `True`.
    """
