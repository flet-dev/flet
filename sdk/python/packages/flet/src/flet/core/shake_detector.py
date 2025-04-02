from typing import Optional

from flet.core.control import Control, control
from flet.core.types import OptionalControlEventCallable, OptionalNumber

__all__ = ["ShakeDetector"]


@control("ShakeDetector")
class ShakeDetector(Control):
    """
    Detects phone shakes.

    It is non-visual and should be added to `page.overlay` list.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        shd = ft.ShakeDetector(
            minimum_shake_count=2,
            shake_slop_time_ms=300,
            shake_count_reset_time_ms=1000,
            on_shake=lambda _: print("SHAKE DETECTED!"),
        )
        page.overlay.append(shd)

        page.add(ft.Text("Program body"))

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/shakedetector
    """

    minimum_shake_count: Optional[int] = None
    shake_slop_time_ms: Optional[int] = None
    shake_count_reset_time_ms: Optional[int] = None
    shake_threshold_gravity: OptionalNumber = None
    on_shake: OptionalControlEventCallable = None
