from flet.core.control import Service, control
from flet.core.types import Number, OptionalControlEventCallable

__all__ = ["ShakeDetector"]


@control("ShakeDetector")
class ShakeDetector(Service):
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

    minimum_shake_count: int = 1
    shake_slop_time_ms: int = 500
    shake_count_reset_time_ms: int = 3000
    shake_threshold_gravity: Number = 2.7
    on_shake: OptionalControlEventCallable = None
