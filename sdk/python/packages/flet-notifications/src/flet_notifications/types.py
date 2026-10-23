from enum import Enum, IntFlag

__all__ = [
    "AndroidAudioAttributesUsage",
    "AndroidForegroundServiceType",
    "AndroidGroupAlertBehavior",
    "AndroidImportance",
    "AndroidNotificationCategory",
    "AndroidNotificationFlag",
    "AndroidScheduleMode",
    "AndroidServiceStartType",
    "DateTimeComponents",
    "LinuxNotificationCategory",
    "RepeatInterval",
    "WebNotificationDirection",
    "WindowsNotificationDuration",
    "WindowsNotificationSound",
]


class AndroidAudioAttributesUsage(Enum):
    """
    Intended use of an Android notification's sound.

    Note:
        Used by :attr:`flet_notifications.NotificationChannel.audio_attributes_usage`
        to help Android apply audio routing, volume, and interruption policies. This
        describes the sound; it does not grant permission to bypass the user's sound or
        Do Not Disturb settings. An existing channel retains its audio configuration.

    See Android's [audio usage
    reference](https://developer.android.com/reference/android/media/AudioAttributes).
    """

    ALARM = "alarm"
    """Audio for an alarm, such as a wake-up alarm."""

    ASSISTANCE_ACCESSIBILITY = "assistanceAccessibility"
    """Audio for accessibility assistance, such as a screen reader."""

    ASSISTANCE_NAVIGATION_GUIDANCE = "assistanceNavigationGuidance"
    """Spoken directions or other navigation guidance."""

    ASSISTANCE_SONIFICATION = "assistanceSonification"
    """Short sounds accompanying user-interface actions."""

    ASSISTANT = "assistant"
    """Responses from an assistant, such as spoken answers or reminders."""

    GAME = "game"
    """Audio associated with gameplay."""

    MEDIA = "media"
    """Media playback, such as music or video audio."""

    NOTIFICATION = "notification"
    """Audio drawing attention to a notification."""

    NOTIFICATION_EVENT = "notificationEvent"
    """Audio for an event that needs attention, such as a reminder."""

    NOTIFICATION_RINGTONE = "notificationRingtone"
    """Ringtone audio announcing an incoming call."""

    UNKNOWN = "unknown"
    """Audio whose intended use is unspecified."""

    VOICE_COMMUNICATION = "voiceCommunication"
    """Speech used for a telephone or VoIP conversation."""

    VOICE_COMMUNICATION_SIGNALLING = "voiceCommunicationSignalling"
    """Call-signalling sounds, such as a dial tone or busy tone."""


class AndroidNotificationFlag(IntFlag):
    """
    Additional behavior bits for an Android notification.

    Combine members with `|` and pass the result to
    :attr:`flet_notifications.AndroidOptions.additional_flags`.

    Note:
        These bits are added after the notification is built; they cannot clear flags
        set by other options. Android's notification permissions, channel settings, and
        platform restrictions still apply.

    Example:
        ```python
        import flet_notifications as ftn

        options = ftn.AndroidOptions(
            additional_flags=ftn.AndroidNotificationFlag.INSISTENT
            | ftn.AndroidNotificationFlag.NO_CLEAR
        )
        ```

    Deprecated flags and system-managed status flags are omitted. To start a foreground
    service, use :meth:`flet_notifications.LocalNotifications.start_foreground_service`.
    See Android's [notification
    flags](https://developer.android.com/reference/android/app/Notification#flags).
    """

    NONE = 0
    """Add no flags; flags set by other notification options remain in effect."""

    ONGOING_EVENT = 2
    """
    Mark the notification as representing work currently in progress, such as a call.

    Prefer :attr:`flet_notifications.AndroidOptions.ongoing` for this behavior.
    """

    INSISTENT = 4
    """
    Request repeating audio until cancellation or the notification window is opened.

    Sound must be enabled and permitted by the notification's channel and user settings.
    """

    ONLY_ALERT_ONCE = 8
    """
    Alert only when the notification is first posted, rather than on later updates.

    Also stops ongoing sound, vibration, or notification-LED alerting. Prefer
    :attr:`flet_notifications.AndroidOptions.only_alert_once` for this behavior.
    """

    AUTO_CANCEL = 16
    """
    Cancel the notification when the user taps it.

    Prefer :attr:`flet_notifications.AndroidOptions.auto_cancel` for this behavior.
    """

    NO_CLEAR = 32
    """
    Request that the notification remain when the user presses Clear all.

    This does not prevent the app from cancelling the notification or guarantee that
    the notification cannot be dismissed individually.
    """

    LOCAL_ONLY = 256
    """
    Mark the notification as relevant only to the current device.

    Recommends that the notification not be bridged to other devices.
    """

    GROUP_SUMMARY = 512
    """
    Mark the notification as the summary of a group.

    Requires :attr:`flet_notifications.AndroidOptions.group`. Prefer setting
    :attr:`flet_notifications.AndroidGroup.summary` for this behavior.
    """


