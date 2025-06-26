from dataclasses import field
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.padding import OptionalPaddingValue
from flet.controls.scrollable_control import ScrollableControl
from flet.controls.types import ClipBehavior, Number, OptionalNumber

__all__ = ["GridView"]


@control("GridView")
class GridView(ConstrainedControl, ScrollableControl, AdaptiveControl):
    """
    A scrollable, 2D array of controls.

    GridView is very effective for large lists (thousands of items). Prefer it over
    wrapping `Column` or `Row` for smooth scrolling.

    Online docs: https://flet.dev/docs/controls/gridview
    """

    controls: list[Control] = field(default_factory=list)
    """
    A list of `Control`s to display inside GridView.
    """

    horizontal: bool = False
    """
    `True` to layout GridView items horizontally.
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

    runs_count: int = 1
    """
    The number of children in the cross axis.
    """

    max_extent: Optional[int] = None
    """
    The maximum width or height of the grid item.
    """

    spacing: Number = 10
    """
    The number of logical pixels between each child along the main axis.
    """

    run_spacing: Number = 10
    """
    The number of logical pixels between each child along the cross axis.
    """

    child_aspect_ratio: Number = 1.0
    """
    The ratio of the cross-axis to the main-axis extent of each child.
    """

    padding: OptionalPaddingValue = None
    """
    The amount of space by which to inset the children.

    Padding is an instance of
    [`Padding`](https://flet.dev/docs/reference/types/padding).
    """

    clip_behavior: Optional[ClipBehavior] = None
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
    Items that fall in the cache area (area before or after the visible area that are
    about to become visible when the user scrolls) are laid out even though they are
    not (yet) visible on screen.

    The cacheExtent describes how many pixels the cache area extends before the leading
    edge and after the trailing edge of the viewport.

    The total extent, which the viewport will try to cover with `controls`, is
    `cache_extent` before the leading edge + extent of the main axis + `cache_extent`
    after the trailing edge.
    """

    build_controls_on_demand: bool = True
    """
    TBD
    """

    def __contains__(self, item):
        return item in self.controls
