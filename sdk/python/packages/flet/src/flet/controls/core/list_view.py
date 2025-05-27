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
    horizontal: bool = False
    spacing: Number = 0
    item_extent: OptionalNumber = None
    first_item_prototype: bool = False
    divider_thickness: Number = 0
    padding: OptionalPaddingValue = None
    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    semantic_child_count: Optional[int] = None
    cache_extent: OptionalNumber = None
    build_controls_on_demand: bool = True