class RepeatInterval(Enum):
    """
    Fixed intervals for :meth:`flet_notifications.LocalNotifications.periodically_show`.

    The first notification is delivered one interval after scheduling. For a particular
    local time, such as 09:00 each day, use
    :class:`flet_notifications.DateTimeComponents` with
    :meth:`flet_notifications.LocalNotifications.schedule` instead.

    Note:
        Supported only on Android, iOS, and macOS.
    """

    EVERY_MINUTE = "everyMinute"
    """Repeat every minute, starting one minute after scheduling."""

    HOURLY = "hourly"
    """Repeat every hour, starting one hour after scheduling."""

    DAILY = "daily"
    """Repeat every day, starting one day after scheduling."""

    WEEKLY = "weekly"
    """Repeat every week, starting one week after scheduling."""


class DateTimeComponents(Enum):
    """
    Calendar components to match when repeating a scheduled notification.

    Used by :meth:`flet_notifications.LocalNotifications.schedule`. The next matching
    date can precede the full date supplied in `when`: matching only the time repeats
    from the next occurrence of that time.

    Note:
        Calendar recurrence is supported only on Android, iOS, and macOS. Windows
        ignores
        these components and schedules a single delivery.
    """

    TIME = "time"
    """Repeat daily at the hour, minute, and second of the scheduled time."""

    DAY_OF_WEEK_AND_TIME = "dayOfWeekAndTime"
    """Repeat weekly on the weekday and at the time of the scheduled date."""

    DAY_OF_MONTH_AND_TIME = "dayOfMonthAndTime"
    """Repeat monthly on the day of the month and at the scheduled time."""

    DATE_AND_TIME = "dateAndTime"
    """Repeat yearly on the month and day and at the time of the scheduled date."""


