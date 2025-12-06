from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import Event, EventHandler
from flet.controls.duration import Duration
from flet.controls.exceptions import FletUnsupportedPlatformException
from flet.controls.services.sensor_error_event import SensorErrorEvent
from flet.controls.services.service import Service

__all__ = ["Gyroscope", "GyroscopeReadingEvent"]


@dataclass(kw_only=True)
class GyroscopeReadingEvent(Event["Gyroscope"]):
    """
    Discrete reading from a gyroscope.

    Gyroscope sample containing device rotation rate (`rad/s`) around each
    axis plus the microsecond timestamp.
    """

    x: float
    """Rotation rate around the X axis, in `rad/s`."""

    y: float
    """Rotation rate around the Y axis, in `rad/s`."""

    z: float
    """Rotation rate around the Z axis, in `rad/s`."""

    timestamp: datetime
    """Event timestamp."""


@control("Gyroscope")
class Gyroscope(Service):
    """
    Streams gyroscope [readings][flet.GyroscopeReadingEvent],
    reporting device rotation rate around each axis in `rad/s`.

    Note:
        * Supported platforms: Android, iOS and web.
        * Web ignores requested sampling intervals.
    """

    enabled: bool = True
    """
    Whether the sensor should be sampled. Disable to stop streaming.
    """

    interval: Optional[Duration] = None
    """
    Desired sampling interval provided as a [`Duration`][flet.Duration].
    Defaults to 200 ms.
    """

    cancel_on_error: bool = True
    """
    Whether the stream subscription should cancel on the first sensor error.
    """

    on_reading: Optional[EventHandler[GyroscopeReadingEvent]] = None
    """
    Fires when a new reading is available.

    `event` contains `x`, `y`, `z` rotation rates and `timestamp`
    (microseconds since epoch).
    """

    on_error: Optional[EventHandler[SensorErrorEvent]] = None
    """
    Fired when the platform reports a sensor error. `event.message` is the error
    description.
    """

    def before_update(self):
        if not (self.page.web or self.page.platform.is_mobile()):
            raise FletUnsupportedPlatformException(
                f"{self.__class__.__name__} is only supported on Android, iOS and web."
            )
