from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import ControlEventHandler
from flet.controls.services.service import Service
from flet.controls.types import Number

__all__ = ["ShakeDetector"]


@control("ShakeDetector")
class ShakeDetector(Service):
    """
    Detects phone shakes.
    """

    minimum_shake_count: int = 1
    """
    Number of shakes required before shake is triggered.
    """

    shake_slop_time_ms: int = 500
    """
    Minimum time between shakes, in milliseconds.
    """

    shake_count_reset_time_ms: int = 3000
    """
    Time, in milliseconds, before shake count resets.
    """

    shake_threshold_gravity: Number = 2.7
    """
    Shake detection threshold, in Gs.
    """

    on_shake: Optional[ControlEventHandler["ShakeDetector"]] = None
    """
    Called when a shake is detected.
    """