class AndroidScheduleMode(Enum):
    """
    How Android schedules the alarm that delivers a notification.

    Inexact modes need no special access but may deliver some minutes late, as
    Android batches alarms to save power. Exact modes deliver on time and need
    exact-alarm access:

    - Declare it in `pyproject.toml`:

      ```toml
      [tool.flet.android.permission]
      SCHEDULE_EXACT_ALARM = true
      ```

    - On Android 14+, the access is off until the user turns it on in system
      settings. Check it with
      :meth:`flet_notifications.LocalNotifications.can_schedule_exact_notifications`
      and open that settings screen with
      :meth:`flet_notifications.LocalNotifications.request_exact_alarm_permission`.
    - Scheduling in an exact mode without the access raises
      :class:`flet_notifications.NotificationPermissionError`.
    - The user or the system can revoke the access at any time. Android then stops
      the app and cancels its future exact alarms, so those notifications are not
      delivered. Check the access when the app starts and reschedule once it is
      granted again. See Android's
      [exact alarm permission](https://developer.android.com/develop/background-work/services/alarms/schedule#exact-permission-declare)
      documentation.

    Note:
        Delivery in every mode remains subject to Android's alarm quotas and
        background-execution restrictions.
    """

    ALARM_CLOCK = "alarmClock"
    """
    Schedule an exact alarm-clock notification that can run during idle mode.

    Uses Android's alarm-clock mechanism and can appear in its next-alarm UI. Requires
    exact-alarm access.
    """

    EXACT = "exact"
    """
    Schedule for the requested time, with deferral possible during idle mode.

    Requires exact-alarm access.
    """

    EXACT_ALLOW_WHILE_IDLE = "exactAllowWhileIdle"
    """
    Schedule an exact alarm that can execute during low-power idle mode.

    Requires exact-alarm access.
    """

    INEXACT = "inexact"
    """
    Schedule approximately at the requested time, allowing idle-mode deferral.

    Does not require exact-alarm access.
    """

    INEXACT_ALLOW_WHILE_IDLE = "inexactAllowWhileIdle"
    """
    Schedule approximately at the requested time, including during idle mode.

    Does not require exact-alarm access; Android may batch or delay delivery. This is
    the default of :meth:`flet_notifications.LocalNotifications.schedule` and
    :meth:`flet_notifications.LocalNotifications.periodically_show`.
    """


class AndroidImportance(Enum):
    """
    Importance of an Android notification channel on Android 8.0 and later.

    Controls how prominently notifications interrupt the user. After a channel is
    created, its importance is controlled by the user in system settings; posting
    another notification does not override that choice. Use
    :class:`~flet_notifications.AndroidPriority` for Android 7.1 and earlier.
    """

    UNSPECIFIED = "unspecified"
    """
    Sentinel indicating that no importance has been specified.

    Maps to Android's `IMPORTANCE_UNSPECIFIED`. It is not an importance level for
    creating a new channel; choose an explicit level instead.
    """

    MIN = "min"
    """Show notifications quietly, with minimal prominence and no status-bar icon."""

    NONE = "none"
    """Disable notifications from the channel."""

    LOW = "low"
    """Show notifications without sound."""

    DEFAULT = "defaultImportance"
    """Use normal prominence, including sound when enabled for the channel."""

    HIGH = "high"
    """Use high prominence, including sound and a heads-up display when allowed."""

    MAX = "max"
    """
    Map to Android's maximum-importance constant.

    Android documents this level as unused; use :attr:`HIGH` for urgent channels.
    """


class AndroidGroupAlertBehavior(Enum):
    """
    Which Android notifications in a group may play sound or vibrate.

    This controls alerting, not whether a notification is visible. Apply the same
    behavior to the group's children and summary for consistent results.
    """

    ALL = "all"
    """Allow both the group summary and child notifications to alert."""

    SUMMARY = "summary"
    """Allow only the group summary to alert; silence its children."""

    CHILDREN = "children"
    """Allow only child notifications to alert; silence the group summary."""


class AndroidNotificationCategory(Enum):
    """
    Semantic category Android uses to classify and rank a notification.

    Set :attr:`~flet_notifications.AndroidOptions.category`. Category describes
    content; it does not grant permissions or change channel importance.
    """

    ALARM = "alarm"
    """Alarm or timer requiring attention."""

    CALL = "call"
    """Incoming voice or video call, or a similar live communication request."""

    EMAIL = "email"
    """Incoming email or another asynchronous bulk message."""

    ERROR = "error"
    """Failure in a background operation or authentication flow."""

    EVENT = "event"
    """Calendar event."""

    LOCATION_SHARING = "locationSharing"
    """Temporary location-sharing activity."""

    MESSAGE = "message"
    """Incoming direct message, such as SMS or a chat message."""

    MISSED_CALL = "missedCall"
    """Missed voice or video call."""

    NAVIGATION = "navigation"
    """Turn-by-turn navigation instruction."""

    PROGRESS = "progress"
    """Progress of a long-running background operation."""

    PROMO = "promo"
    """Promotion or advertisement."""

    RECOMMENDATION = "recommendation"
    """Timely recommendation for a specific item, such as a news story."""

    REMINDER = "reminder"
    """Reminder scheduled by the user."""

    SERVICE = "service"
    """Indication of a running background service."""

    SOCIAL = "social"
    """Social-network or sharing update."""

    STATUS = "status"
    """Ongoing device or contextual status information."""

    STOPWATCH = "stopwatch"
    """Running stopwatch."""

    SYSTEM = "system"
    """System or device-status update. Reserved for system use."""

    TRANSPORT = "transport"
    """Media playback or transport controls."""

    WORKOUT = "workout"
    """Tracking of the user's workout."""


