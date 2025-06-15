from flet.controls.base_control import control
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.services.service import Service
from flet.controls.types import Number

__all__ = ["ShakeDetector"]


@control("ShakeDetector")
class ShakeDetector(Service):
    """
    Detects phone shakes.

    It is non-visual and should be added to `page.services` list.

    Online docs: https://flet.dev/docs/controls/shakedetector
    """

    minimum_shake_count: int = 1
    """
    Number of shakes required before shake is triggered.

    Defaults to `1`.
    """

    shake_slop_time_ms: int = 500
    """
    Minimum time between shakes, in milliseconds.

    Defaults to `500`.
    """

    shake_count_reset_time_ms: int = 3000
    """
    Time, in milliseconds, before shake count resets.

    Defaults to `3000`.
    """

    shake_threshold_gravity: Number = 2.7
    """
    Shake detection threshold, in Gs.

    Defaults to `2.7`.
    """

    on_shake: OptionalControlEventHandler["ShakeDetector"] = None
    """
    Triggers when the shake detected.
    """
