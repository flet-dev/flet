from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import Event, EventHandler
from flet.controls.duration import Duration
from flet.controls.services.sensor_error_event import SensorErrorEvent
from flet.controls.services.service import Service
from flet.utils.platform_utils import FletUnsupportedPlatformException

__all__ = ["Accelerometer", "AccelerometerReadingEvent"]


@dataclass(kw_only=True)
class AccelerometerReadingEvent(Event["Accelerometer"]):
    """
    Discrete reading from an accelerometer. Accelerometers measure the velocity
    of the device. Note that these readings include the effects of gravity.
    Put simply, you can use accelerometer readings to tell if the device
    is moving in a particular direction.
    """

    x: float
    """Acceleration along the X axis, in `m/s^2`."""

    y: float
    """Acceleration along the Y axis, in `m/s^2`."""

    z: float
    """Acceleration along the Z axis, in `m/s^2`."""

    timestamp: datetime
    """Event timestamp."""


@control("Accelerometer")
class Accelerometer(Service):
    """
    Streams raw accelerometer [readings][flet.AccelerometerReadingEvent],
    which describe the acceleration of the device, in `m/s^2`, including
    the effects of gravity.

    Unlike [UserAccelerometer][flet.],
    this service reports raw data from the accelerometer (physical sensor
    embedded in the mobile device) without any post-processing.

    The accelerometer is unable to distinguish between the effect of an
    accelerated movement of the device and the effect of the surrounding
    gravitational field. This means that, at the surface of Earth,
    even if the device is completely still, the reading of [`Accelerometer`][flet.]
    is an acceleration of intensity 9.8 directed upwards (the opposite of
    the graviational acceleration). This can be used to infer information
    about the position of the device (horizontal/vertical/tilted).
    Accelerometer reports zero acceleration if the device is free falling.

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

    Note that mobile platforms treat this value as a suggestion and the actual
    rate can differ depending on hardware and OS limitations.
    """

    cancel_on_error: bool = True
    """
    Whether the stream subscription should cancel on the first sensor error.
    """

    on_reading: Optional[EventHandler[AccelerometerReadingEvent]] = None
    """
    Fires when a new reading is available.

    `event` exposes `x`, `y`, `z` acceleration values and `timestamp`
    (microseconds since epoch).
    """

    on_error: Optional[EventHandler[SensorErrorEvent]] = None
    """
    Fired when the platform reports a sensor error (for example when the device
    does not expose the accelerometer). `event.message` contains the error text.
    """

    def before_update(self):
        if not (self.page.web or self.page.platform.is_mobile()):
            raise FletUnsupportedPlatformException(
                f"{self.__class__.__name__} is only supported on Android, iOS and web."
            )