class LinuxNotificationCategory(Enum):
    """
    Freedesktop category hint used by a Linux notification server.

    Note:
        Set :attr:`flet_notifications.LinuxOptions.category`. The desktop notification
        server decides how to filter or present each category and may ignore the hint.
    """

    DEVICE = "device"
    """Device-related notification that does not fit a more specific category."""

    DEVICE_ADDED = "device.added"
    """A device, such as a USB drive, was connected."""

    DEVICE_ERROR = "device.error"
    """A device encountered an error."""

    DEVICE_REMOVED = "device.removed"
    """A device was disconnected."""

    EMAIL = "email"
    """Email-related notification without a more specific category."""

    EMAIL_ARRIVED = "email.arrived"
    """A new email arrived."""

    EMAIL_BOUNCED = "email.bounced"
    """An email could not be delivered and bounced."""

    IM = "im"
    """Instant-message notification without a more specific category."""

    IM_ERROR = "im.error"
    """An instant-messaging error occurred."""

    IM_RECEIVED = "im.received"
    """An instant message arrived."""

    NETWORK = "network"
    """Network-related notification without a more specific category."""

    NETWORK_CONNECTED = "network.connected"
    """A network connection was established."""

    NETWORK_DISCONNECTED = "network.disconnected"
    """A network connection was lost or closed."""

    NETWORK_ERROR = "network.error"
    """A network connection or operation failed."""

    PRESENCE = "presence"
    """A presence status changed, such as becoming idle or away."""

    PRESENCE_OFFLINE = "presence.offline"
    """A contact or account went offline."""

    PRESENCE_ONLINE = "presence.online"
    """A contact or account came online."""

    TRANSFER = "transfer"
    """File-transfer notification without a more specific category."""

    TRANSFER_COMPLETE = "transfer.complete"
    """A file transfer or download completed."""

    TRANSFER_ERROR = "transfer.error"
    """A file transfer or download failed."""


class WindowsNotificationDuration(Enum):
    """
    How long Windows should display a toast notification.

    Set :attr:`flet_notifications.WindowsOptions.duration`. The scenario and
    Windows settings can influence how long a notification remains visible.
    """

    SHORT = "short"
    """Request the shorter toast display duration."""

    LONG = "long"
    """Request the longer toast display duration."""


class WindowsNotificationSound(Enum):
    """
    Sound choices for Windows notifications.

    Note:
        Set :attr:`flet_notifications.WindowsOptions.audio`. These members select
        Windows system sounds or silence. Custom sound URIs are not supported.
    """

    DEFAULT = "default"
    """Play the standard Windows notification sound."""

    IM = "im"
    """Play the Windows instant-message notification sound."""

    MAIL = "mail"
    """Play the Windows email notification sound."""

    REMINDER = "reminder"
    """Play the Windows reminder notification sound."""

    SMS = "sms"
    """Play the Windows text-message notification sound."""

    SILENT = "silent"
    """Disable audio for this toast."""


