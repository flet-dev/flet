from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import EventHandler
from flet.controls.duration import Duration
from flet.controls.services.sensor_events import (
    GyroscopeReadingEvent,
    SensorErrorEvent,
)
from flet.controls.services.service import Service

__all__ = ["Gyroscope"]


@control("Gyroscope")
class Gyroscope(Service):
    """
    Streams gyroscope [readings][flet.GyroscopeReadingEvent],
    reporting device rotation rate around each axis in `rad/s`.

    Note:
        Supported platforms: Android, iOS, Web (sampling interval
        hints are ignored on Web).
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
