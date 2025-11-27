from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import EventHandler
from flet.controls.duration import Duration
from flet.controls.services.sensor_events import (
    BarometerReadingEvent,
    SensorErrorEvent,
)
from flet.controls.services.service import Service

__all__ = ["Barometer"]


@control("Barometer")
class Barometer(Service):
    """
    Streams barometer [readings][flet.BarometerReadingEvent]
    (atmospheric pressure in `hPa`). Useful for altitude calculations
    and weather-related experiences.

    Note:
        Supported platforms: Android, iOS. Barometer APIs are not exposed on the Web
        or desktop platforms and iOS ignores custom sampling intervals.
    """

    enabled: bool = True
    """
    Whether the sensor should be sampled. Disable to stop streaming.
    """

    interval: Optional[Duration] = None
    """
    Desired sampling interval provided as a [`Duration`][flet.Duration].
    Defaults to 200 ms, though
    some platforms (such as iOS) ignore custom sampling intervals.
    """

    cancel_on_error: bool = True
    """
    Whether the stream subscription should cancel on the first sensor error.
    """

    on_reading: Optional[EventHandler[BarometerReadingEvent]] = None
    """
    Fires when a new reading is available.

    `event` contains `pressure` (hPa) and `timestamp` (microseconds
    since epoch).
    """

    on_error: Optional[EventHandler[SensorErrorEvent]] = None
    """
    Fired when the platform reports a sensor error. `event.message` is the error
    description.
    """
