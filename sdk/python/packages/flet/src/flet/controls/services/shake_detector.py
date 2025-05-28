from flet.controls.base_control import control
from flet.controls.services.service import Service
from flet.controls.types import Number, OptionalControlEventCallable

__all__ = ["ShakeDetector"]


@control("ShakeDetector")
class ShakeDetector(Service):
    """
    Detects phone shakes.

    It is non-visual and should be added to `page.services` list.

    Online docs: https://flet.dev/docs/controls/shakedetector
    """

    minimum_shake_count: int = 1
    shake_slop_time_ms: int = 500
    shake_count_reset_time_ms: int = 3000
    shake_threshold_gravity: Number = 2.7
    on_shake: OptionalControlEventCallable = None
