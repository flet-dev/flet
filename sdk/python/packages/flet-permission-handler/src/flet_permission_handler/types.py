from enum import Enum

__all__ = [
    "Permission",
    "PermissionStatus",
]


class PermissionStatus(Enum):
    """Defines the state of a [`Permission`][(p).]."""

    GRANTED = "granted"
    """
    The user granted access to the requested feature.
    """

    DENIED = "denied"
    """
    The user denied access to the requested feature, permission needs to be asked first.
    """

    PERMANENTLY_DENIED = "permanentlyDenied"
    """
    Permission to the requested feature is permanently denied,
    the permission dialog will not be shown when requesting this permission.
    The user may still change the permission status in the settings.

    Note:
        - On Android:
            - Android 11+ (API 30+): whether the user denied the permission
            for a second time.
            - Below Android 11 (API 30): whether the user denied access
            to the requested feature and selected to never again show a request.
        - On iOS: If the user has denied access to the requested feature.
    """

    LIMITED = "limited"
    """
    The user has authorized this application for limited access.
    So far this is only relevant for the Photo Library picker.

    Note:
        Only supported on iOS (iOS14+) and Android (Android 14+).
    """

    PROVISIONAL = "provisional"
    """
    The application is provisionally authorized to post non-interruptive
    user notifications.

    Note:
        Only supported on iOS (iOS 12+).
    """

    RESTRICTED = "restricted"
    """
    The OS denied access to the requested feature. The user cannot change
    this app's status, possibly due to active restrictions such as parental
    controls being in place.

    Note:
        Only supported on iOS.
    """


# todo: show how pyproject config for each could look like for each permission
#  (what exactly is needed in manifest, plist, etc.)


