from dataclasses import field
from typing import List, Optional

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

    GridView is very effective for large lists (thousands of items). Prefer it over wrapping `Column` or `Row` for smooth scrolling.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "GridView Example"
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 50
        page.update()

        images = ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=150,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,
        )

        page.add(images)

        for i in range(0, 60):
            images.controls.append(
                ft.Image(
                    src=f"https://picsum.photos/150/150?{i}",
                    fit=ft.ImageFit.NONE,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    border_radius=ft.border_radius.all(10),
                )
            )
        page.update()

    ft.app(target=main)

    ```

    -----

    Online docs: https://flet.dev/docs/controls/gridview
    """

    controls: List[Control] = field(default_factory=list)
    horizontal: bool = False
    runs_count: int = 1
    max_extent: Optional[int] = None
    spacing: Number = 10
    run_spacing: Number = 10
    child_aspect_ratio: Number = 1.0
    padding: OptionalPaddingValue = None
    clip_behavior: Optional[ClipBehavior] = None
    semantic_child_count: Optional[int] = None
    cache_extent: OptionalNumber = None

    def __contains__(self, item):
        return item in self.controls
