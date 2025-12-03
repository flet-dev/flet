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