class Permission(Enum):
    """Defines the permissions which can be checked and requested."""

    ACCESS_MEDIA_LOCATION = "accessMediaLocation"
    """
    Permission for accessing the device's media library.

    Allows an application to access any geographic locations persisted in the
    user's shared collection.

    Note:
        Only supported on Android 10+ (API 29+) only.
    """

    ACCESS_NOTIFICATION_POLICY = "accessNotificationPolicy"
    """
    Permission for accessing the device's notification policy.

    Allows the user to access the notification policy of the phone.
    Example: Allows app to turn on and off do-not-disturb.

    Note:
        Only supported on Android Marshmallow+ (API 23+) only.
    """

    ACTIVITY_RECOGNITION = "activityRecognition"
    """
    Permission for accessing the activity recognition.

    Note:
        Only supported on Android 10+ (API 29+) only.
    """

    APP_TRACKING_TRANSPARENCY = "appTrackingTransparency"
    """
    Permission for accessing the device's tracking state.
    Allows user to accept that your app collects data about end users and
    shares it with other companies for purposes of tracking across apps and
    websites.

    Note:
        Only supported on iOS only.
    """

    ASSISTANT = "assistant"
    """
    Info:
        - Android: Nothing
        - iOS: SiriKit
    """

    AUDIO = "audio"
    """
    Permission for accessing the device's audio files from external storage.

    Note:
        Only supported on Android 13+ (API 33+) only.
    """

    BACKGROUND_REFRESH = "backgroundRefresh"
    """
    Permission for reading the current background refresh status.

    Note:
        Only supported on iOS only.
    """

    BLUETOOTH = "bluetooth"
    """
    Permission for accessing the device's bluetooth adapter state.

    Depending on the platform and version, the requirements are slightly different:

    Info:
        - Android: always allowed.
        - iOS:
            - 13 and above: The authorization state of Core Bluetooth manager.
            - below 13: always allowed.
    """

    BLUETOOTH_ADVERTISE = "bluetoothAdvertise"
    """
    Permission for advertising Bluetooth devices
    Allows the user to make this device discoverable to other Bluetooth devices.

    Note:
        Only supported on Android 12+ (API 31+) only.
    """

    BLUETOOTH_CONNECT = "bluetoothConnect"
    """
    Permission for connecting to Bluetooth devices.
    Allows the user to connect with already paired Bluetooth devices.

    Note:
        Only supported on Android 12+ (API 31+) only.
    """

    BLUETOOTH_SCAN = "bluetoothScan"
    """
    Permission for scanning for Bluetooth devices.

    Note:
        Only supported on Android 12+ (API 31+) only.
    """

    CALENDAR_FULL_ACCESS = "calendarFullAccess"
    """
    Permission for reading from and writing to the device's calendar.
    """

    CALENDAR_WRITE_ONLY = "calendarWriteOnly"
    """
    Permission for writing to the device's calendar.

    On iOS 16 and lower, this permission is identical to
    [`CALENDAR_FULL_ACCESS`][(c).].
    """

    CAMERA = "camera"
    """
    Permission for accessing the device's camera.

    Info:
        - Android: Camera
        - iOS: Photos (Camera Roll and Camera)
    """

    CONTACTS = "contacts"
    """
    Permission for accessing the device's contacts.

    Info:
        - Android: Contacts
        - iOS: AddressBook
    """

    CRITICAL_ALERTS = "criticalAlerts"
    """
    Permission for sending critical alerts.
    Allow for sending notifications that override the ringer.

    Note:
        Only supported on iOS only.
    """

    IGNORE_BATTERY_OPTIMIZATIONS = "ignoreBatteryOptimizations"
    """
    Permission for accessing ignore battery optimizations.

    Note:
        Only supported on Android only.
    """

    LOCATION = "location"
    """
    Permission for accessing the device's location.

    Info:
        - Android: Fine and Coarse Location
        - iOS: CoreLocation (Always and WhenInUse)
    """

    LOCATION_ALWAYS = "locationAlways"
    """
    Info:
        iOS: CoreLocation (Always)
    """

    LOCATION_WHEN_IN_USE = "locationWhenInUse"
    """
    Permission for accessing the device's location when the app is
    running in the foreground.

    Info:
        - Android: Fine and Coarse Location
        - iOS: CoreLocation - WhenInUse
    """

    MANAGE_EXTERNAL_STORAGE = "manageExternalStorage"
    """
    Permission for accessing the device's external storage.
    Allows an application a broad access to external storage in scoped storage.

    You should request this permission only when your app cannot
    effectively make use of the more privacy-friendly APIs.
    For more information:
    https://developer.android.com/training/data-storage/manage-all-files

    Info:
        When the privacy-friendly APIs (i.e. [Storage Access Framework](https://developer.android.com/guide/topics/providers/document-provider)
        or the[MediaStore](https://developer.android.com/training/data-storage/shared/media) APIs)
        is all your app needs, the [PermissionGroup.storage] are the only
        permissions you need to request.

        If the usage of this permission is needed, you have to fill out
        the Permission Declaration Form upon submitting your app to the
        Google Play Store.
        More details:
        https://support.google.com/googleplay/android-developer/answer/9214102#zippy=

    Note:
        Only supported on Android 11+ (API 30+) only.
    """  # noqa: E501

    MEDIA_LIBRARY = "mediaLibrary"
    """
    Permission for accessing the device's media library.

    Note:
        Only supported on iOS 9.3+ only
    """

    MICROPHONE = "microphone"
    """
    Permission for accessing the device's microphone.
    """

    NEARBY_WIFI_DEVICES = "nearbyWifiDevices"
    """
    Permission for connecting to nearby devices via Wi-Fi.

    Note:
        Only supported on Android 13+ (API 33+) only.
    """

    NOTIFICATION = "notification"
    """
    Permission for pushing notifications.
    """

    PHONE = "phone"
    """
    Permission for accessing the device's phone state.

    Note:
        Only supported on Android only.
    """

    PHOTOS = "photos"
    """
    Permission for accessing (read & write) the device's photos.

    If you only want to add photos, you can use
    the `PHOTOS_ADD_ONLY` permission instead (iOS only).
    """

    PHOTOS_ADD_ONLY = "photosAddOnly"
    """
    Permission for adding photos to the device's photo library (iOS only).

    If you want to read them as well, use the `Permission.PHOTOS` permission instead.

    Info:
        iOS: Photos (14+ read & write access level)
    """

    REMINDERS = "reminders"
    """
    Permission for accessing the device's reminders.

    Note:
        Only supported on iOS only.
    """

    REQUEST_INSTALL_PACKAGES = "requestInstallPackages"
    """
    Permission for requesting installing packages.

    Note:
        Only supported on Android Marshmallow+ (API 23+) only.
    """

    SCHEDULE_EXACT_ALARM = "scheduleExactAlarm"
    """
    Permission for scheduling exact alarms.

    Note:
        Only supported on Android 12+ (API 31+) only.
    """

    SENSORS = "sensors"
    """
    Permission for accessing the device's sensors.

    Info:
        - Android: Body Sensors
        - iOS: CoreMotion
    """

    SENSORS_ALWAYS = "sensorsAlways"
    """
    Permission for accessing the device's sensors in background.

    Note:
        Only supported on Android 13+ (API 33+) only.
    """

    SMS = "sms"
    """
    Permission for sending and reading SMS messages (Android only).
    """

    SPEECH = "speech"
    """
    Permission for accessing speech recognition.

    Info:
        - Android: Requests access to microphone
            (identical to requesting [`MICROPHONE`][(c).]).
        - iOS: Requests speech access (different from requesting
            [`MICROPHONE`][(c).]).
    """

    STORAGE = "storage"
    """
    Permission for accessing external storage.

    Depending on the platform and version, the requirements are slightly different:

    Info:
        - Android:
            - On Android 13 (API 33) and above, this permission is deprecated and
            always returns `PermissionStatus.denied`. Instead use `Permission.PHOTOS`,
            `Permission.VIDEO`, `Permission.AUDIO` or
            `Permission.MANAGE_EXTERNAL_STORAGE`.
            For more information see
            [this](https://pub.dev/packages/permission_handler#faq).

            - Below Android 13 (API 33), the `READ_EXTERNAL_STORAGE` and
            `WRITE_EXTERNAL_STORAGE` permissions are requested (depending on the
            definitions in the AndroidManifest.xml) file.
        - iOS: Access to folders like `Documents` or `Downloads`. Implicitly granted.
    """

    SYSTEM_ALERT_WINDOW = "systemAlertWindow"
    """
    Permission for creating system alert window.
    Allows an app to create windows shown on top of all other apps.

    Note:
        Only supported on Android only.
    """

    UNKNOWN = "unknown"
    """
    The unknown only used for return type, never requested.
    """

    VIDEOS = "videos"
    """
    Permission for accessing the device's video files from external storage.

    Note:
        Only supported on Android 13+ (API 33+) only.
    """
