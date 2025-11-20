from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import EventHandler
from flet.controls.duration import Duration
from flet.controls.services.sensor_events import (
    MagnetometerReadingEvent,
    SensorErrorEvent,
)
from flet.controls.services.service import Service

__all__ = ["Magnetometer"]


@control("Magnetometer")
class Magnetometer(Service):
    """
    Streams magnetometer [readings][flet.MagnetometerReadingEvent]
    reporting the ambient magnetic field (`uT`) per axis for compass-style
    use cases.

    Note:
        Supported platforms: Android, iOS. Magnetometer APIs are not available on Web
        or desktop, so always handle `on_error` to detect unsupported hardware.
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

    on_reading: Optional[EventHandler[MagnetometerReadingEvent]] = None
    """
    Fires when a new reading is available.

    `event` contains `x`, `y`, `z` magnetic field strengths (uT)
    and `timestamp` (microseconds since epoch).
    """

    on_error: Optional[EventHandler[SensorErrorEvent]] = None
    """
    Fired when the platform reports a sensor error. `event.message` is the error
    description.
    """
