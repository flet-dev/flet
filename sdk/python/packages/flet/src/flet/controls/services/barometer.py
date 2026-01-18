from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import Event, EventHandler
from flet.controls.duration import Duration
from flet.controls.exceptions import FletUnsupportedPlatformException
from flet.controls.services.sensor_error_event import SensorErrorEvent
from flet.controls.services.service import Service

__all__ = ["Barometer", "BarometerReadingEvent"]


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

    timestamp: datetime
    """Event timestamp."""


@control("Barometer")
class Barometer(Service):
    """
    Streams barometer [readings][flet.BarometerReadingEvent]
    (atmospheric pressure in `hPa`). Useful for altitude calculations
    and weather-related experiences.

    Note:
        * Supported platforms: Android, iOS.
        * Barometer APIs are not exposed on the web or desktop platforms.
        * iOS ignores custom sampling intervals.

    /// admonition | Running on iOS
        type: danger
    On iOS you must also include a key called `NSMotionUsageDescription`
    in your app's `Info.plist` file. This key provides a message that tells
    the user why the app is requesting access to the device's motion data.
    Barometer service needs access to motion data to get barometer data.

    For example, add the following to your `pyproject.toml` file:
    ```toml
    [tool.flet.ios.info]
    NSMotionUsageDescription = "This app requires access to the barometer to provide altitude information."
    ```

    **Adding `NSMotionUsageDescription` is a requirement and not doing so will
    crash your app when it attempts to access motion data.**
    ///
    """  # noqa: E501

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

    def before_update(self):
        if self.page.web or not self.page.platform.is_mobile():
            raise FletUnsupportedPlatformException(
                f"{self.__class__.__name__} is only supported on Android and iOS."
            )
