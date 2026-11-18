from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import ControlEventHandler
from flet.controls.exceptions import FletUnsupportedPlatformException
from flet.controls.services.service import Service
from flet.controls.types import Number

__all__ = ["ShakeDetector"]


@control("ShakeDetector")
class ShakeDetector(Service):
    """
    Detects phone shakes.

    Note:
        * Supported platforms: Android, iOS and web.
        * The detector reads the accelerometer every 20 ms. An app has a single
          accelerometer rate, shared with any :class:`~flet.Accelerometer`: on
          Android and iOS the one added last sets it, on web the one added first.
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

    def before_update(self):
        if not (self.page.web or self.page.platform.is_mobile()):
            raise FletUnsupportedPlatformException(
                f"{self.__class__.__name__} is only supported on Android, iOS and web."
            )
