from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from flet.controls.control_event import Event, EventControlType

if TYPE_CHECKING:
    from flet.controls.services.accelerometer import Accelerometer  # noqa: F401
    from flet.controls.services.barometer import Barometer  # noqa: F401
    from flet.controls.services.gyroscope import Gyroscope  # noqa: F401
    from flet.controls.services.magnetometer import Magnetometer  # noqa: F401
    from flet.controls.services.user_accelerometer import (
        UserAccelerometer,  # noqa: F401
    )

__all__ = [
    "AccelerometerReadingEvent",
    "BarometerReadingEvent",
    "GyroscopeReadingEvent",
    "MagnetometerReadingEvent",
    "SensorErrorEvent",
    "UserAccelerometerReadingEvent",
]


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

    timestamp: int
    """Event timestamp, expressed in microseconds since epoch."""


@dataclass(kw_only=True)
class UserAccelerometerReadingEvent(Event["UserAccelerometer"]):
    """
    Like [`AccelerometerReadingEvent`][flet.], this is a discrete reading from
    an accelerometer and measures the velocity of the device. However,
    unlike [`AccelerometerReadingEvent`][flet.], this event does not include
    the effects of gravity.
    """

    x: float
    """Linear acceleration along the X axis, gravity removed, in `m/s^2`."""

    y: float
    """Linear acceleration along the Y axis, gravity removed, in `m/s^2`."""

    z: float
    """Linear acceleration along the Z axis, gravity removed, in `m/s^2`."""

    timestamp: int
    """Event timestamp, expressed in microseconds since epoch."""


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

    timestamp: int
    """Event timestamp, expressed in microseconds since epoch."""


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

    timestamp: int
    """Event timestamp, expressed in microseconds since epoch."""


@dataclass(kw_only=True)
class BarometerReadingEvent(Event["Barometer"]):
    """
    A sensor sample from a barometer.

    Barometers measure the atmospheric pressure surrounding the sensor,
    returning values in hectopascals `hPa`.

    Consider that these samples may be affected by altitude and weather conditions,
    and can be used to predict short-term weather changes or determine altitude.

    Note that water-resistant phones or similar sealed devices may experience
    pressure fluctuations as the device is held or used, due to changes
    in pressure caused by handling the device.

    An altimeter is an example of a general utility for barometer data.
    """

    pressure: float
    """Atmospheric pressure reading, in hectopascals (`hPa`)."""

    timestamp: int
    """Event timestamp, expressed in microseconds since epoch."""


@dataclass(kw_only=True)
class SensorErrorEvent(Event[EventControlType]):
    """
    Generic sensor error event. `message` contains the platform error text.
    """

    message: str
    """Human-readable description of the sensor error."""
