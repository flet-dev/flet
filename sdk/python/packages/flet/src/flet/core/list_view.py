from dataclasses import field
from typing import List, Optional

from flet.core.adaptive_control import AdaptiveControl
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.padding import OptionalPaddingValue
from flet.core.scrollable_control import ScrollableControl
from flet.core.types import ClipBehavior, OptionalNumber

__all__ = ["ListView"]


@control("ListView")
class ListView(ConstrainedControl, ScrollableControl, AdaptiveControl):
    """
    A scrollable list of controls arranged linearly.

    ListView is the most commonly used scrolling control. It displays its children one after another in the scroll direction. In the cross axis, the children are required to fill the ListView.

    Example:

    ```
    from time import sleep
    import flet as ft

    def main(page: ft.Page):
        page.title = "Auto-scrolling ListView"

        lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

        count = 1

        for i in range(0, 60):
            lv.controls.append(ft.Text(f"Line {count}"))
            count += 1

        page.add(lv)

        for i in range(0, 60):
            sleep(1)
            lv.controls.append(ft.Text(f"Line {count}"))
            count += 1
            page.update()

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/listview
    """

    controls: List[Control] = field(default_factory=list)
    horizontal: bool = False
    spacing: OptionalNumber = None
    item_extent: OptionalNumber = None
    first_item_prototype: bool = False
    divider_thickness: OptionalNumber = None
    padding: OptionalPaddingValue = None
    clip_behavior: Optional[ClipBehavior] = None
    semantic_child_count: Optional[int] = None
    cache_extent: OptionalNumber = None
    build_controls_on_demand: bool = True
