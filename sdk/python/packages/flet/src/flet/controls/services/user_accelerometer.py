from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import EventHandler
from flet.controls.duration import Duration
from flet.controls.services.sensor_events import (
    SensorErrorEvent,
    UserAccelerometerReadingEvent,
)
from flet.controls.services.service import Service

__all__ = ["UserAccelerometer"]


@control("UserAccelerometer")
class UserAccelerometer(Service):
    """
    Streams linear acceleration readings.

    If the device is still, or is moving along a straight line at constant speed,
    the reported acceleration is zero. If the device is moving e.g. towards north
    and its speed is increasing, the reported acceleration is towards north;
    if it is slowing down, the reported acceleration is towards south;
    if it is turning right, the reported acceleration is towards east.
    The data of this stream is obtained by filtering out the effect of gravity
    from [`AccelerometerReadingEvent`][flet.].

    Note:
        * Supported platforms: Android, iOS.
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

    on_reading: Optional[EventHandler[UserAccelerometerReadingEvent]] = None
    """
    Fires when a new reading is available.

    `event` contains `x`, `y`, `z` acceleration values and `timestamp`
    (microseconds since epoch).
    """

    on_error: Optional[EventHandler[SensorErrorEvent]] = None
    """
    Fired when the platform reports a sensor error. `event.message` is the error
    description.
    """
