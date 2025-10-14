import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Optional

import flet as ft

if TYPE_CHECKING:
    from flet_geolocator.geolocator import Geolocator  # noqa

__all__ = [
    "ForegroundNotificationConfiguration",
    "GeolocatorAndroidConfiguration",
    "GeolocatorConfiguration",
    "GeolocatorIosActivityType",
    "GeolocatorIosConfiguration",
    "GeolocatorPermissionStatus",
    "GeolocatorPosition",
    "GeolocatorPositionAccuracy",
    "GeolocatorPositionChangeEvent",
    "GeolocatorWebConfiguration",
]


class GeolocatorPositionAccuracy(Enum):
    """Represent the possible location accuracy values."""

    LOWEST = "lowest"
    """
    Location is accurate within a distance of 3000m on iOS and 500m on Android.

    On Android, corresponds to
    [PRIORITY_PASSIVE](https://developers.google.com/android/reference/com/google/android/gms/location/Priority#public-static-final-int-priority_passive).
    """

    LOW = "low"
    """
    Location is accurate within a distance of 1000m on iOS and 500m on Android.

    On Android, corresponds to
    [PRIORITY_LOW_POWER](https://developers.google.com/android/reference/com/google/android/gms/location/Priority#public-static-final-int-priority_low_power).
    """

    MEDIUM = "medium"
    """
    Location is accurate within a distance of 100m on iOS and between 100m and
    500m on Android.

    On Android, corresponds to
    [PRIORITY_BALANCED_POWER_ACCURACY](https://developers.google.com/android/reference/com/google/android/gms/location/Priority#public-static-final-int-priority_balanced_power_accuracy).
    """

    HIGH = "high"
    """
    Location is accurate within a distance of 10m on iOS and between 0m and
    100m on Android.

    On Android, corresponds to
    [PRIORITY_HIGH_ACCURACY](https://developers.google.com/android/reference/com/google/android/gms/location/Priority#public-static-final-int-priority_high_accuracy).
    """

    BEST = "best"
    """
    Location is accurate within a distance of ~0m on iOS and between 0m and
    100m on Android.

    On Android, corresponds to
    [PRIORITY_HIGH_ACCURACY](https://developers.google.com/android/reference/com/google/android/gms/location/Priority#public-static-final-int-priority_high_accuracy).
    """

    BEST_FOR_NAVIGATION = "bestForNavigation"
    """
    Location accuracy is optimized for navigation on iOS and matches the
    `GeolocatorPositionAccuracy.BEST` on Android.

    On Android, corresponds to
    [PRIORITY_HIGH_ACCURACY](https://developers.google.com/android/reference/com/google/android/gms/location/Priority#public-static-final-int-priority_high_accuracy).
    """

    REDUCED = "reduced"
    """
    Location accuracy is reduced for iOS 14+ devices. Matches
    `GeolocatorPositionAccuracy.LOWEST` on iOS 13 and below and all other platforms.

    On Android, corresponds to
    [PRIORITY_PASSIVE](https://developers.google.com/android/reference/com/google/android/gms/location/Priority#public-static-final-int-priority_passive).
    """


class GeolocatorPermissionStatus(Enum):
    """Represent the possible location permissions."""

    DENIED = "denied"
    """
    Permission to access the device's location is denied.

    The app should try to request permission using the
    [`Geolocator.request_permission`][(p).] method.
    """

    DENIED_FOREVER = "deniedForever"
    """
    Permission to access the device's location is permanently denied.

    When requesting permissions, the permission dialog will not be shown until the
    user updates the permission in the app settings.
    """

    WHILE_IN_USE = "whileInUse"
    """
    Permission to access the device's location is allowed only while the app is in use.
    """

    ALWAYS = "always"
    """
    Permission to access the device's location is allowed even when the app is
    running in the background.
    """

    UNABLE_TO_DETERMINE = "unableToDetermine"
    """
    Permission status cannot be determined.

    This status is only returned by the [`Geolocator.request_permission`][(p).] method
    on the web platform for browsers that did not implement the Permissions API.
    See: https://developer.mozilla.org/en-US/docs/Web/API/Permissions_API
    """


class GeolocatorIosActivityType(Enum):
    """Represents the possible iOS activity types."""

    AUTOMOTIVE_NAVIGATION = "automotiveNavigation"
    """
    The location manager is being used specifically during vehicular
    navigation to track location changes to the automobile.
    """

    FITNESS = "fitness"
    """
    The location manager is being used to track fitness activities such as
    walking, running, cycling, and so on.
    """

    OTHER_NAVIGATION = "otherNavigation"
    """
    The location manager is being used to track movements for other types of
    vehicular navigation that are not automobile related.
    """

    AIRBORNE = "airborne"
    """
    The location manager is being used specifically during
    airborne activities.
    """

    OTHER = "other"
    """
    The location manager is being used for an unknown activity.
    """