class AndroidServiceStartType(Enum):
    """
    Android restart policy for the extension's foreground service.

    Note:
        Used by :meth:`flet_notifications.LocalNotifications.start_foreground_service`.
        These policies govern native service recreation, not Python task restart.
        Android's foreground-service start restrictions still apply.
    """

    START_STICKY_COMPATIBILITY = "startStickyCompatibility"
    """
    Use the compatibility form of Android's sticky-service policy.

    Unlike :attr:`START_STICKY`, it does not guarantee a restart callback after
    the service process is killed.
    """

    START_STICKY = "startSticky"
    """
    Ask Android to recreate the service after its process is killed.

    The previous start intent is not retained; a recreated service may receive
    a null intent. This policy does not guarantee uninterrupted execution.
    """

    START_NOT_STICKY = "startNotSticky"
    """
    Do not recreate a killed service unless there are pending start requests.

    The app must explicitly start new work when appropriate.
    """

    START_REDELIVER_INTENT = "startRedeliverIntent"
    """
    Ask Android to recreate a killed service and redeliver its last start intent.

    Application work must tolerate being restarted or delivered again.
    """


class AndroidForegroundServiceType(Enum):
    """
    Kind of work performed by an Android foreground service.

    Used by :meth:`flet_notifications.LocalNotifications.start_foreground_service`. Each
    member below includes its `pyproject.toml` entries and any additional runtime or
    eligibility requirements. The type-specific foreground-service permissions are
    required when targeting Android 14+.

    Start with this shared configuration, then merge the entries for the
    selected member into the same service and permission tables:

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    exported = false

    [tool.flet.android.permission]
    FOREGROUND_SERVICE = true
    ```

    Do not repeat a TOML table header when combining examples. When using more than one
    service type, combine the manifest names with `|`, for example
    `foregroundServiceType = "location|mediaPlayback"`, and include the permissions and
    prerequisites for every selected type. Pass the matching enum members to the
    method's
    [`foreground_service_types`][flet_notifications.LocalNotifications.start_foreground_service]
    argument.

    Note:
        Manifest declarations do not grant runtime permissions. Obtain any required
        runtime grants or consent before starting. Selecting a type does not start
        camera, recording, location, or other application work, and does not remove
        Android's background-start or execution-time restrictions.

    See the [Android service configuration guide](/docs/publish/android#services) for
    how these entries map to the Android manifest.
    """  # noqa: E501

    CAMERA = "camera"
    """
    Camera access while performing foreground-service work.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "camera"

    [tool.flet.android.permission]
    FOREGROUND_SERVICE_CAMERA = true
    CAMERA = true
    ```

    Note:
        Obtain the `CAMERA` runtime grant before starting. While-in-use restrictions
        usually require starting while the app is visible; background and boot starts
        are restricted. Declaring `CAMERA` in this file does not grant access.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#camera)
    for this type.
    """  # noqa: E501

    CONNECTED_DEVICE = "connectedDevice"
    """
    Interaction with an external device, such as a Bluetooth accessory.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`. This example uses
    Bluetooth; adapt its transport permission to your use case.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "connectedDevice"

    [tool.flet.android.permission]
    FOREGROUND_SERVICE_CONNECTED_DEVICE = true
    BLUETOOTH_CONNECT = true
    ```

    Note:
        This example is for a Bluetooth connection on Android 12+. Obtain the
        `BLUETOOTH_CONNECT` runtime grant before starting. Other operations may need
        `BLUETOOTH_SCAN` or `BLUETOOTH_ADVERTISE` instead.

    Note:
        For other transports, satisfy the applicable prerequisite: a declared network,
        Wi-Fi, NFC, or infrared permission; a granted UWB permission; or USB device
        permission obtained through Android's USB permission dialog. Use the permissions
        for the transport your app actually uses.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#connected-device)
    for this type.
    """  # noqa: E501

    DATA_SYNC = "dataSync"
    """
    Data transfer or processing, such as upload, download, backup, or import.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "dataSync"

    [tool.flet.android.permission]
    FOREGROUND_SERVICE_DATA_SYNC = true
    ```

    Note:
        This type has no additional type-specific runtime permission prerequisite.
        Access to the actual data or network may require other permissions. Apps
        targeting Android 15+ cannot start this type from a boot-completed receiver;
        Android also applies execution time limits.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#data-sync)
    for this type.
    """  # noqa: E501

    HEALTH = "health"
    """
    Health or fitness work, such as tracking an exercise session.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`. This example uses activity
    recognition; adapt its sensor permission to your use case.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "health"

    [tool.flet.android.permission]
    FOREGROUND_SERVICE_HEALTH = true
    ACTIVITY_RECOGNITION = true
    ```

    This example is for activity recognition. Obtain the `ACTIVITY_RECOGNITION` runtime
    grant before starting.

    Other health workloads can qualify through `HIGH_SAMPLING_RATE_SENSORS` or an
    appropriate sensor permission. Body-sensor access uses `BODY_SENSORS` on API 35 and
    earlier; newer health access can use `READ_HEART_RATE`, `READ_SKIN_TEMPERATURE`, or
    `READ_OXYGEN_SATURATION`. Declare and request the permissions matching your sensor
    and Android version, rather than adding all of them.

    Note:
        For body-sensor use subject to while-in-use restrictions, background access also
        needs `BODY_SENSORS_BACKGROUND` on API 33–35 or `READ_HEALTH_DATA_IN_BACKGROUND`
        on API 36+, as applicable.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#health)
    for this type.
    """  # noqa: E501

    LOCATION = "location"
    """
    Ongoing location work, such as navigation or location sharing.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "location"

    [tool.flet.android.permission]
    FOREGROUND_SERVICE_LOCATION = true
    ACCESS_COARSE_LOCATION = true
    ACCESS_FINE_LOCATION = true
    ```

    The user must enable device location services and grant coarse or fine location
    access before the service starts. Request coarse and fine together when precise
    location is needed; approximate access may be sufficient for your use case.

    Note:
        While-in-use restrictions usually require starting while the app is visible.
        Starting from the background requires `ACCESS_BACKGROUND_LOCATION` where
        applicable, as well as satisfying Android's foreground-service start rules. The
        block above does not request background location.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#location)
    for this type.
    """  # noqa: E501

    MEDIA_PLAYBACK = "mediaPlayback"
    """
    Ongoing audio or video playback.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "mediaPlayback"

    [tool.flet.android.permission]
    FOREGROUND_SERVICE_MEDIA_PLAYBACK = true
    ```

    Note:
        This type has no additional type-specific runtime permission prerequisite. It
        does not start media playback itself. Apps targeting Android 15+ cannot start
        this type from a boot-completed receiver.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#media)
    for this type.
    """  # noqa: E501

    MEDIA_PROJECTION = "mediaProjection"
    """
    Screen capture or projection of device content.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "mediaProjection"

    [tool.flet.android.permission]
    FOREGROUND_SERVICE_MEDIA_PROJECTION = true
    ```

    Note:
        Obtain the user's screen-capture consent through Android's
        `MediaProjectionManager.createScreenCaptureIntent()` flow before starting the
        service. A manifest permission cannot replace this consent. This extension does
        not expose that flow; the component performing screen capture must obtain it.
        Apps targeting Android 15+ cannot start this type from a boot-completed
        receiver.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#media-projection)
    for this type.
    """  # noqa: E501

    MICROPHONE = "microphone"
    """
    Ongoing microphone capture or audio recording.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "microphone"

    [tool.flet.android.permission]
    FOREGROUND_SERVICE_MICROPHONE = true
    RECORD_AUDIO = true
    ```

    Note:
        Obtain the `RECORD_AUDIO` runtime grant before starting. While-in-use
        restrictions usually require starting while the app is visible; background and
        boot starts are restricted. Declaring the permission does not start recording or
        grant microphone access.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#microphone)
    for this type.
    """  # noqa: E501

    PHONE_CALL = "phoneCall"
    """
    Continuation of a voice or video call.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`. This example is for a
    self-managed calling app.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "phoneCall"

    [tool.flet.android.permission]
    FOREGROUND_SERVICE_PHONE_CALL = true
    MANAGE_OWN_CALLS = true
    ```

    This example is for a self-managed calling app using Android's `ConnectionService`
    APIs and declaring `MANAGE_OWN_CALLS`. Alternatively, the app can qualify by holding
    the default-dialer role. Adding this block does not implement calling or obtain that
    role.

    Note:
        Apps targeting Android 15+ cannot start this type from a boot-completed
        receiver.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#phone-call)
    for this type.
    """  # noqa: E501

    REMOTE_MESSAGING = "remoteMessaging"
    """
    Transfer of text messages between devices for messaging continuity.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "remoteMessaging"

    [tool.flet.android.permission]
    FOREGROUND_SERVICE_REMOTE_MESSAGING = true
    ```

    Note:
        This type has no additional type-specific runtime permission prerequisite. Use
        it for continuity of messaging between devices, rather than ordinary local
        notifications or an incoming push message.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#remote-messaging)
    for this type.
    """  # noqa: E501

    SHORT_SERVICE = "shortService"
    """
    Short, critical work subject to Android's short-service time limit.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "shortService"
    ```

    No type-specific foreground-service permission is required; the shared
    `FOREGROUND_SERVICE` permission is still needed.

    Note:
        Android limits this type to about three minutes and does not support sticky
        restart behavior. Use
        :attr:`flet_notifications.AndroidServiceStartType.START_NOT_STICKY` and call
        :meth:`flet_notifications.LocalNotifications.stop_foreground_service` before the
        deadline. This type cannot start another foreground service. If combined with
        another service type, Android ignores `shortService` and applies the other
        type's requirements.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#short-service)
    for this type.
    """  # noqa: E501

    SPECIAL_USE = "specialUse"
    """
    Qualifying foreground work not covered by another service type.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "specialUse"

    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService".property]
    "android.app.PROPERTY_SPECIAL_USE_FGS_SUBTYPE" = "Describe the service's actual work"

    [tool.flet.android.permission]
    FOREGROUND_SERVICE_SPECIAL_USE = true
    ```

    Note:
        Replace the subtype description with the specific work your service performs and
        why it needs this type. Android requires this service property; Google Play
        reviews the declared use case. This type has no additional type-specific runtime
        permission prerequisite and is not a substitute for another type that already
        describes the work.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#special-use)
    for this type.
    """  # noqa: E501

    SYSTEM_EXEMPTED = "systemExempted"
    """
    System integration work that meets Android's exemption criteria.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "systemExempted"

    [tool.flet.android.permission]
    FOREGROUND_SERVICE_SYSTEM_EXEMPTED = true
    ```

    Note:
        The app must independently meet Android's eligibility criteria, such as being a
        qualifying device-management app, a configured VPN, or holding an applicable
        exact-alarm permission for the permitted use case. Declaring the permission
        alone does not make the app eligible; Android rejects this type for ineligible
        apps. Ordinary applications cannot select it to bypass limits.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#system-exempted)
    for this type.
    """  # noqa: E501


class WebNotificationDirection(Enum):
    """
    Text direction for a browser notification.

    Note:
        Used by :attr:`flet_notifications.WebOptions.direction`. Browsers may ignore
        this hint; it does not translate the notification's content.
    """

    AUTO = "auto"
    """Use the browser's language-setting behavior to choose the text direction."""

    LEFT_TO_RIGHT = "leftToRight"
    """Request left-to-right text layout."""

    RIGHT_TO_LEFT = "rightToLeft"
    """Request right-to-left text layout."""
