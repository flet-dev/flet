from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import Event, EventHandler
from flet.controls.duration import Duration
from flet.controls.exceptions import FletUnsupportedPlatformException
from flet.controls.services.sensor_error_event import SensorErrorEvent
from flet.controls.services.service import Service

__all__ = ["Magnetometer", "MagnetometerReadingEvent"]


@dataclass(kw_only=True)
class MagnetometerReadingEvent(Event["Magnetometer"]):
    """
    A sensor sample from a magnetometer.

    Magnetometers measure the ambient magnetic field surrounding the sensor,
    returning values in microteslas `μT` for each three-dimensional axis.

    Consider that these samples may bear effects of Earth's magnetic field
    as well as local factors such as the metal of the device itself
    or nearby magnets, though most devices compensate for these factors.

    A compass is an example of a general utility for magnetometer data.
    """

    x: float
    """Ambient magnetic field on the X axis, in microteslas (`uT`)."""

    y: float
    """Ambient magnetic field on the Y axis, in `uT`."""

    z: float
    """Ambient magnetic field on the Z axis, in `uT`."""

    timestamp: datetime
    """Event timestamp."""


@control("Magnetometer")
class Magnetometer(Service):
    """
    Streams magnetometer [readings][flet.MagnetometerReadingEvent]
    reporting the ambient magnetic field (`uT`) per axis for compass-style
    use cases.

    Note:
        * Supported platforms: Android, iOS.
        * Magnetometer APIs are not available on web.
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

    def before_update(self):
        if self.page.web or not self.page.platform.is_mobile():
            raise FletUnsupportedPlatformException(
                f"{self.__class__.__name__} is only supported on Android and iOS."
            )