@dataclass
class GeolocatorPosition:
    """Detailed location information."""

    latitude: Optional[ft.Number] = None
    """
    The latitude of this position in degrees normalized to the interval -90.0
    to +90.0 (both inclusive).
    """

    longitude: Optional[ft.Number] = None
    """
    The longitude of the position in degrees normalized to the interval -180
    (exclusive) to +180 (inclusive).
    """

    speed: Optional[ft.Number] = None
    """
    The speed at which the device is traveling in meters per second over ground.

    The speed is not available on all devices.
    In these cases the value is `0.0`.
    """

    altitude: Optional[ft.Number] = None
    """
    The altitude of the device in meters.

    The altitude is not available on all devices.
    In these cases the returned value is `0.0`.
    """

    timestamp: datetime.datetime = None
    """
    The time at which this position was determined.
    """

    accuracy: Optional[ft.Number] = None
    """
    The estimated horizontal accuracy of the position in meters.

    The accuracy is not available on all devices.
    In these cases the value is `0.0`.
    """

    altitude_accuracy: Optional[ft.Number] = None
    """
    The estimated vertical accuracy of the position in meters.

    The accuracy is not available on all devices.
    In these cases the value is `0.0`.
    """

    heading: Optional[ft.Number] = None
    """
    The heading in which the device is traveling in degrees.

    The heading is not available on all devices.
    In these cases the value is `0.0`.
    """

    heading_accuracy: Optional[ft.Number] = None
    """
    The estimated heading accuracy of the position in degrees.

    The heading accuracy is not available on all devices.
    In these cases the value is `0.0`.
    """

    speed_accuracy: Optional[ft.Number] = None
    """
    The estimated speed accuracy of this position, in meters per second.

    The speed accuracy is not available on all devices.
    In these cases the value is `0.0`.
    """

    floor: Optional[int] = None
    """
    The floor specifies the floor of the building on which the device is
    located.

    The floor property is only available on iOS
    and only when the information is available.
    In all other cases this value will be `None`.
    """

    mocked: Optional[bool] = None
    """
    Will be `True` on Android (starting from API level 18) when the location came
    from the mocked provider.

    On iOS this value will always be `False`.
    """


@dataclass
class GeolocatorConfiguration:
    accuracy: GeolocatorPositionAccuracy = GeolocatorPositionAccuracy.BEST
    """
    Defines the desired accuracy that should be used to determine the location data.
    """

    distance_filter: int = 0
    """
    The minimum distance (measured in meters) a device must move
    horizontally before an update event is generated.

    Set to `0` when you want to be notified of all movements.
    """

    time_limit: ft.DurationValue = None
    """
    Specifies a timeout interval.

    For no time limit, set to `None`.
    """


@dataclass
class GeolocatorWebConfiguration(GeolocatorConfiguration):
    """Web specific settings."""

    maximum_age: ft.DurationValue = field(default_factory=lambda: ft.Duration())
    """
    A value indicating the maximum age of a possible cached
    position that is acceptable to return. If set to 0, it means
    that the device cannot use a cached position and must
    attempt to retrieve the real current position.
    """


@dataclass
class GeolocatorIosConfiguration(GeolocatorConfiguration):
    """iOS specific settings."""

    activity_type: GeolocatorIosActivityType = GeolocatorIosActivityType.OTHER
    """
    The location manager uses the information in this property as a cue
    to determine when location updates may be automatically paused.
    """

    pause_location_updates_automatically: bool = False
    """
    Allows the location manager to pause updates to improve battery life
    on the target device without sacrificing location data.
    When this property is set to `True`, the location manager pauses updates
    (and powers down the appropriate hardware) at times when the
    location data is unlikely to change.
    """

    show_background_location_indicator: bool = False
    """
    Flag to ask the Apple OS to show the background location indicator (iOS only)
    if app starts up and background and requests the users location.

    For this setting to work and for the location to be retrieved the user must
    have granted "always" permissions for location retrieval.
    """

    allow_background_location_updates: bool = True
    """
    Flag to allow the app to receive location updates in the background (iOS only)

    Note:
        For this setting to work `Info.plist` should contain the following keys:
            - UIBackgroundModes and the value should contain "location"
            - NSLocationAlwaysUsageDescription
    """


@dataclass
class ForegroundNotificationConfiguration:
    notification_title: str
    """
    The title used for the foreground service notification.
    """

    notification_text: str
    """
    The body used for the foreground service notification.
    """

    notification_channel_name: str = "Background Location"
    """
    The user visible name of the notification channel.

    The notification channel name will be displayed in the system settings.
    The maximum recommended length is 40 characters, the name might be
    truncated if it is to long. Default value: "Background Location".
    """

    notification_enable_wake_lock: bool = False
    """
    When enabled, a Wakelock is acquired when background execution is started.

    If this is false then the system can still sleep and all location
    events will be received at once when the system wakes up again.

    Wake lock permissions should be obtained first by using a permissions library.
    """

    notification_enable_wifi_lock: bool = False
    """
    When enabled, a WifiLock is acquired when background execution is started.
    This allows the application to keep the Wi-Fi radio awake, even when the
    user has not used the device in a while
    (e.g. for background network communications).

    Wifi lock permissions should be obtained first by using a permissions library.
    """

    notification_set_ongoing: bool = False
    """
    When enabled, the displayed notification is persistent and
    the user cannot dismiss it.
    """

    # foreground_notification_color: Optional[ft.ColorValue] = None


@dataclass
class GeolocatorAndroidConfiguration(GeolocatorConfiguration):
    """Android specific settings."""

    interval_duration: ft.DurationValue = field(
        default_factory=lambda: ft.Duration(milliseconds=5000)
    )
    """
    The desired interval for active location updates.
    """

    use_msl_altitude: bool = False
    """
    Whether altitude should be calculated as MSL (EGM2008) from NMEA messages
    and reported as the altitude instead of using the geoidal height (WSG84). Setting
    this property true will help to align Android altitude to that of iOS which
    uses MSL.

    If the NMEA message is empty then the altitude reported will still be
    the standard WSG84 altitude from the GPS receiver.

    MSL Altitude is only available starting from Android N and not all devices support
    NMEA message returning $GPGGA sequences.

    This property only works with position stream updates and has no effect when
    getting the current position or last known position.
    """

    foreground_notification_config: Optional[ForegroundNotificationConfiguration] = None


@dataclass
class GeolocatorPositionChangeEvent(ft.Event["Geolocator"]):
    position: GeolocatorPosition
    """
    The current/new position of the device.
    """
